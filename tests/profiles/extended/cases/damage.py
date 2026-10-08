"""Extended oracle-diff cases for damage: the shared cases without the routines Extended does not build."""
from tests.cases._inherit import inherit

CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('damage', remove=('SubtractFromDamage',))
