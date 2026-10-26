import subprocess, pymupdf, os
from playwright.sync_api import sync_playwright
H=os.path.dirname(os.path.abspath(__file__))
GRAD=open(os.path.join(H,'..','mag','raster_grad.js')).read()
MM=72/25.4
with sync_playwright() as p:
    b=p.chromium.launch()
    for src,out in [('kit.html','raw_screen.pdf'),('kit_bleed.html','raw_print.pdf')]:
        pg=b.new_page(); pg.goto('file://'+os.path.join(H,src)); pg.wait_for_timeout(1200); pg.evaluate(GRAD); pg.wait_for_timeout(500)
        pg.pdf(path=os.path.join(H,out),prefer_css_page_size=True,print_background=True); pg.close()
    b.close()
ICC=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','mag','icc','FOGRA39L_coated.icc')
SCREEN='DrinkHQ-Magazine-Media-Kit-October-2026.pdf'
PRINT='DrinkHQ-Magazine-Media-Kit-PRINT-A5-3mm-bleed-October-2026.pdf'
subprocess.run(['gs','-q','-dNOPAUSE','-dBATCH','-dSAFER','-sDEVICE=pdfwrite','-dCompatibilityLevel=1.6',
  '-sColorConversionStrategy=CMYK','-sProcessColorModel=DeviceCMYK',f'-sOutputICCProfile={ICC}',
  '-dDownsampleColorImages=true','-dColorImageDownsampleType=/Bicubic','-dColorImageResolution=300','-dColorImageDownsampleThreshold=1.0',
  '-dAutoFilterColorImages=false','-dColorImageFilter=/DCTEncode','-dEmbedAllFonts=true','-dSubsetFonts=true','-o','tmp_print.pdf',
  '-c','<< /ColorImageDict << /QFactor 0.4 /Blend 1 /HSamples [2 1 1 2] /VSamples [2 1 1 2] >> >> setdistillerparams','-f','raw_print.pdf'],check=True)
subprocess.run(['gs','-q','-dNOPAUSE','-dBATCH','-dSAFER','-sDEVICE=pdfwrite','-dCompatibilityLevel=1.6',
  '-sColorConversionStrategy=RGB','-dDownsampleColorImages=true','-dColorImageDownsampleType=/Bicubic','-dColorImageResolution=200','-dColorImageDownsampleThreshold=1.0',
  '-dAutoFilterColorImages=false','-dColorImageFilter=/DCTEncode','-o','tmp_screen.pdf',
  '-c','<< /ColorImageDict << /QFactor 0.4 /Blend 1 /HSamples [2 1 1 2] /VSamples [2 1 1 2] >> >> setdistillerparams','-f','raw_screen.pdf'],check=True)
meta={'title':'DrinkHQ Magazine Media Kit · Season 2027–28','author':'DrinkHQ','subject':'MEDIA-001 · October 2026'}
d=pymupdf.open('tmp_print.pdf')
for pg in d:
    r=pg.mediabox; pg.set_trimbox(pymupdf.Rect(3*MM,3*MM,r.width-3*MM,r.height-3*MM)); pg.set_bleedbox(r)
d.set_metadata(dict(meta,subject=meta['subject']+' · A5 148x210mm, 3mm bleed, CMYK FOGRA39')); d.save(PRINT,garbage=3,deflate=True)
d=pymupdf.open('tmp_screen.pdf'); d.set_metadata(meta); d.save(SCREEN,garbage=3,deflate=True)
for f in (SCREEN,PRINT): print(f, os.path.getsize(f)//1024,'KB')
