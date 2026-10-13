import math,time,sys
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
