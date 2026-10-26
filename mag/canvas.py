import sys, os, json, re, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen
tag, blobfile, outroot, title = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
B = json.load(open(blobfile))
def img(k):
    n = k if '.' in k else k + '.jpg'
    return '/_blob/' + B[n]
gen.img = img
pages = int(tag)
P = gen.plan16() if pages == 16 else gen.plan32()
gen.USED.clear()
css = open('style.css').read()
if pages == 32: css = gen.css_min(css)
# drop editor/toolbar/print-only rules
css = re.sub(r'@media print\{.*?\n\}\n', '', css, flags=re.S)
css = re.sub(r'@page\{[^}]*\}', '', css)
keep = []
for line in css.split('\n'):
    if line.startswith(('.toolbar', '.help', 'body.editing', 'body.bleed', '.doc{', '.spread', '.sp-label', '.pages{', '.single-', '.sheet', '.clip', '.crop', 'html,body')):
        continue
    keep.append(line)
css = '\n'.join(keep) + '\nbody{margin:0;background:#FBF8F2}\n.trimline{display:none}\n'
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bebas+Neue&amp;family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400;1,700&amp;family=Raleway:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&amp;display=swap">'
W, H = 582, 816
os.makedirs(os.path.join(outroot, 'project'), exist_ok=True)
boards, order = {}, []
names = {}
for n in range(1, pages + 1):
    names[n] = 'Main.dc.html' if n == 1 else f'P{n:02d}.dc.html'
for n in range(1, pages + 1):
    kind, fn = P[n]
    side = 'recto' if n % 2 == 1 else 'verso'
    inner = fn(n)
    inner = inner.replace(' contenteditable="false"', '')
    inner = re.sub(r'<img class="adart" alt="" hidden>\n?', '', inner)
    inner = re.sub(r' title="Edit mode: click to drop in finished artwork"', '', inner)
    nm = 'Front cover' if n == 1 else ('Back cover' if n == pages else f'Page {n:02d}')
    doc = f'''<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<title>DrinkHQ Magazine Issue 01 · {nm}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{FONTS}
<style>
{css}
</style>
</helmet>
<div class="page {kind} {side}" data-page="{n}" style="width: {W}px; height: {H}px; position: relative; overflow: hidden">
{inner}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{W},"height":{H}}}}}'>
class Component extends DCLogic {{
renderVals() {{
return {{}};
}}
}}
</script>
</body>
</html>
'''
    assert 'data:' not in doc
    open(os.path.join(outroot, 'project', names[n]), 'w').write(doc)
    i = n - 1
    import os as _os
    _T = json.load(open('titles32.json')) if (tag == '32' and _os.path.exists('titles32.json')) else {}
    boards[names[n]] = {'x': (i % 8) * (W + 80), 'y': (i // 8) * (H + 200), 'w': W, 'h': H, 'title': _T.get(names[n], nm),
                        'guides': [{'kind': 'columns', 'count': 1, 'gutter': 0, 'margin': 11, 'color': 'rgba(224,0,106,0.35)'},
                                   {'kind': 'rows', 'count': 1, 'gutter': 0, 'margin': 11, 'color': 'rgba(224,0,106,0.35)'}]}
    order.append(names[n])
idx = {'v': 3, 'createdOnFiles': {'v': 1, 'at': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')},
       'title': title, 'launch': {'view': 'canvas'}, 'pages': [], 'boards': boards, 'order': order,
       'notes': {'title': {'x': 0, 'y': -300, 'text': f'{title} — A5 148×210 mm, artboards include 3 mm bleed (pink guides = trim)', 'kind': 'title1', 'maxW': 8 * (W + 80) - 80}},
       'designSystems': []}
json.dump(idx, open(os.path.join(outroot, 'project', 'canvas.json'), 'w'), indent=1)
print(json.dumps({f'project/{v}': f'project/{v}' for v in order[1:]}))
