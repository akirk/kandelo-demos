import sys
rooms={
 'atrium':('The Atrium','You wake under a blinking cursor. A shutdown bell tolls.\nA brass key lies beside a sign: SAVE WHAT REMEMBERS.',{'east':'archive','west':'pipeworks','north':'tower'}),
 'archive':('The Archive','Shelves of forgotten names surround a locked cabinet.\nIts label reads: A KEY OPENS MEMORY.',{'west':'atrium'}),
 'pipeworks':('The Pipeworks','A broken conduit whispers fragments of speech.\nA copper wire hangs from a hook.',{'east':'atrium','south':'gate'}),
 'tower':('The Clock Tower','A console counts down to darkness. Its memory slot is empty.\nBeside it: RESTORE MEMORY, THEN BRIDGE THE CIRCUIT.',{'south':'atrium'}),
 'gate':('The Exit Gate','A narrow door leads out. You can escape alone with: leave.\nBehind you, the city of sleeping processes waits.',{'north':'pipeworks'})}
room='atrium'; bag=set(); taken=set(); opened=False; restored=False; ticks=36
say=lambda s:print('\033[38;5;151m'+s+'\033[0m')
def look():
 name,text,exits=rooms[room]; say('\n'+name.upper()); print(text)
 if room=='archive' and opened: print('The cabinet stands open. A memory crystal glows inside.' if 'crystal' not in taken else 'The cabinet is empty.')
 if room=='tower' and restored: print('The crystal lights the console. One circuit remains broken.')
 print('Exits: '+', '.join(exits))
 print('Carrying: '+(', '.join(sorted(bag)) or 'nothing'))
print('\033[2J\033[H'); say('THE LAST PROCESS')
print('A tiny adventure in a dying computer. You have 36 actions.\nType help for commands. Looking, hints and mistakes cost no time.')
look()
try:
 while ticks>0:
  command=input(f'\n[{ticks} ticks] > ').strip().lower(); parts=command.split(maxsplit=1)
  if not parts: continue
  verb=parts[0]; obj=parts[1] if len(parts)>1 else ''
  if verb in ('quit','q'): print('You close your eyes. The cursor keeps blinking.'); break
  if verb=='help': print('look | go east (or east) | take key | use key\ntake wire | take crystal | use crystal | use wire\ninventory | hint | leave | quit'); continue
  if verb in ('look','l'): look(); continue
  if verb in ('inventory','i'): print('Carrying: '+(', '.join(sorted(bag)) or 'nothing')); continue
  if verb=='hint':
   print('Find the brass key in the atrium.' if 'key' not in taken else 'Use the key in the archive.' if not opened else 'Take the crystal from the cabinet.' if 'crystal' not in taken else 'Take the wire in the pipeworks.' if 'wire' not in taken else 'Use the crystal, then the wire, in the tower.'); continue
  if verb=='leave' and room=='gate':
   say('ENDING: THE SURVIVOR'); print('You slip through the gate. Behind you the bell falls silent.\nYou survive, but no one remembers the city.'); break
  destination=obj if verb=='go' else verb
  if destination in rooms[room][2]: room=rooms[room][2][destination]; ticks-=1; look()
  elif verb=='take':
   available={'atrium':'key','pipeworks':'wire','archive':'crystal' if opened else ''}.get(room,'')
   if obj==available and obj and obj not in taken: bag.add(obj); taken.add(obj); ticks-=1; say('Taken: '+obj)
   else: print('You cannot take that here.')
  elif verb=='use':
   if obj not in bag: print('You are not carrying that.')
   elif obj=='key' and room=='archive' and not opened: opened=True; ticks-=1; say('The cabinet clicks open. Inside: a memory crystal.')
   elif obj=='crystal' and room=='tower' and not restored: restored=True; bag.remove(obj); ticks-=1; say('Names flood the screen. The circuit needs a wire.')
   elif obj=='wire' and room=='tower' and restored:
    say('ENDING: THE KEEPER'); print('You bridge the circuit. The shutdown clock stops.\nA thousand sleeping processes wake and speak your name.'); break
   else: print('Nothing happens. Perhaps another place, or another order.')
  else: print('That does not work here. Type help or hint.')
 else: say('ENDING: THE LAST TICK'); print('The bell rings once more. Your world becomes a blank line.')
except (EOFError,KeyboardInterrupt): print('\nThe cursor waits for another traveler.')
finally: sys.stdout.write('\033[0m'); sys.stdout.flush()
