import json,sys
from PIL import Image
import numpy as np
R='/mnt/user-data/uploads/Sunnyside_World_ASSET_PACK_V2.1/Sunnyside_World_ASSET_PACK_V2.1/Sunnyside_World_Assets/'
ts=Image.open(R+'Tileset/spr_tileset_sunnysideworld_16px.png').convert('RGBA')
items=[]  # (name, image, meta)
def add(n,im,**m):items.append((n,im.convert('RGBA'),m))
def px(n,x,y,w,h,**m):add(n,ts.crop((x,y,x+w,y+h)),**m)
def tl(n,tx,ty,w=1,h=1):px(n,tx*16,ty*16,w*16,h*16)
# --- ground tiles
for i,(x,y) in enumerate([(1,1),(2,1)]):tl('g%d'%i,x,y)
for i,(x,y) in enumerate([(1,2),(2,2),(3,2),(4,2),(5,2),(6,2),(1,4),(2,4),(3,4)]):tl('gs%d'%i,x,y)
tl('dirt',1,7)
for i,x in enumerate([9,10,11]):tl('dirtp%d'%i,x,7)
for i,x in enumerate([5,7,8,9]):tl('sand%d'%i,x,1)
tl('water',11,18,4,4)
for i,y in enumerate([12,20,28,36,44]):tl('sh%d'%i,16,y)
tl('plank',23,12)
# --- sprites from tileset
S={'bush':(787,21,26,23),'bushBerry':(787,53,26,23),'bushOrange':(787,85,26,23),'pine':(822,99,20,29),
'rock':(498,65,14,12),'fenceH':(612,0,28,12),'fenceH2':(612,33,28,13),'fenceP':(627,15,13,15),
'well':(645,306,22,42),'wellStone':(597,310,22,27),'fire':(595,342,25,22),'crates':(623,143,34,34),'crateBig':(632,184,32,34),
'stand':(719,196,49,29),'statue':(703,291,65,57),
'fl0':(523,17,6,7),'fl1':(532,17,7,8),'fl2':(551,18,9,10),'fl3':(532,33,7,8),'fl4':(562,49,13,13),'fl5':(523,50,6,8),'fl6':(531,50,9,8),'fl7':(550,51,11,10),'fl8':(537,56,8,8),
'tu0':(453,37,10,11),'tu1':(469,37,10,11),'tu2':(437,38,10,10),'tu3':(485,38,10,10),'tu4':(449,48,10,12),'tu5':(465,48,10,12),'tu6':(481,49,10,11),
'cl0':(450,64,15,12),'cl1':(466,64,15,12),'cl2':(434,65,15,11)}
for n,(x,y,w,h) in S.items():px(n,x,y,w,h)
for i,y0 in enumerate([9,17,25,33,41]):tl('house%d'%i,32,y0,3,5)
# --- strips
def strip(n,path,fw,fh=None):
    im=Image.open(R+path).convert('RGBA');fh=fh or im.height
    add(n,im,fw=fw,fh=fh,nf=im.width//fw)
strip('tree1','Elements/Plants/spr_deco_tree_01_strip4.png',32)
strip('tree2','Elements/Plants/spr_deco_tree_02_strip4.png',28)
strip('cow','Elements/Animals/spr_deco_cow_strip4.png',32)
strip('sheep','Elements/Animals/spr_deco_sheep_01_strip4.png',32)
strip('pig','Elements/Animals/spr_deco_pig_01_strip4.png',32)
strip('chicken','Elements/Animals/spr_deco_chicken_01_strip4.png',32)
strip('duck','Elements/Animals/spr_deco_duck_01_strip4.png',16)
# --- humans: hair x shirt variants, frames cropped (x 43..53, y 22..38)
H=['shorthair','bowlhair','curlyhair','longhair','mophair','spikeyhair']
base=Image.open(R+'Characters/Human/WALKING/base_walk_strip8.png').convert('RGBA')
hair={h:Image.open(R+'Characters/Human/WALKING/%s_walk_strip8.png'%h).convert('RGBA') for h in H}
SH=[None,((196,66,66),(132,40,52)),((76,160,96),(46,104,64)),((232,184,64),(176,122,40)),((150,96,200),(96,58,140)),((70,170,190),(40,112,134))]
def recolor(im,pal):
    if not pal:return im
    a=np.array(im);m=(a[:,:,0]==55)&(a[:,:,1]==68)&(a[:,:,2]==100);a[m,:3]=pal[0]
    m=(a[:,:,0]==36)&(a[:,:,1]==43)&(a[:,:,2]==66);a[m,:3]=pal[1];return Image.fromarray(a)
HW,HH=12,17
for hi,h in enumerate(H):
    for si,pal in enumerate(SH):
        row=Image.new('RGBA',(HW*8,HH),(0,0,0,0))
        for f in range(8):
            c=Image.new('RGBA',(96,64),(0,0,0,0))
            c.alpha_composite(recolor(base.crop((f*96,0,f*96+96,64)),pal))
            c.alpha_composite(hair[h].crop((f*96,0,f*96+96,64)))
            row.alpha_composite(c.crop((42,22,42+HW,22+HH)),(f*HW,0))
        add('hu_%d_%d'%(hi,si),row,fw=HW,fh=HH,nf=8)
# --- pack (shelf)
items.sort(key=lambda t:-t[1].height)
AW=640;x=y=rowh=0;pos={}
for n,im,m in items:
    w,h=im.size
    if x+w>AW:x=0;y+=rowh+1;rowh=0
    pos[n]=dict(x=x,y=y,w=w,h=h,**m);x+=w+1;rowh=max(rowh,h)
AH=y+rowh+1
atlas=Image.new('RGBA',(AW,AH),(0,0,0,0))
for n,im,m in items:atlas.alpha_composite(im,(pos[n]['x'],pos[n]['y']))
out='/tmp/claude-0/-home-claude/81a3521c-c2c1-523c-92f7-31dd832fb5c7/scratchpad/atl/'
atlas.save(out+'atlas.png',optimize=True)
json.dump(pos,open(out+'atlas.json','w'),separators=(',',':'))
import os;print(atlas.size,os.path.getsize(out+'atlas.png'),len(pos))
