from playwright.sync_api import sync_playwright
from PIL import Image
import os
with sync_playwright() as pw:
    b=pw.chromium.launch(); p=b.new_page(viewport={'width':1200,'height':1000},device_scale_factor=840/559.4)
    p.goto('file://'+os.path.abspath('out/DrinkHQ-Magazine_Issue-01_16pp_Official-Record.html')); p.wait_for_timeout(1500)
    p.locator('.sheet').first.screenshot(path='qa/cov_new.png'); b.close()
a=Image.open('qa/cov_new.png').convert('RGB').resize((840,1192)); o=Image.open('web_print/cover_issue01.jpg')
S=Image.new('RGB',(1690,1192),'white'); S.paste(o,(0,0)); S.paste(a,(850,0)); S.save('qa/cov_cmp.png')
