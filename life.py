import random,time,sys
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
