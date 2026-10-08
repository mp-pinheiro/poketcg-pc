from tests.cases._symbols import STACK_CANARY, data, sym
POISON = {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC,
          'd': 0xDD, 'e': 0xEE, 'hl': 0x1234}
_STATE = {sym("wCurSongID"): sym("wAudioArg") + 2 - sym("wCurSongID")}

ROUTINES = [
    '_SetupSound', 'SoundTimerHandler', '_PlaySong', '_PlaySFX',
    '_AssertSongFinished', '_AssertSFXFinished', '_PauseSong', '_ResumeSong',
    'SetCurSong', 'SetCurSFX', 'Music_AssertSongFinished',
    'Music_AssertSFXFinished', 'Music_SetupSound', 'MusicUpdate',
    'CheckForNewSound', 'StopAllChannels', 'BeginSong', 'MusicEmptyFunc',
    'UpdateChannel1', 'UpdateChannel2', 'UpdateChannel3', 'UpdateChannel4',
    'GetMusicCommandAndArgs', 'PlayNextNote', 'Music_note', 'Music_speed',
    'Music_octave', 'Music_inc_octave', 'Music_dec_octave', 'Music_tie',
    'Music_stereo_panning', 'Music_MainLoop', 'Music_EndMainLoop',
    'Music_Loop', 'Music_EndLoop', 'Music_jp', 'Music_call', 'Music_ret',
    'Music_frequency_offset', 'Music_duty', 'Music_volume', 'Music_wave',
    'Music_cutoff', 'Music_echo', 'Music_vibrato_type',
    'Music_vibrato_delay', 'Music_pitch_offset', 'Music_adjust_pitch_offset',
    'Music_end', 'GetChannelStackPointer', 'SetChannelStackPointer',
    'PlayNextNote_pop', 'Music_f4714', 'Music_f475a', 'Music_f479c',
    'LoadWaveInstrument', 'Music_f480a', 'Music_f4839', 'Music_f485a',
    'Music_f4866', 'UpdateVibrato', 'Music_f490b', 'Music_f4967',
    'Music_f4980', 'CheckForEndOfSong', 'Music_PauseSong',
    'Music_ResumeSong', 'BackupSong', 'LoadBackup', 'CopyData',
]

CONTRACT = {name: {'compare': (), 'preserve': ()} for name in ROUTINES}
for name in ('_AssertSongFinished', '_AssertSFXFinished',
             'Music_AssertSongFinished', 'Music_AssertSFXFinished'):
    CONTRACT[name] = {'compare': ('a',), 'preserve': ()}
CONTRACT['GetMusicCommandAndArgs'] = {'compare': ('a', 'hl', 'b', 'c'),
                                      'preserve': ('b', 'c')}
CONTRACT['GetChannelStackPointer'] = {'compare': ('hl', 'c'), 'preserve': ('c',)}
CONTRACT['SetChannelStackPointer'] = {'compare': ('c',), 'preserve': ('c',)}
CONTRACT['UpdateVibrato'] = {'compare': ('d', 'e', 'b', 'c'), 'preserve': ('b', 'c')}
CONTRACT['Music_f4967'] = {'compare': ('d', 'e', 'b', 'c'), 'preserve': ('b', 'c')}
CONTRACT['CopyData'] = {'compare': ('hl', 'd', 'e'), 'preserve': ()}

CASES = {}
for name in ROUTINES:
    CASES[name] = [
        {'a': 0x00, 'c': 0x00, 'hl': sym("wDecompressionSecondaryBufferStart") + 0x11,
         'wram': {sym("wDecompressionSecondaryBufferStart") + 0x11: b'\x00\x00\x00'},
         'read': dict(_STATE)},
        dict(POISON, a=0x01, b=0x00, c=0x01, hl=sym("wDecompressionSecondaryBufferStart") + 0x12,
             wram={sym("wDecompressionSecondaryBufferStart") + 0x12: b'\xD0\x01\x02'},
             read=dict(_STATE)),
        dict(POISON, a=0xFF, b=0x00, c=0x03, hl=sym("wDecompressionSecondaryBufferStart") + 0x110,
             wram={sym("wDecompressionSecondaryBufferStart") + 0x110: b'\xFE', sym("wPlayerCardLocations"): b'\xFD\xFC'},
             read=dict(_STATE)),
    ]
STACK_SENSITIVE_MUSIC_COMMANDS = (
    'Music_note', 'PlayNextNote_pop', 'Music_speed', 'Music_octave',
    'Music_inc_octave', 'Music_dec_octave', 'Music_tie',
    'Music_stereo_panning', 'Music_MainLoop', 'Music_EndMainLoop',
    'Music_Loop', 'Music_EndLoop', 'Music_jp', 'Music_call', 'Music_ret',
    'Music_frequency_offset', 'Music_duty', 'Music_volume', 'Music_wave',
    'Music_cutoff', 'Music_echo', 'Music_vibrato_type',
    'Music_vibrato_delay', 'Music_pitch_offset',
    'Music_adjust_pitch_offset', 'Music_end')
_COMMAND_WRAM = {
    sym("wDecompressionSecondaryBufferStart") + 0x11: b'\xFF\xFF\xFF',
    sym("wDecompressionSecondaryBufferStart") + 0x12: b'\xFF\xFF\xFF',
    sym("wMusicCutoff"): b'\x08\x08\x08\x08',
    sym("wMusicSpeed"): b'\x01\x01\x01\x01',
    sym("wMusicMainLoopStart"): b'\x00\xC1\x00\x00\x00\x00\x00\x00',
    sym("wMusicChannelStackPointers"): b'\x00\xC2\x00\x00\x00\x00\x00\x00',
    sym("wAudioArg"): b'\x5A\x00',
}
for name in STACK_SENSITIVE_MUSIC_COMMANDS:
    command_case = {'c': 0x00, 'stack': [sym("wDecompressionSecondaryBufferStart") + 0x11], 'wram': dict(_COMMAND_WRAM),
                    'read': dict(_STATE)}
    poison_case = dict(POISON, b=0x00, c=0x00, stack=[sym("wDecompressionSecondaryBufferStart") + 0x11],
                       wram=dict(_COMMAND_WRAM), read=dict(_STATE))
    if name == 'Music_note':
        command_case['stack'] = [sym("wDecompressionSecondaryBufferStart") + 0x11, 0x0000]
        poison_case['stack'] = [sym("wDecompressionSecondaryBufferStart") + 0x11, data(0xAAF0)]
    elif name == 'Music_EndLoop':
        command_case['wram'].update({sym("wDecompressionSecondaryBufferStart") + 0x110: b'\x01'})
        poison_case['wram'].update({sym("wDecompressionSecondaryBufferStart") + 0x110: b'\x01'})
    elif name == 'Music_ret':
        command_case['wram'].update({sym("wDecompressionSecondaryBufferStart") + 0x10F: b'\xFE\xC0'})
        poison_case['wram'].update({sym("wDecompressionSecondaryBufferStart") + 0x10F: b'\xFE\xC0'})
    CASES[name] = [command_case, poison_case]
CASES['Music_f4967'] = [
    {'b': 0x00, 'c': 0x00, 'd': 0x12, 'e': 0x34},
    dict(POISON, b=0x00, c=0x01, d=0x56, e=0x78),
    dict(POISON, b=0x00, c=0x03, d=0x9A, e=0xBC),
]

CASES['CopyData'] = [
    {'a': 0x00, 'hl': sym("wDecompressionSecondaryBufferStart") + 0x11, 'd': 0xC2, 'e': 0x00,
     'wram': {sym("wDecompressionSecondaryBufferStart") + 0x11: b'\x00' * 256}, 'read': {sym("wPlayerCardLocations"): 256}},
    dict(POISON, a=0x01, hl=sym("wDecompressionSecondaryBufferStart") + 0x11, d=0xC2, e=0x00,
         wram={sym("wDecompressionSecondaryBufferStart") + 0x11: b'\xA5'}, read={sym("wPlayerCardLocations"): 1}),
    dict(POISON, a=0xFF, hl=sym("wDecompressionSecondaryBufferStart") + 0x11, d=0xC2, e=0x00,
         wram={sym("wDecompressionSecondaryBufferStart") + 0x11: b'\x5A' * 255}, read={sym("wPlayerCardLocations"): 255}),
]
CASES['GetMusicCommandAndArgs'] = [
    {'a': 0x42, 'hl': sym("wDecompressionSecondaryBufferStart") + 0x11, 'wram': {sym("wDecompressionSecondaryBufferStart") + 0x11: b'\x00\x00\x00'},
     'read': {sym("wAudioCmd"): 1, sym("wAudioArg"): 2}},
    dict(POISON, a=0x42, hl=sym("wDecompressionSecondaryBufferStart") + 0x11,
         wram={sym("wDecompressionSecondaryBufferStart") + 0x11: b'\xD0\x01\x02'}, read={sym("wAudioCmd"): 1, sym("wAudioArg"): 2}),
    dict(POISON, a=0x42, hl=sym("wDecompressionSecondaryBufferStart") + 0x110,
         wram={sym("wDecompressionSecondaryBufferStart") + 0x110: b'\xFE', sym("wPlayerCardLocations"): b'\xFD\xFC'},
         read={sym("wAudioCmd"): 1, sym("wAudioArg"): 2}),
]
CASES['GetChannelStackPointer'] = [
    {'c': 0x00, 'wram': {sym("wMusicChannelStackPointers"): b'\x00\xC1'}, 'read': {sym("wMusicChannelStackPointers"): 2}},
    dict(POISON, b=0x00, c=0x01, wram={sym("wMusicChannelStackPointers") + 2: b'\x00\xC2'}, read={sym("wMusicChannelStackPointers"): 8}),
    dict(POISON, b=0x00, c=0x03, wram={sym("wMusicChannelStackPointers") + 6: b'\x00\xC4'}, read={sym("wMusicChannelStackPointers"): 8}),
]
CASES['SetChannelStackPointer'] = [
    {'c': 0x00, 'hl': sym("wDecompressionSecondaryBufferStart") + 0x11, 'read': {sym("wMusicChannelStackPointers"): 2}},
    dict(POISON, b=0x00, c=0x01, hl=sym("wPlayerCardLocations"), read={sym("wMusicChannelStackPointers"): 8}),
    dict(POISON, b=0x00, c=0x03, hl=data(0xC3FF), read={sym("wMusicChannelStackPointers"): 8}),
]
_ACTIVE_CHANNELS = {
    sym("wMusicIsPlaying"): b'\x01\x01\x01\x01', sym("wdd8c"): b'\x00', sym("wddbb"): b'\x01\x01\x01\x01',
    sym("wMusicVibratoDelay"): b'\x00\x00\x00\x00', sym("wddb7"): b'\x10\x10\x10\x10', sym("wddc3"): b'\x01\x01\x01\x01',
    sym("wMusicChannelPointers"): b'\x00\xC1\x00\xC1\x00\xC1\x00\xC1', sym("wMusicVolume"): b'\x77\x77\x77',
    sym("wMusicDuty1"): b'\xC0\xC0\xC0\xC0',
}
for name in ('UpdateChannel1', 'UpdateChannel2', 'UpdateChannel3', 'UpdateChannel4'):
    CASES[name].append({'wram': dict(_ACTIVE_CHANNELS), 'read': dict(_STATE)})
for name in ('Music_PauseSong', '_PauseSong'):
    CASES[name].append({'wram': {sym("wCurSongID"): b'\x80', sym("wCurSongBank"): b'\x3D', sym("wdd8c"): b'\x0F',
                                 sym("wMusicIsPlaying"): b'\x01\x01\x01\x01'},
                        'read': dict(_STATE)})
for name in ('MusicEmptyFunc', 'Music_f485a', 'Music_f4866', 'Music_f490b', 'Music_f4980'):
    for record in CASES[name]:
        record['read'] = {**record['read'], STACK_CANARY: 1}

ANCHORS = {
    '_SetupSound': ('\tMusic_SetupSound();', '\t(void)0;'),
    'SoundTimerHandler': ('\tMusicUpdate();', '\t(void)0;'),
    '_PlaySong': ('\tSetCurSong(a);', '\tSetCurSFX(a);'),
    '_PlaySFX': ('\tSetCurSFX(a);', '\tSetCurSong(a);'),
    '_AssertSongFinished': ('\treturn Music_AssertSongFinished();', '\treturn (uint8_t)((Music_AssertSongFinished()) ^ 1u);'),
    '_AssertSFXFinished': ('\treturn Music_AssertSFXFinished();', '\treturn (uint8_t)((Music_AssertSFXFinished()) ^ 1u);'),
    '_PauseSong': ('\tMusic_PauseSong();', '\t(void)0;'),
    '_ResumeSong': ('\tMusic_ResumeSong();', '\t(void)0;'),
    'SetCurSong': ('\tif (a >= gb_read8(ADR_NUMBER_OF_SONGS))', '\tif (a <= gb_read8(ADR_NUMBER_OF_SONGS))'),
    'SetCurSFX': ('\twCurSfxID = a;', '\twCurSfxID = 0u;'),
    'Music_AssertSongFinished': ('\treturn wCurSongID == 0x80u ? 0u : 1u;', '\treturn (uint8_t)((wCurSongID == 0x80u ? 0u : 1u) ^ 1u);'),
    'Music_AssertSFXFinished': ('\treturn wCurSfxID == 0x80u ? 0u : 1u;', '\treturn (uint8_t)((wCurSfxID == 0x80u ? 0u : 1u) ^ 1u);'),
    'Music_SetupSound': ('\twCurSongID = 0x80u;', '\twCurSongID = (uint8_t)((0x80u) ^ 1u);'),
    'MusicUpdate': ('\tCheckForNewSound();', '\t(void)0;'),
    'CheckForNewSound': ('\tif ((wCurSongID & 0x80u) == 0u)', '\tif ((wCurSongID & 0x80u) != 0u)'),
    'StopAllChannels': ('\tgb_write8(wMusicIsPlaying_ADDR, 0u);', '\tgb_write8(wMusicIsPlaying_ADDR, (uint8_t)((0u) ^ 1u));'),
    'BeginSong': ('\tif ((mask & (uint8_t)(1u << ch)) == 0u)', '\tif ((mask & (uint8_t)(1u << ch)) != 0u)'),
    'MusicEmptyFunc': ('void MusicEmptyFunc(void)\n{', 'void MusicEmptyFunc(void)\n{\n\tgb_write8(0xdff0u, 0xFFu);'),
    'UpdateChannel1': ('\tupdate_channel(0u);', '\tupdate_channel(1u);'),
    'UpdateChannel2': ('\tupdate_channel(1u);', '\tupdate_channel(2u);'),
    'UpdateChannel3': ('\tupdate_channel(2u);', '\tupdate_channel(3u);'),
    'UpdateChannel4': ('\tupdate_channel(3u);', '\tupdate_channel(0u);'),
    'GetMusicCommandAndArgs': ('\t*hl = (uint16_t)(*hl + 1u);', '\t*hl = (uint16_t)(*hl + 2u);'),
    'PlayNextNote': ('\t\t\tgb_write8(channel_addr(wMusicIsPlaying_ADDR, ch), 0u);', '\t\t\tgb_write8(channel_addr(wMusicIsPlaying_ADDR, ch), (uint8_t)((0u) ^ 1u));'),
    'Music_note': ('\tnote_body(hl, note, ch);', '\tnote_body(hl, ((note) ^ 1u), ch);'),
    'Music_speed': ('\tcaller_stream = (uint16_t)(caller_stream + 1u);', '\tcaller_stream = (uint16_t)(caller_stream + 2u);'),
    'Music_octave': ('\tgb_write8(channel_addr(wMusicOctave_ADDR, ch), octave);', '\tgb_write8(channel_addr(wMusicOctave_ADDR, ch), (uint8_t)((octave) ^ 1u));'),
    'Music_inc_octave': ('\tgb_write8(addr, (uint8_t)(gb_read8(addr) + 1u));', '\tgb_write8(addr, (uint8_t)(((uint8_t)(gb_read8(addr) + 1u)) ^ 1u));'),
    'Music_dec_octave': ('\tgb_write8(addr, (uint8_t)(gb_read8(addr) - 1u));', '\tgb_write8(addr, (uint8_t)(((uint8_t)(gb_read8(addr) - 1u)) ^ 1u));'),
    'Music_tie': ('\tgb_write8(channel_addr(wMusicTie_ADDR, ch), 0x80u);', '\tgb_write8(channel_addr(wMusicTie_ADDR, ch), (uint8_t)((0x80u) ^ 1u));'),
    'Music_stereo_panning': ('\twMusicStereoPanning = (uint8_t)((wMusicStereoPanning & mask) | value);', '\twMusicStereoPanning = (uint8_t)(((uint8_t)((wMusicStereoPanning & mask) | value)) ^ 1u);'),
    'Music_MainLoop': ('\t        (uint16_t)(caller_stream - 1u));', '\t        (uint16_t)(caller_stream - 2u));'),
    'Music_EndMainLoop': ('\tuint16_t stream = read16(channel_word_addr(wMusicMainLoopStart_ADDR, ch));', '\tuint16_t stream = read16((uint16_t)(channel_word_addr(wMusicMainLoopStart_ADDR, ch) + 1u));'),
    'Music_Loop': ('\tuint16_t continuation = (uint16_t)(caller_stream + 1u);', '\tuint16_t continuation = (uint16_t)(caller_stream + 2u);'),
    'Music_EndLoop': ('\tif (count != 0u)', '\tif (count == 0u)'),
    'Music_jp': ('\tuint16_t stream = (uint16_t)(wAudioArg | ((uint16_t)gb_read8((uint16_t)(wAudioArg_ADDR + 1u)) << 8u));', '\tuint16_t stream = (uint16_t)(wAudioArg | ((uint16_t)gb_read8((uint16_t)(wAudioArg_ADDR + 0x0u)) << 8u));'),
    'Music_call': ('\tSetChannelStackPointer(ch, (uint16_t)(sp + 2u));', '\t(void)0;'),
    'Music_ret': ('\tuint16_t sp = (uint16_t)(GetChannelStackPointer(ch) - 2u);', '\tuint16_t sp = (uint16_t)(GetChannelStackPointer(ch) - 0x3u);'),
    'Music_frequency_offset': ('\tone_byte_command(caller_stream, ch, wMusicFrequencyOffset_ADDR, wAudioArg);', '\tone_byte_command(((caller_stream) ^ 1u), ch, wMusicFrequencyOffset_ADDR, wAudioArg);'),
    'Music_duty': ('\tone_byte_command(caller_stream, ch, wMusicDuty1_ADDR, (uint8_t)(wAudioArg & 0xC0u));', '\tone_byte_command(((caller_stream) ^ 1u), ch, wMusicDuty1_ADDR, (uint8_t)(wAudioArg & 0xC0u));'),
    'Music_volume': ('\tone_byte_command(caller_stream, ch, wMusicVolume_ADDR, wAudioArg);', '\tone_byte_command(((caller_stream) ^ 1u), ch, wMusicVolume_ADDR, wAudioArg);'),
    'Music_wave': ('\twMusicWave = wAudioArg;', '\twMusicWave = (uint8_t)((wAudioArg) ^ 1u);'),
    'Music_cutoff': ('\tone_byte_command(caller_stream, ch, wMusicCutoff_ADDR, wAudioArg);', '\tone_byte_command(caller_stream, ch, wMusicCutoff_ADDR, 0u);'),
    'Music_echo': ('\tone_byte_command(caller_stream, ch, wMusicEcho_ADDR, wAudioArg);', '\tone_byte_command(((caller_stream) ^ 1u), ch, wMusicEcho_ADDR, wAudioArg);'),
    'Music_vibrato_type': ('\tgb_write8(channel_addr(wMusicVibratoType_ADDR, ch), wAudioArg);', '\tgb_write8(channel_addr(wMusicVibratoType_ADDR, ch), (uint8_t)((wAudioArg) ^ 1u));'),
    'Music_vibrato_delay': ('\tone_byte_command(caller_stream, ch, wMusicVibratoDelay_ADDR, wAudioArg);', '\tone_byte_command(((caller_stream) ^ 1u), ch, wMusicVibratoDelay_ADDR, wAudioArg);'),
    'Music_pitch_offset': ('\tone_byte_command(caller_stream, ch, wMusicPitchOffset_ADDR, wAudioArg);', '\tone_byte_command(((caller_stream) ^ 1u), ch, wMusicPitchOffset_ADDR, wAudioArg);'),
    'Music_adjust_pitch_offset': ('\tgb_write8(addr, (uint8_t)(wAudioArg + gb_read8(addr)));', '\tgb_write8(addr, (uint8_t)(((uint8_t)(wAudioArg + gb_read8(addr))) ^ 1u));'),
    'Music_end': ('\tgb_write8(channel_addr(wMusicIsPlaying_ADDR, ch), 0u);', '\tgb_write8(channel_addr(wMusicIsPlaying_ADDR, ch), (uint8_t)((0u) ^ 1u));'),
    'GetChannelStackPointer': ('\treturn read16((uint16_t)(wMusicChannelStackPointers_ADDR + (uint16_t)ch * 2u));', '\treturn read16((uint16_t)(wMusicChannelStackPointers_ADDR + (uint16_t)(ch + 1u) * 2u));'),
    'SetChannelStackPointer': ('\twrite16((uint16_t)(wMusicChannelStackPointers_ADDR + (uint16_t)ch * 2u), sp);', '\twrite16((uint16_t)(wMusicChannelStackPointers_ADDR + (uint16_t)(ch + 1u) * 2u), sp);'),
    'PlayNextNote_pop': ('\tPlayNextNote(&caller_stream, ch);', '\t(void)0;'),
    'Music_f4714': ('\t\twMusicTie = 0u;', '\t\twMusicTie = (uint8_t)((0u) ^ 1u);'),
    'Music_f475a': ('\t\twMusicTie_PTR[1] = 0u;', '\t\twMusicTie_PTR[1] = (uint8_t)((0u) ^ 1u);'),
    'Music_f479c': ('\t\twMusicTie = 0u;', '\t\twMusicTie = (uint8_t)((0u) ^ 1u);'),
    'LoadWaveInstrument': ('\twMusicWaveChange = 0u;', '\twMusicWaveChange = (uint8_t)((0u) ^ 1u);'),
    'Music_f480a': ('\t\twddef = 0u;', '\t\twddef = 0x1u;'),
    'Music_f4839': ('\tif ((wdd8c & 0x08u) != 0u) {', '\tif (!((wdd8c & 0x08u) != 0u)) {'),
    'Music_f485a': ('void Music_f485a(uint8_t ch)\n{', 'void Music_f485a(uint8_t ch)\n{\n\tgb_write8(0xdff0u, 0xFFu);'),
    'Music_f4866': ('void Music_f4866(void)\n{', 'void Music_f4866(void)\n{\n\tgb_write8(0xdff0u, 0xFFu);'),
    'UpdateVibrato': ('\tif (delay == 0u)', '\tif (!(delay == 0u))'),
    'Music_f490b': ('void Music_f490b(uint8_t ch, uint16_t de)\n{', 'void Music_f490b(uint8_t ch, uint16_t de)\n{\n\tgb_write8(0xdff0u, 0xFFu);'),
    'Music_f4967': ('\tuint16_t frequency = de;', '\tuint16_t frequency = (uint16_t)(de + 1u);'),
    'Music_f4980': ('void Music_f4980(void)\n{', 'void Music_f4980(void)\n{\n\tgb_write8(0xdff0u, 0xFFu);'),
    'CheckForEndOfSong': ('\tif (sum == 0u)', '\tif (sum != 0u)'),
    'Music_PauseSong': ('\tStopAllChannels();', '\t(void)0;'),
    'Music_ResumeSong': ('\tLoadBackup();', '\t(void)0;'),
    'BackupSong': ('\twCurSongIDBackup = wCurSongID;', '\twCurSongIDBackup = (uint8_t)((wCurSongID) ^ 1u);'),
    'LoadBackup': ('\twCurSongID = wCurSongIDBackup;', '\twCurSongID = (uint8_t)((wCurSongIDBackup) ^ 1u);'),
    'CopyData': ('\t\tgb_write8(*de, gb_read8(*hl));', '\t\tgb_write8(*de, (uint8_t)(gb_read8(*hl) + 1u));'),
}
WITNESS_INDEX = {name: 0 for name in ANCHORS}
WITNESS_INDEX.update({name: 1 for name in ('_PlaySong', '_PlaySFX', 'SetCurSong', 'SetCurSFX', 'CheckForNewSound', 'BeginSong',
                                          'GetMusicCommandAndArgs', 'Music_speed', 'Music_MainLoop', 'Music_Loop',
                                          'Music_EndLoop', 'Music_cutoff', 'GetChannelStackPointer',
                                          'SetChannelStackPointer', 'Music_f4967', 'CheckForEndOfSong', 'CopyData')})
WITNESS_INDEX.update({'PlayNextNote': 2, '_PauseSong': 3, 'Music_PauseSong': 3, 'UpdateChannel1': 3, 'UpdateChannel2': 3,
                      'UpdateChannel3': 3, 'UpdateChannel4': 3})

MUTATIONS = {
    name: {'source_symbol': name, 'before': before, 'after': after,
           'case_ids': [f'{name}-{WITNESS_INDEX[name]}'],
           'source': 'src/profiles/extended/home/music.c'}
    for name, (before, after) in ANCHORS.items()
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
