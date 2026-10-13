import math,time,sys
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
