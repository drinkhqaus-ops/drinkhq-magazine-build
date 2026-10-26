import os,sys
from playwright.sync_api import sync_playwright
from PIL import Image
os.makedirs('qa',exist_ok=True)
with sync_playwright() as pw:
    b=pw.chromium.launch()
    for tag in ['16','32']:
        f=os.path.abspath(f'out/DrinkHQ-Magazine_Issue-01_{tag}pp_Official-Record.html')
        p=b.new_page(viewport={'width':1400,'height':900},device_scale_factor=1.3)
        p.goto('file://'+f); p.wait_for_timeout(1500)
        # overflow check: any .safe whose scrollHeight > clientHeight
        ov=p.evaluate("""()=>[...document.querySelectorAll('.page')].map(pg=>{const s=pg.querySelector('.safe');return s&&(s.scrollHeight>s.clientHeight+2||s.scrollWidth>s.clientWidth+2)?pg.dataset.page:null}).filter(Boolean)""")
        print(tag,'overflow pages:',ov)
        els=p.locator('.spread .pages')
        for i in range(els.count()): els.nth(i).screenshot(path=f'qa/{tag}_s{i:02d}.png')
        p.close()
    b.close()
