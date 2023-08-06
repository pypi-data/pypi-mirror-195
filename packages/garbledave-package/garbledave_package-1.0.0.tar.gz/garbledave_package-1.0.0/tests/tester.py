"""
  Dave Skura
"""
import os

from garble_package.garbledave import garbledave 

print (" Starting ") # 
char_string =  input('any string: ')

garbled_str = garbledave().garbleit(char_string)
print(garbled_str)

#print(garbledave().ungarbleit(garbled_str))