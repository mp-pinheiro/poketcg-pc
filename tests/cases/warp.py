POISON={"a":0xAA,"f":0xF0,"b":0xBB,"c":0xCC,"d":0xDD,"e":0xEE,"hl":0x1234}
wCurMap=0xD32F;wPlayerXCoord=0xD330;wPlayerYCoord=0xD331;wPlayerDirection=0xD334;wTempMap=0xD0BB;wTempPlayerXCoord=0xD0BC;wTempPlayerYCoord=0xD0BD;wTempPlayerDirection=0xD0BE
CONTRACT={"_HandleMapWarp":{"compare":("a","f","b","c","d","e","hl"),"preserve":("b","c","d","e","hl")}}
def _memory(m,x,y,d,t=b"\x11\x22\x33\x44"):return {wCurMap:bytes((m,)),wPlayerXCoord:bytes((x,)),wPlayerYCoord:bytes((y,)),wPlayerDirection:bytes((d,)),wTempMap:t}
CASES={"_HandleMapWarp":[{"wram":_memory(1,0,0,0)},dict(POISON,wram=_memory(1,0x1A,0x0A,2,b"\0\0\0\0")),{"wram":_memory(1,0x0E,0x1C,1)},{"wram":_memory(1,0x10,0x1C,3)},{"wram":_memory(2,0,0x0A,4)}]}
MUTATIONS={"_HandleMapWarp":{"source_symbol":"_HandleMapWarp","before":"if(wx==x){","after":"if(wx!=x){","case_ids":["_HandleMapWarp-0","_HandleMapWarp-1","_HandleMapWarp-2","_HandleMapWarp-3","_HandleMapWarp-4"]}}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES=legacy_to_schema(CASES,CONTRACT)
