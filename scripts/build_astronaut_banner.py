"""Build a borderless space banner from local Friday scene captures.

Usage: python scripts/build_astronaut_banner.py path/to/frames --fonts C:/Windows/Fonts
Requires Pillow, NumPy and OpenCV. Source captures remain local; the website is never modified.
"""
import argparse
import math
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
COUNT = 160
SIZE = (1000, 430)


def planet(radius, color, ring=False):
    r=radius*3
    tile=Image.new("RGBA", (r*4,r*3))
    d=ImageDraw.Draw(tile)
    cx,cy=r*2,r*1.5
    for y in range(-r,r+1):
        for x in range(-r,r+1):
            if x*x+y*y>r*r: continue
            z=math.sqrt(max(0,1-(x*x+y*y)/(r*r)))
            light=max(.12, .28+.72*max(0,(-x/r*.45-y/r*.5+z*.72)))
            d.point((int(cx+x),int(cy+y)),fill=tuple(int(c*light) for c in color)+(255,))
    if ring:
        d.arc((cx-r*1.85,cy-r*.42,cx+r*1.85,cy+r*.42),5,175,fill=(186,170,217,210),width=2)
        d.arc((cx-r*1.85,cy-r*.42,cx+r*1.85,cy+r*.42),185,355,fill=(115,125,165,170),width=1)
    if not ring:
        # Low-contrast craters keep the moon from looking like a plain sphere.
        for x,y,size in ((-.3,-.2,.16),(.22,.3,.22),(.35,-.35,.12),(-.4,.4,.1)):
            px,py=cx+x*r,cy+y*r
            d.ellipse((px-size*r,py-size*r,px+size*r,py+size*r),fill=(135,149,166,255))
    return tile.resize((radius*4,radius*3),Image.Resampling.LANCZOS)


def motion_frames(scenes):
    """Estimate both motion directions instead of dissolving between silhouettes."""
    gray=[cv2.cvtColor(np.asarray(scene),cv2.COLOR_RGB2GRAY) for scene in scenes]
    forward=[]; backward=[]
    for a,b in zip(gray,gray[1:]):
        forward.append(cv2.calcOpticalFlowFarneback(a,b,None,.5,4,25,4,7,1.5,0))
        backward.append(cv2.calcOpticalFlowFarneback(b,a,None,.5,4,25,4,7,1.5,0))
    return forward,backward


def interpolate(scenes, flows, at):
    low=int(at); high=min(low+1,len(scenes)-1); amount=at-low
    if low==high or amount<.001: return scenes[low]
    a,b=np.asarray(scenes[low]),np.asarray(scenes[high])
    y,x=np.mgrid[:a.shape[0],:a.shape[1]].astype(np.float32)
    fwd,back=flows[0][low],flows[1][low]
    first=cv2.remap(a,x-amount*fwd[:,:,0],y-amount*fwd[:,:,1],cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
    second=cv2.remap(b,x-(1-amount)*back[:,:,0],y-(1-amount)*back[:,:,1],cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
    return Image.fromarray(cv2.addWeighted(first,1-amount,second,amount,0))


def build(frames_dir, fonts):
    captures=sorted(frames_dir.glob("[0-9][0-9][0-9].png"))
    if len(captures)<2: raise ValueError("At least two captured PNG frames are required")
    font=lambda size,bold=False: ImageFont.truetype(str(fonts/("segoeuib.ttf" if bold else "segoeui.ttf")),size)
    base=Image.new("RGB",SIZE,"black")
    # Sparse, fixed stars keep the lettering readable.
    rng=random.Random(19)
    d=ImageDraw.Draw(base)
    for _ in range(170):
        x,y=rng.randrange(1000),rng.randrange(430)
        if 35<x<415 and 115<y<290: continue
        value=rng.choice((40,55,75,100,135))
        d.point((x,y),fill=(value,value,min(255,value+22)))
    for x,y in ((87,58),(360,72),(255,337),(470,380)):
        d.line((x-2,y,x+2,y),fill=(107,132,168));d.line((x,y-2,x,y+2),fill=(107,132,168))
    mask=Image.new("L",(600,414))
    pixels=mask.load()
    for y in range(414):
        for x in range(600):
            # Smoothstep avoids a visible rectangular fade around Earth.
            edge=min(1,x/125)
            fade=edge*edge*(3-2*edge)*min(1,y/12)
            pixels[x,y]=int(255*fade)
    scenes=[]
    for path in captures:
        with Image.open(path) as shot:
            scenes.append(shot.convert("RGB").crop((155,125,900,640)).resize((600,414),Image.Resampling.LANCZOS))
    flows=motion_frames(scenes)
    moon=planet(15,(181,193,212))
    saturn=planet(19,(175,151,203),True)
    satellite=Image.new("RGBA",(78,58))
    sd=ImageDraw.Draw(satellite)
    sd.rectangle((2,18,28,39),fill="#254f86");sd.rectangle((49,18,75,39),fill="#254f86")
    for x in (9,18,56,65):sd.line((x,19,x,38),fill="#7392b9")
    sd.line((3,28,74,28),fill="#7392b9")
    sd.rounded_rectangle((29,19,48,38),radius=3,fill="#b1bbc9")
    sd.rectangle((33,21,44,24),fill="#e5e5db")
    sd.line((38,19,44,7),fill="#9ca9bb",width=2);sd.ellipse((40,4,47,9),fill="#cfb894")
    satellite=satellite.resize((156,116),Image.Resampling.LANCZOS)
    frames=[]
    for i in range(COUNT):
        phase=i/COUNT*math.tau
        # A cosine timeline pauses naturally at both ends, including the wrap.
        at=(1-math.cos(phase))*.5*(len(scenes)-1)
        scene=interpolate(scenes,flows,at)
        frame=base.copy();frame.paste(scene,(400,16),mask)
        layer=frame.convert("RGBA")
        layer.alpha_composite(moon,(337+int(7*math.sin(phase)),18+int(5*math.cos(phase))))
        layer.alpha_composite(saturn,(871+int(9*math.sin(phase+.8)),18+int(7*math.cos(phase))))
        craft=satellite.rotate(-16+8*math.sin(phase),resample=Image.Resampling.BICUBIC,expand=True)
        craft=craft.resize((craft.width//2,craft.height//2),Image.Resampling.LANCZOS)
        layer.alpha_composite(craft,(857+int(11*math.cos(phase)),329+int(7*math.sin(phase))))
        glow=Image.new("RGBA",SIZE)
        gd=ImageDraw.Draw(glow)
        # Sparse twinkles breathe slowly rather than flashing.
        for n,(x,y) in enumerate(((87,58),(360,72),(255,337),(470,380))):
            brightness=int(30+25*(1+math.sin(phase+n*1.7)))
            gd.ellipse((x-3,y-3,x+3,y+3),fill=(95,145,220,brightness))
        layer=Image.alpha_composite(layer,glow.filter(ImageFilter.GaussianBlur(2)))
        d=ImageDraw.Draw(layer)
        # A small, repeating meteor stays clear of the name and astronaut.
        t=(i/COUNT+.35)%1
        if t<.18:
            u=t/.18;x=320+int(u*90);y=35+int(u*38)
            alpha=int(180*math.sin(u*math.pi))
            d.line((x-16,y-7,x,y),fill=(152,183,229,alpha),width=1)
        d.text((45,127),"I’m Koushoo.",font=font(44,True),fill="#eef2f8")
        d.text((47,191),"A student, building small things.",font=font(18),fill="#adb9cd")
        d.text((47,226),"learning as I go.",font=font(14),fill="#8091ab")
        d.text((47,371),"Python  ·  Linux  ·  small tools",font=font(13),fill="#7f93b2")
        # Flatten alpha against black so stars and meteor never create transparency.
        canvas=Image.new("RGB",SIZE,"black");canvas.paste(layer,mask=layer.getchannel("A"))
        frames.append(canvas)
    # Full-colour delivery avoids GIF banding in Earth's atmosphere.
    webp=ROOT/"assets"/"space-orbit-v2.webp"
    frames[0].save(webp,save_all=True,append_images=frames[1:],duration=90,loop=0,
                   quality=90,method=4,allow_mixed=True,minimize_size=True)
    print("Full-colour WebP:",webp.stat().st_size,"bytes",flush=True)
    sample=Image.new("RGB",(400,172*len(frames)))
    for i,frame in enumerate(frames):sample.paste(frame.resize((400,172)),(0,i*172))
    palette=sample.quantize(colors=248)
    values=palette.getpalette()[:744]
    for color in ("000000","eef2f8","adb9cd","8091ab","7f93b2"):values.extend(bytes.fromhex(color))
    values.extend([0]*(768-len(values)));palette.putpalette(values)
    indexed=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
    target=ROOT/"assets"/"space-orbit-v2.gif"
    indexed[0].save(target,save_all=True,append_images=indexed[1:],duration=90,loop=0,optimize=True,disposal=1)
    frames[0].save(ROOT/"assets"/"space-orbit-v2-still.png")
    print(COUNT,"frames;",target.stat().st_size,"bytes")


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("frames",type=Path)
    parser.add_argument("--fonts",type=Path,required=True)
    args=parser.parse_args();build(args.frames,args.fonts)
