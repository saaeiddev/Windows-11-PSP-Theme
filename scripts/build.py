#!/usr/bin/env python3
"""Build a PTF v1 theme from the project PNGs, without a PSP firmware image."""
import io,json,struct,zlib
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]
def u16(x): return struct.pack('<H',x)
def u32(x): return struct.pack('<I',x)
def block(t,body,next=None):
 size=16+len(body); return struct.pack('<HHIII',t,0,size,size if next is None else next,16)+body
def imgblock(t,fmt,order,w,h,bpp,pixels,level):
 hbuf=bytearray(64);struct.pack_into('<HHHHHHHHH',hbuf,0,48,0,fmt,order,w,h,bpp,16,8);struct.pack_into('<H',hbuf,18,2);struct.pack_into('<III',hbuf,24,48,64,64+len(pixels));struct.pack_into('<HHHH',hbuf,40,level,1,3,1);struct.pack_into('<I',hbuf,48,64)
 return block(t,bytes(hbuf)+pixels)
def gim(image,indexed,focus=False):
 im=image.convert('RGBA');w,h=im.size
 if indexed:
  if focus:
   pal=[0,0,0,0]+[v for i in range(1,64) for v in (255,255,255,round(i*255/63))]+[0]*(192*4)
   idx=bytes(round(a*63/255) for a in im.getchannel('A').tobytes())
  else:
   q=im.quantize(colors=256,method=Image.Quantize.FASTOCTREE,dither=Image.Dither.NONE)
   pal=q.getpalette('RGBA');pal=(pal+[0]*1024)[:1024];idx=q.tobytes()
  tile=bytearray()
  for oy in range(0,(h+7)//8*8,8):
   for ox in range(0,(w+15)//16*16,16):
    for y in range(8):
     for x in range(16): tile.append(idx[(oy+y)*w+ox+x] if ox+x<w and oy+y<h else 0)
  inner=imgblock(5,3,0,256,1,32,bytes(pal),2)+imgblock(4,5,1,w,h,8,bytes(tile),1)
 else: inner=imgblock(4,3,0,w,h,32,im.tobytes(),1)
 picture=block(3,inner,next=16);root=block(2,picture,next=16)
 return b'MIG.00.1PSP\0\0\0\0\0'+root

def record(sub,typ,raw,mode=False):
 if mode: comp=2;payload=raw
 else:
  z=zlib.compress(raw,9)
  comp,payload=(2,z) if len(z)+3<len(raw) else (0,raw)
  payload+=b'\0'*((-len(payload))%4)
  if comp==0 and len(payload)!=len(raw): raise ValueError('unaligned uncompressed record')
 return struct.pack('<HHHHII',sub,0,typ,comp,len(payload),len(raw))+bytes(16)+payload

def fixed(buf,off,length,s):
 b=s.encode('utf-8'); assert len(b)<length;buf[off:off+len(b)]=b

def build():
 m=json.loads((R/'source/icon-map.json').read_text()); groups={}
 preview=Image.open(R/'assets/preview.png'); thumb=Image.open(R/'assets/thumbnail.png')
 groups[0]=[record(0,5,gim(thumb,True)),record(1,5,gim(preview,False)),record(2,5,u32(8),True)]
 bmp=io.BytesIO();Image.open(R/'wallpapers/bloom-480x272.png').convert('RGB').save(bmp,'BMP');groups[1]=[record(0,4,bmp.getvalue())]
 groups[2]=[record(int(k),5,gim(Image.open(R/f'assets/categories/{int(k):02}.png'),True)) for k in m['category']]
 for group,folder in [(3,'first'),(4,'second')]:
  groups[group]=[]
  for key in m['first' if group==3 else 'second']:
   i=int(key)
   for slot,suffix in [(i,'body'),(i+1,'focus')]:groups[group].append(record(slot,5,gim(Image.open(R/f'assets/{folder}/{i:02}-{suffix}.png'),True,focus=suffix=='focus')))
 header=bytearray(0x120);header[:8]=b'\x00PTF\x00\x01\x00\x00';fixed(header,8,128,'Windows 11 PSP Theme');fixed(header,136,48,'WINDOWS11');fixed(header,184,8,'6.20');fixed(header,192,8,'0.9.0');struct.pack_into('<I',header,200,8)
 data=bytearray(header)
 for i,(group,records) in enumerate(sorted(groups.items())):
  offset=len(data);struct.pack_into('<I',data,0x100+4*i,offset);body=b''.join(records);data+=struct.pack('<HHII',group,len(records),len(body),offset+32)+bytes(20)+body
 out=R/'dist/Windows_11_PSP_Theme.ptf';out.write_bytes(data);print(f'{out} {len(data)} bytes');assert len(data)<=768*1024
if __name__=='__main__':build()
