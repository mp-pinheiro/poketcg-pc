#include "home/indirect_dispatch.h"

#include <stdio.h>
#include <stdlib.h>

void DispatchIndirect(const char *site, uint16_t target)
{
	if (target == 0u)
		return;
	fprintf(stderr, "indirect dispatch miss site=%s target=$%04X\n",
	        site, (unsigned)target);
	abort();
}
