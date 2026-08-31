#include "runtime.h"

#include "home/frames.h"
#include "home/game_loop.h"
#include "home/start.h"
#include "mem.h"
#include "ppu.h"
#include "shell.h"

#include <pthread.h>
#include <stdint.h>
#include <string.h>
#define AUDIO_SAMPLES_PER_FRAME 1470u

typedef struct {
	pthread_mutex_t lock;
	pthread_cond_t condition;
	Shell *shell;
	Ppu ppu;
	uint16_t framebuffer[SCREEN_W * SCREEN_H];
	int16_t audio[AUDIO_SAMPLES_PER_FRAME];
	uint32_t frame_limit;
	uint32_t frames;
	int frame_ready;
	int resume;
	int stop;
	int stopped_by_user;
	int worker_done;
} RuntimeState;

static void boundary(void *context)
{
	RuntimeState *state = context;
	pthread_mutex_lock(&state->lock);
	state->frame_ready = 1;
	pthread_cond_broadcast(&state->condition);
	while (!state->resume && !state->stop)
		pthread_cond_wait(&state->condition, &state->lock);
	state->resume = 0;
	pthread_mutex_unlock(&state->lock);
}

static int stopped(RuntimeState *state)
{
	int stop;
	pthread_mutex_lock(&state->lock);
	stop = state->stop;
	pthread_mutex_unlock(&state->lock);
	return stop;
}

static void *run_game(void *context)
{
	RuntimeState *state = context;
	Start(0x11u);
	GameLoop();
	for (;;) {
		DoFrame();
		if (stopped(state))
			break;
	}
	pthread_mutex_lock(&state->lock);
	state->worker_done = 1;
	pthread_cond_broadcast(&state->condition);
	pthread_mutex_unlock(&state->lock);
	return NULL;
}

int runtime_run(Shell *shell, uint32_t frame_limit, RuntimeResult *result)
{
	RuntimeState state;
	memset(&state, 0, sizeof state);
	state.shell = shell;
	state.frame_limit = frame_limit;
	if (pthread_mutex_init(&state.lock, NULL) != 0)
		return -1;
	if (pthread_cond_init(&state.condition, NULL) != 0) {
		pthread_mutex_destroy(&state.lock);
		return -1;
	}
	ppu_init_offsets(&state.ppu);
	frame_boundary_install(boundary, &state);
	pthread_t worker;
	if (pthread_create(&worker, NULL, run_game, &state) != 0) {
		frame_boundary_install(NULL, NULL);
		pthread_cond_destroy(&state.condition);
		pthread_mutex_destroy(&state.lock);
		return -1;
	}
	for (;;) {
		pthread_mutex_lock(&state.lock);
		while (!state.frame_ready && !state.worker_done)
			pthread_cond_wait(&state.condition, &state.lock);
		if (state.worker_done && !state.frame_ready) {
			pthread_mutex_unlock(&state.lock);
			break;
		}
		state.frame_ready = 0;
		pthread_mutex_unlock(&state.lock);

		InputFrame input = {0};
		if (!shell_pump(shell, &input)) {
			pthread_mutex_lock(&state.lock);
			state.stop = 1;
			state.stopped_by_user = 1;
			state.resume = 1;
			pthread_cond_broadcast(&state.condition);
			pthread_mutex_unlock(&state.lock);
			continue;
		}
		g_keys = input.buttons;
		state.frames++;
		apu_trace_set_tick(state.frames);
		size_t pcm_count = apu_trace_render_pcm(
			state.audio, AUDIO_SAMPLES_PER_FRAME);
		ppu_render_frame(&state.ppu, state.framebuffer);
		shell_present(shell, state.framebuffer);
		shell_queue_audio(shell, state.audio, pcm_count);

		pthread_mutex_lock(&state.lock);
		if (state.frame_limit && state.frames >= state.frame_limit)
			state.stop = 1;
		state.resume = 1;
		pthread_cond_broadcast(&state.condition);
		pthread_mutex_unlock(&state.lock);
	}
	pthread_join(worker, NULL);
	frame_boundary_install(NULL, NULL);
	if (result) {
		result->frame_limit = frame_limit;
		result->frames = state.frames;
		result->stopped_by_user = state.stopped_by_user;
		memcpy(result->framebuffer, state.framebuffer, sizeof state.framebuffer);
	}
	pthread_cond_destroy(&state.condition);
	pthread_mutex_destroy(&state.lock);
	return 0;
}
