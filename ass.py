import re

oplen = {}
symTable = {}
globTable = {}
filelen = {}

def isvariable(line):
	var = re.compile(r'var (.+*)=(.+*)')

def calculatelen():
	inputFile = open('lenopcodes.cf',"r")
	code = inputFile.read()
	lines = code.split('\n')
	for line in lines :
		line = line.lstrip().rstrip()
		if line != '' :
			oplen[line.split(' ')[0]] = int(line.split(' ')[1])

def tryInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def test( fileNames ):
	calculatelen()
	glo = re.compile(r'glob var (.*)=(.*)')
	ext = re.compile(r'extern(.*)')
	var = re.compile(r'var (.*)=(.*)')
	add = re.compile(r'(.+)=(.+)\+(.+)')
	sub = re.compile(r'(.+)=(.+)\-(.+)')
	ana = re.compile(r'(.+)=(.+)\&(.+)')
	ora = re.compile(r'(.+)=(.+)\|(.+)')
	slop = re.compile(r'loop(.+)')
	elop = re.compile(r'endloop(.*)')
	ifgt = re.compile(r'if (.*)>(.*)')
	ifgte = re.compile(r'endif(.*)')
	ifeq = re.compile(r'if (.*)=(.*)')
	for fileName in fileNames :
		inputFile = open(fileName, "r")
		fileName = fileName.split('.')[0]
		outFile = open(fileName+'.l','w')
		code = inputFile.read()
		lines = code.split('\n')
		newCode = []
		memaddr = 0
		loopctr = 0
		ifctr = 0
		ifjmp = {}
		symTable[fileName] = {}
		globTable[fileName] = {}
		for line in lines :
			line = line.lstrip().rstrip()
			if var.match(line):
				symTable[fileName][var.match(line).group(1).lstrip().rstrip()] = '#'+str(memaddr + 3)
				newCode.append('JMP #'+str(memaddr+4))
				newCode.append('DB '+var.match(line).group(2).lstrip().rstrip())
				memaddr = memaddr + 4
			elif glo.match(line):
				symTable[fileName][glo.match(line).group(1).lstrip().rstrip()] = '#'+str(memaddr + 3)
				globTable[fileName][glo.match(line).group(1).lstrip().rstrip()] = '#'+str(memaddr + 3)
				newCode.append('JMP #'+str(memaddr+4))
				newCode.append('DB '+glo.match(line).group(2).lstrip().rstrip())
				memaddr = memaddr + 4
			elif ext.match(line):
				symTable[fileName][ext.match(line).group(1).lstrip().rstrip()] = '$'+str(ext.match(line).group(1).lstrip().rstrip())
			elif add.match(line):
				x = add.match(line).group(1).lstrip().rstrip()
				y = add.match(line).group(2).lstrip().rstrip()
				z = add.match(line).group(3).lstrip().rstrip()
				if tryInt(y) and tryInt(z):
					newCode.append('MVI A,'+y)
					newCode.append('ADI '+z)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['MVI']
					memaddr += oplen['ADI']
					memaddr += oplen['STA']
				elif tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symTable[fileName][z]))
					newCode.append('ADI '+y)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['ADI']
					memaddr += oplen['STA']
				elif tryInt(z) and not tryInt(y):
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('ADI '+z)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['ADI']
					memaddr += oplen['STA']
				elif not tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('MOV B,A')
					newCode.append('LDA '+str(symTable[fileName][z]))
					newCode.append('ADD B')
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['MOV']
					memaddr += oplen['LDA']
					memaddr += oplen['ADD']
					memaddr += oplen['STA']
			elif sub.match(line):
				x = sub.match(line).group(1).lstrip().rstrip()
				y = sub.match(line).group(2).lstrip().rstrip()
				z = sub.match(line).group(3).lstrip().rstrip()
				if tryInt(y) and tryInt(z):
					newCode.append('MVI A,'+y)
					newCode.append('SUI '+z)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['MVI']
					memaddr += oplen['SUI']
					memaddr += oplen['STA']
				elif tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symTable[fileName][z]))
					newCode.append('SUI '+y)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['SUI']
					memaddr += oplen['STA']
				elif tryInt(z) and not tryInt(y):
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('SUI '+z)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['SUI']
					memaddr += oplen['STA']
				elif not tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('MOV B,A')
					newCode.append('LDA '+str(symTable[fileName][z]))
					newCode.append('SUB B')
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['MOV']
					memaddr += oplen['LDA']
					memaddr += oplen['SUB']
					memaddr += oplen['STA']
			elif ana.match(line):
				x = ana.match(line).group(1).lstrip().rstrip()
				y = ana.match(line).group(2).lstrip().rstrip()
				z = ana.match(line).group(3).lstrip().rstrip()
				if tryInt(y) and tryInt(z):
					newCode.append('MVI A,'+y)
					newCode.append('ANI '+z)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['MVI']
					memaddr += oplen['ANI']
					memaddr += oplen['STA']
				elif tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symTable[fileName][z]))
					newCode.append('ANI '+y)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['ANI']
					memaddr += oplen['STA']
				elif tryInt(z) and not tryInt(y):
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('ANI '+z)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['ANI']
					memaddr += oplen['STA']
				elif not tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('MOV B,A')
					newCode.append('LDA '+str(symTable[fileName][z]))
					newCode.append('ANA B')
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['MOV']
					memaddr += oplen['LDA']
					memaddr += oplen['ANA']
					memaddr += oplen['STA']
			elif ora.match(line):
				x = ora.match(line).group(1).lstrip().rstrip()
				y = ora.match(line).group(2).lstrip().rstrip()
				z = ora.match(line).group(3).lstrip().rstrip()
				if tryInt(y) and tryInt(z):
					newCode.append('MVI A,'+y)
					newCode.append('ORI '+z)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['MVI']
					memaddr += oplen['ORI']
					memaddr += oplen['STA']
				elif tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symTable[fileName][z]))
					newCode.append('ORI '+y)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['ORI']
					memaddr += oplen['STA']
				elif tryInt(z) and not tryInt(y):
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('ORI '+z)
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['ORI']
					memaddr += oplen['STA']
				elif not tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symTable[fileName][y]))
					newCode.append('MOV B,A')
					newCode.append('LDA '+str(symTable[fileName][z]))
					newCode.append('ORA B')
					newCode.append('STA '+str(symTable[fileName][x]))
					memaddr += oplen['LDA']
					memaddr += oplen['MOV']
					memaddr += oplen['LDA']
					memaddr += oplen['ORA']
					memaddr += oplen['STA']
			elif slop.match(line):
				x = slop.match(line).group(1).lstrip().rstrip()
				if tryInt(x):
					newCode.append('PUSH D')
					newCode.append('MVI E,'+x)
					memaddr += oplen['PUSH']
					memaddr += oplen['MVI']
					symTable[fileName][loopctr] = '#' + str(memaddr)
					loopctr += 1
				# else:
				# 	newCode.append('PUSH E')
				# 	newCode.append('MVI E,'+str(symTable[fileName][x]))
				# 	memaddr += oplen['PUSH']
				# 	memaddr += oplen['MVI']
				# 	symTable[fileName][loopctr] = memaddr
				# 	loopctr += 1
			elif elop.match(line):
				newCode.append('MOV A,E')
				newCode.append('SUI 1')
				newCode.append('MOV E,A')
				newCode.append('JNZ '+str(symTable[fileName][loopctr-1]))
				newCode.append('POP D')
				loopctr -= 1
				memaddr += oplen['MOV']
				memaddr += oplen['SUI']
				memaddr += oplen['MOV']
				memaddr += oplen['JNZ']
				memaddr += oplen['POP']
			elif ifgt.match(line):
				x = ifgt.match(line).group(1).lstrip().rstrip()
				y = ifgt.match(line).group(2).lstrip().rstrip()
				newCode.append('LDA '+str(symTable[fileName][x]))
				newCode.append('MOV B,A')
				newCode.append('LDA '+str(symTable[fileName][y]))
				newCode.append('SUB B')
				newCode.append('JP &&&'+str(ifctr))
				newCode.append('JZ &&&'+str(ifctr))
				ifctr += 1
				memaddr += oplen['LDA']
				memaddr += oplen['MOV']
				memaddr += oplen['LDA']
				memaddr += oplen['SUB']
				memaddr += oplen['JP']
				memaddr += oplen['JZ']
			elif ifeq.match(line):
				x = ifeq.match(line).group(1).lstrip().rstrip()
				y = ifeq.match(line).group(2).lstrip().rstrip()
				newCode.append('LDA '+str(symTable[fileName][x]))
				newCode.append('MOV B,A')
				newCode.append('LDA '+str(symTable[fileName][y]))
				newCode.append('SUB B')
				newCode.append('JNZ &&&'+str(ifctr))
				ifctr += 1
				memaddr += oplen['LDA']
				memaddr += oplen['MOV']
				memaddr += oplen['LDA']
				memaddr += oplen['SUB']
				memaddr += oplen['JNZ']
			elif ifgte.match(line):
				ifjmp[ifctr-1] = memaddr
			
		outFile.write('\n'.join(newCode))
		outFile.close()
		filelen[fileName] = memaddr
		################################
		inputFile = open(fileName+'.l','r')
		code = inputFile.read()
		lines = code.split('\n')
		newCode = []
		for line in lines :
			if '&&&' in line:
				tag = line.split(' ')[1]
				linenum = tag.split('&&&')[1].lstrip().rstrip()
				linenum = int(linenum)
				newtag = '#'+str(ifjmp[linenum])
				newCode.append(line.replace(tag, newtag))
			else:
				newCode.append(line)
		outFile = open(fileName+'.li','w')
		outFile.write('\n'.join(newCode))
		outFile.close()