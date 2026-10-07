POISON = {'a': 0xAA, 'f': 0xF0, 'b': 0xBB, 'c': 0xCC,
          'd': 0xDD, 'e': 0xEE, 'hl': 0x1234}

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
        {'a': 0x00, 'c': 0x00, 'hl': 0xC100,
         'wram': {0xC100: b'\x00\x00\x00'},
         'read': {0xD7A4: 1, 0xD7A6: 1, 0xD7B0: 4}},
        dict(POISON, a=0x01, c=0x01, hl=0xC101,
             wram={0xC101: b'\xD0\x01\x02'},
             read={0xD7A4: 1, 0xD7A6: 1, 0xD7B0: 4}),
        dict(POISON, a=0xFF, c=0x03, hl=0xC1FF,
             wram={0xC1FF: b'\xFE', 0xC200: b'\xFD\xFC'},
             read={0xD7A4: 1, 0xD7A6: 1, 0xD7B0: 4}),
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
    0xC100: b'\xFF\xFF\xFF',
    0xC101: b'\xFF\xFF\xFF',
    0xD7E2: b'\x08\x08\x08\x08',
    0xD7F2: b'\x01\x01\x01\x01',
    0xD7C0: b'\x00\xC1\x00\x00\x00\x00\x00\x00',
    0xD816: b'\x00\xC2\x00\x00\x00\x00\x00\x00',
    0xD90A: b'\x5A\x00',
}
for name in STACK_SENSITIVE_MUSIC_COMMANDS:
    command_case = {'c': 0x00, 'stack': [0xC100], 'wram': dict(_COMMAND_WRAM)}
    poison_case = dict(POISON, b=0x00, c=0x00, stack=[0xC100],
                       wram=dict(_COMMAND_WRAM))
    if name == 'Music_note':
        command_case['stack'] = [0xC100, 0x0000]
        poison_case['stack'] = [0xC100, 0xF0AA]
    elif name == 'Music_EndLoop':
        command_case['wram'].update({0xC1FF: b'\x01'})
        poison_case['wram'].update({0xC1FF: b'\x01'})
    elif name == 'Music_ret':
        command_case['wram'].update({0xC1FE: b'\xFE\xC0'})
        poison_case['wram'].update({0xC1FE: b'\xFE\xC0'})
    CASES[name] = [command_case, poison_case]
CASES['Music_f4967'] = [
    {'b': 0x00, 'c': 0x00, 'd': 0x12, 'e': 0x34},
    dict(POISON, b=0x00, c=0x01, d=0x56, e=0x78),
    dict(POISON, b=0x00, c=0x03, d=0x9A, e=0xBC),
]

CASES['CopyData'] = [
    {'a': 0x00, 'hl': 0xC100, 'd': 0xC2, 'e': 0x00,
     'wram': {0xC100: b'\x00' * 256}, 'read': {0xC200: 256}},
    dict(POISON, a=0x01, hl=0xC100, d=0xC2, e=0x00,
         wram={0xC100: b'\xA5'}, read={0xC200: 1}),
    dict(POISON, a=0xFF, hl=0xC100, d=0xC2, e=0x00,
         wram={0xC100: b'\x5A' * 255}, read={0xC200: 255}),
]
CASES['GetMusicCommandAndArgs'] = [
    {'a': 0x42, 'hl': 0xC100, 'wram': {0xC100: b'\x00\x00\x00'},
     'read': {0xD909: 1, 0xD90A: 2}},
    dict(POISON, a=0x42, hl=0xC100,
         wram={0xC100: b'\xD0\x01\x02'}, read={0xD909: 1, 0xD90A: 2}),
    dict(POISON, a=0x42, hl=0xC1FF,
         wram={0xC1FF: b'\xFE', 0xC200: b'\xFD\xFC'},
         read={0xD909: 1, 0xD90A: 2}),
]
CASES['GetChannelStackPointer'] = [
    {'c': 0x00, 'wram': {0xD816: b'\x00\xC1'}, 'read': {0xD816: 2}},
    dict(POISON, b=0x00, c=0x01, wram={0xD818: b'\x00\xC2'}, read={0xD816: 8}),
    dict(POISON, b=0x00, c=0x03, wram={0xD81C: b'\x00\xC4'}, read={0xD816: 8}),
]
CASES['SetChannelStackPointer'] = [
    {'c': 0x00, 'hl': 0xC100, 'read': {0xD816: 2}},
    dict(POISON, b=0x00, c=0x01, hl=0xC200, read={0xD816: 8}),
    dict(POISON, b=0x00, c=0x03, hl=0xC3FF, read={0xD816: 8}),
]

ANCHORS = {
    '_SetupSound': ('\tMusic_SetupSound();', '\tMusicUpdate();'),
    'SoundTimerHandler': ('\tMusicUpdate();', '\tMusic_SetupSound();'),
    '_PlaySong': ('\tSetCurSong(a);', '\tSetCurSFX(a);'),
    '_PlaySFX': ('\tSetCurSFX(a);', '\tSetCurSong(a);'),
    '_AssertSongFinished': ('\treturn Music_AssertSongFinished();', '\treturn Music_AssertSFXFinished();'),
    '_AssertSFXFinished': ('\treturn Music_AssertSFXFinished();', '\treturn Music_AssertSongFinished();'),
    '_PauseSong': ('\tMusic_PauseSong();', '\tMusic_ResumeSong();'),
    '_ResumeSong': ('\tMusic_ResumeSong();', '\tMusic_PauseSong();'),
    'SetCurSong': ('\tif (a < gb_read8(ADR_NUMBER_OF_SONGS))', '\tif (a <= gb_read8(ADR_NUMBER_OF_SONGS))'),
    'SetCurSFX': ('\twCurSfxID = a;', '\twCurSfxID = 0u;'),
    'Music_AssertSongFinished': ('\treturn wCurSongID == 0x80u ? 0u : 1u;', '\treturn wCurSongID == 0x81u ? 0u : 1u;'),
    'Music_AssertSFXFinished': ('\treturn wCurSfxID == 0x80u ? 0u : 1u;', '\treturn wCurSfxID == 0x81u ? 0u : 1u;'),
    'Music_SetupSound': ('\tgb_write8(APU_ENA, 0u);', '\tgb_write8(APU_ENA, AUDENA_ON);'),
    'MusicUpdate': ('\tif (wddf2 != 0u)', '\tif (wddf2 == 0u)'),
    'CheckForNewSound': ('\tif ((wCurSongID & 0x80u) == 0u)', '\tif ((wCurSongID & 0x80u) != 0u)'),
    'StopAllChannels': ('\tif ((d & 0x01u) == 0u)', '\tif ((d & 0x01u) != 0u)'),
    'BeginSong': ('\tif ((mask & (uint8_t)(1u << ch)) == 0u)', '\tif ((mask & (uint8_t)(1u << ch)) != 0u)'),
    'MusicEmptyFunc': ('\tg_rom_bank = MUSIC_BANK;', '\tg_rom_bank = 0u;'),
    'UpdateChannel1': ('\tupdate_channel(0u);', '\tupdate_channel(1u);'),
    'UpdateChannel2': ('\tupdate_channel(1u);', '\tupdate_channel(2u);'),
    'UpdateChannel3': ('\tupdate_channel(2u);', '\tupdate_channel(3u);'),
    'UpdateChannel4': ('\tupdate_channel(3u);', '\tupdate_channel(0u);'),
    'GetMusicCommandAndArgs': ('\t*hl = (uint16_t)(*hl + 1u);', '\t*hl = (uint16_t)(*hl + 2u);'),
    'PlayNextNote': ('\t\tif (command < 0xD0u)', '\t\tif (command <= 0xD0u)'),
    'Music_note': ('\t(void)instrument;', '\t(void)note;'),
    'Music_speed': ('\tcaller_stream = (uint16_t)(caller_stream + 1u);', '\tcaller_stream = (uint16_t)(caller_stream + 2u);'),
    'Music_octave': ('\tif (ch == 2u)', '\tif (ch == 1u)'),
    'Music_inc_octave': ('\tplay_next_from(caller_stream, ch);', '\tplay_next_from((uint16_t)(caller_stream + 1u), ch);'),
    'Music_dec_octave': ('\tplay_next_from(caller_stream, ch);', '\tplay_next_from((uint16_t)(caller_stream + 1u), ch);'),
    'Music_tie': ('\tgb_write8(channel_addr(wMusicTie_ADDR, ch), 0x80u);', '\tgb_write8(channel_addr(wMusicTie_ADDR, ch), 0u);'),
    'Music_stereo_panning': ('\tuint8_t mask = 0xEEu;', '\tuint8_t mask = 0xEFu;'),
    'Music_MainLoop': ('\t        (uint16_t)(caller_stream - 1u));', '\t        (uint16_t)(caller_stream - 2u));'),
    'Music_EndMainLoop': ('\tuint16_t stream = read16(channel_word_addr(wMusicMainLoopStart_ADDR, ch));', '\tuint16_t stream = (uint16_t)(read16(channel_word_addr(wMusicMainLoopStart_ADDR, ch)) + 1u);'),
    'Music_Loop': ('\tuint16_t continuation = (uint16_t)(caller_stream + 1u);', '\tuint16_t continuation = (uint16_t)(caller_stream + 2u);'),
    'Music_EndLoop': ('\tif (count != 0u)', '\tif (count == 0u)'),
    'Music_jp': ('\tuint16_t stream = (uint16_t)(wAudioArg |', '\tuint16_t stream = (uint16_t)(wAudioArg + 1u |'),
    'Music_call': ('\twrite16(sp, caller_stream);', '\twrite16(sp, (uint16_t)(caller_stream + 1u));'),
    'Music_ret': ('\tuint16_t stream = (uint16_t)(read16(sp) + 2u);', '\tuint16_t stream = (uint16_t)(read16(sp) + 3u);'),
    'Music_frequency_offset': ('\tone_byte_command(caller_stream, ch, wMusicFrequencyOffset_ADDR, wAudioArg);', '\tone_byte_command(caller_stream, ch, wMusicFrequencyOffset_ADDR, 0u);'),
    'Music_duty': ('\tone_byte_command(caller_stream, ch, wMusicDuty1_ADDR, (uint8_t)(wAudioArg & 0xC0u));', '\tone_byte_command(caller_stream, ch, wMusicDuty1_ADDR, 0u);'),
    'Music_volume': ('\tone_byte_command(caller_stream, ch, wMusicVolume_ADDR, wAudioArg);', '\tone_byte_command(caller_stream, ch, wMusicVolume_ADDR, 0u);'),
    'Music_wave': ('\twMusicWaveChange = 1u;', '\twMusicWaveChange = 0u;'),
    'Music_cutoff': ('\tone_byte_command(caller_stream, ch, wMusicCutoff_ADDR, wAudioArg);', '\tone_byte_command(caller_stream, ch, wMusicCutoff_ADDR, 0u);'),
    'Music_echo': ('\tone_byte_command(caller_stream, ch, wMusicEcho_ADDR, wAudioArg);', '\tone_byte_command(caller_stream, ch, wMusicEcho_ADDR, 0u);'),
    'Music_vibrato_type': ('\tgb_write8(channel_addr(wMusicVibratoType_ADDR, ch), wAudioArg);', '\tgb_write8(channel_addr(wMusicVibratoType_ADDR, ch), 0u);'),
    'Music_vibrato_delay': ('\tone_byte_command(caller_stream, ch, wMusicVibratoDelay_ADDR, wAudioArg);', '\tone_byte_command(caller_stream, ch, wMusicVibratoDelay_ADDR, 0u);'),
    'Music_pitch_offset': ('\tone_byte_command(caller_stream, ch, wMusicPitchOffset_ADDR, wAudioArg);', '\tone_byte_command(caller_stream, ch, wMusicPitchOffset_ADDR, 0u);'),
    'Music_adjust_pitch_offset': ('\tgb_write8(addr, (uint8_t)(wAudioArg + gb_read8(addr)));', '\tgb_write8(addr, (uint8_t)(wAudioArg - gb_read8(addr)));'),
    'Music_end': ('\tgb_write8(channel_addr(wMusicIsPlaying_ADDR, ch), 0u);', '\tgb_write8(channel_addr(wMusicIsPlaying_ADDR, ch), 1u);'),
    'GetChannelStackPointer': ('\treturn read16((uint16_t)(wMusicChannelStackPointers_ADDR + (uint16_t)ch * 2u));', '\treturn read16((uint16_t)(wMusicChannelStackPointers_ADDR + (uint16_t)(ch + 1u) * 2u));'),
    'SetChannelStackPointer': ('\twrite16((uint16_t)(wMusicChannelStackPointers_ADDR + (uint16_t)ch * 2u), sp);', '\twrite16((uint16_t)(wMusicChannelStackPointers_ADDR + (uint16_t)(ch + 1u) * 2u), sp);'),
    'PlayNextNote_pop': ('\tPlayNextNote(&caller_stream, ch);', '\tPlayNextNote(&caller_stream, (uint8_t)(ch + 1u));'),
    'Music_f4714': ('\tif ((wdd8c & 0x01u) != 0u)', '\tif ((wdd8c & 0x02u) != 0u)'),
    'Music_f475a': ('\tif ((wdd8c & 0x02u) != 0u)', '\tif ((wdd8c & 0x01u) != 0u)'),
    'Music_f479c': ('\tif ((wdd8c & 0x04u) != 0u)', '\tif ((wdd8c & 0x02u) != 0u)'),
    'LoadWaveInstrument': ('\tfor (uint8_t i = 0u; i < AUD3WAVE_SIZE; i++)', '\tfor (uint8_t i = 0u; i < AUD3WAVE_SIZE - 1u; i++)'),
    'Music_f480a': ('\tif ((wdd8c & 0x08u) != 0u)', '\tif ((wdd8c & 0x04u) != 0u)'),
    'Music_f4839': ('\tif ((wdd8c & 0x08u) != 0u)', '\tif ((wdd8c & 0x04u) != 0u)'),
    'Music_f485a': ('\tuint16_t frequency = UpdateVibrato(ch);', '\tuint16_t frequency = UpdateVibrato((uint8_t)(ch + 1u));'),
    'Music_f4866': ('\tgb_write8(APU_VOL, wMusicPanning);', '\tgb_write8(APU_VOL, 0u);'),
    'UpdateVibrato': ('\tif (delay == 0u)', '\tif (delay != 0u)'),
    'Music_f490b': ('\tuint8_t low = (uint8_t)de;', '\tuint8_t low = (uint8_t)(de + 1u);'),
    'Music_f4967': ('\tuint16_t frequency = de;', '\tuint16_t frequency = (uint16_t)(de + 1u);'),
    'Music_f4980': ('\tif ((d & 0x01u) == 0u)', '\tif ((d & 0x01u) != 0u)'),
    'CheckForEndOfSong': ('\tif (sum == 0u)', '\tif (sum != 0u)'),
    'Music_PauseSong': ('\tBackupSong();', '\tLoadBackup();'),
    'Music_ResumeSong': ('\tLoadBackup();', '\tBackupSong();'),
    'BackupSong': ('\twCurSongIDBackup = wCurSongID;', '\twCurSongIDBackup = 0u;'),
    'LoadBackup': ('\twCurSongID = wCurSongIDBackup;', '\twCurSongID = 0u;'),
    'CopyData': ('\t\tgb_write8(*de, gb_read8(*hl));', '\t\tgb_write8(*de, (uint8_t)(gb_read8(*hl) + 1u));'),
}

MUTATIONS = {
    name: {'source_symbol': name, 'before': before, 'after': after,
           'case_ids': [f'{name}-1'],
           'source': 'src/profiles/extended/home/music.c'}
    for name, (before, after) in ANCHORS.items()
}

from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES = legacy_to_schema(CASES, CONTRACT)
