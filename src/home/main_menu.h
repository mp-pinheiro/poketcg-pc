#ifndef POKETCG_HOME_MAIN_MENU_H
#define POKETCG_HOME_MAIN_MENU_H

#include <stdint.h>

/* >>> factory MainMenu_CardPop */
uint8_t MainMenu_CardPop(void);
/* <<< factory MainMenu_CardPop */
/* >>> factory MainMenu_NewGame */
void MainMenu_NewGame(void);
/* <<< factory MainMenu_NewGame */
/* >>> factory MainMenu_ContinueFromDiary */
void MainMenu_ContinueFromDiary(void);
/* <<< factory MainMenu_ContinueFromDiary */
/* >>> factory MainMenu_ContinueDuel */
void MainMenu_ContinueDuel(void);
/* <<< factory MainMenu_ContinueDuel */
/* >>> factory _GameLoop */
void _GameLoop(void);
/* <<< factory _GameLoop */
#endif /* POKETCG_HOME_MAIN_MENU_H */
