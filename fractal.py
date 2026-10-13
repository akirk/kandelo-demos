import sys,time
print('\033[2J\033[?25l',end='')
try:
 for f in range(24):
  scale=3.2*(.82**f); lines=[]
  for y in range(22):
   row=''
   for x in range(64):
    c=complex(-.7435+(x/63-.5)*scale,.1314+(y/21-.5)*scale*.68); z=0j; n=0
    while abs(z)<2 and n<70: z=z*z+c; n+=1
    color=16 if n==70 else 16+36*(n%6)+6*((n//3)%6)+(n//7)%6
    row+=f'\033[48;5;{color}m '
   lines.append(row+'\033[0m')
  sys.stdout.write('\033[H'+'\n'.join(lines)+f'\nZoom {3.2/scale:.1f}x'); sys.stdout.flush(); time.sleep(.15)
finally: print('\033[0m\033[?25h\nBoundary complete.')
