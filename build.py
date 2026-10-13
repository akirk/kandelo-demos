import base64, gzip, hashlib, html, json
from pathlib import Path
ROOT=Path(__file__).parent
DEMO=[
('donut','01','Orbit / rotating donut','A shaded torus spins in a terminal. Trigonometry, perspective and a depth buffer in a tiny program.','Python · 3D · 12 seconds',r'''import math,time,sys
w,h=64,24
print('\033[2J\033[?25l',end='')
try:
 for f in range(120):
  a,b=f*.055,f*.03
  ca,sa,cb,sb=math.cos(a),math.sin(a),math.cos(b),math.sin(b)
  pixels=[' ']*(w*h); depth=[0.]*(w*h)
  for j in range(90):
   cj,sj=math.cos(j*.07),math.sin(j*.07)
   for i in range(180):
    ci,si=math.cos(i*.035),math.sin(i*.035)
    q=cj+2; z=1/(si*q*sa+sj*ca+5); t=si*q*ca-sj*sa
    x=int(w/2+26*z*(ci*q*cb-t*sb)); y=int(h/2+13*z*(ci*q*sb+t*cb))
    n=int(8*((sj*sa-si*cj*ca)*cb-si*cj*sa-sj*ca-ci*cj*sb))
    if 0<=x<w and 0<=y<h and z>depth[x+y*w]:
     depth[x+y*w]=z; pixels[x+y*w]='.,-~:;=!*#$@'[max(0,min(11,n))]
  sys.stdout.write('\033[H\033[38;5;220m'+'\n'.join(''.join(pixels[y*w:(y+1)*w]) for y in range(h))); sys.stdout.flush(); time.sleep(.1)
finally: print('\033[0m\033[?25h\nOrbit complete.')
'''),
('plasma','02','Chromatic / sine plasma','Interfering sine waves turn ordinary terminal cells into a shifting field of color.','Python · ANSI color · 12 seconds',r'''import math,time,sys
print('\033[2J\033[?25l',end='')
try:
 for f in range(120):
  t=f*.13; lines=[]
  for y in range(22):
   row=''
   for x in range(64):
    v=math.sin(x*.16+t)+math.sin(y*.28-t)+math.sin((x+y)*.12+t)+math.sin(math.hypot(x-32,y*2-22)*.18-t)
    r=int(127+127*math.sin(v+t)); g=int(127+127*math.sin(v+t+2)); b=int(127+127*math.sin(v+t+4))
    row+=f'\033[48;2;{r};{g};{b}m '
   lines.append(row+'\033[0m')
  sys.stdout.write('\033[H'+'\n'.join(lines)); sys.stdout.flush(); time.sleep(.1)
finally: print('\033[0m\033[?25h\nChromatic complete.')
'''),
('life','03','Seed / cellular life','A deterministic random seed becomes a colony. Four hundred cells of code? Much less.','Python · cellular automaton · 12 seconds',r'''import random,time,sys
random.seed(42); w,h=64,22
cells={(x,y) for y in range(h) for x in range(w) if random.random()<.28}
print('\033[2J\033[?25l',end='')
try:
 for step in range(100):
  sys.stdout.write('\033[H\033[38;5;120m'+'\n'.join(''.join('o' if (x,y) in cells else ' ' for x in range(w)) for y in range(h))+f'\033[0m\nGeneration {step:03} | living cells {len(cells):04}'); sys.stdout.flush()
  counts={}
  for x,y in cells:
   for dx,dy in [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]:
    p=((x+dx)%w,(y+dy)%h); counts[p]=counts.get(p,0)+1
  cells={p for p,n in counts.items() if n==3 or n==2 and p in cells}; time.sleep(.12)
finally: print('\033[0m\033[?25h\nSeed complete.')
'''),
('fractal','04','Boundary / Mandelbrot','A looping journey into and out of the Mandelbrot set. Rendered frames are cached for smooth replay.','Python · fractal · continuous loop',r'''import sys,time
print('\033[2J\033[?25l',end='')
cache={}; f=0; direction=1; w,h=48,18; limit=160
try:
 while True:
  scale=3.2*(.82**f)
  if f not in cache:
   lines=[]
   for y in range(h):
    row=''
    for x in range(w):
     c=complex(-.743643887037151+(x/(w-1)-.5)*scale,.131825904205330+(y/(h-1)-.5)*scale*.68); z=0j; n=0
     while z.real*z.real+z.imag*z.imag<4 and n<limit: z=z*z+c; n+=1
     color=16 if n==limit else 16+36*(n%6)+6*((n//3)%6)+(n//7)%6
     row+=f'\033[48;5;{color}m '
    lines.append(row+'\033[0m')
   cache[f]='\n'.join(lines)
  sys.stdout.write('\033[H'+cache[f]+f'\nZoom {3.2/scale:.1f}x | looping in/out | Ctrl+C to stop   '); sys.stdout.flush(); time.sleep(.12)
  if f==58: direction=-1
  elif f==0: direction=1
  f+=direction
except KeyboardInterrupt: pass
finally: print('\033[0m\033[?25h\nBoundary stopped.')
''')]
DEMO.append(('adventure','05','The Last Process / text adventure','Explore a dying computer, unlock its memory and stop the shutdown. Five rooms, three puzzles, and a choice of endings.','Python · interactive · 36 actions',(ROOT/'adventure.py').read_text()))
b64=lambda b:base64.urlsafe_b64encode(b).decode().rstrip('=')
vfs='https://kandelo.dev/vfs-groups/release-1/images/shell.vfs.zst'
items=[]
for slug,num,title,desc,meta,source in DEMO:
 (ROOT/(slug+'.py')).write_text(source)
 script=("python3 - <<'KANDELO_PY'\n"+source+'KANDELO_PY\n').encode()
 if slug=='adventure': script=("cat > /tmp/kandelo-adventure.py <<'KANDELO_PY'\n"+source+'KANDELO_PY\npython3 /tmp/kandelo-adventure.py\n').encode()
 d={'version':1,'id':'shell','title':title,'base':'kandelo:shell@abi8','runtime':{'arch':'wasm32','kernel':'kernel@local','memoryPages':2048,'features':[],'time':'real'},'packages':[],'mounts':[{'path':'/','source':'image','ref':vfs}],'boot':{'argv':['/usr/bin/login'],'cwd':'/home/maker','env':{},'inputs':[{'id':'script','filename':'kandelo-link.sh','byteLength':len(script),'sha256':hashlib.sha256(script).hexdigest(),'source':{'kind':'inline','data':b64(gzip.compress(script,mtime=0)),'compression':'gzip'}}],'parameters':{'runScript':'script','runScriptShell':'bash'}}}
 url='https://kandelo.dev/#k1='+b64(gzip.compress(json.dumps(d,separators=(',',':')).encode(),mtime=0))
 # Verify transport and script integrity before emitting the link.
 decoded=json.loads(gzip.decompress(base64.urlsafe_b64decode(url.split('=')[1]+'===')))
 recovered=gzip.decompress(base64.urlsafe_b64decode(decoded['boot']['inputs'][0]['source']['data']+'==='))
 assert recovered==script and hashlib.sha256(recovered).hexdigest()==decoded['boot']['inputs'][0]['sha256']
 items.append({'slug':slug,'title':title,'url':url,'urlBytes':len(url.encode()),'scriptBytes':len(script)})
 preview={'adventure':'THE LAST PROCESS\n\n[36 ticks] > look\nA cursor blinks.\nThe city waits.','donut':'       .,-~:;=!*#$*=;~-.\n    .~;=!*##########*!=;~.\n   :=!*####*=:  :=*####*!: \n   :=!*####*=:  :=*####*!: \n    .~;=!*##########*!=;~.\n       `-~:;=!*#$*=;~-´','plasma':'▁▂▃▄▅▆▇█▇▆▅▄▃▂▁\n▂▃▄▅▆▇█▇▆▅▄▃▂▁▂\n▃▄▅▆▇█▇▆▅▄▃▂▁▂▃','life':'  o o      ooo     o\n   oo      o       oo\n   o        o      o o\n        oo      ooo\n       o  o      o\n        oo','fractal':'             .\n           .:::..\n        ..::###::.\n  ...::::#########:.\n:::::#############::.\n  ...::::#########:.'}[slug]
 card=f'''<article class="{slug}"><div class="art" aria-hidden="true"><pre>{html.escape(preview)}</pre><span>Illustrative motif</span></div><div class="body"><p class="eyebrow">EXPERIMENT {num}</p><h2>{html.escape(title)}</h2><p>{html.escape(desc)}</p><p class="meta">{meta}</p><a class="launch" target="_blank" rel="noopener" href="{html.escape(url,quote=True)}">Launch in Kandelo <span aria-hidden="true">↗</span></a><p class="budget">{len(url.encode()):,} URL bytes · {len(script):,} script bytes</p><details><summary>Inspect the startup script</summary><pre><code>{html.escape(script.decode())}</code></pre></details></div></article>'''
 items[-1]['card']=card
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kandelo / Small code, big worlds</title><style>
:root{color-scheme:dark;font-family:ui-sans-serif,system-ui,sans-serif;background:#101311;color:#edf1e9}*{box-sizing:border-box}body{margin:0}main{max-width:1120px;margin:auto;padding:40px 26px 60px}.mast{display:flex;justify-content:space-between;border-bottom:1px solid #354036;padding-bottom:20px;font-size:13px;letter-spacing:.12em}.mast a{color:#d8e4d0}header{padding:65px 0 40px;max-width:830px}.eyebrow{color:#c4f078;font-size:11px;font-weight:700;letter-spacing:.15em}h1{font-size:clamp(42px,7vw,78px);line-height:1.02;letter-spacing:-.055em;margin:20px 0}header p{color:#b8c4b4;font-size:18px;line-height:1.7;max-width:670px}.note{border-left:3px solid #c4f078;padding:12px 18px;background:#1a2119;font-size:14px;line-height:1.6;color:#c7d0c1;margin-bottom:30px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:24px}article{border:1px solid #354036;border-radius:12px;overflow:hidden;background:#171c17}.art{height:195px;display:flex;position:relative;align-items:center;justify-content:center;background:#0a0e0b;color:#d9f0aa}.art pre{font:16px/1.3 monospace;margin:0;white-space:pre}.art span{position:absolute;bottom:12px;right:14px;font-size:10px;color:#8b9b87}.plasma .art{background:linear-gradient(130deg,#49248b,#dc387a,#ea9d45,#4aa682);color:#ffffff99}.life .art{color:#a9f582}.fractal .art{background:#171027;color:#be92f1}.body{padding:26px}h2{font-size:24px;letter-spacing:-.04em;margin:10px 0}.body>p{line-height:1.6;color:#bcc7b7}.body .eyebrow{color:#c4f078}.body .meta,.body .budget{font-size:12px;color:#8e9c87}.launch{display:flex;justify-content:space-between;align-items:center;padding:13px 16px;margin-top:22px;background:#c4f078;color:#192112;border-radius:6px;text-decoration:none;font-weight:650}.launch:hover{background:#d8ffa0}a:focus-visible,summary:focus-visible{outline:3px solid #fff;outline-offset:4px}details{border-top:1px solid #354036;margin-top:20px;padding-top:15px}summary{cursor:pointer;font-size:13px;color:#d5dfce}details pre{font:12px/1.6 monospace;overflow:auto;max-height:350px;background:#0e120e;padding:15px}footer{margin-top:35px;padding-top:24px;border-top:1px solid #354036;color:#93a18c;font-size:13px;line-height:1.7}footer a{color:#c4f078}@media(max-width:700px){.grid{grid-template-columns:1fr}header{padding-top:40px}.mast{font-size:10px}.body{padding:22px}}
</style><body><main><div class="mast"><strong>KANDELO / CODE SKETCHES</strong><a href="https://kandelo.dev/" target="_blank" rel="noopener">OPEN THE LAB ↗</a></div><header><p class="eyebrow">FIVE SMALL TERMINAL EXPERIMENTS</p><h1>Small code.<br>Big worlds.</h1><p>No pictures packed into the link. Just equations, rules and a little Python, turning a browser-local terminal into a canvas.</p></header><div class="note">Launch opens a new Kandelo tab and runs the encoded script. Python and the operating system load separately; only the startup code travels in the URL. The donut, plasma and Life animations finish automatically. Mandelbrot loops inward and outward through a fixed range of detail, caching frames as it goes; press Ctrl+C to stop. All restore the cursor on exit. The adventure accepts typed commands; enter help to begin or quit to exit. Reloading resets the environment.<br><strong>Validation:</strong> scripts and link encoding checked locally; these demos have not yet been verified on the live Kandelo runtime.</div><section class="grid" aria-label="Demo gallery">'''+''.join(i.pop('card') for i in items)+'''</section><footer>Made for the constraint: generate the spectacle, carry the recipe. Sizes are UTF-8 bytes of the complete launch URL, including its compressed descriptor.<br>Each source is visible above. These demos use Python's standard library and ANSI terminal escape sequences. Runtime speed depends on your browser and Kandelo.<br><a href="https://github.com/Automattic/kandelo">Kandelo source</a></footer></main></body></html>'''
(ROOT/'index.html').write_text(page)
(ROOT/'links.json').write_text(json.dumps(items,indent=2))
for i in items: print(i['slug'],i['urlBytes'],'URL bytes')
