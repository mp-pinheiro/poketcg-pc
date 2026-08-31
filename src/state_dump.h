#ifndef POKETCG_STATE_DUMP_H
#define POKETCG_STATE_DUMP_H

#include "runtime.h"

int runtime_write_state(const char *path, const RuntimeResult *runtime);
int runtime_write_trace(const char *path, const RuntimeResult *runtime);

#endif
