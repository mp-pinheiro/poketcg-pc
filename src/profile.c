#include "profile.h"

ProfileDescriptor profile_current(void)
{
#ifdef POKETCG_PROFILE_EXTENDED
	return (ProfileDescriptor){PROFILE_ID_EXTENDED, "EXTD", 1u};
#else
	return (ProfileDescriptor){PROFILE_ID_VANILLA, "VANL", 0u};
#endif
}
