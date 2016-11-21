from fann2 import libfann
import sys
from decimal import Decimal

ann - libfann.neural_net()
ann.create_from_file(sys.argv[1])
with open(sys.argv[2], 'r') as test_file:
  for line in test_file:
    string_list = line.split('')
    test_list = [0,0,0]
    test_list[0] = Decimal(string_list[0])
    test_list[1] = Decimal(string_list[1])
    test_list[2] = Decimal(string_list[2])
    #Get original FANN result
    result_list = ann.run([test_list[0], test_list[1], test_list[2]])
    
    if result_list[0] > 0.5:
      result_list[0] = 1
    else:
      result_list[0] = 0
    if result_list[1] > 0.5:
      result_list[1] = 1
    else:
      result_list[1] = 0
    print result_list
