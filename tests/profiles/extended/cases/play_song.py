"""Extended oracle-diff cases for play_song: the shared cases without the routines Extended does not build."""
from tests.cases._inherit import inherit

CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('play_song', remove=('Func_3c87',))
