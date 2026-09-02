#ifndef POKETCG_CHECKPOINT_H
#define POKETCG_CHECKPOINT_H

/* Load a reference checkpoint (tools/completion/explore.py's
 * reference-checkpoint-v1) into the port's memory arrays, so a subsystem can be
 * exercised without the port first having to reach it correctly. The duel engine
 * is 1,270 of the ROM's 3,009 routines and sits behind naming and the overworld;
 * injection decouples testing it from repairing that path.
 *
 * A run started this way proves nothing about the path it skipped. It is a test
 * fixture, never evidence that the game works. */

int checkpoint_load(const char *path);

#endif /* POKETCG_CHECKPOINT_H */
