#!/usr/bin/env python3
"""DrinkHQ Magazine / Official Record — Issue 01 generator (16pp and 32pp).
A5 trim (148x210mm) + 3mm bleed, Record ad sizes as labelled placeholders."""
import base64, os, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.environ.get('DHQ_IMGDIR') or os.path.join(HERE, 'web')

def b64(name):
    p = os.path.join(WEB, name)
    mt = 'image/png' if name.endswith('.png') else 'image/jpeg'
    return f"data:{mt};base64," + base64.b64encode(open(p, 'rb').read()).decode()

IMG = {}
def img(k):
    if k not in IMG:
        n = k if '.' in k else k + '.jpg'
        IMG[k] = b64(n)
    return IMG[k]

def font_faces():
    out = []
    spec = [('Playfair Display', 'fontsource-playfair-display-5.3.0', [(400, 'normal'), (700, 'normal'), (400, 'italic'), (700, 'italic'), (900, 'normal')]),
            ('Raleway', 'fontsource-raleway-5.3.0', [(300, 'normal'), (400, 'normal'), (600, 'normal'), (700, 'normal'), (800, 'normal'), (400, 'italic')]),
            ('Bebas Neue', 'fontsource-bebas-neue-5.3.0', [(400, 'normal')])]
    for fam, d, ws in spec:
        slug = d.split('-', 1)[1].rsplit('-', 1)[0]
        for w, st in ws:
            f = os.path.join(HERE, os.environ.get('DHQ_FONTDIR','fonts'), d, 'files', f'{slug}-latin-{w}-{st}.woff2')
            if not os.path.exists(f):
                print('missing font', f, file=sys.stderr); continue
            data = base64.b64encode(open(f, 'rb').read()).decode()
            out.append(f"@font-face{{font-family:'{fam}';font-style:{st};font-weight:{w};src:url(data:font/woff2;base64,{data}) format('woff2');}}")
            fx = f.replace('-latin-', '-latin-ext-')
            if os.environ.get('DHQ_LATINEXT') and os.path.exists(fx):
                dx = base64.b64encode(open(fx, 'rb').read()).decode()
                out.append(f"@font-face{{font-family:'{fam}';font-style:{st};font-weight:{w};src:url(data:font/woff2;base64,{dx}) format('woff2');unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF;}}")
    return '\n'.join(out)

# ---------------------------------------------------------------- facts
ISSUE = 'DHQM01'
CONTACT = 'hello@thedrinkhqexperience.com.au'
PARTNER = 'partner@thedrinkhqexperience.com.au'
REGISTER = 'register@thedrinkhqexperience.com.au'
WEBSITE = 'thedrinkhqexperience.com.au'
ROUNDS = [
    ('01', 'Mon 21 June 2027', 'Cinematic Cocktails', 'Iconic films, captured in a glass.'),
    ('02', 'Mon 2 August 2027', 'The Science of Cocktails', 'Technique, texture and a little chemistry.'),
    ('03', 'Mon 13 September 2027', 'The Perfect Pairing', 'Drinks built to sit beside food.'),
    ('04', 'Mon 25 October 2027', 'Sweet & Savoury', 'Balancing the two ends of the palate.'),
    ('05', 'Mon 6 December 2027', 'Smoke & Spice', 'Heat, char and aromatic depth.'),
    ('06', 'Mon 17 January 2028', 'Around the World', 'Classic serves from every continent, reimagined.'),
    ('07', 'Mon 28 February 2028', 'The Art of Garnish', 'The finishing touch becomes the story.'),
    ('08', 'Mon 10 April 2028', 'Mystery Box', 'Unseen ingredients, no second chances.'),
]
TASTE = [('T', 'Taste', 30, 'The foundation of any great cocktail.'),
         ('A', 'Appearance', 20, 'Because we drink with our eyes first.'),
         ('S', 'Skill', 15, 'The technical craft behind the glass.'),
         ('T', 'Theme Adherence', 10, 'Creativity within the round’s brief.'),
         ('E', 'Engagement', 25, 'The performance, the story, the room.')]

# ---------------------------------------------------------------- helpers
def ph(t='PLACEHOLDER'):
    return f'<span class="ph" contenteditable="false">{t}</span>'

def folio(n, strip=False):
    cls = 'folio strip' if strip else 'folio'
    return f'<div class="{cls}">// {ISSUE}_ [AU-Melb] // Page {n:02d} //</div>'

def frame():
    return '<div class="gframe"></div>'

def head(word, kicker='', light=False):
    k = f'<div class="kicker">{kicker}</div>' if kicker else ''
    c = ' light' if light else ''
    return f'{k}<h1 class="sec{c}">{word}<span class="gt">&gt;</span></h1>'

USED=set()
RESERVED={'orange','daiq','mojito','cover','cover_issue01'}
POOL=['negroni','pinkmart','pour2','stir','pour3','martini','ice','lemonmart','tie','limes','mint','mintglass','laugh','team2','team3','team4','bw','bottles','barrels','edv','b1806','barA','barB','barC','cane','crowd']
def pick(k, fixed=False):
    if fixed or k in RESERVED or k not in USED:
        USED.add(k); return k
    for c in POOL:
        if c not in USED and c not in RESERVED:
            USED.add(c); return c
    return k
def photo(k, cls='', style='', tag='', fixed=False):
    k = pick(k, fixed)
    t = f'<span class="ph imgtag" contenteditable="false">{tag}</span>' if tag else ''
    return f'<div class="ph-wrap {cls}" style="{style}"><img class="pic" src="{img(k)}" alt="">{t}</div>'

AD_SPECS = {
    'full':  ('FULL PAGE', '148 × 210 mm trim', 'Supply 154 × 216 mm (3 mm bleed all sides)'),
    'dps':   ('DOUBLE PAGE SPREAD', '296 × 210 mm trim', 'Supply 302 × 216 mm (3 mm bleed)'),
    'half':  ('HALF PAGE · VERTICAL', '70 × 210 mm', 'Supply 73 × 216 mm (bleed on outer edge, top, bottom)'),
    'third': ('THIRD PAGE · VERTICAL', '49 × 210 mm', 'Supply 52 × 216 mm (bleed on outer edge, top, bottom)'),
    'vstrip': ('STRIP · VERTICAL', '45 × 210 mm', 'Supply 48 × 216 mm (bleed on outer edge, top, bottom)'),
    'hstrip': ('STRIP · HORIZONTAL', '148 × 55 mm', 'Supply 154 × 58 mm (bleed on sides and bottom)'),
    'hstrips': ('SMALL STRIP · HORIZONTAL', '148 × 30 mm', 'Supply 154 × 33 mm (bleed on sides and bottom)'),
    'hthird': ('THIRD PAGE · HORIZONTAL', '148 × 70 mm', 'Supply 154 × 73 mm (bleed on sides and bottom)'),
    'hquarter': ('QUARTER PAGE · HORIZONTAL', '148 × 52.5 mm', 'Supply 154 × 55.5 mm (bleed on sides and bottom)'),
}

def ad(kind, slot, note='', recto=True, art=None, fit='cover', pos='50% 50%', bg='#111'):
    name, size, supply = AD_SPECS[kind]
    side = 'r' if recto else 'l'
    n = f'<div class="ad-note">{note}</div>' if note else ''
    if art and art is not True:
        a = f'<img class="adart" alt="" src="{img(art)}" style="object-fit:{fit};object-position:{pos};background:{bg}">'
        badge = f'<div class="sample-tag" contenteditable="false">SAMPLE AD · ARCHIVE · {slot} · {name}</div>'
        hc = ' has-art'
    else:
        a = '<img class="adart" alt="" hidden>'; badge = ''; hc = ''
    return f'''<div class="ad ad-{kind} ad-{side}{hc}" data-slot="{slot}" title="Edit mode: click to drop in finished artwork">
{a}{badge}
<div class="ad-inner" contenteditable="false"><div class="ad-tag">ADVERTISEMENT · {slot}</div>
<div class="ad-name">{name}</div><div class="ad-size">{size}</div><div class="ad-supply">{supply}</div>{n}
<div class="ad-book">Bookings · {PARTNER}</div></div></div>'''

# ---------------------------------------------------------------- pages
def cover(n):
    return f'''<div class="bleedimg">{photo('cover','fill','object-position:58% 40%')}</div>
<div class="cv-shade"></div>
<div class="cv-frame"><span class="cv-top">2027 OFFICIAL RECORD // {ISSUE} // AU-MELB</span></div>
<img class="cv-logo" src="{img('lockup_white.png')}" alt="DrinkHQ Cocktail Mastery Championship">
<div class="cv-date">JUNE 2027 / VOL.01 / RD1</div>
<div class="cv-lines">
<div><b>Round 1 · Cinematic Cocktails</b><span>Monday 21 June 2027 · 7:00 PM</span></div>
<div><b>Meet the Founding 12</b><span>Twelve teams. Eight rounds. One title.</span></div>
<div><b>TASTE, explained</b><span>How every cocktail is scored</span></div>
</div>
<div class="cv-free">FREE · DrinkHQ Magazine</div>'''


def cover_issue(n, r1page, items):
    """Issue 01 'Cinematic Cocktails' cover, rebuilt live: full-resolution photo (IMG_4506) with real type."""
    rows = ''.join(f'<div class="ci-item"><span>P.{p:02d} · {lab}</span>{txt}</div>' for p, lab, txt in items)
    return f'''<div class="cl-photo"><img class="pic" src="{img('cover_martini')}" alt="Cocktail with orange-peel spiral"></div>
<div class="cl-top-fade"></div><div class="cl-bot-fade"></div>
<div class="cl-kick">THE OFFICIAL MAGAZINE OF THE COCKTAIL MASTERY CHAMPIONSHIP</div>
<div class="cl-code">{ISSUE} // AU-MELB</div>
<img class="cl-word" src="{img('wordmark_gold.png')}" alt="drinkhq">
<div class="cl-mag">MAGAZINE</div>
<div class="cl-issue"><b>01</b><span>ISSUE · JUNE 2027</span><i>FREE · TAKE ONE</i></div>
<img class="cl-lockup" src="{img('lockup_gold.png')}" alt="DrinkHQ Cocktail Mastery Championship">
<div class="ci-r1">ROUND 1 PREVIEW · P.{r1page:02d}</div>
<div class="cl-head">Cinematic<br><i>Cocktails.</i></div>
<div class="cl-stand">The brief, the stage and the serves that open the Cocktail Mastery Championship.</div>
<div class="cl-band">JUNE 2027 / ISSUE 01 / RD1</div>
<div class="ci-panel"><div class="ci-head">INSIDE&gt;</div>{rows}</div>'''

def contents(n, items):
    rows = ''.join(f'<div class="ct-row"><span class="ct-n">{p:02d}</span><div><b>{t}</b><span>{d}</span></div></div>' for p, t, d in items)
    return f'''{frame()}<div class="safe">{head('Contents', 'Issue 01 · June 2027')}
<div class="ct-grid">{rows}</div>
<div class="ct-photo">{photo('martini','fill','object-position:50% 30%')}</div>
</div>{folio(n)}'''

def welcome(n, with_contents=None, masthead=False):
    ct = ''
    if with_contents:
        ct = '<div class="mini-ct"><div class="label">Inside this issue</div>' + ''.join(
            f'<div><span>{p:02d}</span>{t}</div>' for p, t in with_contents) + '</div>'
    mh = ''
    if masthead:
        mh = f'''<div class="masthead"><div class="label">DrinkHQ Magazine</div>
<p><b>Publisher</b> Mark Buckley · mark@thedrinkhqexperience.com.au</p>
<p><b>Advertising</b> {PARTNER}</p>
<p class="small">Published by Business Intelligence International Pty Ltd, trading as The DrinkHQ Experience · PO Box 5112, Hughesdale VIC 3166 · {CONTACT} · {WEBSITE}</p>
<p class="small">DrinkHQ Magazine is a free publication distributed through selected venues. Views expressed are not necessarily those of the publisher. No responsibility is accepted for the accuracy of advertisements. Material sent to the magazine is assumed to be for publication unless marked “Not for publication”. No reproduction in whole or in part without permission. DrinkHQ supports the responsible service and consumption of alcohol. © DrinkHQ 2027. Please do not litter.</p></div>'''
    return f'''{frame()}<div class="safe">
<div class="hrow"><h1 class="big">Welcome<span class="gt">.</span></h1><img class="hlogo" src="{img('lockup_blue.png')}" alt=""></div>
<div class="cols2 body">
<p class="lede">Welcome to Issue 01 of DrinkHQ Magazine, the Official Record of the inaugural DrinkHQ Cocktail Mastery Championship. Season 2027–28 is where it all starts: twelve of Melbourne’s best bar teams, eight themed rounds and one Grand Final.</p>
<p>Across the season our teams will push the limits of flavour, presentation and technique, from reimagined classics to drinks no one has tasted before. Every round is scored on TASTE, our five-part judging system, and every point counts towards the Championship ladder.</p>
<p>The top six teams on the ladder after Round 8 go through to the Grand Final to compete for the title of DrinkHQ Cocktail Mastery Champions. Each issue of this magazine lands four days before its round, with the fixture, the theme, the standings and the stories from behind the bar.</p>
<p>Pull up a stool, grab a drink and enjoy the show.</p>
<p class="sign"><i>Mark Buckley</i><br><span>Founder &amp; Competition Director</span></p>
</div>{ct}{mh}
{'' if masthead else photo('mint','flexpic','object-position:50% 40%')}
</div>{folio(n)}'''

def art_of_mastery(n, team=True):
    exp = [('Themed rounds', 'Eight rounds, each with its own brief, from cinema to the Mystery Box.'),
           ('Team &amp; individual matches', 'Head-to-head challenges that test the whole bar team.'),
           ('Racing the clock', 'Seven minutes to create and present three identical cocktails.'),
           ('Tastings', 'Sample signature serves and meet the bartenders who made them.'),
           ('Up to 500 guests a round', 'A live crowd, a big room and a proper atmosphere.')]
    e = ''.join(f'<li><b>{a}</b> {b}</li>' for a, b in exp)
    tm = f'''<div class="teambox"><div class="label">Event Team&gt;</div>
<div><span>Founder &amp; Competition Director</span><b>Mark Buckley</b><i>mark@thedrinkhqexperience.com.au</i></div>
<div><span>Event Manager</span><b>Ezzie Magrin</b><i>{CONTACT}</i></div>
<div><span>Partnerships</span><b>Commercial team</b><i>{PARTNER}</i></div>
<div><span>Team registration</span><b>Registrations</b><i>{REGISTER}</i></div></div>''' if team else ''
    return f'''{frame()}<div class="safe">
<div class="hrow"><h1 class="big">The Art of <i>Cocktail Mastery</i></h1><img class="hlogo" src="{img('lockup_blue.png')}" alt=""></div>
<div class="kicker2">THE BATTLE FOR COCKTAIL SUPREMACY BEGINS…</div>
<p class="body">The DrinkHQ Cocktail Mastery Championship is a league-style season that celebrates the art of mixology and the bartenders who practise it. It challenges seasoned professionals and rising talent alike to show their creativity, technical skill and passion for the craft — and it is built like a sport.</p>
<div class="label mt">What to expect</div><ul class="expect">{e}</ul>
{tm}
<div class="strip3">{photo('ice')}{photo('negroni')}{photo('pinkmart')}</div>
</div>{folio(n)}'''

def taste_page(n, strip=False, club=False):
    t = ''.join(f'<div class="taste"><div class="tl">{l}</div><div class="tw">{w}<small>%</small></div><b>{nm}</b><span>{d}</span></div>' for l, nm, w, d in TASTE)
    s = ad('hstrip', f'AD-{n:02d}-S', 'Bottom strip, as Record p8', n % 2 == 1) if strip else ''
    return f'''{frame()}<div class="safe {'withstrip' if strip else ''}">
<div class="kicker">How it works</div>
<h1 class="big">Match <i>Overview</i></h1>
<p class="body">A single round is a high-stakes test of a team’s creativity, skill and efficiency. Each round brings a new theme, designed to push teams to their limits and show their mastery of the craft.</p>
<div class="steps"><div><span class="num">01</span><b>Preparation · 2 minutes</b><p>Teams set up their station and check every ingredient and tool is ready.</p></div>
<div><span class="num">02</span><b>Creation &amp; presentation · 7 minutes</b><p>Three identical cocktails, true to the round’s theme, presented to the judges with the story behind them.</p></div></div>
<div class="label mt">Judging · the TASTE system</div>
<div class="tastes">{t}</div>
<p class="note">Teams of up to four bartenders. Five scoring judges per round. Weights shown are the published TASTE weights for Season 2027–28.</p>
{CLUBBOX.replace('CLUBIMG', img('club_crest.png')) if club else ('' if strip else photo('pour2','flexpic'))}</div>{s}{folio(n, strip)}'''

CLUBBOX = '''<div class="tp-club"><div class="tp-club-l"><img src="CLUBIMG" alt=""><div class="big2">Connoisseurs <i>Club</i></div>
<p>Membership for people who love great drinks: admission to all eight Championship rounds, a complimentary cocktail at every event, member pricing on merchandise and more.</p>
<div class="tp-join">connoisseursclub.com.au</div></div>
<div class="tiers"><div><b>Taste Trailblazer</b><span>$239 / year</span></div><div><b>Cocktail Connoisseur</b><span>$359 / year</span></div><div><b>Liquid Luminary</b><span>$549 / year</span></div>
<p class="small">Prices include GST. Benefits vary by tier and are subject to the current Membership Terms.</p></div></div>'''

def ladder(n, strip=False):
    rows = ''.join(f'<tr class="{"q" if i < 6 else ""}"><td>{i+1}</td><td>Team {i+1:02d} · [Team name / venue]</td><td>–</td><td>–</td><td>–</td><td>–</td><td>–</td></tr>' for i in range(12))
    s = ad('hstrip', f'AD-{n:02d}-S', '', n % 2 == 1) if strip else ''
    return f'''{frame()}<div class="safe {'withstrip' if strip else ''}">
<div class="kicker">Season 2027–28</div>
<h1 class="big">Championship <i>Ladder</i></h1>
<div class="flow"><div><b>Round-by-round</b><span>Teams face off across eight themed rounds. Points from every round count towards the ladder.</span></div>
<div class="arrow">→</div><div><b>Grand Final</b><span>The top six teams after Round 8 qualify for the Grand Final. Date to be announced.</span></div>
<div class="arrow">→</div><div class="dark"><b>Champions</b><span>DrinkHQ Cocktail Mastery Champions 2027–28</span></div></div>
<table class="ladder"><thead><tr><th>#</th><th>Team</th><th>MP</th><th>W</th><th>L</th><th>PF</th><th>Pts</th></tr></thead><tbody>{rows}</tbody></table>
<p class="note">The ladder opens after Round 1. Gold rows mark the Grand Final places. Team names are published once the Founding 12 are confirmed. {ph()}</p>
</div>{s}{folio(n, strip)}'''

def round1(n, strip=False):
    fx = ''.join(f'<div class="fx {"alt" if i % 2 == 0 else ""}"><span>Team {2*i+1:02d} · [Name]</span><em>vs</em><span>Team {2*i+2:02d} · [Name]</span></div>' for i in range(6))
    s = ad('hstrip', f'AD-{n:02d}-S', 'Bottom strip, as Record p8', n % 2 == 1) if strip else ''
    return f'''{frame()}<div class="safe {'withstrip' if strip else ''}">
<div class="r1-head"><div><div class="kicker">Round 1</div><h1 class="big">Cinematic <i>Cocktails</i></h1></div>
<div class="r1-date"><b>MONDAY 21 JUNE 2027</b><span>7:00 PM · Venue to be announced</span></div></div>
<div class="r1-body">{photo('tie','r1-pic')}
<p class="body">Round 1 brings the magic of cinema to life. Teams create cocktails inspired by iconic films — capturing a scene, a character or a moment in every sip. From classic Hollywood glamour to futuristic sci-fi, each drink tells a story, blending artistry with mixology.</p></div>
<div class="label mt">Match fixture {ph('RELEASED AFTER TEAM SELECTION')}</div>
<div class="fixture">{fx}</div>
<div class="theme-box"><b>THEME OVERVIEW</b><p>Lights, camera, shake. Teams are judged on how clearly the drink tells its film’s story — in the glass, the garnish and the presentation.</p></div>
<p class="note">General Admission from $15 (advance). Ticket sales open soon at {WEBSITE}. Round themes subject to change.</p>
{'' if strip else photo('lemonmart','flexpic')}</div>{s}{folio(n, strip)}'''

def calendar(n):
    rows = ''.join(f'<div class="cal"><span class="num">{r}</span><div><b>{t}</b><i>{d}</i><span>{s}</span></div></div>' for r, d, t, s in ROUNDS)
    return f'''{frame()}<div class="safe">
<div class="kicker">Season 2027–28</div>
<h1 class="big">The <i>Season</i></h1>
<p class="body">Eight rounds, six weeks apart, every one on a Monday night. Each issue of DrinkHQ Magazine lands four days before its round.</p>
<div class="cal-grid">{rows}</div>
{photo('negroni','flexpic')}<div class="gf"><span class="num">GF</span><div><b>Grand Final</b><span>Top six teams · Date to be announced</span></div></div>
</div>{folio(n)}'''

def founding12(n, first, side_note=True):
    cards = ''.join(f'<div class="tcard"><div class="tc-img">{ph("TEAM PHOTO")}</div><b>Team {i:02d}</b><span>[Team name]</span><i>[Home venue] · [Suburb]</i></div>' for i in range(first, first + 6))
    hdr = head('Teams', 'Meet the Founding 12') if first == 1 else '<div class="kicker">Meet the Founding 12 · continued</div>'
    txt = '<p class="body">Twelve bar teams, selected for their craft and creativity, team chemistry, professionalism and championship potential. Each team fields up to four bartenders. Team profiles appear here once selection is complete.</p>' if first == 1 else '<p class="body">Every team plays every round. Points from every round build the ladder — and only six teams make the Grand Final.</p>'
    return f'''{frame()}<div class="safe">{hdr}{txt}<div class="tgrid">{cards}</div></div>{folio(n)}'''

def founding12_single(n):
    cards = ''.join(f'<div class="tcard sm"><div class="tc-img">{ph("PHOTO")}</div><b>Team {i:02d}</b><span>[Team name]</span><i>[Venue]</i></div>' for i in range(1, 13))
    return f'''{frame()}<div class="safe">{head('Teams', 'Meet the Founding 12')}
<p class="body">Twelve bar teams, selected for their craft and creativity, team chemistry, professionalism and championship potential. Each team fields up to four bartenders. Full profiles follow once selection is complete. {ph()}</p>
<div class="tgrid g12">{cards}</div>
<div class="calmini">{''.join(f'<div><b>R{r}</b><span>{d.split(" ",1)[1]}</span><i>{t}</i></div>' for r,d,t,s in ROUNDS)}<div><b>GF</b><span>Date TBA</span><i>Grand Final</i></div></div>
</div>{folio(n)}'''

def teams_club(n):
    cards = ''.join(f'<div class="tcard sm"><div class="tc-img">{ph("PHOTO")}</div><b>Team {i:02d}</b><span>[Team name]</span><i>[Venue]</i></div>' for i in range(1, 13))
    return f'''{frame()}<div class="safe tcl">{head('Teams', 'Meet the Founding 12')}
<p class="body">Twelve bar teams, selected for their craft, creativity and championship potential. Each fields up to four bartenders. Full profiles follow once selection is complete. {ph()}</p>
<div class="tgrid g12">{cards}</div>
<div class="calmini">{''.join(f'<div><b>R{r}</b><span>{d.split(" ",1)[1]}</span><i>{t}</i></div>' for r,d,t,s in ROUNDS)}<div><b>GF</b><span>Date TBA</span><i>Grand Final</i></div></div>
{CLUBBOX.replace('CLUBIMG', img('club_crest.png'))}
</div>{folio(n)}'''

RECIPES = [('orange', 'Blood on Sand', ['60 ml aged rum', '20 ml honey', '½ lime', 'Juice of 1 blood orange', 'Dash of orange bitters'],
            'Add rum, honey and fruit to a shaker and fill with ice. Shake hard and strain into a rocks glass over fresh ice. Finish with a dash of bitters and an orange wheel.'),
           ('daiq', 'Classic Daiquiri', ['60 ml white rum', '20 ml sugar syrup', '25 ml fresh lime juice'],
            'Shake all ingredients hard with ice and fine-strain into a chilled coupe. No garnish needed — or a thin lime wheel.'),
           ('mojito', 'Basil &amp; Ginger Highball', ['60 ml white rum', '60 ml dry ginger ale', '20 ml sugar syrup', '¾ lime', '6 basil leaves', 'Slice of fresh ginger'],
            'Muddle lime and basil with the syrup, add rum and ice and shake. Strain into a highball over ice, top with dry ginger and garnish with fresh ginger.')]

def mixology(n):
    cards = ''.join(f'''<div class="rcp">{photo(k,'rcp-img',fixed=True)}<div class="rcp-body"><h3>{t}</h3><div class="ing"><b>&lt;Ingredients&gt;</b>{''.join(f"<span>{x}</span>" for x in ing)}</div><p><b>&lt;Method&gt;</b> {m}</p></div></div>''' for k, t, ing, m in RECIPES)
    return f'''{frame()}<div class="safe">{head('Mixology', 'Featuring [Spirit Partner] ' + ph('SPONSORED FEATURE SLOT'))}
<div class="rcps">{cards}</div>
<p class="note">Recipes are written for a generic spirit until the featured brand for this issue is confirmed. Please enjoy responsibly.</p>
</div>{folio(n)}'''

def news(n, strip=False, vstrip=False):
    s = (strip_ad(n, strip, 'Bottom strip, as 2007 News page') if isinstance(strip, str) else ad('hstrip', f'AD-{n:02d}-S', 'Bottom strip, as 2007 News page', n % 2 == 1)) if strip else ''
    v = ad('vstrip', f'AD-{n:02d}-V', '', n % 2 == 1) if vstrip else ''
    cls = 'withstrip' if strip else ('withv-' + ('r' if n % 2 == 1 else 'l') if vstrip else '')
    return f'''{frame()}<div class="safe {cls}">{head('News', 'The facts, and nothing but the facts')}
<div class="news">
<div><h3>The Founding 12 take shape</h3><p>Invitations have gone to bars across Melbourne for twelve places in the inaugural Championship. Teams register their interest now; application dates go to registered teams first. Contact {REGISTER}. {ph()}</p></div>
<div><h3>Season 2027–28 calendar confirmed</h3><p>Eight Monday-night rounds, six weeks apart, from 21 June 2027 to 10 April 2028. The Grand Final date will be announced later in the season.</p></div>
<div><h3>Join the DrinkHQ team</h3><p>DrinkHQ Magazine is growing. If you write, shoot or simply know Melbourne’s bars better than anyone, we want to hear from you at {CONTACT}.</p></div>
<div><h3>[News headline]</h3><p>[Short industry news item — new openings, product launches, people moves.] {ph()}</p></div>
</div>{photo('martini','flexpic','object-position:50% 35%')}</div>{s}{v}{folio(n, strip)}'''

def whats_hot(n, vstrip=True):
    recto = n % 2 == 1
    v = ad('vstrip', f'AD-{n:02d}-V', 'Outer-edge vertical strip', recto) if vstrip else ''
    cls = ('withv-' + ('r' if recto else 'l')) if vstrip else ''
    items = ['[Trend or drink #1]', '[Trend or drink #2]', '[Trend or drink #3]', '[Trend or drink #4]', '[Trend or drink #5]']
    return f'''<div class="bleedimg navyfill"></div><div class="safe {cls} onnavy">
<h1 class="big light">What’s <i>Hot</i></h1>
<div class="hot">{''.join(f'<div><span>✱</span>{x}</div>' for x in items)}</div>{ph()}
{photo('laugh','flexpic')}
<div class="chasers"><div class="label gold">Chasers · from our readers</div>
<p>“[Reader letter or SMS.]”<br><i>[Name] · via email</i></p>
<p>“[Reader letter or SMS.]”<br><i>[Name] · via Instagram</i></p>
<p class="small">Send yours to {CONTACT}</p></div>
</div>{v}{folio(n)}'''

def reviews(n):
    prods = ''.join(f'<div class="prod"><div class="prod-img">{ph("PACK SHOT")}</div><h3>[Product name]</h3><p>[50–70 word tasting note: what it is, how it drinks, and the serve we’d recommend.] {ph()}</p><div class="stars">★★★☆☆</div></div>' for _ in range(3))
    return f'''{frame()}<div class="safe">{head('Review', 'New on the back bar')}
<div class="prods">{prods}</div>
<div class="win"><b>{WEBSITE}</b><span>win stuff</span></div>
</div>{folio(n)}'''

TOP10 = [('Vesper Martini', 'Casino Royale'), ('White Russian', 'The Big Lebowski'), ('Mint Julep', 'Goldfinger'),
         ('Gin Rickey', 'The Great Gatsby'), ('Manhattan', 'Some Like It Hot'), ('Singapore Sling', 'Fear and Loathing in Las Vegas'),
         ('Martini', 'The Thin Man'), ('Mojito', 'Die Another Day'), ('Old Fashioned', 'Crazy, Stupid, Love'), ('Cosmopolitan', 'Sex and the City')]
GLOSS = [('Back bar', 'The shelves of bottles behind the bartender — the bar’s shop window.'),
         ('Build', 'Making a drink straight in the glass it’s served in.'),
         ('Dash', 'A few drops, usually of bitters, shaken from the bottle.'),
         ('Dry shake', 'Shaking without ice to whip egg white or aquafaba into foam.'),
         ('Expressed', 'Citrus peel squeezed over a drink to release its oils.'),
         ('Fine strain', 'Straining through a second, fine sieve for a silky drink.'),
         ('Garnish', 'The finishing touch — aroma, colour and story in one.'),
         ('Highball', 'A spirit lengthened with a mixer over plenty of ice.'),
         ('Jigger', 'The measuring cup that keeps every pour honest.'),
         ('Julep strainer', 'A perforated spoon-like strainer used with a mixing glass.'),
         ('Kick', 'What an over-proof pour adds — and what judges notice.'),
         ('Long drink', 'A mixed drink served tall, with plenty of mixer.'),
         ('Muddle', 'Pressing fruit, herbs or sugar to release their flavour.'),
         ('Neat', 'A spirit poured straight from the bottle: no ice, no mixer.'),
         ('On the rocks', 'Poured over ice.'),
         ('Proof', 'A measure of alcohol strength; in the US, twice the ABV.'),
         ('Rinse', 'Coating the glass with a spirit, such as absinthe, and tipping out the rest.'),
         ('Shrub', 'A drinking vinegar of fruit, sugar and vinegar.'),
         ('Twist', 'A strip of citrus peel twisted over the drink.'),
         ('Up', 'Chilled with ice, then strained and served without it.'),
         ('Vermouth', 'Wine fortified and flavoured with botanicals.'),
         ('Well', 'The house spirits kept within the bartender’s reach.'),
         ('Zest', 'The coloured outer peel of citrus, rich in oils.')]

def top10(n):
    t = ''.join(f'<li><span>{i+1}</span><b>{a}</b><i>{b}</i></li>' for i, (a, b) in enumerate(TOP10))
    g = ''.join(f'<p><b>{a}</b> {b}</p>' for a, b in GLOSS)
    return f'''{frame()}<div class="safe t10b">
<div class="t10b-col"><div class="t10b-left">{photo('martini','t10b-bg',fixed=True)}<div class="t10b-tint"></div>
<div class="t10b-in"><div class="kicker">DrinkHQ</div><h1 class="sec t10b-sec">Top 10</h1><h2>Movie cocktails worth a <i>rewatch</i></h2><ol>{t}</ol></div></div>
<div class="t10b-cta"><span>See it live</span><b>Round 1 · Cinematic Cocktails</b><p>Monday 21 June 2027, 7:00 PM. Tickets from $15.</p><div class="t10b-btn"><small>Book tickets at</small><b>{WEBSITE}</b></div></div></div>
<div class="t10b-right"><h2 class="t10b-h">The DrinkHQ Guide to <i>Bar Lingo</i></h2><div class="kicker2">A TO Z</div><div class="gloss2">{g}</div>
<div class="strip3 t10b-pics">{''.join(f'<div class="t10b-pic">{photo(k,fixed=True)}<div class="t10b-pcap"><b>{t}</b>{d}</div></div>' for k,t,d in (('negroni','Expressed','Orange peel over a Negroni'),('pour3','Jigger','Every pour measured'),('lemonmart','Garnish','The finishing touch')))}</div></div>
</div>{folio(n)}'''

def traveller(n):
    return f'''<div class="bleedimg">{photo('b1806','fill')}<span class="ph imgtag" contenteditable="false">PLACEHOLDER IMAGE</span></div><div class="trav-shade"></div>
<div class="safe onnavy trav"><div class="kicker light">[ traveller ]</div>
<h1 class="huge light">[Bar name]</h1><div class="addr">[Street address, city] · [Phone] {ph()}</div>
<div class="trav-box"><p class="lede">[Standfirst: one or two sentences that sell the venue — what makes it worth the trip.]</p>
<p>[Feature copy, 250–300 words. A bar abroad worth planning a trip around: the room, the drinks list, the people behind the stick, and when to go. Written in the DrinkHQ voice — knowledgeable, warm and a little cheeky.]</p>
<p class="small">[ Story: Contributor name ]</p></div></div>{folio(n)}'''

def shaken(n, half=False):
    recto = n % 2 == 1
    h = ad('half', f'AD-{n:02d}-H', 'Half page vertical, as 2007 Shaken &amp; Stirred', recto) if half else ''
    cls = ('withh-' + ('r' if recto else 'l')) if half else ''
    if not half:
        items = [('Shake or stir?', 'Shake anything with citrus, cream or egg — it needs the air and dilution. Stir spirit-only drinks like the Martini and Manhattan for a clear, silky texture.'),
                 ('Ice is an ingredient', 'Big, cold, dense ice melts slowly and keeps a drink tasting the way the bartender intended. Small wet ice waters it down.'),
                 ('Hair of the dog?', 'Another drink doesn’t cure a hangover — it only delays it. Water, food and sleep do the work.')]
        body = ''.join(f'<div class="ss"><h3>{a}</h3><p>{b}</p></div>' for a, b in items)
        return f'''<div class="bleedimg navyfill"></div><div class="safe onnavy">
<div class="ss-grid">{photo('mint','ss-img')}{photo('bottles','ss-img')}{photo('ice','ss-img')}</div>
<div class="ss-cols light">{body}</div></div>{folio(n)}'''
    items = [('Where “cocktail” began', 'The word was first defined in print in 1806, in a New York newspaper: spirits, sugar, water and bitters. Two centuries on, that’s still the outline of an Old Fashioned.'),
             ('Pick ’em up', '[A bar-top one-liner from our readers.] ' + ph()),
             ('Overheard at the bar', '“[Quote from a bartender or guest.]” ' + ph())]
    body = ''.join(f'<div class="ss"><h3>{a}</h3><p>{b}</p></div>' for a, b in items)
    return f'''<div class="bleedimg navyfill"></div><div class="safe onnavy {cls}">
<div class="kicker light">[ shaken &amp; stirred ]</div><h1 class="big light">Shaken <i>&amp; Stirred</i></h1>
<p class="light body">All the info you need to get through life.</p>
<div class="ss-one">{photo('pour3','ss-img tall')}</div>
<div class="ss-cols light one">{body}</div></div>{h}{folio(n)}'''

def recommended(n):
    return f'''<div class="bleedimg top55">{photo('edv','fill')}<span class="ph imgtag" contenteditable="false">PLACEHOLDER IMAGE</span></div>
<div class="safe rec">
<div class="rec-title"><div class="kicker light">[ recommended ]</div><h1 class="huge light">[Bar name]</h1><div class="addr light">[Address], Melbourne · Ph [number]</div></div>
<p class="lede">[Standfirst — why this bar is our pick this issue.] {ph()}</p>
<div class="cols2 body"><p>[Review copy, 300–350 words. The room and the welcome; the drinks list and what to order; the food; the details that make it special; and who it’s for.]</p>
<p>[Close with the one thing you should not leave without trying.]</p></div>
<div class="rec-strip">{photo('ice')}{photo('lemonmart')}{photo('orange')}</div>
<div class="facts"><span><b>Type</b> [Cocktail bar]</span><span><b>Hours</b> [Days, times]</span><span><b>Food</b> [Yes/No]</span><span><b>Bookings</b> [Yes/No]</span></div>
</div>{folio(n)}'''

def bib_card(k, i):
    return f'''<div class="bib">{photo(k,'bib-img',tag='PLACEHOLDER IMAGE')}<h3>[Bar name {i}]</h3><div class="addr">[Address] · [Phone]</div>
<p>[60–80 word review: the room, the crowd, the drinks, the verdict.]</p>
<table class="bibt"><tr><td>Type</td><td>[Bar / pub]</td></tr><tr><td>Feature</td><td>[Rooftop, fireplace…]</td></tr><tr><td>Hours</td><td>[Times]</td></tr><tr><td>Food</td><td>[Yes / No]</td></tr><tr><td>Cocktails</td><td>[Number / on request]</td></tr></table>
<div class="score"><b>DrinkHQ score</b><span>Atmosphere ★★☆</span><span>Service ★★★</span><span>Products ★★☆</span><span><b>We recommend</b> [the one thing to order]</span></div></div>'''

def bars_in_brief(n, part):
    ks = ['barA', 'barB', 'barC'] if part == 0 else ['b1806', 'ice', 'bottles']
    cards = ''.join(bib_card(k, part * 3 + i + 1) for i, k in enumerate(ks))
    h = '<h1 class="bib-head">bars in brief</h1>' if part == 0 else ''
    key = ('<div class="key">★ Satisfactory — the general run of the mill · ★★ Decent — an individual twist, not yet at full potential</div>' if part == 0 else
           '<div class="key">★★★ Fantastic — something unique, original, consistent · ★★★★ Exceptional — very hard to fault, total originality that works</div>')
    return f'''{frame()}<div class="safe">{h}<div class="bibs">{cards}</div>{key}</div>{folio(n)}'''

def spirit(n, part, strip=False):
    s = ad('hstrip', f'AD-{n:02d}-S', '', n % 2 == 1) if strip else ''
    if part == 0:
        return f'''<div class="bleedimg">{photo('cane','fill')}</div><div class="sp-shade"></div>
<div class="safe onnavy"><div class="kicker light">[ spirit explained ]</div><h1 class="huge light">RUM</h1>
<blockquote class="light">Sun, sugar and centuries of seafaring — no spirit carries its history in the glass quite like rum.</blockquote>
<div class="cols2 light sp">
<p>Ask people about rum and plenty will screw up their faces and mention a night on the house rum and cola. Fortunately, the world of premium rum has moved on a long way since then — and bartenders have noticed.</p>
<p>Rum is distilled from sugarcane: either fresh-pressed cane juice or molasses, the dark syrup left behind when sugar is made. Most rum starts with molasses, which brings rich, toffee-like depth. Cane-juice rums, like the French Caribbean <i>rhum agricole</i>, taste grassier and brighter.</p>
<p>Fermentation shapes the flavour too. Short, fast fermentations make lighter rums; slow ones build heavier, fruitier styles. Then comes the cask — rum ages quickly in tropical heat, picking up colour and spice from the oak.</p>
<p>Rum’s story runs through the Caribbean, where records of it date back to the 1600s, and through the Royal Navy, which issued sailors a daily ration for more than three centuries until “Black Tot Day” on 31 July 1970.</p></div></div>{folio(n)}'''
    styles = [('White', 'Light, clean and usually filtered after ageing. The backbone of the Daiquiri and Mojito.'),
              ('Gold', 'Lightly aged for a touch of vanilla and spice. Easy in highballs.'),
              ('Dark', 'Molasses-rich and full-bodied. Think punches and tiki.'),
              ('Aged', 'Years in oak for sipping-level depth. Try it neat or in an Old Fashioned.'),
              ('Agricole', 'Made from fresh cane juice. Grassy, vibrant, and made for the Ti’ Punch.')]
    sty = ''.join(f'<div class="sty"><span class="num">{i+1:02d}</span><div><b>{a}</b><p>{b}</p></div></div>' for i, (a, b) in enumerate(styles))
    return f'''{frame()}<div class="safe {'withstrip' if strip else ''}"><div class="kicker">[ spirit explained ]</div>
<h1 class="big">Rumba, Rumba, <i>with Rum</i></h1><p class="body">Five styles to know before your next order.</p>
<div class="stys">{sty}</div>
<p class="note">Turn to Mixology for three rum serves to make at home.</p>{photo('barrels','flexpic')}</div>{s}{folio(n, strip)}'''

def wwyln(n):
    ks = ['laugh', 'bw', 'team2', 'team3', 'team4', 'pour2', 'pour3', 'stir', 'tie']
    g = ''.join(f'<div class="ww">{photo(k,"fill")}<span>{i+1}</span></div>' for i, k in enumerate(ks))
    return f'''<div class="bleedimg greenfill"></div><div class="safe">
<div class="kicker light">[ where were you last night? ]</div><h1 class="big light">Where were you <i>last night?</i></h1>
<div class="wwg">{g}</div>
<p class="light small">1–9. [Venue names / event] {ph('PLACEHOLDER PHOTOS — PRE-LAUNCH EVENT')} Only publish photos of people who have agreed to appear.</p>
<p class="light">Want to appear here with the beautiful people? Tag us or send your photos to {CONTACT}</p>
</div>{folio(n)}'''

def back_page_extras(n):
    return f'''{frame()}<div class="safe x3">
<div class="col comp"><img src="{img('wordmark_gold.png')}" class="wm" alt=""><div class="big2">Competitions</div>
<div class="cbox"><b>Win a [prize]</b><p>[Prize description and how to enter.] {ph()}</p></div>
<div class="cbox"><b>Win a [prize]</b><p>[Prize description and how to enter.] {ph()}</p></div>
<p class="small">Enter at {CONTACT}. Entrants must be 18+. Terms apply.</p>{photo('mintglass','flexpic')}</div>
<div class="col iv">{photo('pour3','iv-img')}<div class="big2 navy">Bartender <i>Interview&gt;</i></div>
<span class="arch">FROM THE ARCHIVE · DRINK SCANDINAVIA 2010</span>
<p><b>Name:</b> Micke Karlsson · <b>Bar:</b> Kåken, Stockholm</p><p><b>Dream bar:</b> An old-fashioned Prohibition-style cocktail bar — a purist’s bar for cocktail lovers.</p><p><b>Favourite tipple:</b> Depends on my mood, but I keep it clean with bourbon and tequila.</p><p><b>Favourite quote:</b> “I have taken more out of alcohol than alcohol has taken out of me.” — Winston Churchill</p></div>
<div class="col club"><div class="clubchip"><img src="{img('club_crest.png')}" class="clublogo" alt=""></div><div class="big2 navy">Connoisseurs <i>Club</i></div>
<p>Membership for people who love great drinks — admission to all eight Championship rounds, a complimentary cocktail at every event, member pricing on merchandise and more.</p>
<div class="tiers"><div><b>Taste Trailblazer</b><span>$239 / year</span></div><div><b>Cocktail Connoisseur</b><span>$359 / year</span></div><div><b>Liquid Luminary</b><span>$549 / year</span></div></div>
<p class="small">Prices include GST. Benefits vary by tier and are subject to the current Membership Terms.</p>
<div class="join">connoisseursclub.com.au<br>{CONTACT}</div></div>
</div>{folio(n)}'''

def page_ad(n, slot, note='', art=None, pos='50% 50%'):
    return ad('full', slot, note, n % 2 == 1, art=art, pos=pos)

# ---------------------------------------------------------------- plans
# ---------------------------------------------------------------- archive-based sections (Oct 2026)
ARCH = '<span class="arch" contenteditable="false">FROM THE ARCHIVE · DRINK 2007</span>'

def strip_ad(n, art, note=''):
    fit = 'cover'
    bg = '#111'
    if art in ('strip_tajga', 'strip_tajga_c'):
        fit, bg = 'contain', '#E4232B'
    if art == 'strip_nash':
        fit, bg = 'contain', '#3F3C9E'
    return ad('hstrip', f'AD-{n:02d}-S', note, n % 2 == 1, art=art, fit=fit, bg=bg)

def news_hot(n, strip=None):
    s = ad('hquarter', f'AD-{n:02d}-Q', 'Quarter page · horizontal · foot of News', n % 2 == 1, art=strip, fit='contain', bg=('#E4232B' if 'tajga' in strip else '#3F3C9E')) if strip else ''
    news = [('The Founding 12 take shape', f'Invitations have gone to bars across Melbourne for twelve places in the inaugural Championship. Application dates go to registered teams first. Contact {REGISTER}.'),
            ('Season 2027–28 confirmed', 'Eight Monday-night rounds, six weeks apart, from 21 June 2027 to 10 April 2028. The Grand Final date will be announced later in the season.'),
            ('Get the taste of it', f'DrinkHQ will run its own tasting series, with experts sharing what they know with the willing few. Register your interest at {CONTACT}.'),
            ('Every drink, scored on TASTE', 'Each cocktail is judged on Taste, Appearance, Skill, Theme and Engagement, so every point on the ladder can be traced back to the glass.'),
            ('People’s Choice Awards', 'Alongside the Championship, the public will vote for the bars and bartenders they love most. Voting details to come in a later issue.'),
            ('The Connoisseurs Club opens', 'Membership for people who like to know what’s in the glass: entry to all eight rounds, a cocktail on us every round and members’ nights.')]
    hot = ['Monday nights at the Championship', 'Hosting your own home cocktail party', 'Travelling to new bars',
           'Low and no serves done properly', 'The onset of winter (lots of warm bars)', 'Bitter aperitifs before dinner',
           'Small-batch Australian gin', 'Bartenders doing guest shifts']
    items = ''.join(f'<div class="nh2-i"><h3>{t}</h3><p>{p}</p></div>' for t, p in news)
    return f'''{frame()}<div class="safe {'withquarter' if strip else ''}">{head('News', 'Giving you the facts and nothing but the facts')}
<div class="nh2">
<div class="nh2-news">{items}</div>
<div class="nh2-hot">{photo('crowd','nh2-bg',fixed=True)}<div class="nh2-tint"></div><div class="hot-h">What’s <i>Hot</i></div>{''.join(f'<div class="hot-i">{x}</div>' for x in hot)}</div>
</div>
<div class="nh2-sub"><div><b>Never miss an issue</b><span>Subscribe free and get every DrinkHQ Magazine in your inbox before each round, plus first word on tickets and tastings.</span></div><div class="nh2-btn">Subscribe free<small>drinkhqmedia.com/contact</small></div></div>
</div>{s}<div class="{'folio quarter' if strip else 'folio'}">// {ISSUE}_ [AU-Melb] // Page {n:02d} //</div>'''

def whats_hot2(n, strip=None):
    s = strip_ad(n, strip) if strip else ''
    hot = ['Monday nights at the Championship', 'Hosting your own home cocktail party', 'Travelling to new bars',
           'Low and no serves done properly', 'The onset of winter (lots of warm bars)']
    return f'''{frame()}<div class="safe {'withstrip' if strip else ''}">
<div class="wh2">
<div class="wh2-hot"><div class="hot-h big2">What’s <i>Hot</i></div>{''.join(f'<div class="hot-i">{x}</div>' for x in hot)}</div>
<div class="wh2-side">
<h1 class="sec">Drink Chasers<span class="gt">&gt;</span></h1>
<p class="small">Feedback from our valued and not so valued readers. We love you all.</p>
<div class="letter">“As a tourist, thanks for Drink — it certainly hit the spot.”<i>Anon · via SMS · from the archive</i></div>
<div class="letter">“When is there going to be a decent place to drink after 1am that doesn’t make me line up?”<i>Sean · via SMS · from the archive</i></div>
<div class="letter-cta">Send yours to {CONTACT}</div>
</div></div>
<div class="trivia">
<div><b>Got some time?</b><p>H. L. Mencken is said to have calculated that 17,864,392,788 different cocktails could be made from the ingredients in a well-stocked bar.</p></div>
<div><b>Living like a king</b><p>In 1694 the English admiral Edward Russell is said to have turned a garden fountain into a punch bowl — brandy, wine, sugar and thousands of lemons — with a boy rowing around in a little boat to fill the guests’ cups.</p></div>
</div></div>{s}{folio(n, bool(strip))}'''

FIX = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10), (11, 12)]
def championship(n):
    fx = ''.join(f'<div class="cf-row"><span>Team {a:02d} · [Name]</span><em>vs</em><span>Team {b:02d} · [Name]</span></div>' for a, b in FIX)
    rd = ''.join(f'<div class="cf-rd"><b>{r}</b><span>{t}</span><i>{d.replace("Mon ", "")}</i></div>' for r, d, t, s in ROUNDS)
    tw = ''.join(f'<div><b>{nm}</b><span>{w}%</span></div>' for l, nm, w, d in TASTE)
    return f'''{frame()}<div class="safe">
<div class="cf-top"><div><div class="kicker">The DrinkHQ Experience · Season 2027–28</div><h1 class="big">Round <i>Fixture</i></h1></div>
<img class="cf-logo" src="{img('lockup_blue.png')}" alt=""></div>
<p class="body">Every round night, twelve teams meet in six head-to-head match-ups — an Individual match and a Team match, seven minutes each — scored on TASTE.</p>
<div class="cf-panel">
<div class="cf-fix"><div class="cf-h">01 · Cinematic Cocktails <span>Mon 21 June 2027 · 7:00 PM</span></div>{fx}<div class="cf-note">Match-ups released after team selection. {ph()}</div></div>
<div class="cf-season"><div class="cf-h">The season</div>{rd}<div class="cf-rd gf"><b>GF</b><span>Grand Final · top six</span><i>Date TBA</i></div></div>
</div>
<div class="cf-3">
<div><h3>Ladder</h3><p>Each round, teams are ranked on their round TASTE total (Team match counts double). The top ten earn Championship points: 25, 18, 15, 12, 10, 8, 6, 4, 2, 1. Points accumulate all season.</p><p>Level on points? Separated by TASTE percentage, then the Sporting Code tie-break.</p></div>
<div><h3>Scoring · TASTE</h3><div class="cf-tw">{tw}</div><p class="small">Five scoring judges per round; a performance’s score is the average of their totals.</p></div>
<div><h3>Bonus points</h3><p>Mystery Box +5 · People’s Choice +3 · Consistency +3 · Fastest Finish +2 · Best Teamwork +2 · Rookie of the Round +2</p><p>Top six after Round 8 go to the Grand Final, seeded by ladder position.</p></div>
</div>
<p class="note">Round themes subject to change. General Admission from $15. Ticket sales open soon at {WEBSITE}.</p>
</div>{folio(n)}'''

BARS16 = [
 ('bib_gb', 'great britain hotel', '447 Church St, Richmond', 'The familiarity hits you as you walk in the door. Good beer, good friends, great place. GB’s the kind of pub everyone wants as their local, big night or quiet one slouched on the comfy couches. The music is chilled, the food is good and the staff are as casual as their customers — plus the summer favourite, a beer garden with picnic tables and palm trees.',
  [('Type', 'Pub'), ('Feature', '9 beers on tap'), ('Hours', '7 days 4pm–1am'), ('Food', 'Bar menu plus pizza'), ('Cocktails', 'No')], (3, 2, 1), 'A pot from the tap'),
 ('bib_elwood', 'elwood lounge', '49–51 Glenhuntly Rd, Elwood', 'A little less hedonistic than big sister St Kilda, but much cooler in many regards. Elwood Lounge may need a fresh coat of paint, but it does the job of a laid-back lounge in a sweet bayside town. Pool out the back, locals mulling over lunch and the paper in the courtyard, and live acoustic acts on Sundays.',
  [('Type', 'Bar / Lounge / Café'), ('Feature', 'Pool tables'), ('Hours', '7 days 9am–1am'), ('Food', 'Café menu'), ('Cocktails', 'On request')], (2, 1, 1), 'VB longneck'),
 ('bib_prahran', 'prahran hotel', '82 High St, Prahran', 'My first reaction was “oh, it’s quite nice” — and it is, especially on quiet nights (avoid Friday). Angel-like statues on the bar top, a chandelier and candles on the windowsill give it a European feel, and the polished floorboards scream pub class. One of the most extensive wine lists around, and Guinness on tap.',
  [('Type', 'Boutique hotel'), ('Feature', 'Renaissance grandeur'), ('Hours', 'Sun–Wed 12–11pm, Thu–Sat 12pm–12am'), ('Food', 'Full menu'), ('Cocktails', 'On request')], (2, 3, 2), 'Mojito'),
]
BARS32 = [
 ('bib_event', 'scubar', '389 Lonsdale St, City', 'Follow the leopard print down the staircase into this little grungy heaven, a dark haven of acid house on Fridays and hip hop on Thursdays. The fish tank glows an iridescent blue as you sink into the boxy couches or hide away in the corner lounges. The small bar is stocked with all you need — the place to end a night.',
  [('Type', 'Bar / Club'), ('Feature', 'Leopard-skin pool table'), ('Hours', 'Mon 7pm–12am, Tue–Sat 4pm–4am'), ('Food', 'No'), ('Cocktails', 'On request')], (3, 1, 1), 'Vodka Martini'),
 ('bib_garden', 'jackie o', '204 Barkly St, St Kilda', 'Don’t be put off by the neon sign on the corner — shut your eyes and delve in, because this is the least pretentious of St Kilda’s haunts. Kitsch meshes with class from brekkie to dinner, and the bar comes alive as people watch Acland Street’s creatures venture into the night. Frozen cocktails are a must; don’t miss happy hour on Fridays.',
  [('Type', 'Bar / Café'), ('Feature', 'Tarot readings'), ('Hours', '7 days 7.30am–1am'), ('Food', 'Full menu'), ('Cocktails', '25')], (2, 1, 2), 'Frangelico Sour'),
 ('bib_lux', 'back bar, tusk', '133 Chapel St, Windsor', 'A winter gem (and just wait for summer) for a leisurely evening in an intimate cocktail bar where time stands still. Chaise lounges straight out of a grandmother’s tearoom tempt you to unwind. The cocktail list would make New York envious — lose yourself in a Cosmopolitan, and late risers with a sweet tooth should try a Breakfast Martini.',
  [('Type', 'Cocktail bar'), ('Feature', 'Fireplace'), ('Hours', '7 days 6pm–late'), ('Food', 'Tapas'), ('Cocktails', '7')], (3, 2, 1), 'Bar Gorgeous'),
]
def dots(k):
    return '<span class="dt">' + '●' * k + '<span class="off">' + '●' * (4 - k) + '</span></span>'

def bars_brief(n, bars, strip=None, small=False):
    if strip and small:
        s = ad('hstrips', f'AD-{n:02d}-S', 'Small strip · foot of Bars in Brief', n % 2 == 1, art=strip, fit='contain', bg='#3F3C9E')
    else:
        s = strip_ad(n, strip) if strip else ''
    cards = ''
    for k, nm, addr, txt, info, sc, rec in bars:
        rows = ''.join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in info)
        cards += f'''<div class="bb">{photo(k,'bb-img',fixed=True)}<h3>{nm}</h3><div class="addr">{addr}</div><p>{txt}</p>
<table class="bbt">{rows}</table>
<div class="bbs"><b>drink score</b><div><span>Atmosphere</span>{dots(sc[0])}</div><div><span>Service</span>{dots(sc[1])}</div><div><span>Products</span>{dots(sc[2])}</div><div class="rec"><span>Drink recommends</span>{rec}</div></div></div>'''
    sc = ('withstrip-s' if small else 'withstrip') if strip else ''
    fo = f'<div class="folio strip-s">// {ISSUE}_ [AU-Melb] // Page {n:02d} //</div>' if (strip and small) else folio(n, bool(strip))
    sc = sc or ('bb100' if bars is BARS32 else '')
    return f'''{frame()}<div class="safe {sc}"><div class="bb-top">{'<div>'+head('Bars in Brief', 'A pinch of pubs, a dash of bars')+'</div>' if (small or bars is BARS32) else '<h1 class="bib-head">bars in brief</h1>'}{ARCH}</div>
<div class="bbs3">{cards}</div>
<div class="bbkey">● Satisfactory · ●● Decent · ●●● Fantastic · ●●●● Exceptional — reviews reproduced from Drink magazine (2007) as layout copy; venues and details will change.</div>
</div>{s}{fo}'''

def featured_bars(n):
    def col(k, nm, addr, paras, typ):
        return f'''<div class="fb">{photo(k,'fb-img',fixed=True)}<div class="fb-name">{nm}</div><div class="fb-body"><div class="addr">{addr}</div>{''.join(f'<p>{p}</p>' for p in paras)}<div class="fb-type"><b>Type</b> {typ}</div></div></div>'''
    a = col('feat_edv', 'Eau De Vie', '1 Malthouse Ln, Melbourne', ['Eau De Vie, in the heart of Melbourne, is a cocktail bar celebrated for its sophisticated ambience and exceptional mixology. Its refined, elegant decor blends classic charm with modern polish — ideal for intimate gatherings and special occasions.', 'Knowledgeable, attentive staff make every guest feel welcome. Whether you’re a cocktail connoisseur or after a memorable night out, Eau De Vie combines elegance, innovation and service.'], 'Cocktail bar')
    b = col('feat_1806', '1806', '169 Exhibition St, Melbourne', ['1806 is a standout cocktail bar in Melbourne’s theatre district, named after the year the word “cocktail” was first defined in print.', 'The menu is a journey through cocktail history, with drinks from every era and the stories behind them. With meticulous attention to mixology and service, guests are greeted at the door and shown to their table to enjoy expertly made cocktails without leaving their seats.'], 'Cocktail bar')
    return f'''<div class="bleedimg blackfill"></div><div class="safe onnavy"><div class="fb-top"><h1 class="sec light">Featured Bars<span class="gt">&gt;</span></h1>{ARCH.replace('DRINK 2007','DRINKHQ RECORD 2025')}</div>
<div class="fb2">{a}{b}</div></div>{folio(n)}'''

WHISKY = [('rv_bushmills', 'Bushmills 1608', 'Irish whiskey', 'This special edition celebrating Bushmills’ 400th anniversary is the perfect start to any collection: triple distillation with crystal malt for exceptional smoothness.', 4),
          ('rv_tyrconnell', 'Tyrconnell Single Malt', 'Irish single malt', 'Distilled by the award-winning Cooley distillery, a driving force behind the Irish single malt revival. Most Irish malt goes into blends, so finding it bottled pure is rare.', 4),
          ('rv_jameson', 'Jameson Gold Reserve', 'Irish whiskey', 'New-oak ageing gives a remarkable boost in oak flavour, balanced with just the right share of sherry-aged whiskey and a good dose of pot-still character. Big and bold.', 4),
          ('rv_chambord', 'Chambord', 'Black raspberry liqueur, France', 'Turning up on more and more back bars, and bartenders swear by it in a Chambord Cosmopolitan. On its own it is very sweet, all rich dark berry, so mix it rather than sip it.', 3),
          ('rv_zywiec', 'Żywiec', 'Polish lager', 'Brewed since 1856 and sold in a 500 ml bottle. A rich, honeyed, malty lager; if you can’t pronounce it, just ask for the beer with the dancing couple on the label.', 4)]
def review2(n, side_art=None):
    recto = n % 2 == 1
    h = ad('third', f'AD-{n:02d}-T', 'Third page vertical', recto, art=side_art) if side_art else ''
    cls = 'witht-' + ('r' if recto else 'l')
    items = ''.join(f'<div class="wk">{photo(k,"wk-img",fixed=True)}<div><h3>{t}</h3><div class="wk-cat">{c}</div><p>{d}</p><div class="stars">{"★"*st}{"☆"*(5-st)}</div></div></div>' for k, t, c, d, st in WHISKY)
    return f'''{frame()}<div class="safe {cls} rv5 lite">{head('Review', 'New on the back bar')}{ARCH.replace(' · DRINK 2007','')}
<div class="wks">{items}</div></div>{h}{folio(n)}'''

def spirit_abs(n):
    return f'''<div class="bleedimg absfill"></div><div class="safe onnavy abs">
<div class="kicker light">[ spirit explained ]</div><h1 class="huge light">Absinthe</h1>
<p class="abs-lede">Was it the absinthe that sent half of Paris mad, or everything else they were drinking? Either way, the green fairy went from the toast of the Belle Époque to banned — and back again.</p>
<div class="abs-grid"><div class="abs-txt">
<p>Like Bénédictine, Pernod and vermouth, absinthe is a herbal spirit. Wormwood, green anise and fennel are macerated and distilled into a high-strength spirit, usually bottled between 45 and 74 per cent alcohol. It began in Switzerland in the late 1700s as a medicinal tonic before taking Paris by storm.</p>
<p>By the late nineteenth century it was the drink of painters and poets — Van Gogh, Rimbaud, Verlaine, Toulouse-Lautrec — and <i>l’heure verte</i>, the green hour, was a fixture of café life. Its reputation grew with its popularity: Switzerland banned it in 1910, the United States in 1912 and France in 1915.</p>
<p>Most of that reputation is now put down to sheer strength and poor imitations rather than thujone, the wormwood compound once blamed for hallucinations. Europe let it back under thujone limits from the late 1980s, and Switzerland and the US followed in the 2000s.</p>
</div><div class="abs-side">{photo('abs_glass','abs-img',fixed=True)}
<div class="abs-box"><b>The ritual</b><p>Rest a slotted spoon and sugar cube on the glass and slowly drip iced water over it — three to five parts water to one. The spirit louches to a cloudy, opalescent green.</p></div>
<div class="abs-box"><b>Try it</b><p>Sazerac · Corpse Reviver No. 2 · Death in the Afternoon (absinthe topped with Champagne, credited to Hemingway).</p></div></div></div>
<p class="small light">Rewritten from Drink magazine’s 2007 Spirit Explained. Please enjoy responsibly.</p>
</div>{folio(n)}'''

def art_feature(n):
    exp = [('Themed rounds', 'Eight rounds, each with its own brief, from cinema to the Mystery Box.'),
           ('Team &amp; individual matches', 'Head-to-head challenges that test the whole bar team.'),
           ('Racing the clock', 'Seven minutes to create and present three identical cocktails.'),
           ('Tastings', 'Sample signature serves and meet the bartenders who made them.'),
           ('Up to 500 guests a round', 'A live crowd, a big room and a proper atmosphere.')]
    e = ''.join(f'<li><b>{a}</b> {b}</li>' for a, b in exp)
    t = ''.join(f'<div><b>{l}</b><span>{w}%</span><i>{nm}</i></div>' for l, nm, w, d in TASTE)
    rd = ''.join(f'<div><b>R{r}</b><span>{d.replace("Mon ", "")}</span><i>{tt}</i></div>' for r, d, tt, ss in ROUNDS)
    return f'''<div class="bleedimg">{photo('pour2','fill',fixed=True)}</div><div class="af-shade2"></div>
<div class="safe onnavy af2"><img class="af-logo" src="{img('lockup_gold.png')}" alt="DrinkHQ Cocktail Mastery Championship">
<div class="af-head"><div class="kicker light">[ the championship ] · season 2027–28</div>
<h1 class="huge light">The Art of <i>Cocktail Mastery</i></h1>
<p class="lede">The battle for cocktail supremacy begins…</p>
<p class="af-intro">The DrinkHQ Cocktail Mastery Championship is a league-style season that celebrates the art of mixology and the bartenders who practise it. It challenges seasoned professionals and rising talent alike to show their creativity, technical skill and passion for the craft, and it is built like a sport.</p></div>
<div class="af-cols"><div><div class="af-label">What to expect</div><ul class="af-exp">{e}</ul></div>
<div><div class="af-label">How a round works</div>
<div class="af-steps"><div><b>01</b><span><i>Preparation · 2 min</i>Teams set up their station and check every ingredient.</span></div><div><b>02</b><span><i>Individual match · 7 min</i>One bartender from each team, head to head.</span></div><div><b>03</b><span><i>Team match · 7 min</i>The whole team, true to the theme, with the story behind the drink. Counts double.</span></div></div>
<p class="af-small af-mb">Six match-ups a night · every round includes a Mystery Box element.</p>
</div></div>
<div class="af-label">Judged on TASTE</div><div class="af-taste">{t}</div>
<p class="af-small"><b>The Grand Final.</b> The top six on the ladder play off on one night. First and second go straight to the semi-finals; third to sixth play for the other two places. Teams of up to four · five judges a round.</p>
<div class="af-label">Season 2027–28 · Monday nights</div><div class="af-dates">{''.join(f'<div><b>R{r}</b><span>{d.split()[1]} {d.split()[2][:3]} {d.split()[3][2:]}</span></div>' for r, d, t, _ in ROUNDS)}<div><b>GF</b><span>TBA</span></div></div>
<div class="trav-info af-team"><span><b>Founder &amp; Competition Director</b> Mark Buckley · mark@thedrinkhqexperience.com.au</span><span><b>Event Manager</b> Ezzie Magrin · {CONTACT}</span><span><b>Partnerships</b> {PARTNER}</span><span><b>Team registration</b> {REGISTER}</span></div>
</div>{folio(n)}'''

def traveller_caretakers(n):
    return f'''<div class="bleedimg">{photo('bib_backbar','fill',fixed=True)}<span class="ph imgtag" contenteditable="false">ILLUSTRATIVE IMAGE</span></div><div class="trav-shade"></div>
<div class="safe onnavy trav"><div class="kicker light">[ traveller ] · a bar worth the trip</div>
<h1 class="huge light">Caretaker’s <i>Cottage</i></h1><div class="addr">139–141 Little Lonsdale Street, Melbourne</div>
<div class="trav-box"><p class="lede">The best bar in Australasia is a tiny bluestone cottage tucked behind a city church. Cross town for it. Cross the world, even: plenty of people do.</p>
<p>The cottage has stood behind the Wesley Place church since 1914, built as the caretaker’s quarters. It was an empty shell when Rob Libecans, Ryan Noreiks and Matt Stirling took it on and opened in 2022, keeping the original staircase and the homely feel. At around 50 square metres it may be the smallest pub in Victoria.</p>
<p>The list is short by design: three classic cocktails, three house creations and one Martini, plus a rotating milk punch and Guinness on tap, poured on the lawn when the weather allows. British pub snacks such as smoked-trout dip and Welsh rarebit keep you going, and the soundtrack comes off vinyl through handmade bronze-and-oak speakers. In 2026 it was named 45th on The World’s 50 Best Bars, its third year running on the list.</p>
<div class="trav-info"><span><b>Type</b> Cottage pub &amp; cocktail bar</span><span><b>Order</b> The Martini, or a Guinness on the lawn</span><span><b>Accolade</b> World’s 50 Best Bars, 2026</span></div>
<p class="small">Details checked October 2026; check hours before you go. Photo is illustrative, not the venue.</p></div></div>{folio(n)}'''

def traveller_riche(n):
    return f'''<div class="bleedimg">{photo('barB','fill',fixed=True)}<span class="ph imgtag" contenteditable="false">PLACEHOLDER IMAGE — NOT RICHE</span></div><div class="trav-shade"></div>
<div class="safe onnavy trav"><div class="kicker light">[ traveller ] · a bar worth the trip</div>
<h1 class="huge light">Riche, <i>‘Lilla Baren’</i></h1><div class="addr">Birger Jarlsgatan 4, Stockholm</div>
<div class="trav-box"><p class="lede">If Stockholm is the fashion and art capital of Scandinavia, then Stureplan is Stockholm’s capital — and Riche’s ‘Lilla Baren’ is where its fashionistas drink.</p>
<p>Riche has held this classic restaurant address since 1893, changing guises over the years. Its Parisian-style dining room plays host to the city’s well-heeled, while Lilla Baren, the decadent little bar next door, gives the hip and fashionable their stage. Here your style counts for more than your bank balance.</p>
<p>The bar keeps its swagger with the quiet confidence of professionals who know their craft, ready for whatever classic or modern drink you throw at them. DJs arrive late in the week and play to the bitter end. Lilla Baren is a bar and a canvas: fashion, art, music, food, drink and wine, and by the end of the night a finished piece full of texture, life and colour.</p>
<div class="trav-info"><span><b>Type</b> Cocktail lounge / wine bar</span><span><b>Highlights</b> Decadent decor, music, people</span><span><b>Cocktails</b> Designer and classic</span></div>
<p class="small">From the archive · Drink Scandinavia, Issue 1, 2010. Details may have changed — check before you travel.</p></div></div>{folio(n)}'''

def spirit_cachaca(n):
    rec = [('Caipirinha', '60 ml cachaça · ½ lime cut into wedges · 2 tsp sugar', 'Muddle lime and sugar in a rocks glass, add cachaça, fill with crushed ice and stir.'),
           ('Cachaça Sour', '50 ml cachaça · 30 ml lemon juice · 20 ml sugar syrup · 20 ml egg white', 'Dry shake, shake again with ice, double strain into a chilled glass. Three drops of Angostura on top.'),
           ('Röd Rouge', '40 ml cachaça · 20 ml Lillet Rouge · 5 ml sugar syrup · 3 dashes orange bitters', 'Stir slowly with ice, strain over one large cube in an old fashioned glass, finish with orange zest.')]
    r = ''.join(f'<div class="cc"><b>{a}</b><span>{b}</span><p>{c}</p></div>' for a, b, c in rec)
    return f'''<div class="bleedimg cachfill"></div><div class="safe onnavy abs">
<div class="kicker light">[ spirit explained ]</div><h1 class="huge light">Viva <i>Cachaça!</i></h1>
<p class="abs-lede">Think Brazil: football, samba, sunshine — and cachaça (kah-sha-sa), the country’s national spirit and the soul of the Caipirinha.</p>
<div class="abs-grid"><div class="abs-txt">
<p>Cachaça was born more than 400 years ago on Brazil’s sugar plantations. Where most rum is made from molasses, cachaça is distilled from fresh-pressed sugarcane juice, fermented and then distilled — which gives it a grassier, livelier character. Some call it rum’s cousin; Brazilians would rather you didn’t.</p>
<p>Unaged cachaça (<i>branca</i> or <i>prata</i>) is bright and fiery, made for mixing. Aged cachaça (<i>amarela</i> or <i>ouro</i>) rests in oak or in native Brazilian woods, mellowing into something smooth and warming that is worth sipping neat — the real test of a good one.</p>
<p>It is one of Brazil’s most popular drinks, and with thousands of producers it pays to have a bartender who knows what is hot and what is not. Like vodka and tequila before it, it has been moving steadily from party spirit to back-bar favourite.</p>
</div><div class="abs-side">{photo('limes','abs-img',fixed=True)}{r}</div></div>
<p class="small light">Rewritten from Drink Scandinavia’s 2010 feature. Please enjoy responsibly.</p>
</div>{folio(n)}'''

def _spchip():
    return '<div class="sp-chip"><span>Sponsorship</span><div>AVAILABLE</div></div>'

def cachaca_a(n):
    stats = [('400+', 'years of history'), ('100%', 'fresh cane juice'), ('38–48%', 'ABV, by Brazilian law'), ('1', 'country: Brazil only')]
    st = ''.join(f'<div><b>{a}</b><span>{b}</span></div>' for a, b in stats)
    return f'''<div class="bleedimg navyfill"></div><div class="safe onnavy cxa">
<div class="cxa-hero">{photo('cane','cxa-img',fixed=True)}<div class="cxa-shade"></div>
<div class="cxa-t"><div class="kicker">[ Spirit explained ] · Brazil</div><h1>Viva <i>Cachaça!</i></h1><p>Say it kah-SHAH-sah. Brazil’s national spirit, and the soul of the Caipirinha.</p></div>
{_spchip()}</div>
<div class="cxa-cols">
<p class="cxa-first">Think Brazil and you think football, samba and sunshine. Think Brazil in a glass and it has to be cachaça, the national spirit and the backbone of the Caipirinha. It has been made for more than 400 years, since the first sugar mills went up along the coast, and almost all of it is still drunk in Brazil.</p>
<p>What sets it apart is the raw material. Most rum is distilled from molasses, the sticky leftover of sugar-making. Cachaça starts with fresh sugarcane juice, pressed soon after the cane is cut, then fermented and distilled. That is where its grassy, green, lively character comes from, and why Brazilians bristle when it is filed under rum.</p>
<p>Small producers still distil in copper pot stills, batch by batch; the big brands use column stills. Either way, the law keeps it between 38 and 48 per cent alcohol, and only spirit made in Brazil can carry the name.</p>
<p>Unaged, it is bright and fiery and made for mixing. Rested in wood it becomes something else: producers use oak and native Brazilian woods such as amburana, each with its own effect on colour and flavour. With more than 1,500 registered producers to choose from, it pays to have a bartender who knows the good ones.</p>
<blockquote class="cxa-q">“Some call it rum’s cousin. Brazilians would rather you didn’t.”</blockquote>
</div>
<div class="cxa-stats">{st}</div>
</div>{folio(n)}'''

def cachaca_b(n):
    steps = [('Cut', 'Sugarcane is harvested, often by hand on small farms.'), ('Press', 'The fresh cane is crushed for its juice soon after cutting.'), ('Ferment', 'The juice ferments for a day or two, often with natural yeasts.'), ('Distil', 'Copper pot stills for small batches, columns for volume.'), ('Rest', 'Steel or neutral wood for prata; oak or native woods for ouro.')]
    sp = ''.join(f'<div><i>{k+1:02d}</i><b>{a}</b><span>{b}</span></div>' for k, (a, b) in enumerate(steps))
    rec = [('limes', 'Caipirinha', '60 ml cachaça · ½ lime in wedges · 2 tsp sugar', 'Muddle lime and sugar in a rocks glass, add cachaça, fill with crushed ice and stir.'),
           ('daiq', 'Cachaça Sour', '50 ml cachaça · 30 ml lemon · 20 ml sugar syrup · 20 ml egg white', 'Dry shake, shake with ice, double strain. Three drops of Angostura on top.'),
           ('orange', 'Röd Rouge', '40 ml cachaça · 20 ml Lillet Rouge · 5 ml syrup · 3 dashes orange bitters', 'Stir with ice, strain over one large cube, finish with orange zest.')]
    rc = ''.join(f'<div class="cxb-r">{photo(k,"cxb-rimg",fixed=True)}<div><b>{t}</b><span>{i}</span><p>{m}</p></div></div>' for k, t, i, m in rec)
    return f'''{frame()}<div class="safe cxb lite">
<div class="cs-h"><div><div class="kicker">[ Spirit explained ] · From cane to glass</div><h2>How it’s <i>made</i></h2></div></div>
<div class="cxb-steps">{sp}</div>
<div class="cxb-st">
<div class="cxb-s">{photo('bottles','cxb-simg',fixed=True)}<div><em>Clear</em><b>Branca · Prata</b><p>Clear, bright and fiery. Made for mixing, and the one for a Caipirinha.</p></div></div>
<div class="cxb-s dark">{photo('barrels','cxb-simg',fixed=True)}<div><em>Rested in wood</em><b>Amarela · Ouro</b><p>Golden, smooth and warming. Sip it neat to taste what the wood has done.</p></div></div>
</div>
<table class="cxb-t"><tr><th></th><td class="h">Cachaça</td><td class="h">Rum</td></tr><tr><th>Made from</th><td>Fresh sugarcane juice</td><td>Mostly molasses</td></tr><tr><th>Made in</th><td>Brazil only</td><td>Around the world</td></tr><tr><th>Aged in</th><td>Oak and native Brazilian woods</td><td>Mostly oak</td></tr></table>
<div class="cs-h"><div><div class="kicker">[ Make it ] · Three serves</div></div></div>
<div class="cxb-rs">{rc}</div>
<p class="cxb-note">Updated from Drink Scandinavia’s 2010 feature. Please enjoy responsibly.</p>
</div>{folio(n)}'''

def wwyln2(n, start):
    ks = [f'ww{i:02d}' for i in range(start, start + 12)]
    g = ''.join(f'<div class="pol" style="transform:rotate({[-2,1.5,-1,2,-1.5,1][i%6]}deg)">{photo(k,"pol-img",fixed=True)}<span>{i+1}</span></div>' for i, k in enumerate(ks))
    return f'''<div class="bleedimg greenfill"></div><div class="safe">
<div class="kicker light">[ where were you last night? ]</div><h1 class="big light">Where were you <i>last night?</i></h1>
<div class="polg">{g}</div>
<p class="light small">1–12. Drink magazine nights, from the archive — replaced with Season 2027–28 round-night photos. Only publish photos of people who have agreed to appear. {ph('ARCHIVE PHOTOS')}</p>
<p class="light">Want to appear here with the beautiful people? Tag us or send your photos to {CONTACT}</p>
</div>{folio(n)}'''

SHAKEN = [
 ('ss_capone', 'Did You Know?', 'g', 'Al Capone is said to have made around $50 million a year from bootleg alcohol during Prohibition.', 'r'),
 ('ss_schweppes', 'Bottled Money', 'g', 'Bottled soda water was so popular that its pioneer, Jacob Schweppe, retired in 1799, only seven years after opening his London factory.', 'l'),
 ('ss_pour', 'Hooch', 'r', 'Strong, rough spirits. The word comes from Hoochinoo, a Tlingit village in Alaska whose people made liquor and sold it to travellers.', 'r'),
 ('ss_eye', 'Pick ’em up!', 'r', '“Your father’s a thief. He stole the stars out of the sky and put them in your eyes.”', 'l'),
 ('ss_yeats', 'Quote', 'g', '“The problem with some people is that when they aren’t drunk, they’re sober.” — attributed to W. B. Yeats', 'r'),
 ('ss_ice', 'Bar Trick', 't', 'Bet someone a drink they can’t lift an ice cube with a single hair. The trick: lay the hair across the cube and sprinkle on salt. The ice refreezes around the hair, and up it comes.', 'l'),
]
def shaken_v2(n):
    cards = [('ss_schweppes', 'Bottled money', 'Soda water was such a hit that its pioneer, Jacob Schweppe, retired in 1799, only seven years after opening his London factory.'),
             ('ss_shots', 'Hooch', 'Strong, rough spirits. The word comes from Hoochinoo, a Tlingit village in Alaska whose people made liquor and sold it to travellers.'),
             ('ss_eye', 'Pick ’em up!', '“Your father’s a thief. He stole the stars out of the sky and put them in your eyes.” An old bar line, use at your own risk.'),
             ('ss_yeats', 'Quote', '“The problem with some people is that when they aren’t drunk, they’re sober.” Attributed to W. B. Yeats.')]
    c = ''.join(f'<div class="s2-card"><div class="s2-ph">{photo(k,"s2-img",fixed=True)}</div><div><h3>{h}</h3><p>{d}</p></div></div>' for k, h, d in cards)
    return f'''<div class="bleedimg navyfill"></div><div class="safe onnavy s2">
<div class="s2-hero">{photo('ss_pour','s2-hero-img',fixed=True)}<div class="s2-hshade"></div>
<div class="s2-ht"><div class="kicker">[ shaken &amp; stirred ]</div><h1>Shaken <i>&amp; Stirred</i></h1><p>All the info you need to get through life.</p></div>
<div class="s2-spons"><span>Brought to you by</span><div class="w-logo">SPONSORSHIP AVAILABLE</div><em>partner@thedrinkhqexperience.com.au</em></div></div>
<div class="s2-dyk"><div class="s2-dyk-ph">{photo('ss_capone','s2-img',fixed=True)}</div>
<div><div class="s2-tag">Did you know?</div><div class="s2-big">$50 million</div><p>That is roughly what Al Capone is said to have made in a single year from bootleg alcohol during Prohibition.</p></div></div>
<div class="s2-grid">{c}</div>
<div class="s2-trick"><div class="s2-trick-ph">{photo('ss_ice','s2-img',fixed=True)}</div><div><div class="s2-tag dark">Bar trick</div><p>Bet someone a drink they can’t lift an ice cube with a single hair. Lay the hair across the cube, sprinkle on salt, wait a moment: the ice refreezes around the hair, and up it comes.</p></div></div>
<p class="s2-note">From the archive · Drink magazine. Facts are as commonly told; please enjoy responsibly.</p>
</div>{folio(n)}'''

def shaken_bubbles(n):
    cells = ''.join(f'''<div class="sb"><div class="sb-bub tail-{t}">{photo(k,'sb-img',fixed=True)}</div><h3 class="c-{c}">{h}</h3><p>{d}</p></div>''' for k, h, c, d, t in SHAKEN)
    return f'''<div class="bleedimg navyfill"></div><div class="safe onnavy ss">
<div class="ss-top"><div><div class="kicker">[ shaken &amp; stirred ]</div><h1 class="big light">Shaken <i>&amp; Stirred</i></h1><p class="ss-sub">All the info you need to get through life.</p></div>
<div class="ss-spons"><img src="{img('ss_183')}" alt="1883 Maison Routin"><span>SAMPLE · PAGE SPONSOR</span></div></div>
<div class="ss-grid">{cells}</div>
<p class="small light">From the archive · Drink magazine. Facts are as commonly told; enjoy responsibly.</p>
</div>{folio(n)}'''

def contents_mast(n, items, tiles, short=False):
    rows = ''.join(f'<div class="cm-row"><span class="cm-n">{p:02d}</span><div><b>{t}</b><span>{d}</span></div></div>' for p, t, d in items)
    tl = ''.join(f'<div class="cm-tile">{photo(k,"cm-img",fixed=True)}<div><span>{p:02d}</span>{t}</div></div>' for k, p, t in tiles)
    return f'''{frame()}<div class="safe cm">
<div class="cm-main{' long' if len(items)>8 else ''}">
<div class="cm-hero{'' if short else ' tall'}">{photo('laugh','cm-hero-img',fixed=True)}<div class="cm-hero-shade"></div>
<div class="cm-issue cm-issue2"><b>01</b><span>ISSUE · JUNE 2027</span></div>
<div class="cm-hero-t"><h1>Contents</h1>
<div class="cm-intro"><span>A word from the source</span>{"Welcome to Issue 01, the Official Record of the inaugural DrinkHQ Cocktail Mastery Championship. Pull up a stool, grab a drink and enjoy the show." if short else "Welcome to Issue 01, the Official Record of the inaugural DrinkHQ Cocktail Mastery Championship: twelve of Melbourne’s best bar teams, eight themed rounds and one Grand Final. Every issue lands before its round with the fixture, the standings and the stories from behind the bar. Pull up a stool, grab a drink and enjoy the show."}<b class="cm-sig">Mark Buckley <small>Founder &amp; Competition Director</small></b></div></div></div>
<div class="cm-tiles">{tl}</div>
<div class="cm-list{' dense' if len(items)>8 else ''}">{rows}</div>
<div class="cm-win"><div class="cw-head"><b>WIN</b><span>with DrinkHQ</span></div>
<div class="cw-prizes"><div><i>01</i><b>A table for five</b><span>Food &amp; Drink Package at Round 1 of the Championship</span></div><div><i>02</i><b>Double pass, all season</b><span>General Admission for two to all 8 rounds</span></div><div><i>03</i><b>Liquid Luminary</b><span>A year’s top-tier Connoisseurs Club membership</span></div></div>
<div class="cw-enter">Enter at <b>drinkhqmedia.com/win</b> · Entries close Thu 15 July 2027 · 18+ only. Full terms online.</div></div>
</div>
<div class="cm-mast">
<img class="cm-logo" src="{img('wordmark_gold.png')}" alt="drinkhq"><div class="cm-mag">MAGAZINE</div>
<dl>
<dt>Publisher</dt><dd>Mark Buckley<br>mark@thedrinkhqexperience.com.au</dd>
<dt>Advertising</dt><dd>partner@thedrinkhqexperience.com.au</dd>
<dt>Special thanks</dt><dd>All the bartenders who drank with us.</dd>
</dl>
<div class="cm-contrib"><b>Write for us</b><div class="cm-qr">{_qr('https://drinkhqmedia.com/contribute/')}</div><span>Stories, photos and bartender interviews. Scan to send yours in.</span></div>
<div class="cm-addr"><b>DrinkHQ Magazine</b><br>PO Box 5112, Hughesdale VIC 3166<br>{CONTACT}<br>drinkhqmedia.com</div>
<p class="cm-legal">{"Published by Business Intelligence International Pty Ltd (ACN 635 792 326), trading as The DrinkHQ Experience. Views expressed are not necessarily those of the publisher. No reproduction without permission. © 2027" if short else "Published by Business Intelligence International Pty Ltd (ACN 635 792 326), trading as The DrinkHQ Experience. DrinkHQ Magazine is a free publication distributed through selected outlets. Views expressed are not necessarily those of the editors or publisher. No responsibility is accepted for the accuracy of advertisements or information in this publication. Material sent to the magazine is assumed to be for publication unless marked “Not for publication”. No reproduction in whole or in part without permission. © 2027"}</p>
<p class="cm-rsa">DrinkHQ supports the responsible service and consumption of alcohol.</p>
</div></div>{folio(n)}'''

# ---------------------------------------------------------------- plans
def art_match(n, house=False, qart=None):
    exp = [('Themed rounds', 'Eight rounds, each with its own brief.'),
           ('Team &amp; individual matches', 'Head-to-head, testing the whole bar team.'),
           ('Racing the clock', 'Seven minutes, three identical cocktails.'),
           ('Tastings', 'Sample the serves, meet the bartenders.'),
           ('Up to 500 guests a round', 'A live crowd and a proper atmosphere.')]
    e = ''.join(f'<li><b>{a}</b> {b}</li>' for a, b in exp)
    t = ''.join(f'<div class="taste"><div class="tl">{l}</div><div class="tw">{w}<small>%</small></div><b>{nm}</b><span>{d}</span></div>' for l, nm, w, d in TASTE)
    q = ad('hquarter', f'AD-{n:02d}-Q', 'Quarter page · horizontal · foot of The Art of Cocktail Mastery', n % 2 == 1, art=qart, fit='contain', bg='#171a21') if qart else ad('hquarter', f'AD-{n:02d}-Q', 'Quarter page · horizontal · foot of The Art of Cocktail Mastery', n % 2 == 1)
    hd = (f'<div><div class="kicker">The Championship</div><h1 class="sec am-sec">The Art of Cocktail Mastery</h1></div>' if house else '<h1 class="big">The Art of <i>Cocktail Mastery</i></h1>')
    return f'''{frame()}<div class="safe withquarter am">
<div class="hrow">{hd}<img class="hlogo" src="{img('lockup_blue.png')}" alt=""></div>
<p class="body">A league-style season that celebrates the art of mixology and the bartenders who practise it, built like a sport. Each round brings a new theme, designed to push teams to their limits.</p>
<div class="am-row"><div><div class="label">What to expect</div><ul class="expect">{e}</ul></div>
<div><div class="label">Match overview</div><div class="steps am-steps"><div><span class="num">01</span><b>Preparation · 2 min</b><p>Teams set up their station and check every ingredient and tool.</p></div>
<div><span class="num">02</span><b>Creation &amp; presentation · 7 min</b><p>Three identical cocktails, true to the theme, presented with the story behind them.</p></div></div></div></div>
<div class="label">Judging · the TASTE system</div>
<div class="tastes">{t}</div>
<div class="strip3 am-pics">{photo('ice')}{photo('negroni')}{photo('pinkmart')}</div>
<p class="note">Teams of up to four bartenders. Five scoring judges per round. Published TASTE weights for Season 2027–28. Event team: Mark Buckley, Founder &amp; Competition Director · Ezzie Magrin, Event Manager · Registrations {REGISTER}</p>
</div>{q}<div class="folio quarter">// {ISSUE}_ [AU-Melb] // Page {n:02d} //</div>'''

def round1_ladder(n):
    fx = ''.join(f'<div class="fx {"alt" if i % 2 == 0 else ""}"><span>Team {2*i+1:02d} · [Name]</span><em>vs</em><span>Team {2*i+2:02d} · [Name]</span></div>' for i in range(6))
    rows = ''.join(f'<tr class="{"q" if i < 6 else ""}"><td>{i+1}</td><td>Team {i+1:02d} · [Team name / venue]</td><td>–</td><td>–</td><td>–</td><td>–</td><td>–</td></tr>' for i in range(12))
    return f'''{frame()}<div class="safe rl">
<div class="r1-head"><div><div class="kicker">Round 1</div><h1 class="big">Cinematic <i>Cocktails</i></h1></div>
<div class="r1-date"><b>MONDAY 21 JUNE 2027</b><span>7:00 PM · Venue to be announced</span></div></div>
<div class="rl-top"><div class="rl-intro">{photo('tie','r1-pic')}<p class="body">Teams create cocktails inspired by iconic films, capturing a scene, a character or a moment in every sip. Judged on how clearly the drink tells its film’s story, in the glass, the garnish and the presentation.</p></div>
<div><div class="label">Match fixture {ph('AFTER TEAM SELECTION')}</div><div class="fixture">{fx}</div></div></div>
<div class="rl-lad"><div class="rl-lh"><div class="kicker">Season 2027–28</div><h2 class="rl-h2">Championship <i>Ladder</i></h2></div>
<div class="flow"><div><b>Round-by-round</b><span>Eight themed rounds. Every round counts.</span></div><div class="arrow">→</div><div><b>Grand Final</b><span>Top six after Round 8. Date TBA.</span></div><div class="arrow">→</div><div class="dark"><b>Champions</b><span>DrinkHQ Cocktail Mastery Champions 2027–28</span></div></div></div>
<table class="ladder"><thead><tr><th>#</th><th>Team</th><th>MP</th><th>W</th><th>L</th><th>PF</th><th>Pts</th></tr></thead><tbody>{rows}</tbody></table>
<p class="note">The ladder opens after Round 1; gold rows mark Grand Final places. General Admission from $15 (advance) at {WEBSITE}. Round themes subject to change.</p>
</div>{folio(n)}'''

def news_v3(n):
    news = [('Season 2027–28 confirmed', 'Eight Monday-night rounds, six weeks apart, from 21 June 2027 to 10 April 2028. The Grand Final date will be announced later in the season.'),
            ('Get the taste of it', f'DrinkHQ will run its own tasting series, with experts sharing what they know with the willing few. Register your interest at {CONTACT}.'),
            ('Every drink, scored on TASTE', 'Each cocktail is judged on Taste, Appearance, Skill, Theme and Engagement, so every point on the ladder can be traced back to the glass.'),
            ('People’s Choice Awards', 'Alongside the Championship, the public will vote for the bars and bartenders they love most. Voting details to come in a later issue.'),
            ('The Connoisseurs Club opens', 'Membership for people who like to know what’s in the glass: entry to all eight rounds, a cocktail on us every round and members’ nights.')]
    hot = ['Monday nights at the Championship', 'Hosting your own home cocktail party', 'Travelling to new bars',
           'Low and no serves done properly', 'The onset of winter (lots of warm bars)', 'Bitter aperitifs before dinner', 'Small-batch Australian gin', 'Bartenders doing guest shifts']
    items = ''.join(f'<div class="nh2-i"><h3>{t}</h3><p>{p}</p></div>' for t, p in news)
    hots = ''.join(f'<div class="hot-i">{x}</div>' for x in hot)
    stats = ''.join(f'<div><b>{a}</b><span>{b}</span></div>' for a, b in [('12', 'Founding teams'), ('8', 'Monday rounds'), ('6', 'Weeks between rounds'), ('5', 'TASTE criteria')])
    return f'''<div class="bleedimg navyfill"></div><div class="safe onnavy n3 n3nav">{head('News', 'Giving you the facts and nothing but the facts', light=True)}
<div class="n3-lead">{photo('team3','n3-lead-img',fixed=True)}<div class="n3-lead-shade"></div>
<div class="n3-lead-t"><span class="n3-tag">Lead story</span><h2>The Founding 12 take shape</h2><p>Invitations have gone to bars across Melbourne for twelve places in the inaugural Championship. Application dates go to registered teams first. Contact {REGISTER}.</p></div></div>
<div class="n3-stats">{stats}</div>
<div class="n3-body">
<div class="n3-news">{items}</div>
<div class="nh2-hot n3-hot">{photo('crowd','nh2-bg',fixed=True)}<div class="nh2-tint"></div><div class="hot-h">What’s <i>Hot</i></div>{hots}</div>
</div>
<div class="nh2-sub"><div><b>Never miss an issue</b><span>Subscribe free and get every DrinkHQ Magazine in your inbox before each round, plus first word on tickets and tastings.</span></div><div class="nh2-btn">Subscribe free<small>drinkhqmedia.com/contact</small></div></div>
</div>{folio(n)}'''

def round1_full(n):
    fx = ''.join(f'<div class="r2-fx"><span><i>{2*i+1:02d}</i>[Team name]</span><em>VS</em><span>[Team name]<i>{2*i+2:02d}</i></span></div>' for i in range(6))
    night = [('Doors 5 pm', 'The bar opens, the crowd settles in.'),
             ('Six match-ups from 7 pm', 'Individual match, 7 min, one bartender per team. Team match, 7 min, the whole team. Counts double.'),
             ('Five judges, one crowd', 'Every drink scored on TASTE. The crowd votes People’s Choice.'),
             ('Done by 11 pm', 'Points go on the season ladder, published after each round.')]
    nights = ''.join(f'<div class="r3-n"><i>{k+1}</i><div><b>{t}</b><span>{d}</span></div></div>' for k, (t, d) in enumerate(night))
    pics = ''.join(f'<div class="t10b-pic">{photo(k,fixed=True)}<div class="t10b-pcap"><b>{t}</b>{d}</div></div>' for k, t, d in [('pinkmart', 'On screen', 'A cocktail that plays a part'), ('martini', 'In the glass', 'A scene you can taste'), ('stir', 'Behind the bar', 'The craft in every pour')])
    taste = ''.join(f'<div class="r3-t"><b>{l}</b><span>{w}%</span><i>{name.split()[0]}</i></div>' for l, name, w, _ in TASTE)
    return f'''{frame()}<div class="safe r3">
<div class="r3-hero">{photo('tie','r3-hero-img',fixed=True)}<div class="r3-shade"></div>
<div class="r3-ht"><div class="kicker">Round 1 · Season 2027–28</div><h1>Cinematic <i>Cocktails</i></h1><p>Iconic films, captured in a glass.</p></div>
<div class="r2-date r3-date"><b>MON 21 JUNE 2027</b><span>7:00 PM · Venue to be announced</span></div></div>
<div class="r3-brief"><span class="r3-tag">The brief</span><p>Capture a scene, a character or a moment in every sip. Each team creates a cocktail inspired by a film, and the judges score how clearly the drink tells that story: in the glass, the garnish and the presentation. As in every round, there is a Mystery Box element.</p></div>
<div class="r3-pics">{pics}</div>
<div class="r3-mid">
<div class="r3-fix"><div class="r3-lab">Match fixture {ph('AFTER TEAM SELECTION')}</div>{fx}</div>
<div class="r3-night"><div class="r3-lab">How the night runs</div>{nights}</div>
</div>
<div class="r3-taste"><span class="r3-lab">Scored on TASTE</span>{taste}</div>
<div class="r3-tix"><div><b>Be in the room</b><span>General Admission from $15 and Food &amp; Drink tables for five. Sales open soon.</span></div><div class="nh2-btn">Book tickets<small>{WEBSITE}</small></div></div>
</div>{folio(n)}'''

def team_focus(n):
    def col(k, num):
        facts = ''.join(f'<div><i>{a}</i><b>{b}</b></div>' for a, b in [('Captain', '[Name]'), ('Team', '[Names, up to four]'), ('Feature', '[Feature]'), ('Hours', '[Days, hours]')])
        return f'''<div class="tg-card"><div class="tg-ph">{photo(k,'tg-img',fixed=True)}<div class="tg-shade"></div><span class="ph imgtag" contenteditable="false">PLACEHOLDER IMAGE</span>
<div class="tg-name"><span>Team {num:02d}</span>[Team name]</div></div>
<div class="tg-body"><div class="tg-addr">[Bar name] · [Venue address], Melbourne · Ph: [phone]</div>
<p>[Team profile, about 100 words. Who they are, where they pour, how the team came together, their style behind the bar, the drink they’re known for, what the regulars say about them and how they plan to win the season.]</p>
<div class="tg-facts">{facts}</div>
<div class="tg-sig"><div><i>Signature serve</i><b>[Cocktail name]</b><span>[Two-line description of the drink]</span></div><div class="tg-qr">QR {ph()}</div></div>
</div></div>'''
    return f'''<div class="bleedimg navyfill"></div><div class="safe onnavy tg">
<div class="s2-hero tg-hero">{photo('team4','s2-hero-img',fixed=True)}<div class="s2-hshade"></div>
<div class="s2-ht"><div class="kicker">[ Teams ]</div><h1>Team <i>Focus</i></h1><p>Meet the bars behind the bartenders.</p></div>
<div class="r2-date tg-badge"><b>AFTER TEAM SELECTION</b><span>Names and profiles to come</span></div></div>
<div class="tg2">{col('barA', 1)}{col('barC', 2)}</div>
<div class="tg-foot"><b>Two teams every issue.</b> By the Grand Final you’ll have met all twelve. Round 1 fixture on page 08.</div>
</div>{folio(n)}'''

def news_v4(n):
    news = [('team3', 'The Founding 12 take shape', f'Invitations have gone to bars across Melbourne for twelve places in the inaugural Championship. Application dates go to registered teams first.'),
            (None, 'Season 2027–28 confirmed', 'Eight Monday-night rounds, six weeks apart, from 21 June 2027 to 10 April 2028. The Grand Final date will be announced later in the season.'),
            (None, 'Every drink, scored on TASTE', 'Each cocktail is judged on Taste, Appearance, Skill, Theme and Engagement, so every point on the ladder can be traced back to the glass.'),
            ('mint', 'Get the taste of it', f'DrinkHQ will run its own tasting series, with experts sharing what they know with the willing few. Register your interest through the contacts on page 3.'),
            ('bw', 'People’s Choice Awards', 'Alongside the Championship, the public will vote for the bars and bartenders they love most. Voting details to come in a later issue.'),
            (None, 'The Connoisseurs Club opens', 'Membership for people who like to know what’s in the glass: entry to all eight rounds, a cocktail on us every round and members’ nights.')]
    hot = ['Monday nights at the Championship', 'Hosting your own home cocktail party', 'Travelling to new bars',
           'Low and no serves done properly', 'Bitter aperitifs before dinner', 'Small-batch Australian gin', 'Bartenders doing guest shifts']
    items = ''.join(f'<div class="nh2-i n4-i">{photo(k,"n4-img",fixed=True) if k else ""}<h3>{t}</h3><p>{p}</p></div>' for k, t, p in news)
    hots = ''.join(f'<div class="hot-i">{x}</div>' for x in hot)
    stats = ''.join(f'<div><b>{a}</b><span>{b}</span></div>' for a, b in [('12', 'Founding teams'), ('8', 'Monday rounds'), ('6', 'Weeks between rounds'), ('5', 'TASTE criteria')])
    return f'''{frame()}<div class="safe n3 n4 lite">
<div class="s2-hero n4-hero">{photo('team2','s2-hero-img',fixed=True)}<div class="s2-hshade"></div>
<div class="s2-ht"><div class="kicker">[ News ] · Issue 01</div><h1>News <i>&amp; What’s Hot</i></h1><p>Giving you the facts and nothing but the facts.</p></div></div>
<div class="n3-stats">{stats}</div>
<div class="n3-body"><div class="n3-news n4-news">{items}</div>
<div class="nh2-hot n3-hot">{photo('crowd','nh2-bg',fixed=True)}<div class="nh2-tint"></div><div class="hot-h">What’s <i>Hot</i></div>{hots}</div></div>
<div class="nh2-sub"><div><b>Never miss an issue</b><span>Subscribe free and get every DrinkHQ Magazine in your inbox before each round, plus first word on tickets and tastings.</span></div><div class="nh2-btn">Subscribe free<small>drinkhqmedia.com/contact</small></div></div>
</div>{folio(n)}'''

def above_board_review(n):
    paras = ['Look for a laneway, not a sign. Above Board sits up a flight of stairs at the back of 306 Smith Street, reached from Chopper Lane off Perry Street, or through the unmarked back door of BeerMash downstairs when it’s open. Find the door and you’re in one of the smallest serious cocktail bars in Melbourne.',
             'The room is built around a single island bar with twelve stools, plus two banquettes for two behind it. That’s sixteen seats, and no corner tables or booths to hide in. Every guest sits within arm’s reach of the bartender, which is exactly the point.',
             'Behind that bar is owner Hayden Lambert, who learned his trade at Melbourne’s Bar Americano and Belfast’s Merchant Hotel. He runs the place with partners Manu Potoi and Cornelis Ribbe, and he runs it his way: a tight list of about 25 drinks, split between house signatures and reworked classics.',
             'The classics are where to start. The Negroni, Old Fashioned, Manhattan and Martini are all on the list and all made with care. Then let the signatures take you somewhere new. Don’t expect him to make whatever you ask for. Do expect whatever he makes to be worth it.',
             'There are no bookings, and with sixteen seats that makes timing everything. Go early, go small, and leave the big group for somewhere else. It is a bar for sitting up, paying attention and drinking very well.']
    body = ''.join(f'<p>{p}</p>' for p in paras)
    facts = ''.join(f'<div><i>{a}</i><b>{b}</b></div>' for a, b in [('Type', 'Hidden cocktail bar'), ('Seats', '16, around an island bar'), ('The list', 'About 25: signatures &amp; classics'), ('Bookings', 'None. Walk in early')])
    return f'''{frame()}<div class="vr-photo">{photo('stir','vr-img',fixed=True)}<div class="vr-pshade"></div><span class="ph imgtag" contenteditable="false">ILLUSTRATIVE IMAGE</span>
<div class="vr-stamp">Recommended</div><div class="vr-cap"><b>DrinkHQ recommends</b>Start with a classic, then hand the next one to the bartender.</div></div>
<div class="safe vr lite"><div class="kicker">[ Bar Review ]</div><h1 class="vr-h">Above Board</h1>
<div class="vr-addr">306 Smith Street (via Chopper Lane), Collingwood</div>
<p class="vr-lede">Sixteen seats, one island bar and a bartender who won’t make just anything: Collingwood’s hidden room for serious drinking.</p>
<div class="vr-body">{body}</div>
<div class="vr-facts">{facts}</div>
<p class="vr-note">Details checked October 2026. Hours change, so check before you go. Photo is illustrative, not the venue.</p>
</div>{folio(n)}'''

def venu_review(n):
    paras = ['Venu doesn’t subscribe to the traditional school of thought when it comes to exclusive South Side Dublin drinking establishments. It hasn’t the need to advertise itself with garish neon interiors, faux Parisian terraces or snooty doormen. A simple, embossed glass door and a plain white lobby are the only clues to Venu’s existence.',
             'Located two storeys underground, you might be forgiven for thinking you were about to enter a Cold War bunker. But no: Venu is bright and airy, with a touch of New York chic for added effect. Muted tones are highlighted ever so slightly by coloured spotlights, high ceilings and large mirrors.',
             'Venu isn’t strictly a bar but a brasserie cum cocktail lounge. Ordinarily you’d pass through the bar on your way to the dining area, but the management, nice folk that they are, are only too happy to entertain you if you only want to pop in for a drink or two. Pull up a stool and let the bartender regale you with witty anecdotes about high shelves and celebrity hijinks.',
             'No mucking about here: the cocktail menu has been devised to complement the food menu, and even has a selection of before-dinner cocktails in case your taste buds need loosening. Venu also claims the best Mojito in Dublin, a tall claim but one we were only too glad to put to the test. It passed with flying colours.',
             'Venu is an establishment in its infancy, yet it has gained the kind of reputation usually reserved for the longer-standing bastions of Dublin’s dining circle. In its short life it has become a favourite with rock bands, Miss Worlds and the odd rugby player. Here’s hoping it keeps delighting the critics for years to come.']
    body = ''.join(f'<p>{p}</p>' for p in paras)
    facts = ''.join(f'<div><i>{a}</i><b>{b}</b></div>' for a, b in [('Type', 'Brasserie &amp; cocktail lounge'), ('Feature', 'Two storeys underground'), ('Before dinner', 'Aperitif cocktail list'), ('Crowd', 'Rock bands &amp; Miss Worlds')])
    return f'''{frame()}<div class="vr-photo">{photo('rv_venu','vr-img',fixed=True)}<div class="vr-pshade"></div>
<div class="vr-stamp">Recommended</div><div class="vr-cap"><b>Drink recommends</b>The Mojito, said to be the best in Dublin.</div></div>
<div class="safe vr lite"><div class="kicker">[ Bar Review ]</div><h1 class="vr-h">Venu</h1>
<div class="vr-addr">Annes Lane, Dublin 2 · Ph: 01 670 6755</div>{ARCH}
<p class="vr-lede">A plain glass door, a white lobby and two flights down: Dublin’s quietest entrance hides one of its brightest rooms.</p>
<div class="vr-body">{body}</div>
<div class="vr-facts">{facts}</div>
<p class="vr-note">Reproduced from Drink magazine (Ireland, 2007) as layout copy; venue details will have changed.</p>
</div>{folio(n)}'''

def _pol(k, num, rot):
    return f'<div class="wpol" style="transform:rotate({rot}deg)">{photo(k,"wpol-img",fixed=True)}<span>{num}</span></div>'

def _wspons(cls=''):
    return f'<div class="w-spons {cls}"><span>Brought to you by</span><div class="w-logo">SPONSORSHIP AVAILABLE</div><em>partner@thedrinkhqexperience.com.au</em></div>'

def wwyln_a(n):
    rots = [-2, 1.5, -1, 2, -1.5, 1, -1, 2, -2]
    g = ''.join(_pol(f'ww{i:02d}', i + 1, rots[i]) for i in range(9))
    return f'''<div class="bleedimg navyfill"></div><div class="safe onnavy wwp">
<div class="s2-hero ww-hero">{photo('ww09','s2-hero-img',fixed=True)}<div class="s2-hshade"></div>
<div class="s2-ht"><div class="kicker">[ WWYLN ] · Round-night photos</div><h1>Where were you <i>last night?</i></h1><p>The beautiful people, the big nights, the morning after.</p></div>
{_wspons('top')}</div>
<div class="ww-grid3">{g}</div>
<p class="ww-note">1–20. Drink magazine nights, from the archive, to be replaced with Season 2027–28 round-night photos. {ph('ARCHIVE PHOTOS')}</p>
</div>{folio(n)}'''

def wwyln_b(n):
    big = ''.join(_pol(f'ww{i:02d}', i + 1, r) for i, r in ((9, -1.5), (10, 2)))
    rots = [1, -2, 1.5, -1, 2, -1.5, 1, -1, 2]
    small = ''.join(_pol(f'ww{11 + j:02d}', 12 + j, rots[j]) for j in range(9))
    return f'''<div class="bleedimg navyfill"></div><div class="safe onnavy wwp">
<div class="ww-big">{big}</div>
<div class="ww-grid3 sm">{small}</div>
<div class="ww-cta"><div><b>Want to appear here with the beautiful people?</b><span>Tag DrinkHQ in your photos from any round night, or scan the code to send them in. Only photos of people who have agreed to appear are published.</span></div><div class="ww-qr"><div>{_qr('https://drinkhqmedia.com/contribute/#photos')}</div><em>Send photos</em></div>{_wspons('cta')}</div>
</div>{folio(n)}'''

def martini_history(n):
    paras = ['So how do you like your Martini? “Shaken, not stirred” by any chance? We’ve all said it at some stage, in our best dodgy Sean Connery accents. But what is the best way to drink it? Should we follow Somerset Maugham, who said martinis “should always be stirred, not shaken, so that the molecules lie sensuously one on top of the other”? And who came up with this mix of gin and vermouth in the first place?',
             'The Martini is one of the longest-established cocktails, and most accounts trace it to a drink called the Martinez. The story goes that a San Francisco bartender was asked to make something special for a gold miner heading to the town of Martinez, 40 miles east, in hope of striking it rich. History doesn’t record how the miner fared, but bartender Jerry Thomas certainly struck gold with his mix of vermouth, gin, bitters and maraschino.',
             'Another account credits one Julio Richelieu, who named the drink after his home town around 1870, allegedly inspired when a miner plonked a small bag of gold on the bar by way of incentive.',
             'As for how Martinez became Martini, the general view is that it came from the Italian Martini sweet vermouth used to make it. If you’d prefer a less prosaic answer, some say it was named after the Martini-Henry rifle used by the British army in the late 19th century, as both had something of a kick.',
             'Prohibition in 1920s America helped it along. Whiskey had been the spirit of choice, but gin was easier and cheaper to make and needed no ageing, so a gin cocktail like the Martini was bound to thrive in the speakeasies.',
             'Its place in popular culture did the rest. Beyond Bond and Maugham, its devotees included F. Scott Fitzgerald, Roosevelt, Hemingway, Capote, Hitchcock and Churchill. Hemingway’s “Montgomery” ran 15 parts gin to one of vermouth, said to be the odds Field Marshal Montgomery liked before a battle. Churchill skipped the vermouth entirely: a cold glass of gin and a nod in the direction of Italy.']
    body = ''.join(f'<p>{p}</p>' for p in paras)
    return f'''{frame()}<div class="safe mh lite">
<div class="s2-hero mh-hero">{photo('mt_olive','s2-hero-img',fixed=True)}<div class="s2-hshade"></div>
<div class="s2-ht"><div class="kicker">[ History of… ]</div><h1>The <i>Martini</i></h1><p>Shaken or stirred, and who poured the first one.</p></div></div>
<div class="mh-body">{body}</div>
<div class="mh-quote">“One Martini is all right. Two are too many, and three are not enough.”<i>James Thurber</i></div>
<div class="mh-recipes"><div><b>The James Bond</b><span>3 measures gin</span><span>1 measure vodka</span><span>½ measure Kina Lillet</span><span>Large slice of lemon peel to garnish. Shaken, naturally.</span></div>
<div><b>The Original</b><span>2½ oz (75 ml) gin</span><span>½ oz (15 ml) dry vermouth</span><span>Green olive or lemon twist to garnish</span><span>Shake or stir: the choice is yours.</span></div></div>
<p class="vr-note">Adapted from Drink magazine (Ireland, 2007).</p>
</div>{folio(n)}'''

def mixology_x(n):
    R = [('mx_pink', 'Pink Champagne', ['30 ml X-Rated Fusion', 'Topped with chilled Moët', 'Fresh raspberries to garnish'], 'Build in a flute: liqueur first, then top slowly with champagne.'),
         ('mx_sour', 'Fusion Sour', ['30 ml X-Rated Fusion', '20 ml Cointreau', 'Fresh lime and lemon'], 'Muddle the citrus, add the spirits, shake hard. Garnish with a lime wheel.'),
         ('mx_straw', 'Strawberry Fusion', ['45 ml X-Rated Fusion', '30 ml Ketel One vodka', '15 ml strawberry liqueur', '4 fresh strawberries'], 'Blend everything with crushed ice until smooth.'),
         ('mx_apple', 'X-Rated Apple', ['30 ml Ketel One vodka', '20 ml X-Rated Fusion', '20 ml Midori', 'Apple, cranberry and lime juice'], 'Shake the spirits with the juices and strain over ice.')]
    cards = ''.join(f'''<div class="mx-card"><div class="mx-ph">{photo(k,'mx-img',fixed=True)}<i>{i+1:02d}</i></div><div class="mx-b"><h3>{t}</h3>{''.join(f"<span>{x}</span>" for x in ing)}<p>{m}</p></div></div>''' for i, (k, t, ing, m) in enumerate(R))
    return f'''{frame()}<div class="safe mx">
<div class="s2-hero mx-hero">{photo('mx_barman2','s2-hero-img',fixed=True)}<div class="s2-hshade"></div>
<div class="s2-ht"><div class="kicker">[ Mixology ] · Featuring X-Rated Fusion</div><h1>Drink <i>Pink</i></h1><p>Four serves from the bar at The Morgan, Dublin.</p></div>
<div class="mx-barman"><b>Barman</b><span>Peter O’Connor</span><em>The Morgan Bar, Temple Bar</em></div></div>
<div class="mx-grid">{cards}</div>
<div class="mx-brand">{photo('mx_xbottle','mx-bottle',fixed=True)}<div><b>X-Rated Fusion Liqueur</b><p>Ultra-premium French vodka and blood oranges from Provence, mingled with mango and passion fruit from Brazil. Pure fruit juices and vodka, fused in a secret process into the first fusion liqueur.</p></div><div class="sample-chip">SAMPLE · ARCHIVE FEATURE</div></div>
<p class="vr-note">Recipes adapted from Drink magazine (Ireland, 2007); measures converted to ml. Please enjoy responsibly.</p>
</div>{folio(n)}'''

def _cspons(cls=''):
    return f'<div class="w-spons {cls}"><span>Sponsored by</span><div class="w-logo">SPONSORSHIP AVAILABLE</div><em>partner@thedrinkhqexperience.com.au</em></div>'

def champ_season(n):
    pics = ['tie', 'stir', 'negroni', 'pinkmart', 'barrels', 'cane', 'mint', 'bottles']
    tiles = ''.join(f'<div class="cs-t{" on" if r == "01" else ""}">{photo(k,"cs-timg",fixed=True)}<div class="cs-tsh"></div><b>R{r}</b><div class="cs-tt"><span>{d.replace("Mon ", "")}</span><i>{t}</i></div></div>' for (r, d, t, s), k in zip(ROUNDS, pics))
    return f'''{frame()}<div class="safe cs lite">
<div class="s2-hero cs-hero">{photo('b1806','s2-hero-img',fixed=True)}<div class="s2-hshade"></div>
<div class="s2-ht"><div class="kicker">[ The Championship ] · Season 2027–28</div><h1>Eight Mondays, <i>one champion</i></h1><p>Twelve bar teams. Up to 500 guests a night. Doors 5 pm, judging from 7 pm.</p></div>
{_cspons('top')}</div>
<div class="cs-tiles">{tiles}</div>
<div class="cs-gf"><b>GF</b><div><span>Date to be announced</span><i>The Grand Final</i><em>The top six on the ladder play off for the title.</em></div></div>
<p class="vr-note">Round themes subject to change. Venues to be announced.</p>
</div>{folio(n)}'''

def _club_qr(i):
    import segno
    slug = ('trailblazer', 'connoisseur', 'luminary')[i]
    q = segno.make(f'https://connoisseursclub.com.au/join/{slug}', error='h', micro=False)
    svg = q.svg_inline(scale=1, border=2, dark='#0E1F4D', light='#ffffff', omitsize=True)
    w, _ = q.symbol_size(scale=1, border=2)
    d = w * 0.26; x = (w - d) / 2
    logo = f'<circle cx="{w/2}" cy="{w/2}" r="{d/2+0.6}" fill="#fff"/><image href="{img('club_crest.png')}" x="{x}" y="{x}" width="{d}" height="{d}"/>'
    return svg.replace('</svg>', logo + '</svg>')

def _qr(url, border=2):
    import segno
    q = segno.make(url, error='m', micro=False)
    return q.svg_inline(scale=1, border=border, dark='#0E1F4D', light='#ffffff', omitsize=True)

def champ_tickets(n):
    tix = [('General Admission', '$15', 'advance · $25 at the door', 'Entry to one round night: the matches, the judging and the bar.'),
           ('Food &amp; Drink Package', '$400', 'table of five · $80 a head', 'A reserved table for five with food and drink included.')]
    tc = ''.join(f'<div class="ct-c"><b>{a}</b><strong>{p}</strong><span>{u}</span><p>{d}</p></div>' for a, p, u, d in tix) + '<div class="ct-c club"><b>Coming to every round?</b><strong>Join</strong><span>the Connoisseurs Club</span><p>Every membership includes entry to all eight rounds. See below.</p></div>'
    tiers = [('Taste Trailblazer', '$239', ['All 8 rounds, general entry', 'A cocktail on us every round', 'Members’ lounge on round nights', 'Digital magazine and recipe book', 'Members-only community', '5% off merchandise']),
             ('Cocktail Connoisseur', '$359', ['Everything in Trailblazer', 'Priority entry on round nights', 'People’s Choice vote every round', 'Grand Final People’s Choice vote', 'Quarterly masterclasses', 'Expanded recipe collection', '10% off merchandise']),
             ('Liquid Luminary', '$549', ['Everything in Connoisseur', 'VIP entry and meet-and-greet', 'Pre-event tasting', 'A guest ticket and numbered pin', 'Behind-the-scenes tour', 'Live Q&amp;A, quarterly', '15% off merchandise'])]
    cc = ''.join(f'<div class="cc-t{" top" if i == 2 else ""}"><b>{t}</b><strong>{p}<small> a year</small></strong>{"".join(f"<span>{x}</span>" for x in xs)}<div class="cc-qr"><div>{_club_qr(i)}</div><em>Scan to join<br><small>{("Trailblazer","Connoisseur","Luminary")[i]}</small></em></div></div>' for i, (t, p, xs) in enumerate(tiers))
    return f'''{frame()}<div class="safe cs lite">
<div class="cs-h"><div><div class="kicker">[ Be in the room ]</div><h2>Tickets</h2></div><div class="cs-soon">Sales open soon · {WEBSITE}</div></div>
<div class="ct-grid">{tc}</div>
<div class="cs-h"><div class="cs-hl"><img class="cc-crest" src="{img('club_crest.png')}" alt="DrinkHQ Connoisseurs Club"><div><div class="kicker">[ Connoisseurs Club ]</div><h2>Join the Club</h2></div></div>{_cspons('mini')}</div>
<div class="cc-every"><b>Every member gets</b><span>Entry to all 8 rounds</span><span>A cocktail on us each round</span><span>DrinkHQ Magazine and the recipe book</span></div>
<div class="cc-grid">{cc}</div>
<div class="cc-photo">{photo('edv','cc-img',fixed=True)}<div class="cc-shade"></div><p>Members’ nights, masterclasses and the best seat in the room.</p></div>
<div class="cs-cta"><b>Billed yearly, renews automatically.</b> Prices include GST. 18+ only. Join at connoisseursclub.com.au</div>
</div>{folio(n)}'''

def round1_v2(n):
    fx = ''.join(f'<div class="r2-fx"><span><i>{2*i+1:02d}</i>[Team name]</span><em>VS</em><span>[Team name]<i>{2*i+2:02d}</i></span></div>' for i in range(6))
    rows = ''.join(f'<tr class="{"q" if i < 6 else ""}"><td>{i+1}</td><td>Team {i+1:02d} · [Team name / venue]</td><td>–</td><td>–</td><td>–</td><td>–</td><td>–</td></tr>' for i in range(12))
    return f'''{frame()}<div class="safe r2">
<div class="r2-hero">{photo('tie','r2-hero-img',fixed=True)}<div class="r2-shade"></div>
<div class="r2-ht"><div class="kicker">Round 1 · Season 2027–28</div><h1>Cinematic <i>Cocktails</i></h1><p>Iconic films, captured in a glass.</p></div>
<div class="r2-date"><b>MON 21 JUNE 2027</b><span>7:00 PM · Venue TBA</span></div></div>
<div class="r2-mid"><div class="r2-fix"><div class="label">Match fixture {ph('AFTER TEAM SELECTION')}</div>{fx}</div>
<div class="r2-theme"><div class="r2-strip">{photo('pinkmart','r2-s',fixed=True)}{photo('martini','r2-s',fixed=True)}{photo('stir','r2-s',fixed=True)}</div>
<b>The brief</b><p>Capture a scene, a character or a moment in every sip. Judged on how clearly the drink tells its film’s story, in the glass, the garnish and the presentation.</p>
<div class="r2-tix">Tickets from $15 · {WEBSITE}</div></div></div>
<div class="r2-lh"><div><div class="kicker">Season 2027–28</div><h2 class="rl-h2">Championship <i>Ladder</i></h2></div>
<div class="r2-steps"><span>8 rounds</span><em>→</em><span>Top 6 to the Grand Final</span><em>→</em><span class="gd">Champions</span></div></div>
<table class="ladder"><thead><tr><th>#</th><th>Team</th><th>MP</th><th>W</th><th>L</th><th>PF</th><th>Pts</th></tr></thead><tbody>{rows}</tbody></table>
<p class="note">The ladder opens after Round 1; gold rows mark Grand Final places. Round themes subject to change.</p>
</div>{folio(n)}'''

def plan16():
    # 9 full ad pages + 2 strips; Championship pages replace the archive features (24 Oct 2026)
    P = {}
    P[1] = ('cover', lambda n: cover_issue(n, 8, [(8, 'ROUND 1', '<b>Cinematic <i>Cocktails</i></b>, fixture and the ladder'), (6, 'THE ART OF COCKTAIL MASTERY', 'What to expect, and TASTE explained'), (10, 'THE TEAMS', 'Meet the Founding 12'), (4, 'NEWS', 'What’s hot, and the facts'), (13, 'BARS IN BRIEF', 'Three Melbourne bars, rated'), (3, 'WELCOME', 'A word from the source')]))
    P[2] = ('ad', lambda n: page_ad(n, 'AD-02', 'Inside front cover · facing Contents', 'ad_patron'))
    P[3] = ('ed', lambda n: contents_mast(n, [(4, 'News &amp; What’s Hot', 'Giving you the facts'), (6, 'The Art of Cocktail Mastery', 'Match overview &amp; TASTE'), (8, 'Round 1 · Cinematic Cocktails', 'Fixture &amp; Championship ladder'), (10, 'Teams', 'Meet the Founding 12 · the season'), (10, 'Connoisseurs Club', 'Three ways to join'), (13, 'Bars in Brief', 'A pinch of pubs, a dash of bars')],
        [('pour3', 6, 'The Art'), ('tie', 8, 'Round 1'), ('bib_gb', 13, 'Bars in Brief')]))
    P[4] = ('ed', lambda n: news_hot(n, 'strip_nash_c'))
    P[5] = ('ad', lambda n: page_ad(n, 'AD-05', 'Full page · right hand · facing News', 'ad_ketel'))
    P[6] = ('ed', art_match)
    P[7] = ('ad', lambda n: page_ad(n, 'AD-07', 'Full page · right hand · facing The Art of Cocktail Mastery', 'ad_chambord'))
    P[8] = ('ed', round1_ladder)
    P[9] = ('ad', lambda n: page_ad(n, 'AD-09', 'Full page · right hand · facing Round 1', 'ad_social'))
    P[10] = ('ed', teams_club)
    P[11] = ('ad', lambda n: page_ad(n, 'AD-11', 'Full page · right hand, facing Teams', 'ad_frangelico'))
    P[12] = ('ad', lambda n: page_ad(n, 'AD-12', 'Full page · left hand, facing Bars in Brief', 'ad_vibe'))
    P[13] = ('ed', lambda n: bars_brief(n, BARS16, 'strip_tajga_c'))
    P[14] = ('ad', lambda n: page_ad(n, 'AD-14', 'Full page · left hand', 'ad_haze'))
    P[15] = ('ad', lambda n: page_ad(n, 'AD-15', 'Inside back cover', 'ad_epicurean'))
    P[16] = ('ad', lambda n: page_ad(n, 'AD-16', 'Outside back cover', 'ad_illusion'))
    return P

def plan32():
    # 17 full ad pages + 3 strips + 1 half = 18.3 of 32 pp (57%) — Traveller page added Oct 2026
    P = {}
    P[1] = ('cover', lambda n: cover_issue(n, 8, [(16, 'TEAM FOCUS', '<b>Meet the <i>Founding 12</i></b>'), (8, 'ROUND 1', 'Cinematic Cocktails: the brief and the night'), (20, 'BARS IN BRIEF', 'Three Melbourne bars, rated'), (22, 'SPIRIT EXPLAINED', 'Viva Cachaça! Brazil’s national spirit'), (27, 'TRAVELLER', 'Caretaker’s Cottage, Melbourne: a bar worth the trip')]))
    P[2] = ('ad', lambda n: page_ad(n, 'AD-02', 'Inside front cover · facing Contents', 'ad_patron'))
    ct = [(4, 'News &amp; What’s Hot', 'Keeping you in the know'), (6, 'The Art of Cocktail Mastery', 'The format &amp; how TASTE works'), (8, 'Round 1 · Cinematic Cocktails', 'The brief, fixture &amp; the night'), (10, 'Shaken &amp; Stirred', 'All the info you need'), (12, 'Top 10 &amp; Bar Lingo', 'Movie cocktails, A to Z of the bar'), (14, 'Review', 'Five new on the back bar'), (16, 'Team Focus', 'Two of the Founding 12'), (18, 'Bar Review', 'Above Board, Collingwood'), (20, 'Bars in Brief', 'Three bars, rated'), (22, 'Spirit Explained', 'Viva Cachaça!'), (24, 'Mixology', 'Drink Pink: four serves'), (26, 'History of the Martini', 'Shaken or stirred'), (27, 'Traveller', 'Caretaker’s Cottage'), (28, 'The Championship', 'Season, tickets &amp; the Club'), (30, 'Where were you last night?', 'Two pages of the beautiful people')]
    P[3] = ('ed', lambda n: contents_mast(n, ct, short=True, tiles=[('tie', 8, 'Round 1'), ('bib_lux', 20, 'Bars in Brief'), ('limes', 22, 'Cachaça')]))
    P[4] = ('ed', news_v4)
    P[5] = ('ad', lambda n: page_ad(n, 'AD-05', 'Full page · right hand · facing News', 'ad_fidels'))
    P[6] = ('ed', art_feature)
    P[7] = ('ad', lambda n: page_ad(n, 'AD-07', 'Full page · right hand, facing The Art of Cocktail Mastery', 'ad_cooleswan'))
    P[8] = ('ed', round1_full)
    P[9] = ('ad', lambda n: page_ad(n, 'AD-09', 'Full page · right hand, facing Round 1', 'ad_zimmer'))
    P[10] = ('ed', shaken_v2)
    P[11] = ('ad', lambda n: page_ad(n, 'AD-11', 'Full page · right hand, facing Shaken & Stirred', 'ad_ketelthanks'))
    P[12] = ('ed', top10)
    P[13] = ('ad', lambda n: page_ad(n, 'AD-13', 'Full page · right hand, facing Top 10', 'ad_beach'))
    P[14] = ('ed', lambda n: review2(n, 'ad_ketel'))
    P[15] = ('ad', lambda n: page_ad(n, 'AD-15', 'Full page · right hand, facing Review', 'ad_mickeyfinn'))
    P[16] = ('ed', team_focus)
    P[17] = ('ad', lambda n: page_ad(n, 'AD-17', 'Centre spread · right hand', 'ad_chambord'))
    P[18] = ('ed', above_board_review)
    P[19] = ('ad', lambda n: page_ad(n, 'AD-19', 'Full page · right hand, facing Bar Review', 'ad_haze'))
    P[20] = ('ed', lambda n: bars_brief(n, BARS32, None, small=True))
    P[21] = ('ad', lambda n: page_ad(n, 'AD-21', 'Full page · right hand, facing Bars in Brief', 'ad_frangelico2'))
    P[22] = ('ed', cachaca_a)
    P[23] = ('ed', cachaca_b)
    P[24] = ('ed', mixology_x)
    P[25] = ('ad', lambda n: page_ad(n, 'AD-25', 'Full page · right hand, facing Mixology', 'ad_matusalem'))
    P[26] = ('ed', martini_history)
    P[27] = ('ed', traveller_caretakers)
    P[28] = ('ed', champ_season)
    P[29] = ('ed', champ_tickets)
    P[30] = ('ed', wwyln_a)
    P[31] = ('ed', wwyln_b)
    P[32] = ('ad', lambda n: page_ad(n, 'AD-32', 'Outside back cover', 'ad_illusion'))
    return P


# ---------------------------------------------------------------- css / shell
CSS = open(os.path.join(HERE, 'style.css')).read()
JS = open(os.path.join(HERE, 'editor.js')).read()


import re as _re
_SKIP = ('.folio', '.sample-tag', '.ad-', '.ad ', '.ad{', '.toolbar', '.help', '.ph', '.imgtag', 'body.editing', '.sp-label', '.spread')
def css_min(css, minpt=7.5):
    def rule(m):
        sel, body = m.group(1), m.group(2)
        if '@' in sel or any(k in sel for k in _SKIP):
            return m.group(0)
        def fix(mm):
            return f'{minpt:g}pt' if float(mm.group(1)) < minpt else mm.group(0)
        return sel + '{' + _re.sub(r'(?<![\d.])(\d+(?:\.\d+)?)pt', fix, body) + '}'
    return _re.sub(r'([^{}]+)\{([^{}]*)\}', rule, css)

def build(name, P, pages, out):
    USED.clear(); total = len(P)
    assert sorted(P) == list(range(1, pages + 1)), sorted(P)
    html_pages = {}
    for n in range(1, pages + 1):
        kind, fn = P[n]
        side = 'recto' if n % 2 == 1 else 'verso'
        html_pages[n] = f'<div class="page {kind} {side}" data-page="{n}">{fn(n)}<div class="trimline"></div></div>'
    spreads = [[1]] + [[i, i + 1] for i in range(2, pages, 2)] + [[pages]]
    sp = ''
    for s in spreads:
        lab = ' – '.join(f'{x:02d}' for x in s)
        inner = ''.join(f'<div class="sheet"><div class="crop tl"></div><div class="crop tr"></div><div class="crop bl"></div><div class="crop br"></div><div class="clip">{html_pages[x]}</div></div>' for x in s)
        cls = 'single-r' if s == [1] else ('single-l' if s == [pages] else '')
        sp += f'<div class="spread {cls}"><div class="sp-label">Pages {lab}</div><div class="pages">{inner}</div></div>'
    title = f'DrinkHQ Magazine Issue 01 {pages}pp'
    html = f'''<!doctype html><html lang="en-AU"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>{font_faces()}
{css_min(CSS) if name == '32' else CSS}</style></head><body>
<div class="toolbar" contenteditable="false"><b>DrinkHQ Magazine · Issue 01 · Official Record</b><span>{pages} pages · A5 148×210 mm · 3 mm bleed</span>
<button id="bEdit">Edit text &amp; images</button><button id="bBleed">Show bleed</button><button id="bSave">Save edited copy</button><button id="bPress" title="A5 with 3 mm bleed and crop marks, full-resolution images">Print for press</button><button id="bEmail" title="A5 trimmed, no marks, images reduced to 180 dpi for email">Print for email</button></div>
<div class="help" contenteditable="false">Edit mode: click any text to type. Click a photo or an ad box to replace it with your own image. Yellow tags mark placeholders — they never print in the final once removed. “Save edited copy” downloads this file with your changes. “Print for press” makes the printer file (bleed and crop marks); “Print for email” makes a trimmed, lighter file for Gmail or HubSpot — choose “Save as PDF” in the print window.</div>
<div class="doc">{sp}</div><script>{JS}</script></body></html>'''
    open(out, 'w').write(html)
    print(out, os.path.getsize(out) // 1024, 'KB')

if __name__ == '__main__':
    OUT = os.environ.get('DHQ_OUTDIR') or os.path.join(HERE, 'out')
    os.makedirs(OUT, exist_ok=True)
    build('16', plan16(), 16, os.path.join(OUT, 'DrinkHQ-Magazine_Issue-01_16pp_Official-Record.html'))
    build('32', plan32(), 32, os.path.join(OUT, 'DrinkHQ-Magazine_Issue-01_32pp_Official-Record.html'))
