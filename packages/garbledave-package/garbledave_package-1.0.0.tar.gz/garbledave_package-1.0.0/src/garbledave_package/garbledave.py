"""
  Dave Skura
  
	A=65, Z = 90
	a=97, z = 122
	0=48, 9=57
"""

class garbledave:

	def garbleit(self,prm):
		newstr = ''
		for i in range(0,len(prm)):
			onechar = prm[i]

			if 'abcdefghijklmnopqrstuvwxyz'.find(onechar) > -1:
				if onechar == 'z':
					onechar = 'a'
				else:
					onechar = chr(ord(onechar)+1)
			elif  'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.find(onechar) > -1:
				if onechar == 'Z':
					onechar = 'A'
				else:
					onechar = chr(ord(onechar)+1)
			elif  '0123456789'.find(onechar) > -1:
				if onechar == '9':
					onechar = '0'
				else:
					onechar = chr(ord(onechar)+1)

			newstr += onechar

		return newstr

	def ungarbleit(self,prm):
		newstr = ''
		for i in range(0,len(prm)):
			onechar = prm[i]

			if 'abcdefghijklmnopqrstuvwxyz'.find(onechar) > -1:
				if onechar == 'a':
					onechar = 'z'
				else:
					onechar = chr(ord(onechar)-1)
			elif  'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.find(onechar) > -1:
				if onechar == 'A':
					onechar = 'Z'
				else:
					onechar = chr(ord(onechar)-1)
			elif  '0123456789'.find(onechar) > -1:
				if onechar == '0':
					onechar = '9'
				else:
					onechar = chr(ord(onechar)-1)

			newstr += onechar

		return newstr


if __name__ == '__main__':
	
	print (" Starting ") # 
	char_string =  input('any string: ')

	garbled_str = garbledave().garbleit(char_string)
	print(garbled_str)

	#print(garbledave().ungarbleit(garbled_str))

