import os, subprocess, pymupdf
from playwright.sync_api import sync_playwright
EMAIL_CSS='@page{size:148mm 210mm;margin:0}@media print{.sheet{width:148mm!important;height:210mm!important}.clip{left:-3mm!important;top:-3mm!important}.sheet::before,.sheet::after{display:none!important}}'
GRAD=open('raster_grad.js').read()
subprocess.run('DHQ_LATINEXT=1 DHQ_IMGDIR=web_print DHQ_OUTDIR=out_canva DHQ_FONTDIR=fonts_canva python3 gen.py',shell=True,check=True,stdout=subprocess.DEVNULL)
with sync_playwright() as pw:
    b=pw.chromium.launch(); p=b.new_page()
    p.goto('file://'+os.path.abspath('out_canva/DrinkHQ-Magazine_Issue-01_32pp_Official-Record.html')); p.wait_for_timeout(3000)
    p.add_style_tag(content=EMAIL_CSS); p.wait_for_timeout(300); p.evaluate(GRAD)
    p.pdf(path='pdf/raw_canva_32.pdf',width='148mm',height='210mm',print_background=True,prefer_css_page_size=True); b.close()
subprocess.run(['gs','-q','-dNOPAUSE','-dBATCH','-dSAFER','-sDEVICE=pdfwrite','-dCompatibilityLevel=1.6','-sColorConversionStrategy=RGB',
 '-dDownsampleColorImages=true','-dColorImageDownsampleType=/Bicubic','-dColorImageResolution=250','-dColorImageDownsampleThreshold=1.0',
 '-dAutoFilterColorImages=false','-dColorImageFilter=/DCTEncode','-dEmbedAllFonts=true','-dSubsetFonts=false','-o','pdf/canva_full.pdf',
 '-c','<< /ColorImageDict << /QFactor 0.3 /Blend 1 /HSamples [1 1 1 1] /VSamples [1 1 1 1] >> >> setdistillerparams','-f','pdf/raw_canva_32.pdf'],check=True)
d=pymupdf.open('pdf/canva_full.pdf'); os.makedirs('canva',exist_ok=True)
for a,b in [(1,8),(9,16),(17,24),(25,32)]:
    o=pymupdf.open(); o.insert_pdf(d,from_page=a-1,to_page=b-1)
    o.set_metadata({'title':f'DrinkHQ Magazine Issue 01 — Canva edition — pages {a}–{b}','author':'DrinkHQ'})
    fn=f'canva/DrinkHQ-Magazine-Issue-01-Canva-Pages-{a:02d}-{b:02d}-October-2026.pdf'
    o.save(fn,garbage=3,deflate=True)
    n=sum(sum(len(l['spans']) for bl in pg.get_text('dict')['blocks'] if bl['type']==0 for l in bl['lines'])+len(pg.get_images())+len(pg.get_drawings()) for pg in o)
    print(os.path.basename(fn), os.path.getsize(fn)//1024,'KB', 'elements≈',n)
