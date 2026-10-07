/* >>> factory CreateCardSetList */
static void adapt_CreateCardSetList(ProbeState *s)
{
	CreateCardSetList(s->a);
	s->a = 0u;
	s->f = 0x80u;
}
/* <<< factory CreateCardSetList */
