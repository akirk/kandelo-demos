import sys,time
print('\033[2J\033[?25l',end='')
try:
 f=0
 while True:
  scale=3.2*(.82**f); lines=[]
  for y in range(22):
   row=''
   for x in range(64):
    c=complex(-.743643887037151+(x/63-.5)*scale,.131825904205330+(y/21-.5)*scale*.68); z=0j; n=0
    while abs(z)<2 and n<120+f*4: z=z*z+c; n+=1
    color=16 if n==120+f*4 else 16+36*(n%6)+6*((n//3)%6)+(n//7)%6
    row+=f'\033[48;5;{color}m '
   lines.append(row+'\033[0m')
  sys.stdout.write('\033[H'+'\n'.join(lines)+f'\nZoom {3.2/scale:.1f}x | Ctrl+C to stop   '); sys.stdout.flush(); time.sleep(.15)
  f=(f+1)%150
except KeyboardInterrupt: pass
finally: print('\033[0m\033[?25h\nBoundary stopped.')
