"""Extended oracle-diff cases for unsafe_bg_map: the shared cases without the routines Extended does not build."""
from tests.cases._inherit import inherit

CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('unsafe_bg_map', remove=('UnsafeWriteDataBlockToBGMap0',))
