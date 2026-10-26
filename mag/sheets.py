from PIL import Image
import glob,sys
def sheet(files,out,w=1500):
    ims=[Image.open(f) for f in files]
    for im in ims: im.thumbnail((w//2-10,560))
    rows=[ims[i:i+2] for i in range(0,len(ims),2)]
    H=sum(max(i.height for i in r)+10 for r in rows)
    c=Image.new('RGB',(w,H),(60,60,70)); y=0
    for r in rows:
        x=0
        for im in r: c.paste(im,(x,y)); x+=w//2
        y+=max(i.height for i in r)+10
    c.save(out,quality=85)
a=sorted(glob.glob('qa/16_s*.png'));b=sorted(glob.glob('qa/32_s*.png'))
sheet(a[:6],'qa/A16a.jpg');sheet(a[6:],'qa/A16b.jpg')
sheet(b[:6],'qa/B1.jpg');sheet(b[6:12],'qa/B2.jpg');sheet(b[12:],'qa/B3.jpg')
