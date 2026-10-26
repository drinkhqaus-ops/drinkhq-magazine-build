"""DrinkHQ Magazine Media Kit (MEDIA-001), A5, DrinkHQ house look.
python3 kit.py            -> kit.html (trim size, screen)
BLEED=3 python3 kit.py    -> kit_bleed.html (3 mm bleed, print)
"""
import base64, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
MAG = os.path.join(HERE, '..', 'mag')
WEB = os.path.join(MAG, 'web')
BLEED = float(os.environ.get('BLEED', '0'))

_c = {}
def img(name, d=None):
    p = os.path.join(d or WEB, name)
    if p not in _c:
        ext = name.rsplit('.', 1)[1].lower()
        mt = 'image/png' if ext == 'png' else 'image/jpeg'
        _c[p] = f'data:{mt};base64,' + base64.b64encode(open(p, 'rb').read()).decode()
    return _c[p]
def pg(n):
    return img(n, os.path.join(HERE, 'pg'))

def fonts():
    out = []
    spec = [('Playfair Display', 'fontsource-playfair-display-5.3.0', [(400, 'normal'), (700, 'normal'), (400, 'italic'), (700, 'italic')]),
            ('Raleway', 'fontsource-raleway-5.3.0', [(400, 'normal'), (600, 'normal'), (700, 'normal'), (800, 'normal'), (400, 'italic')]),
            ('Bebas Neue', 'fontsource-bebas-neue-5.3.0', [(400, 'normal')])]
    for fam, d, ws in spec:
        slug = d.split('-', 1)[1].rsplit('-', 1)[0]
        for w, st in ws:
            for sub in ('latin', 'latin-ext'):
                f = os.path.join(MAG, 'fonts', d, 'files', f'{slug}-{sub}-{w}-{st}.woff2')
                if os.path.exists(f):
                    data = base64.b64encode(open(f, 'rb').read()).decode()
                    rng = ';unicode-range:U+0100-024F,U+1E00-1EFF' if sub == 'latin-ext' else ''
                    out.append(f"@font-face{{font-family:'{fam}';font-style:{st};font-weight:{w};src:url(data:font/woff2;base64,{data}) format('woff2'){rng};}}")
    return '\n'.join(out)

FOOT = 'thedrinkhqexperience.com.au · 0415 090 244 · Season 2027–28'

def page(n, body, cls='', foot=True):
    f = f'<div class="foot"><span>{FOOT}</span><b>{n:02d}</b></div>' if foot else ''
    return f'<section class="page {cls}"><div class="trim">{body}{f}</div></section>'

def eyebrow(t):
    return f'<div class="eb">{t}</div>'

# ------------------------------------------------------------------ pages
P = []

# 1 · cover
P.append(page(1, f'''
<div class="cv-band">
  <div class="cv-top"><img class="cv-word" src="{img('wordmark_gold.png')}" alt="drinkhq"><span>DrinkHQ Magazine<br>Season 2027–28</span></div>
  {eyebrow('Advertising &amp; partnerships')}
  <h1 class="cv-h">Media <i>Kit.</i></h1>
  <p class="cv-lede">The magazine of Melbourne’s bar culture. Nine issues a season, each one timed to a night of the Cocktail Mastery Championship.</p>
</div>
<div class="cv-photo" style="background-image:url({img('pour3.jpg')})"><div class="cv-shade"></div>
  <img class="cv-issue" src="{pg('p1-01.jpg')}" alt="Issue 01 cover">
  <div class="cv-tag"><span>Issue 01 · on sale</span><b>Thu 17 June 2027</b></div>
</div>
<div class="cv-stats">
  <div><b>9</b><span>issues a season</span></div>
  <div><b>200</b><span>venues at launch</span></div>
  <div><b>A5</b><span>print format</span></div>
  <div><b>Free</b><span>to readers</span></div>
</div>
 <div class="cv-foot"><img src="{img('lockup_gold.png')}" alt="DrinkHQ Cocktail Mastery Championship"><span>Book your space<br><b>hello@thedrinkhqexperience.com.au</b></span></div>
''', 'cream cover', foot=False))

# 2 · the magazine
P.append(page(2, f'''
<div class="hd">{eyebrow('01 · The magazine')}<h2>More than where to go. <i>Why it matters.</i></h2></div>
<p class="lead">DrinkHQ Magazine is DrinkHQ’s editorial platform covering bars, cocktails, spirits, wine, music, product and nightlife culture. It is the publishing arm of the DrinkHQ ecosystem, alongside the Cocktail Mastery Championship, Trade Connect and the Connoisseurs Club.</p>
<p>It gives the context and conversation around drinking culture, written for readers who are actively engaged in bars, cocktails and nightlife.</p>
<div class="card gl"><b class="pf">Our mission</b><p>To inform and connect the drinks and nightlife community, through original editorial, expert perspective and coverage of DrinkHQ’s competitions, experiences and membership.</p></div>
<div class="spread-show">
  <div class="sp-lab">{eyebrow('Inside Issue 01')}</div>
  <div class="sp-row"><img src="{pg('p22-22.jpg')}" alt=""><img src="{pg('p23-23.jpg')}" alt=""></div>
  <div class="sp-cap">Spirit Explained · a two-page feature with a sponsor credit</div>
</div>
''', 'cream'))

# 3 · editorial + audience
cov = [('Bars &amp; venues', 'The venues, people and openings shaping the city’s bar scene.'),
       ('Cocktails &amp; mixology', 'Recipes, technique and the bartenders behind the drinks.'),
       ('Spirits &amp; wine', 'Category deep-dives, producers and what’s worth pouring.'),
       ('Music &amp; nightlife', 'The culture around the night, from sound to scene.'),
       ('Product news &amp; reviews', 'New releases and honest reviews.'),
       ('The DrinkHQ ecosystem', 'The Championship, the Club and Trade Connect partners.')]
cards = ''.join(f'<div class="nc"><b>{i+1:02d}</b><div><h4>{t}</h4><p>{d}</p></div></div>' for i, (t, d) in enumerate(cov))
P.append(page(3, f'''
<div class="hd">{eyebrow('02 · Editorial')}<h2>What we <i>cover.</i></h2></div>
<div class="ncgrid">{cards}</div>
<div class="hd sm">{eyebrow('Who reads it')}<h3>A focused readership of people who go out <i>for the drinks.</i></h3></div>
<div class="tiles">
  <div><b>18–39</b><span>Core age, urban</span></div>
  <div><b>Engaged</b><span>Drinks &amp; nightlife enthusiasts</span></div>
  <div><b>Free</b><span>Free publication</span></div>
</div>
<div class="photo-strip"><div style="background-image:url({img('pour2.jpg')})"></div><div style="background-image:url({img('crowd.jpg')})"></div><div style="background-image:url({img('mx_barman1.jpg')})"></div></div>
''', 'cream'))

# 4 · the season
iss = [('1', 'Cinematic Cocktails', 'Thu 17 Jun 2027', 'Thu 20 May', 'Thu 27 May'),
       ('2', 'The Science of Cocktails', 'Thu 29 Jul 2027', 'Thu 1 Jul', 'Thu 8 Jul'),
       ('3', 'The Perfect Pairing', 'Thu 9 Sep 2027', 'Thu 12 Aug', 'Thu 19 Aug'),
       ('4', 'Sweet &amp; Savoury', 'Thu 21 Oct 2027', 'Thu 23 Sep', 'Thu 30 Sep'),
       ('5', 'Smoke &amp; Spice', 'Thu 2 Dec 2027', 'Thu 4 Nov', 'Thu 11 Nov'),
       ('6', 'Around the World', 'Thu 13 Jan 2028', 'Thu 16 Dec', 'Thu 23 Dec'),
       ('7', 'The Art of Garnish', 'Thu 24 Feb 2028', 'Thu 27 Jan', 'Thu 3 Feb'),
       ('8', 'Mystery Box', 'Thu 6 Apr 2028', 'Thu 9 Mar', 'Thu 16 Mar')]
rows = ''.join(f'<tr><td class="n">{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td></tr>' for a, b, c, d, e in iss)
rows += '<tr class="gf"><td class="n">GF</td><td>Grand Final</td><td colspan="3">Date to be announced · same booking and artwork rules</td></tr>'
P.append(page(4, f'''
<div class="hd">{eyebrow('03 · The season')}<h2>Nine issues. <i>One season.</i></h2></div>
<p>One issue for every Championship event: eight round nights and the Grand Final. Each issue goes on sale on the Thursday before its Monday round night.</p>
<table class="tb sched"><thead><tr><th></th><th>Round theme</th><th>On sale</th><th>Book by</th><th>Artwork</th></tr></thead><tbody>{rows}</tbody></table>
<div class="two">
  <div class="nc"><b>28</b><div><h4>Days before on-sale · bookings close</h4><p>Book through hello@thedrinkhqexperience.com.au.</p></div></div>
  <div class="nc"><b>21</b><div><h4>Days before on-sale · artwork due</h4><p>Print-ready files to the specs on page 07.</p></div></div>
</div>
<div class="photo-strip" style="margin-top:4mm"><div style="background-image:url({img('negroni.jpg')})"></div><div style="background-image:url({img('mx_pink.jpg')})"></div><div style="background-image:url({img('daiq.jpg')})"></div></div>
''', 'cream'))

# 5 · distribution + issue 01
P.append(page(5, f'''
<div class="half-photo" style="background-image:url({img('bib_event.jpg')})"><div class="hp-shade"></div>
  <div class="hp-txt">{eyebrow('04 · Distribution')}<h2 class="onnavy">Where it <i>lands.</i></h2></div></div>
<div class="tiles t3">
  <div><b>200</b><span>Venues at launch</span></div>
  <div><b>9</b><span>Issues a season</span></div>
  <div><b>500+</b><span>Venues we’re growing to</span></div>
</div>
<p>DrinkHQ Magazine goes to a subscription list and to a curated list of 200 hospitality, lifestyle and entertainment venues at launch, growing towards 500 and more. Every Connoisseurs Club tier includes digital access to the magazine, and every issue is in the room on its Championship round night.</p>
<div class="spread-show">
  <div class="sp-row three"><img src="{pg('p8-08.jpg')}" alt=""><img src="{pg('p14-14.jpg')}" alt=""><img src="{pg('p29-29.jpg')}" alt=""></div>
  <div class="sp-cap">Issue 01 · the round preview, the Review with its side ad, and the Club page</div>
</div>
''', 'cream'))

# 6 · rates
rates = [('Full page', '$4,400', True), ('Back cover', '$4,600', False), ('Inside front cover', '$2,850', False),
         ('Inside back cover', '$2,850', False), ('Double page spread', '$6,500', False), ('Half page', '$1,900', False),
         ('Strip', '$1,500', False), ('Editorial page sponsorship', '$1,800', False), ('Display unit sponsorship', 'POA', False)]
rr = ''.join(f'<tr{" class=hl" if h else ""}><td>{a}</td><td class="r">{b}</td></tr>' for a, b, h in rates)
P.append(page(6, f'''
<div class="hd">{eyebrow('05 · Advertising')}<h2>Rates, <i>per issue.</i></h2></div>
<table class="tb rates"><thead><tr><th>Placement</th><th class="r">Rate</th></tr></thead><tbody>{rr}</tbody></table>
<p class="note">All rates are per issue and exclude GST.</p>
<div class="navy-band"><b class="pf">Founding advertisers</b><p>Book in Season 2027–28 and take <span class="gold">20% off the card</span>.</p></div>
<div class="two">
  <div class="card gl sm"><b class="pf">Additional options</b><ul><li>Inside front &amp; inside back gatefolds</li><li>Inserts and tip-ons</li><li>Advertorials</li><li>Reverse back covers</li><li>Product placements</li></ul></div>
  <div class="card gl sm"><b class="pf">Bigger than a page</b><p>Magazine placements can sit inside a wider Championship partnership through Trade Connect.</p><p class="em">Editorial coverage is never for sale.</p></div>
</div>
''', 'cream'))

# 7 · specs
P.append(page(7, f'''
<div class="hd">{eyebrow('06 · Specifications')}<h2>Artwork <i>specs.</i></h2></div>
<div class="sizes">
  <div><i class="sz dps"></i><b>Double page spread</b><span>296 × 210 mm</span></div>
  <div><i class="sz fp"></i><b>Full page</b><span>148 × 210 mm</span></div>
  <div><i class="sz hp"></i><b>Half page, vertical</b><span>70 × 210 mm</span></div>
  <div><i class="sz sv"></i><b>Strip, vertical</b><span>45 × 210 mm</span></div>
  <div><i class="sz sh"></i><b>Strip, across</b><span>148 × 55 mm</span></div>
</div>
<p class="note">Magazine format A5 (148 × 210 mm), portrait. Sizes are trim.</p>
<div class="two">
  <div class="card gl sm"><b class="pf">Files</b><ul>
    <li><b>Bleed</b> 3 mm on all sides. Ads without bleed are trimmed 2–3 mm inside the supplied size.</li>
    <li><b>Colour</b> CMYK only.</li><li><b>Images</b> 300 dpi at final print size.</li>
    <li><b>Fonts</b> converted to outlines.</li>
    <li><b>Formats</b> Photoshop TIFF or Illustrator EPS. Open layout files are not accepted.</li>
    <li><b>Proof</b> a PDF, a 72 dpi JPEG or a colour print.</li></ul></div>
  <div class="card gl sm"><b class="pf">Conditions</b><ul>
    <li>The advertiser is responsible for the accuracy of supplied artwork.</li>
    <li>Printed colour can vary between proofing systems and between issues.</li>
    <li>No cancellations after bookings close.</li>
    <li>The advertiser warrants that artwork does not breach copyright or any other law.</li></ul></div>
</div>
''', 'cream'))

# 8 · back
P.append(page(8, f'''
<div class="bk-photo" style="background-image:url({img('stir.jpg')})"><div class="hp-shade"></div>
  <div class="hp-txt">{eyebrow('07 · The DrinkHQ Experience')}<h2 class="onnavy">Part of something <i>bigger.</i></h2></div></div>
<div class="bk-cards">
  <div class="bc"><img src="{img('lockup_gold.png')}" alt="DrinkHQ Cocktail Mastery Championship"><div><h4>Cocktail Mastery <i>Championship</i></h4><p>Twelve bartending teams, eight themed Monday nights in Melbourne, one season ladder and a Grand Final. Every issue is timed to a round night.</p><span>500 guests a night · $10,000 grand prize</span></div></div>
  <div class="bc"><img class="crest" src="{img('club_crest.png')}" alt="DrinkHQ Connoisseurs Club"><div><h4>The Connoisseurs <i>Club</i></h4><p>DrinkHQ’s membership for people who love cocktails: Taste Trailblazer, Cocktail Connoisseur and Liquid Luminary. Every tier includes digital access to DrinkHQ Magazine.</p></div></div>
</div>
<div class="contacts">
  <div><span>Advertising</span><b>hello@thedrinkhqexperience.com.au</b></div>
  <div><span>Partnerships</span><b>partner@thedrinkhqexperience.com.au</b></div>
  <div><span>Phone</span><b>0415 090 244</b></div>
  <div><span>Online</span><b>drinkhqmedia.com</b></div>
  <div class="w"><span>Post</span><b>DrinkHQ, PO Box 5112, Hughesdale VIC 3166</b></div>
</div>
<div class="bk-end"><img src="{img('lockup_gold.png')}" alt=""><p>DrinkHQ Magazine is published by Business Intelligence International Pty Ltd trading as The DrinkHQ Experience. Rates and dates may change; confirm at booking.<br>MEDIA-001 · October 2026</p></div>
''', 'navy'))

B = BLEED
CSS = f'''
{fonts()}
@page{{size:{148+2*B}mm {210+2*B}mm;margin:0}}
:root{{--royal:#002060;--navy:#0B2049;--gold:#FFC000;--gold2:#D9A20C;--cream:#F6F1E8;--card:#FFFDF8;--ink:#1D1D24;--muted:#5A6680}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:#888}}
body{{-webkit-print-color-adjust:exact;print-color-adjust:exact;font:400 8pt/1.45 'Raleway',sans-serif;color:var(--ink)}}
.page{{width:{148+2*B}mm;height:{210+2*B}mm;position:relative;overflow:hidden;break-after:page;background:var(--cream)}}
.page.navy,.page.cover{{background:var(--royal)}}
.trim{{position:absolute;left:{B}mm;top:{B}mm;width:148mm;height:210mm;padding:11mm 11mm 14mm}}
.eb{{font:800 6.6pt/1 'Raleway';letter-spacing:.24em;text-transform:uppercase;color:var(--gold2);margin-bottom:2.2mm}}
.navy .eb,.onnavy+.eb,.hp-txt .eb,.cv-band .eb{{color:var(--gold)}}
h2{{font:700 21pt/1.05 'Playfair Display';color:var(--royal);letter-spacing:-.005em}}
h2 i,h3 i,h4 i,.cv-h i{{font-style:italic;color:var(--gold2);font-weight:700}}
h2.onnavy{{color:#fff}} h2.onnavy i{{color:var(--gold)}}
h3{{font:700 12pt/1.2 'Playfair Display';color:var(--royal)}}
.hd{{margin-bottom:4mm}} .hd.sm{{margin:5mm 0 3mm}}
p{{margin-bottom:2.4mm}} .lead{{font-size:9pt;color:var(--royal);font-weight:600}}
.note{{font-size:7.5pt;color:var(--muted);margin-top:1.5mm}}
.pf{{font:700 9.5pt 'Playfair Display';color:var(--royal);display:block;margin-bottom:1.2mm}}
.gold{{color:var(--gold)}}
.card{{background:var(--card);padding:3.2mm 3.6mm;border-left:1.2mm solid var(--gold);margin:3mm 0}}
.card.sm{{margin:0}} .card p:last-child{{margin-bottom:0}}
.card ul{{list-style:none}} .card li{{position:relative;padding-left:3mm;margin-bottom:1.1mm;font-size:7.5pt}}
.card li::before{{content:'';position:absolute;left:0;top:1.35mm;width:1.2mm;height:1.2mm;background:var(--gold);border-radius:50%}}
.card li b{{color:var(--royal)}} .em{{font-style:italic;color:var(--royal)}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:3mm;margin-top:3.5mm}}
.foot{{position:absolute;left:11mm;right:11mm;bottom:6mm;display:flex;justify-content:space-between;align-items:center;border-top:.25mm solid rgba(0,32,96,.18);padding-top:2mm}}
.foot span{{font:700 6.2pt 'Raleway';letter-spacing:.14em;text-transform:uppercase;color:var(--gold2)}}
.foot b{{font:700 11pt 'Playfair Display';color:var(--gold2)}}
.navy .foot{{border-top-color:rgba(255,255,255,.18)}} .navy .foot span,.navy .foot b{{color:var(--gold)}}
/* numbered navy cards */
.ncgrid{{display:grid;grid-template-columns:1fr 1fr;gap:2.4mm}}
.nc{{background:var(--navy);color:#fff;display:flex;gap:3mm;padding:3mm 3.4mm;align-items:flex-start}}
.nc>b{{font:700 17pt/1 'Playfair Display';color:var(--gold);flex:none;min-width:8mm}}
.nc h4{{font:700 9pt/1.2 'Playfair Display';color:#fff;margin-bottom:.8mm}}
.nc p{{font-size:7.5pt;color:#D5DAE8;margin:0;line-height:1.35}}
.tiles{{display:grid;grid-template-columns:repeat(3,1fr);gap:2.4mm;margin:2mm 0 3.5mm}}
.tiles div{{background:var(--navy);padding:3.2mm 2mm;text-align:center;border-top:1mm solid var(--gold)}}
.tiles b{{display:block;font:700 15pt/1 'Playfair Display';color:var(--gold)}}
.tiles span{{display:block;margin-top:1.2mm;font:700 6.4pt/1.25 'Raleway';letter-spacing:.12em;text-transform:uppercase;color:#fff}}
.photo-strip{{display:grid;grid-template-columns:repeat(3,1fr);gap:2mm;height:30mm}}
.photo-strip div{{background:center/cover no-repeat}}
/* tables */
.tb{{width:100%;border-collapse:collapse;margin:2mm 0}}
.tb th{{background:var(--royal);color:var(--gold);font:800 6.4pt 'Raleway';letter-spacing:.16em;text-transform:uppercase;text-align:left;padding:2mm 2.2mm}}
.tb td{{padding:1.75mm 2.2mm;border-bottom:.25mm solid #E3D9C4;font-size:7.6pt;background:var(--card)}}
.tb .r{{text-align:right}} .tb td.r{{font:700 10pt 'Playfair Display';color:var(--royal)}}
.tb td.n{{font:700 10pt 'Playfair Display';color:var(--gold2);width:7mm}}
.sched td:nth-child(2){{font-weight:700;color:var(--royal)}}
.sched tr.gf td{{background:#EFE6D2}}
.rates td{{font:600 8.4pt 'Raleway';color:var(--royal);padding:2.1mm 3mm}}
.rates tr.hl td{{background:var(--navy);color:#fff}} .rates tr.hl td.r{{color:var(--gold)}}
.navy-band{{background:var(--royal);color:#fff;padding:3mm 4mm;margin:3mm 0 0;display:flex;gap:4mm;align-items:center;border-left:1.2mm solid var(--gold)}}
.navy-band .pf{{color:var(--gold);margin:0;flex:none}} .navy-band p{{margin:0;font-size:8pt}}
.navy-band .gold{{font-weight:800}}
/* issue pages show */
.spread-show{{margin-top:3mm}}
.sp-row{{display:flex;gap:0;justify-content:center;box-shadow:0 1.2mm 3mm rgba(0,0,0,.18)}}
.sp-row img{{width:50%;display:block}}
.sp-row.three{{gap:3mm;box-shadow:none}} .sp-row.three img{{width:31%;box-shadow:0 1mm 2.5mm rgba(0,0,0,.2)}}
.sp-cap{{font:italic 400 7.5pt 'Raleway';color:var(--muted);margin-top:2mm;text-align:center}}
/* cover */
.cover .trim{{padding:0}}
.cv-band{{background:var(--royal);padding:9mm 11mm 6mm;position:relative}}
.cv-top{{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:9mm}}
.cv-word{{width:26mm}} .cv-top span{{font:800 6.4pt/1.5 'Raleway';letter-spacing:.2em;text-transform:uppercase;color:var(--gold);text-align:right}}
.cv-h{{font:700 40pt/.95 'Playfair Display';color:#fff;margin:1mm 0 3mm}}
.cv-h i{{color:var(--gold)}}
.cv-lede{{color:#D5DAE8;font-size:8.6pt;max-width:76mm;margin:0}}
.cv-photo{{height:84mm;background:center 40%/cover no-repeat;position:relative}}
.cv-shade{{position:absolute;inset:0;background:linear-gradient(90deg,rgba(0,32,96,.55),rgba(0,32,96,0) 60%)}}
.cv-issue{{position:absolute;right:11mm;top:-30mm;width:44mm;box-shadow:0 2mm 5mm rgba(0,0,0,.45);border:.6mm solid #fff}}
.cv-tag{{position:absolute;left:11mm;bottom:7mm;background:var(--gold);padding:2mm 3mm}}
.cv-tag span{{display:block;font:800 6.2pt 'Raleway';letter-spacing:.16em;text-transform:uppercase;color:var(--royal)}}
.cv-tag b{{font:700 10pt 'Playfair Display';color:var(--royal)}}
.cv-stats{{display:grid;grid-template-columns:repeat(4,1fr);background:var(--navy)}}
.cv-stats div{{padding:4mm 1mm;text-align:center;border-right:.25mm solid rgba(255,255,255,.12)}}
.cv-stats div:last-child{{border:0}}
.cv-stats b{{display:block;font:700 15pt/1 'Playfair Display';color:var(--gold)}}
.cv-stats span{{display:block;margin-top:1.2mm;font:700 6.2pt 'Raleway';letter-spacing:.12em;text-transform:uppercase;color:#fff}}
.cv-foot{{display:flex;justify-content:space-between;align-items:center;padding:5mm 11mm;background:var(--royal);border-top:.6mm solid var(--gold);position:absolute;left:0;right:0;bottom:0;height:31mm}}
.cv-foot img{{width:34mm}}
.cv-foot span{{text-align:right;font:800 6.4pt/1.6 'Raleway';letter-spacing:.18em;text-transform:uppercase;color:var(--gold)}}
.cv-foot span b{{display:block;font:600 8pt 'Raleway';letter-spacing:0;text-transform:none;color:#fff}}
/* photo heads */
.half-photo,.bk-photo{{margin:-11mm -11mm 4mm;height:58mm;background:center/cover no-repeat;position:relative}}
.bk-photo{{height:52mm}}
.hp-shade{{position:absolute;inset:0;background:linear-gradient(0deg,rgba(0,32,96,.92),rgba(0,32,96,.25) 70%)}}
.hp-txt{{position:absolute;left:11mm;right:11mm;bottom:5mm}}
/* sizes */
.sizes{{display:grid;grid-template-columns:1.7fr 1fr 1fr 1fr 1fr;gap:2mm;align-items:end;background:var(--card);padding:4mm 3mm 3mm;border-top:1mm solid var(--gold)}}
.sizes div{{text-align:center}}
.sizes b{{display:block;font:700 7.5pt/1.15 'Raleway';color:var(--royal);margin-top:2mm;min-height:6mm}}
.sizes span{{font:700 8pt 'Playfair Display';color:var(--gold2)}}
.sz{{display:block;margin:0 auto;height:25.5mm;background:var(--royal);position:relative}}
.sz.dps{{width:36mm;height:25.5mm;background:linear-gradient(90deg,var(--royal) 49.6%,var(--gold) 49.6% 50.4%,var(--royal) 50.4%)}}
.sz.fp{{width:18mm}}
.sz.hp,.sz.sv,.sz.sh{{width:18mm;background:#E6DCC6}}
.sz.hp::after,.sz.sv::after,.sz.sh::after{{content:'';position:absolute;background:var(--royal)}}
.sz.hp::after{{right:0;top:0;bottom:0;width:47.3%}}
.sz.sv::after{{right:0;top:0;bottom:0;width:30.4%}}
.sz.sh::after{{left:0;right:0;bottom:0;height:26.2%}}
/* back */
.navy .trim{{color:#fff}}
.bk-cards{{display:grid;gap:2.6mm}}
.bc{{display:flex;gap:3.5mm;background:rgba(255,255,255,.06);border-left:1.2mm solid var(--gold);padding:3mm 3.5mm;align-items:center}}
.bc>img{{width:26mm;flex:none}} .bc>img.crest{{width:24mm;margin:0 1mm}}
.clubchip{{width:24mm;flex:none;background:#fff;padding:1.6mm;border-radius:1mm}} .clubchip img{{width:100%;display:block}}
.bc h4{{font:700 10pt 'Playfair Display';color:#fff;margin-bottom:.8mm}} .bc h4 i{{color:var(--gold)}}
.bc p{{font-size:7.5pt;color:#D5DAE8;margin:0 0 1mm;line-height:1.35}}
.bc span{{font:800 6.2pt 'Raleway';letter-spacing:.16em;text-transform:uppercase;color:var(--gold)}}
.contacts{{display:grid;grid-template-columns:1fr 1fr;gap:1.6mm 4mm;margin:4mm 0 0;padding:3mm 0;border-top:.25mm solid rgba(255,255,255,.2);border-bottom:.25mm solid rgba(255,255,255,.2)}}
.contacts .w{{grid-column:1/-1}}
.contacts span{{display:block;font:800 6.2pt 'Raleway';letter-spacing:.18em;text-transform:uppercase;color:var(--gold)}}
.contacts b{{font:600 8pt 'Raleway';color:#fff}}
.bk-end{{display:flex;gap:4mm;align-items:center;margin-top:4mm}}
.bk-end img{{width:30mm;flex:none}}
.bk-end p{{font-size:7.5pt;color:#AEB7CF;margin:0;line-height:1.4}}
@media screen{{.page{{margin:6mm auto;box-shadow:0 2px 10px rgba(0,0,0,.3)}}}}
'''
if B:
    CSS += f'''
.cv-band{{margin:-{B}mm -{B}mm 0;padding:{9+B}mm {11+B}mm 6mm}}
.cv-photo,.cv-stats{{margin:0 -{B}mm}} .cv-foot{{left:-{B}mm;right:-{B}mm;bottom:-{B}mm;height:calc(31mm + {B}mm);padding:5mm {11+B}mm calc(5mm + {B}mm)}}
.cv-tag{{left:{11+B}mm}} .cv-issue{{right:{11+B}mm}}
.half-photo,.bk-photo{{margin:-{11+B}mm -{11+B}mm 4mm;height:calc(58mm + {B}mm)}}
.bk-photo{{height:calc(52mm + {B}mm)}}
.hp-txt{{left:{11+B}mm;right:{11+B}mm}}
'''

html = f'<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><title>DrinkHQ Magazine Media Kit · Season 2027–28</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>'
out = os.path.join(HERE, 'kit_bleed.html' if B else 'kit.html')
open(out, 'w').write(html)
print(out, len(html) // 1024, 'KB')
