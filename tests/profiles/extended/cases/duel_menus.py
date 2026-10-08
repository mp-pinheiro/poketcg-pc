"""Extended oracle-diff cases for duel_menus: the shared cases without the routines Extended does not build."""
from tests.cases._inherit import inherit

CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('duel_menus', remove=('DrawPlayersPrizeAndBenchCards',))
