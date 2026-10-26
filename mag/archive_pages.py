# ---------------------------------------------------------------- archive-based sections (Oct 2026)
ARCH = '<span class="arch" contenteditable="false">FROM THE ARCHIVE · DRINK 2007</span>'

def strip_ad(n, art, note=''):
    fit = 'cover'
    bg = '#111'
    if art == 'strip_tajga':
        fit, bg = 'contain', '#E4232B'
    if art == 'strip_13cabs':
        fit = 'cover'
    return ad('hstrip', f'AD-{n:02d}-S', note, n % 2 == 1, art=art, fit=fit, bg=bg)

def news_hot(n, strip=None):
    s = strip_ad(n, strip) if strip else ''
    hot = ['Monday nights at the Championship', 'Hosting your own home cocktail party', 'Travelling to new bars',
           'Low and no serves done properly', 'The onset of winter (lots of warm bars)']
    return f'''{frame()}<div class="safe {'withstrip' if strip else ''}">{head('News', 'Giving you the facts and nothing but the facts')}
<div class="nh">
<div class="nh-news">
<div><h3>The Founding 12 take shape</h3><p>Invitations have gone to bars across Melbourne for twelve places in the inaugural Championship. Application dates go to registered teams first. Contact {REGISTER}.</p></div>
<div><h3>Season 2027–28 confirmed</h3><p>Eight Monday-night rounds, six weeks apart, from 21 June 2027 to 10 April 2028. The Grand Final date will be announced later in the season.</p></div>
<div><h3>Get the taste of it</h3><p>DrinkHQ will run its own tasting series, with experts sharing what they know with the willing few. Register your interest at {CONTACT}.</p></div>
</div>
<div class="nh-hot"><div class="hot-h">What’s <i>Hot</i></div>{''.join(f'<div class="hot-i">{x}</div>' for x in hot)}</div>
</div></div>{s}{folio(n, bool(strip))}'''

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
<div class="letter">“[Reader letter, email or DM.]”<i>[Name] · via email</i></div>
<div class="letter">“[Reader letter, email or DM.]”<i>[Name] · via Instagram</i></div>
<div class="letter-cta">Send yours to {CONTACT}</div>
</div></div>
<div class="trivia">
<div><b>Got some time?</b><p>H. L. Mencken is said to have calculated that 17,864,392,788 different cocktails could be made from the ingredients in a well-stocked bar.</p></div>
<div><b>Quote</b><p>“One Martini is all right. Two are too many, and three are not enough.” — attributed to James Thurber</p></div>
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
 ('bib_scubar', 'scubar', '389 Lonsdale St, City', 'Follow the leopard print down the staircase into this little grungy heaven, a dark haven of acid house on Fridays and hip hop on Thursdays. The fish tank glows an iridescent blue as you sink into the boxy couches or hide away in the corner lounges. The small bar is stocked with all you need — the place to end a night.',
  [('Type', 'Bar / Club'), ('Feature', 'Leopard-skin pool table'), ('Hours', 'Mon 7pm–12am, Tue–Sat 4pm–4am'), ('Food', 'No'), ('Cocktails', 'On request')], (3, 1, 1), 'Vodka Martini'),
 ('bib_jackie', 'jackie o', '204 Barkly St, St Kilda', 'Don’t be put off by the neon sign on the corner — shut your eyes and delve in, because this is the least pretentious of St Kilda’s haunts. Kitsch meshes with class from brekkie to dinner, and the bar comes alive as people watch Acland Street’s creatures venture into the night. Frozen cocktails are a must; don’t miss happy hour on Fridays.',
  [('Type', 'Bar / Café'), ('Feature', 'Tarot readings'), ('Hours', '7 days 7.30am–1am'), ('Food', 'Full menu'), ('Cocktails', '25')], (2, 1, 2), 'Frangelico Sour'),
 ('bib_backbar', 'back bar, tusk', '133 Chapel St, Windsor', 'A winter gem (and just wait for summer) for a leisurely evening in an intimate cocktail bar where time stands still. Chaise lounges straight out of a grandmother’s tearoom tempt you to unwind. The cocktail list would make New York envious — lose yourself in a Cosmopolitan, and late risers with a sweet tooth should try a Breakfast Martini.',
  [('Type', 'Cocktail bar'), ('Feature', 'Fireplace'), ('Hours', '7 days 6pm–late'), ('Food', 'Tapas'), ('Cocktails', '7')], (3, 2, 1), 'Bar Gorgeous'),
]
def dots(k):
    return '●' * k + '<span class="off">' + '●' * (4 - k) + '</span>'

def bars_brief(n, bars, strip=None):
    s = strip_ad(n, strip) if strip else ''
    cards = ''
    for k, nm, addr, txt, info, sc, rec in bars:
        rows = ''.join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in info)
        cards += f'''<div class="bb">{photo(k,'bb-img',fixed=True)}<h3>{nm}</h3><div class="addr">{addr}</div><p>{txt}</p>
<table class="bbt">{rows}</table>
<div class="bbs"><b>drink score</b><div><span>Atmosphere</span>{dots(sc[0])}</div><div><span>Service</span>{dots(sc[1])}</div><div><span>Products</span>{dots(sc[2])}</div><div class="rec"><span>Drink recommends</span>{rec}</div></div></div>'''
    return f'''{frame()}<div class="safe {'withstrip' if strip else ''}"><div class="bb-top"><h1 class="bib-head">bars in brief</h1>{ARCH}</div>
<div class="bbs3">{cards}</div>
<div class="bbkey">● Satisfactory · ●● Decent · ●●● Fantastic · ●●●● Exceptional — reviews reproduced from Drink magazine (2007) as layout copy; venues and details will change.</div>
</div>{s}{folio(n, bool(strip))}'''

def featured_bars(n):
    def col(k, nm, addr, paras, typ):
        return f'''<div class="fb">{photo(k,'fb-img',fixed=True)}<div class="fb-name">{nm}</div><div class="fb-body"><div class="addr">{addr}</div>{''.join(f'<p>{p}</p>' for p in paras)}<div class="fb-type"><b>Type</b> {typ}</div></div></div>'''
    a = col('feat_edv', 'Eau De Vie', '1 Malthouse Ln, Melbourne', ['Eau De Vie, in the heart of Melbourne, is a cocktail bar celebrated for its sophisticated ambience and exceptional mixology. Its refined, elegant decor blends classic charm with modern polish — ideal for intimate gatherings and special occasions.', 'Knowledgeable, attentive staff make every guest feel welcome. Whether you’re a cocktail connoisseur or after a memorable night out, Eau De Vie combines elegance, innovation and service.'], 'Cocktail bar')
    b = col('feat_1806', '1806', '169 Exhibition St, Melbourne', ['1806 is a standout cocktail bar in Melbourne’s theatre district, named after the year the word “cocktail” was first defined in print.', 'The menu is a journey through cocktail history, with drinks from every era and the stories behind them. With meticulous attention to mixology and service, guests are greeted at the door and shown to their table to enjoy expertly made cocktails without leaving their seats.'], 'Cocktail bar')
    return f'''<div class="bleedimg blackfill"></div><div class="safe onnavy"><div class="fb-top"><h1 class="sec light">Featured Bars<span class="gt">&gt;</span></h1>{ARCH.replace('DRINK 2007','DRINKHQ RECORD 2025')}</div>
<div class="fb2">{a}{b}</div></div>{folio(n)}'''

WHISKY = [('rv_bushmills', 'Bushmills 1608', 'This special edition celebrating Bushmills’ 400th anniversary is the perfect start to any collection: triple distillation with crystal malt for exceptional smoothness.'),
          ('rv_tyrconnell', 'Tyrconnell Single Malt', 'Distilled by the award-winning Cooley distillery, a driving force behind the Irish single malt revival. Most Irish malt goes into blends, so finding it bottled pure is rare.'),
          ('rv_jameson', 'Jameson Gold Reserve', 'New-oak ageing gives a remarkable boost in oak flavour, balanced with just the right share of sherry-aged whiskey and a good dose of pot-still character. Big and bold.')]
def review2(n, half_art=None):
    recto = n % 2 == 1
    h = ad('half', f'AD-{n:02d}-H', 'Half page vertical', recto, art=half_art) if half_art else ''
    cls = 'withh-' + ('r' if recto else 'l')
    items = ''.join(f'<div class="wk">{photo(k,"wk-img",fixed=True)}<div><h3>{t}</h3><p>{d}</p><div class="stars">★★★★☆</div></div></div>' for k, t, d in WHISKY)
    return f'''{frame()}<div class="safe {cls}">{head('Review', 'Three whiskeys for any home collection')}{ARCH.replace('DRINK 2007','DRINKHQ RECORD 2025')}
<div class="wks">{items}</div><div class="win"><b>{WEBSITE}</b><span>win stuff</span></div></div>{h}{folio(n)}'''

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

def wwyln2(n, start):
    ks = [f'ww{i:02d}' for i in range(start, start + 12)]
    g = ''.join(f'<div class="pol" style="transform:rotate({[-2,1.5,-1,2,-1.5,1][i%6]}deg)">{photo(k,"pol-img",fixed=True)}<span>{i+1}</span></div>' for i, k in enumerate(ks))
    return f'''<div class="bleedimg greenfill"></div><div class="safe">
<div class="kicker light">[ where were you last night? ]</div><h1 class="big light">Where were you <i>last night?</i></h1>
<div class="polg">{g}</div>
<p class="light small">1–12. Drink magazine nights, from the archive — replaced with Season 2027–28 round-night photos. Only publish photos of people who have agreed to appear. {ph('ARCHIVE PHOTOS')}</p>
<p class="light">Want to appear here with the beautiful people? Tag us or send your photos to {CONTACT}</p>
</div>{folio(n)}'''

# ---------------------------------------------------------------- plans
def plan16():
    # 60% ad / 40% editorial: 9 full ad pages + 2 strips = 9.5 of 16 pp; last spread = photos + ad (as 2007)
    P = {}
    P[1] = ('cover', lambda n: cover_issue(n, 7, [(7, 'THE CHAMPIONSHIP', '<b>Round 1 <i>fixture</i></b>, the ladder and TASTE'), (6, 'NEWS', 'What’s hot, and the facts'), (10, 'BARS IN BRIEF', 'Three Melbourne bars, rated'), (13, 'SPIRIT EXPLAINED', 'Absinthe: the green fairy'), (14, 'LAST NIGHT', 'Where were you last night?'), (4, 'WELCOME', 'Eight rounds, one Grand Final')]))
    P[2] = ('ad', lambda n: page_ad(n, 'AD-02', 'Inside front cover spread · left', 'ad_patron'))
    P[3] = ('ad', lambda n: page_ad(n, 'AD-03', 'Inside front cover spread · right', 'ad_ketel'))
    P[4] = ('ed', lambda n: welcome(n, [(6, 'News &amp; What’s Hot'), (7, 'The Championship · Round 1'), (10, 'Bars in Brief'), (13, 'Spirit Explained · Absinthe'), (14, 'Where were you last night?')]))
    P[5] = ('ad', lambda n: page_ad(n, 'AD-05', 'Full page · right hand, facing Welcome', 'ad_chambord'))
    P[6] = ('ed', lambda n: news_hot(n, 'strip_nash'))
    P[7] = ('ed', championship)
    P[8] = ('ad', lambda n: page_ad(n, 'AD-08', 'Centre double page spread · left', 'ad_letsmeet'))
    P[9] = ('ad', lambda n: page_ad(n, 'AD-09', 'Centre double page spread · right', 'ad_social'))
    P[10] = ('ed', lambda n: bars_brief(n, BARS16, 'strip_tajga'))
    P[11] = ('ad', lambda n: page_ad(n, 'AD-11', 'Full page · right hand, facing Bars in Brief', 'ad_frangelico'))
    P[12] = ('ad', lambda n: page_ad(n, 'AD-12', 'Full page · left hand, facing Spirit Explained', 'ad_vibe'))
    P[13] = ('ed', spirit_abs)
    P[14] = ('ed', lambda n: wwyln2(n, 0))
    P[15] = ('ad', lambda n: page_ad(n, 'AD-15', 'Inside back cover · facing the photo page, as 2007', 'ad_veludo'))
    P[16] = ('ad', lambda n: page_ad(n, 'AD-16', 'Outside back cover', 'ad_illusion'))
    return P

def plan32():
    # 60% ad / 40% editorial: 18 full ad pages + 3 strips + 1 half = 19.3 of 32 pp
    P = {}
    P[1] = ('cover', lambda n: cover_issue(n, 18, [(20, 'THE TEAMS', '<b>Meet the <i>Founding 12</i></b>'), (18, 'THE CHAMPIONSHIP', 'Round 1 fixture, the ladder and TASTE'), (14, 'BARS IN BRIEF', 'Three Melbourne bars, rated'), (21, 'FEATURED BARS', 'Eau De Vie and 1806'), (23, 'SPIRIT EXPLAINED', 'Absinthe: the green fairy'), (12, 'REVIEW', 'Three whiskeys for the home bar')]))
    P[2] = ('ad', lambda n: page_ad(n, 'AD-02', 'Inside front cover spread · left', 'ad_patron'))
    P[3] = ('ad', lambda n: page_ad(n, 'AD-03', 'Inside front cover spread · right', 'ad_ketel'))
    ct = [(6, 'News', 'Keeping you in the know'), (8, 'What’s Hot &amp; Drink Chasers', 'And your letters'), (10, 'Top 10 &amp; Bar Lingo', 'Movie cocktails, A to K'),
          (12, 'Review', 'Three whiskeys for the home bar'), (14, 'Bars in Brief', 'Three bars, rated'), (18, 'The Championship', 'Round 1 fixture, ladder &amp; TASTE'),
          (20, 'Teams', 'Meet the Founding 12'), (21, 'Featured Bars', 'Eau De Vie and 1806'), (23, 'Spirit Explained', 'Absinthe: the green fairy'),
          (24, 'Mixology', 'Three serves to make'), (28, 'Competitions · Interview · Club', 'Win, read, join'), (30, 'Where were you last night?', 'The beautiful people')]
    P[4] = ('ed', lambda n: contents(n, ct))
    P[5] = ('ad', lambda n: page_ad(n, 'AD-05', 'Full page · right hand, facing Contents', 'ad_chambord'))
    P[6] = ('ed', lambda n: news(n, strip='strip_tajga'))
    P[7] = ('ad', lambda n: page_ad(n, 'AD-07', 'Full page · right hand, facing News', 'ad_fidels'))
    P[8] = ('ed', lambda n: whats_hot2(n, 'strip_13cabs'))
    P[9] = ('ad', lambda n: page_ad(n, 'AD-09', 'Full page · right hand, facing What’s Hot', 'ad_vibe'))
    P[10] = ('ed', top10)
    P[11] = ('ad', lambda n: page_ad(n, 'AD-11', 'Full page · right hand, facing Top 10', 'ad_fcafe'))
    P[12] = ('ed', lambda n: review2(n, 'ad_frangelico2'))
    P[13] = ('ad', lambda n: page_ad(n, 'AD-13', 'Full page · right hand, facing Review', 'ad_zimmer'))
    P[14] = ('ed', lambda n: bars_brief(n, BARS32, 'strip_nash'))
    P[15] = ('ad', lambda n: page_ad(n, 'AD-15', 'Full page · right hand, facing Bars in Brief', 'ad_beach'))
    P[16] = ('ad', lambda n: page_ad(n, 'AD-16', 'Centre double page spread · left', 'ad_letsmeet'))
    P[17] = ('ad', lambda n: page_ad(n, 'AD-17', 'Centre double page spread · right', 'ad_social'))
    P[18] = ('ed', championship)
    P[19] = ('ad', lambda n: page_ad(n, 'AD-19', 'Full page · right hand, facing the Championship', 'ad_blackpearl'))
    P[20] = ('ed', founding12_single)
    P[21] = ('ed', featured_bars)
    P[22] = ('ad', lambda n: page_ad(n, 'AD-22', 'Full page · left hand, facing Spirit Explained', 'ad_chaise'))
    P[23] = ('ed', spirit_abs)
    P[24] = ('ed', mixology)
    P[25] = ('ad', lambda n: page_ad(n, 'AD-25', 'Full page · right hand, facing Mixology', 'ad_epicurean'))
    P[26] = ('ad', lambda n: page_ad(n, 'AD-26', 'Full page · left hand', 'ad_stanne'))
    P[27] = ('ad', lambda n: page_ad(n, 'AD-27', 'Full page · right hand', 'ad_santalia'))
    P[28] = ('ed', back_page_extras)
    P[29] = ('ad', lambda n: page_ad(n, 'AD-29', 'Full page · right hand, facing Club', 'ad_haze'))
    P[30] = ('ed', lambda n: wwyln2(n, 12))
    P[31] = ('ad', lambda n: page_ad(n, 'AD-31', 'Inside back cover · facing the photo page, as 2007', 'ad_veludo'))
    P[32] = ('ad', lambda n: page_ad(n, 'AD-32', 'Outside back cover', 'ad_illusion'))
    return P

