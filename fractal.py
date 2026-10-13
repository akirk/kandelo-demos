import sys,time
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
