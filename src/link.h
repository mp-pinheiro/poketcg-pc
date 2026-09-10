#ifndef POKETCG_LINK_H
#define POKETCG_LINK_H

#include <stdint.h>

int link_open(int fd);
void link_close(void);
int link_active(void);
void link_note_sc_write(uint8_t value);
void link_pump(void);
void link_drain(void);
uint32_t link_exchanges(void);
uint32_t link_timeouts(void);
uint32_t link_drain_timeouts(void);
int link_first_received(void);

#endif /* POKETCG_LINK_H */
