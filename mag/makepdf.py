import os, subprocess, pymupdf
from playwright.sync_api import sync_playwright
EMAIL_CSS='@page{size:148mm 210mm;margin:0}@media print{.sheet{width:148mm!important;height:210mm!important}.clip{left:-3mm!important;top:-3mm!important}.sheet::before,.sheet::after{display:none!important}}'
MM=72/25.4
GRAD=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'raster_grad.js')).read()
import sys
if 'render' in sys.argv:
  with sync_playwright() as pw:
      b=pw.chromium.launch()
      for t in ['16','32']:
          # press (raw)
          p=b.new_page(); p.goto('file://'+os.path.abspath(f'out_press/DrinkHQ-Magazine_Issue-01_{t}pp_Official-Record.html')); p.wait_for_timeout(2500); p.evaluate(GRAD)
          p.pdf(path=f'pdf/raw_press_{t}.pdf',width='160mm',height='222mm',print_background=True,prefer_css_page_size=True); p.close()
          # email (raw)
          p=b.new_page(); p.goto('file://'+os.path.abspath(f'out/DrinkHQ-Magazine_Issue-01_{t}pp_Official-Record.html')); p.wait_for_timeout(2000)
          p.add_style_tag(content=EMAIL_CSS); p.wait_for_timeout(300); p.evaluate(GRAD)
          p.pdf(path=f'pdf/raw_email_{t}.pdf',width='148mm',height='210mm',print_background=True,prefer_css_page_size=True); p.close()
      b.close()
ICC='/usr/share/texlive/texmf-dist/tex/generic/colorprofiles/FOGRA39L_coated.icc'
for t in ['16','32']:
    press=f'pdf/DrinkHQ-Magazine-Issue-01-{t}pp-Press-300dpi-October-2026.pdf'
    email=f'pdf/DrinkHQ-Magazine-Issue-01-{t}pp-Email-October-2026.pdf'
    subprocess.run(['gs','-q','-dNOPAUSE','-dBATCH','-dSAFER','-sDEVICE=pdfwrite','-dCompatibilityLevel=1.6',
        '-sColorConversionStrategy=CMYK','-sProcessColorModel=DeviceCMYK',f'-sOutputICCProfile={ICC}',
        '-dDownsampleColorImages=true','-dColorImageDownsampleType=/Bicubic','-dColorImageResolution=300','-dColorImageDownsampleThreshold=1.0',
        '-dDownsampleGrayImages=true','-dGrayImageResolution=300','-dGrayImageDownsampleThreshold=1.0',
        '-dAutoFilterColorImages=false','-dColorImageFilter=/DCTEncode','-dEmbedAllFonts=true','-dSubsetFonts=true','-o',press+'.tmp',
        '-c','<< /ColorACSImageDict << /QFactor 0.66 /Blend 1 /HSamples [2 1 1 2] /VSamples [2 1 1 2] >> /ColorImageDict << /QFactor 0.66 /Blend 1 /HSamples [2 1 1 2] /VSamples [2 1 1 2] >> >> setdistillerparams',
        '-f',f'pdf/raw_press_{t}.pdf'],check=True)
    d=pymupdf.open(press+'.tmp')
    for pg in d:
        r=pg.mediabox
        pg.set_bleedbox(pymupdf.Rect(3*MM,3*MM,r.width-3*MM,r.height-3*MM))
        pg.set_trimbox(pymupdf.Rect(6*MM,6*MM,r.width-6*MM,r.height-6*MM))
    d.set_metadata({'title':f'DrinkHQ Magazine Issue 01 — {t}pp — Press','author':'DrinkHQ','subject':'A5 148x210mm, 3mm bleed, crop marks, CMYK FOGRA39'})
    d.save(press,garbage=3,deflate=True); d.close(); os.remove(press+'.tmp')
    subprocess.run(['gs','-q','-dNOPAUSE','-dBATCH','-dSAFER','-sDEVICE=pdfwrite','-dCompatibilityLevel=1.6',
        '-sColorConversionStrategy=RGB','-dDownsampleColorImages=true','-dColorImageDownsampleType=/Bicubic','-dColorImageResolution=180','-dColorImageDownsampleThreshold=1.0',
        '-dAutoFilterColorImages=false','-dColorImageFilter=/DCTEncode','-dEmbedAllFonts=true','-dSubsetFonts=true','-o',email,
        '-c','<< /ColorACSImageDict << /QFactor 0.4 /Blend 1 /HSamples [2 1 1 2] /VSamples [2 1 1 2] >> /ColorImageDict << /QFactor 0.4 /Blend 1 /HSamples [2 1 1 2] /VSamples [2 1 1 2] >> >> setdistillerparams',
        '-f',f'pdf/raw_email_{t}.pdf'],check=True)
    for f in [press,email]:
        d=pymupdf.open(f); pg=d[0]
        print(os.path.basename(f), d.page_count,'pp', round(pg.mediabox.width/MM,1),'x',round(pg.mediabox.height/MM,1),'mm', os.path.getsize(f)//1024,'KB','trim',[round(x/MM,1) for x in pg.trimbox])
