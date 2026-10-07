/* >>> part EMPTY_MAIL_NAME_TEXT */
#define EMPTY_MAIL_NAME_TEXT EmptyMailNameText
/* <<< part EMPTY_MAIL_NAME_TEXT */
/* >>> part kPCPackNameTextIDs */
static const uint16_t kPCPackNameTextIDs[NUM_MAILS] = {
	Mail1Text, Mail2Text, Mail3Text, Mail4Text, Mail5Text,
	Mail6Text, Mail7Text, Mail8Text, Mail9Text, Mail10Text,
	Mail11Text, Mail12Text, Mail13Text, Mail14Text, Mail15Text,
};
/* <<< part kPCPackNameTextIDs */
/* >>> factory GetPCPackNameTextID */
uint16_t GetPCPackNameTextID(uint8_t a)
{
	return kPCPackNameTextIDs[a];
}
/* <<< factory GetPCPackNameTextID */
/* === factory TryOpenPCMailBoosterPack */
