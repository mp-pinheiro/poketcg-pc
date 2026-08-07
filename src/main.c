#include "mem.h"
#include "ppu.h"
#include "shell.h"

#include <stdio.h>
#include <string.h>

int main(int argc, char **argv)
{
	ShellConfig config = {0};
	for (int i = 1; i < argc; i++)
		if (strcmp(argv[i], "--headless") == 0)
			config.headless = 1;

	mem_reset();
	g_io[0x40] = 0x91;
	g_vram[0] = 0xFF;
	g_vram[1] = 0x00;
	g_vram[0x1800] = 0;
	g_pal[2] = 0x1F;
	g_pal[3] = 0x00;

	Shell *shell = shell_create(&config);
	if (!shell)
		return 1;
	InputFrame input = {0};
	if (!shell_pump(shell, &input)) {
		shell_destroy(shell);
		return 0;
	}
	Ppu ppu;
	uint16_t framebuffer[SCREEN_W * SCREEN_H];
	ppu_init_offsets(&ppu);
	ppu_render_frame(&ppu, framebuffer);
	shell_present(shell, framebuffer);
	shell_queue_audio(shell, NULL, 0);

	size_t nonzero = 0;
	for (size_t i = 0; i < sizeof framebuffer / sizeof framebuffer[0]; i++)
		if (framebuffer[i] != 0)
			nonzero++;
	printf("%s frame: %zu non-zero pixels, P1=0x%02X\n",
	       shell_backend_name(shell), nonzero, g_io[0]);
	shell_destroy(shell);
	return 0;
}
