#!/usr/bin/env python3
"""Rasterize editable SVGs and make native assets and labelled simulated previews."""
import json,subprocess,tempfile
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageChops
R=Path(__file__).resolve().parents[1]; M=json.loads((R/'source/icon-map.json').read_text()); L=Image.Resampling.LANCZOS
for group,items in M.items():
 for key,(_,name) in items.items():
  src=R/f'source/icons/{group}-{key}-{name}.svg'
  with tempfile.NamedTemporaryFile(suffix='.png') as tmp:
   subprocess.run(['inkscape',str(src),'--export-filename='+tmp.name,'--export-width=192','--export-height=192'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
   im=Image.open(tmp.name).convert('RGBA')
   if group=='category':
    base=Image.new('RGBA',(64,48));base.alpha_composite(im.resize((48,48),L),(8,0)); base.save(R/f'assets/categories/{int(key):02}.png')
   else:
    size=48 if group=='first' else 32; folder='first' if group=='first' else 'second';body=im.resize((size,size),L);body.save(R/f'assets/{folder}/{int(key):02}-body.png')
    core=Image.new('L',(size+16,size+16));core.paste(body.getchannel('A'),(8,8)); halo=ImageChops.subtract(core.filter(ImageFilter.GaussianBlur(4)).point(lambda x:int(x*.9)),core)
    # 63 visible alpha levels and transparent black; focus is an outer halo.
    halo=halo.point(lambda x:round(round(x*63/255)*255/63));focus=Image.new('RGBA',core.size,(255,255,255,0));focus.putalpha(halo);focus.save(R/f'assets/{folder}/{int(key):02}-focus.png')
wall=Image.open(R/'wallpapers/bloom-480x272.png').convert('RGBA')
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';f=ImageFont.truetype(font,11);small=ImageFont.truetype(font,9)
cat=[1,2,3,4,6,7,8]; names={1:'Settings',2:'Photo',3:'Music',4:'Video',6:'Game',7:'Network',8:'Extras'}

def screen(selected,rows,filename):
 im=wall.copy();d=ImageDraw.Draw(im);x=110; pos=cat.index(selected)
 for i,c in enumerate(cat):
  xx=x+(i-pos)*82;icon=Image.open(R/f'assets/categories/{c:02}.png').convert('RGBA')
  if c!=selected: icon.putalpha(icon.getchannel('A').point(lambda a:int(a*.38)))
  im.alpha_composite(icon,(xx-32,48))
 d=ImageDraw.Draw(im)
 def txt(xy,t,font=f,fill='white'):
  x,y=xy;d.text((x+1,y+1),t,font=font,fill='#102445');d.text((x,y),t,font=font,fill=fill)
 txt((94,99),names[selected]);txt((368,14),'10/30   12:00',small)
 for j,(id,label) in enumerate(rows[:3]):
  yy=137+j*64; body=Image.open(R/f'assets/first/{id:02}-body.png').convert('RGBA')
  if j: body.putalpha(body.getchannel('A').point(lambda a:int(a*.36)))
  im.alpha_composite(body,(86,yy-24));d=ImageDraw.Draw(im);txt((149,yy-6),label)
 im.convert('RGB').save(R/'screenshots'/filename)
 return im
p=screen(1,[(16,'USB Connection'),(22,'System Settings'),(24,'Theme Settings')],'01-settings-preview.png')
screen(6,[(54,'System Storage'),(54,'Saved Data Utility — System Storage')],'02-psp-go-preview.png')
screen(6,[(8,'Game Sharing'),(10,'Saved Data Utility'),(2,'Memory Stick')],'07-game-preview.png')
screen(2,[(6,'Camera'),(2,'Memory Stick')],'03-photo-preview.png')
screen(3,[(2,'Memory Stick')],'04-music-preview.png')
screen(4,[(2,'Memory Stick')],'05-video-preview.png')
screen(7,[(48,'Internet Browser'),(38,'Network Settings')],'06-network-preview.png')
p.resize((300,170),L).save(R/'assets/preview.png')
thumb=Image.new('RGBA',(16,16));td=ImageDraw.Draw(thumb);td.rectangle((2,2,7,7),fill='#16a4f3');td.rectangle((9,2,14,7),fill='#16a4f3');td.rectangle((2,9,7,14),fill='#16a4f3');td.rectangle((9,9,14,14),fill='#16a4f3');thumb.save(R/'assets/thumbnail.png')
print('Rendered all assets and six simulated previews')
