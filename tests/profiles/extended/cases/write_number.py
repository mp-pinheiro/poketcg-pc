"""Extended oracle-diff cases for write_number: the shared cases without the routines Extended does not build."""
from tests.cases._inherit import inherit

CONTRACT, CASES, SCHEMA2_CASES, MUTATIONS = inherit('write_number', remove=(
    'WriteBCDDigitInTextFormat',
    'WriteBCDNumberInTextFormat',
    'WriteFourDigitBCDNumber',
    'WriteOneByteNumber',
    'WriteOneDigitBCDNumber',
    'WriteTwoByteNumber',
    'WriteTwoDigitBCDNumber',
))
