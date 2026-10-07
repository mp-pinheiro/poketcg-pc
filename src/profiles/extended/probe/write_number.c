/* --- factory WriteBCDDigitInTextFormat */
/* --- factory WriteBCDNumberInTextFormat */
/* --- factory WriteTwoDigitBCDNumber */
/* --- factory WriteFourDigitBCDNumber */
/* --- factory WriteOneDigitBCDNumber */
/* --- factory WriteOneByteNumber */
/* --- factory WriteTwoByteNumber */
/* >>> part probe_entries_write_number */
const ProbeEntry probe_entries_write_number[] = {
	{ "TwoByteNumberToText", adapt_TwoByteNumberToText },
	{ NULL, NULL },
};
/* <<< part probe_entries_write_number */
