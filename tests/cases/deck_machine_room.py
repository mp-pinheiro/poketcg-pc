POISON={"a":0xAA,"f":0xF0,"b":0xBB,"c":0xCC,"d":0xDD,"e":0xEE,"hl":0x1234}
wTxRam2=0xCE3F
CONTRACT={"Func_d96c":{"compare":("a","b","c","d","e","hl"),"preserve":("d","e")}}
CASES={"Func_d96c":[{"a":0,"wram":{wTxRam2:b"\xff\xff\xff"},"read":{wTxRam2:3}},{"a":2,"wram":{wTxRam2:b"\xff\xff\xff"},"read":{wTxRam2:3}},dict(POISON,a=2,wram={wTxRam2:b"\xff\xff\xff"},read={wTxRam2:3}),{"a":9,"wram":{wTxRam2:b"\xff\xff\xff"},"read":{wTxRam2:3}},dict(POISON,a=0xFF,wram={wTxRam2:b"\xff\xff\xff"},read={wTxRam2:3})]}
from tests.cases._schema_migration import legacy_to_schema
SCHEMA2_CASES=legacy_to_schema(CASES,CONTRACT)
MUTATIONS={"Func_d96c":{"source_symbol":"Func_d96c","before":"uint8_t offset=(uint8_t)((uint8_t)(a-2u)<<1);","after":"uint8_t offset=(uint8_t)((uint8_t)(a-1u)<<1);","case_ids":["Func_d96c-1","Func_d96c-2","Func_d96c-3"]}}
