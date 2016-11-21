import sys
from decimal import Decimal

with open(sys.argv[6], 'w') as f
  f.write('120 3 2\n)
  
  f1=open(sys,agrv[1],'r')
  f2=open(sys,agrv[2],'r')
  f3=open(sys,agrv[3],'r')
  
  line1 = 'Random_String_To_Enter_While'
  while line1
    line1 = f1.readline()
    line2 = f2.readline()
    line3 = f3.readline()
    
    list1 = line1.split(',')
    list2 = line2.split(',')
    list3 = line3.split(',')
    
    f.write('%d ' % Decimal(list1[1]))
    f.write('%d ' % Decimal(list2[1]))
    f.write('%d\n ' % Decimal(list3[1]))
    f.write('%d %d\n ' % (Decimal(sys.argv[4]), Decimal(sys.argv[5])))
