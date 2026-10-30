#!/usr/bin/env python3
"""Structural PTF validation using only Python standard library."""
import struct,zlib,sys
from pathlib import Path
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'dist/Windows_11_PSP_Theme.ptf'
b=p.read_bytes(); assert b[:8]==b'\0PTF\0\1\0\0';assert len(b)<=768*1024
u16=lambda p:struct.unpack_from('<H',b,p)[0]
u32=lambda p:struct.unpack_from('<I',b,p)[0]
def fixed(off,n):return b[off:off+n].split(b'\0',1)[0].decode()
expected={0:{0,1,2},1:{0},2:set(range(1,9)),3:set(range(2,60)),4:{0,1,2,3}}
groups={}
for i in range(8):
 pos=u32(0x100+4*i)
 if not pos:continue
 assert pos+32<=len(b);g,n=u16(pos),u16(pos+2);end=u32(pos+8)+u32(pos+4);q=u32(pos+8);assert end<=len(b); slots=set()
 for _ in range(n):
  sub,typ,comp=u16(q),u16(q+4),u16(q+6);size,rawsize=u32(q+8),u32(q+12); assert sub not in slots;slots.add(sub);payload=b[q+32:q+32+size];assert len(payload)==size
  raw=zlib.decompress(payload) if comp==2 and size<rawsize else payload[:rawsize]
  assert len(raw)==rawsize
  if typ==5 and (g,sub)!=(0,2):assert raw[:12]==b'MIG.00.1PSP\0'
  if (g,sub)==(0,2):assert raw==struct.pack('<I',8) and comp==2
  if (g,sub)==(1,0):assert raw[:2]==b'BM' and struct.unpack_from('<ii',raw,18)==(480,272)
  q+=32+size
 assert q==end;groups[g]=slots
assert groups==expected,(groups,expected)
print(f'PASS: {p.name}; {len(b)} bytes; title={fixed(8,128)}; product={fixed(136,48)}; version={fixed(192,8)}; records={sum(map(len,groups.values()))}; groups={sorted(groups)}')
print('PASS: valid offsets, zlib payloads, supported slots, GIM signatures, wallpaper BMP dimensions, and 768 KiB limit')
