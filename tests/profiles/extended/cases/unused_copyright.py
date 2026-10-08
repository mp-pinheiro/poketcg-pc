"""Extended oracle-diff cases for unused_copyright: the shared cases without the routines Extended does not build."""
from tests.cases._inherit import inherit

CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('unused_copyright', remove=('UnusedCopyrightScreen',))
