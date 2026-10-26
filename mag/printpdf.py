import os, pymupdf
from playwright.sync_api import sync_playwright
from PIL import Image
names={'16':'DrinkHQ-Magazine-Issue-01-Official-Record-16pp-June-2027','32':'DrinkHQ-Magazine-Issue-01-Official-Record-32pp-June-2027'}
with sync_playwright() as pw:
    b=pw.chromium.launch()
    for t,nm in names.items():
        p=b.new_page(); p.goto('file://'+os.path.abspath(f'out/DrinkHQ-Magazine_Issue-01_{t}pp_Official-Record.html')); p.wait_for_timeout(2000)
        out=f'out/{nm}_print-A5-3mm-bleed.pdf'
        p.pdf(path=out,width='160mm',height='222mm',print_background=True,prefer_css_page_size=True)
        d=pymupdf.open(out); print(t,d.page_count,os.path.getsize(out)//1024,'KB')
        ims=[]
        for pg in d:
            pix=pg.get_pixmap(dpi=28); ims.append(Image.frombytes('RGB',(pix.width,pix.height),pix.samples))
        cols=8; w,h=ims[0].size
        c=Image.new('RGB',(cols*(w+6),((len(ims)+cols-1)//cols)*(h+6)),'#777')
        for i,im in enumerate(ims): c.paste(im,((i%cols)*(w+6),(i//cols)*(h+6)))
        c.save(f'qa/pdfall{t}.png')
    b.close()
