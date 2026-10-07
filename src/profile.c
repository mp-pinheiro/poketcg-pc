#include "profile.h"

#include "generated/profile_features.h"

ProfileDescriptor profile_current(void)
{
	return (ProfileDescriptor){(ProfileId)PROFILE_INDEX, PROFILE_SAVE_TAG, PROFILE_SAVE_SCHEMA};
}
