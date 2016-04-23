import ass

symbol_table = ass.symbol_table
globTable = ass.globTable
file_size= ass.file_size
externtable = {}
finalsymbol_table = {}

def getLoc(exter, files):
	for fl in files:
		fl = fl.split('.')[0]
		for vari in globTable[fl]:
			# print vari
			if vari == exter:
				val = symbol_table[fl][vari]
				val = val.split('#')[1]
				return (fl,val)

def linker( files ):
	startCount = {}
	lastcount = 0
	for fl in files:
		startCount[fl.split('.')[0]] = lastcount
		lastcount += file_size[fl.split('.')[0]]
	for fl in files :
		fl = fl.split('.')[0]
		inputFile = open(fl+'.li','r')
		code = inputFile.read()
		lines = code.split('\n')
		outFile = open(fl+'.loaded','w')
		newCode = []
		for line in lines :
			line = line
			if '$' in line:
				exter = line.split(' ')[1].split('$')[1]
				x, y = getLoc(exter, files)
				newLine = line.replace('$'+exter, '@' + str(int(startCount[x]+int(y))))
				newCode.append(newLine)
			else:
				newCode.append(line)

		outFile.write('\n'.join(newCode))
		outFile.close()

	outFile = open(files[0].split('.')[0]+'.ls','w')
	linkCode = []
	progCount = 0
	for fl in files :
		fl = fl.split('.')[0]
		inputFile = open(fl+'.loaded','r')
		code = inputFile.read()
		lines = code.split('\n')
		for line in lines :
			line = line
			if '#' in line:
				tag = line.split(' ')[1]
				newtag = '#' + str((int(tag.split('#')[1]) + startCount[fl]))
				linkCode.append(line.replace(tag, newtag))
			elif '@' in line:
				newtag = line.replace('@','#')
				linkCode.append(newtag)
			else:
				linkCode.append(line)
	outFile.write('\n'.join(linkCode))
	outFile.close()