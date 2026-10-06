#ifndef POKETCG_PROFILE_H
#define POKETCG_PROFILE_H

#include <stdint.h>

typedef enum {
	PROFILE_ID_VANILLA = 0,
	PROFILE_ID_EXTENDED = 1,
} ProfileId;

typedef struct {
	ProfileId id;
	const char *tag;
	uint32_t save_schema;
} ProfileDescriptor;

ProfileDescriptor profile_current(void);

#endif
