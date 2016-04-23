import re

opCode_len = {}
symbol_table = {}
globTable = {}
file_size= {}

# def isvariable(line):
# 	var = re.compile(r'var (.+*)=(.+*)')


def tryInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def run( fileNames ):
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
	
	lines = open('lenopcodes.cf',"r").read().split('\n')
	for line in lines:
		if line != '' :
			opCode_len[line.split(' ')[0]] = int(line.split(' ')[1])
	
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
		symbol_table[fileName] = {}
		globTable[fileName] = {}
		for line in lines :
			line = line.lstrip().rstrip()
			if var.match(line):
				symbol_table[fileName][var.match(line).group(1).lstrip().rstrip()] = '#'+str(memaddr + 3)
				newCode.append('JMP #'+str(memaddr+4))
				newCode.append('DB '+var.match(line).group(2).lstrip().rstrip())
				memaddr = memaddr + 4
			elif glo.match(line):
				symbol_table[fileName][glo.match(line).group(1).lstrip().rstrip()] = '#'+str(memaddr + 3)
				globTable[fileName][glo.match(line).group(1).lstrip().rstrip()] = '#'+str(memaddr + 3)
				newCode.append('JMP #'+str(memaddr+4))
				newCode.append('DB '+glo.match(line).group(2).lstrip().rstrip())
				memaddr = memaddr + 4
			elif ext.match(line):
				symbol_table[fileName][ext.match(line).group(1).lstrip().rstrip()] = '$'+str(ext.match(line).group(1).lstrip().rstrip())
			elif add.match(line):
				x = add.match(line).group(1).lstrip().rstrip()
				y = add.match(line).group(2).lstrip().rstrip()
				z = add.match(line).group(3).lstrip().rstrip()
				if tryInt(y) and tryInt(z):
					newCode.append('MVI A,'+y)
					newCode.append('ADI '+z)
					newCode.append('STA '+str(symbol_table[fileName][x]))
					memaddr += opCode_len['MVI']
					memaddr += opCode_len['ADI']
					memaddr += opCode_len['STA']
				elif tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symbol_table[fileName][z]))
					newCode.append('ADI '+y)
					newCode.append('STA '+str(symbol_table[fileName][x]))
					memaddr += opCode_len['LDA']
					memaddr += opCode_len['ADI']
					memaddr += opCode_len['STA']
				elif tryInt(z) and not tryInt(y):
					newCode.append('LDA '+str(symbol_table[fileName][y]))
					newCode.append('ADI '+z)
					newCode.append('STA '+str(symbol_table[fileName][x]))
					memaddr += opCode_len['LDA']
					memaddr += opCode_len['ADI']
					memaddr += opCode_len['STA']
				elif not tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symbol_table[fileName][y]))
					newCode.append('MOV B,A')
					newCode.append('LDA '+str(symbol_table[fileName][z]))
					newCode.append('ADD B')
					newCode.append('STA '+str(symbol_table[fileName][x]))
					memaddr += opCode_len['LDA']
					memaddr += opCode_len['MOV']
					memaddr += opCode_len['LDA']
					memaddr += opCode_len['ADD']
					memaddr += opCode_len['STA']
			elif sub.match(line):
				x = sub.match(line).group(1).lstrip().rstrip()
				y = sub.match(line).group(2).lstrip().rstrip()
				z = sub.match(line).group(3).lstrip().rstrip()
				if tryInt(y) and tryInt(z):
					newCode.append('MVI A,'+y)
					newCode.append('SUI '+z)
					newCode.append('STA '+str(symbol_table[fileName][x]))
					memaddr += opCode_len['MVI']
					memaddr += opCode_len['SUI']
					memaddr += opCode_len['STA']
				elif tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symbol_table[fileName][z]))
					newCode.append('SUI '+y)
					newCode.append('STA '+str(symbol_table[fileName][x]))
					memaddr += opCode_len['LDA']
					memaddr += opCode_len['SUI']
					memaddr += opCode_len['STA']
				elif tryInt(z) and not tryInt(y):
					newCode.append('LDA '+str(symbol_table[fileName][y]))
					newCode.append('SUI '+z)
					newCode.append('STA '+str(symbol_table[fileName][x]))
					memaddr += opCode_len['LDA']
					memaddr += opCode_len['SUI']
					memaddr += opCode_len['STA']
				elif not tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symbol_table[fileName][y]))
					newCode.append('MOV B,A')
					newCode.append('LDA '+str(symbol_table[fileName][z]))
					newCode.append('SUB B')
					newCode.append('STA '+str(symbol_table[fileName][x]))
					memaddr += opCode_len['LDA']
					memaddr += opCode_len['MOV']
					memaddr += opCode_len['LDA']
					memaddr += opCode_len['SUB']
					memaddr += opCode_len['STA']
			elif ana.match(line):
				x = ana.match(line).group(1).lstrip().rstrip()
				y = ana.match(line).group(2).lstrip().rstrip()
				z = ana.match(line).group(3).lstrip().rstrip()
				if tryInt(y) and tryInt(z):
					newCode.append('MVI A,'+y)
					newCode.append('ANI '+z)
					newCode.append('STA '+str(symbol_table[fileName][x]))
					memaddr += opCode_len['MVI']
					memaddr += opCode_len['ANI']
					memaddr += opCode_len['STA']
				elif tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symbol_table[fileName][z]))
					newCode.append('ANI '+y)
					newCode.append('STA '+str(symbol_table[fileName][x]))
					memaddr += opCode_len['LDA']
					memaddr += opCode_len['ANI']
					memaddr += opCode_len['STA']
				elif tryInt(z) and not tryInt(y):
					newCode.append('LDA '+str(symbol_table[fileName][y]))
					newCode.append('ANI '+z)
					newCode.append('STA '+str(symbol_table[fileName][x]))
					memaddr += opCode_len['LDA']
					memaddr += opCode_len['ANI']
					memaddr += opCode_len['STA']
				elif not tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symbol_table[fileName][y]))
					newCode.append('MOV B,A')
					newCode.append('LDA '+str(symbol_table[fileName][z]))
					newCode.append('ANA B')
					newCode.append('STA '+str(symbol_table[fileName][x]))
					memaddr += opCode_len['LDA']
					memaddr += opCode_len['MOV']
					memaddr += opCode_len['LDA']
					memaddr += opCode_len['ANA']
					memaddr += opCode_len['STA']
			elif ora.match(line):
				x = ora.match(line).group(1).lstrip().rstrip()
				y = ora.match(line).group(2).lstrip().rstrip()
				z = ora.match(line).group(3).lstrip().rstrip()
				if tryInt(y) and tryInt(z):
					newCode.append('MVI A,'+y)
					newCode.append('ORI '+z)
					newCode.append('STA '+str(symbol_table[fileName][x]))
					memaddr += opCode_len['MVI']
					memaddr += opCode_len['ORI']
					memaddr += opCode_len['STA']
				elif tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symbol_table[fileName][z]))
					newCode.append('ORI '+y)
					newCode.append('STA '+str(symbol_table[fileName][x]))
					memaddr += opCode_len['LDA']
					memaddr += opCode_len['ORI']
					memaddr += opCode_len['STA']
				elif tryInt(z) and not tryInt(y):
					newCode.append('LDA '+str(symbol_table[fileName][y]))
					newCode.append('ORI '+z)
					newCode.append('STA '+str(symbol_table[fileName][x]))
					memaddr += opCode_len['LDA']
					memaddr += opCode_len['ORI']
					memaddr += opCode_len['STA']
				elif not tryInt(y) and not tryInt(z):
					newCode.append('LDA '+str(symbol_table[fileName][y]))
					newCode.append('MOV B,A')
					newCode.append('LDA '+str(symbol_table[fileName][z]))
					newCode.append('ORA B')
					newCode.append('STA '+str(symbol_table[fileName][x]))
					memaddr += opCode_len['LDA']
					memaddr += opCode_len['MOV']
					memaddr += opCode_len['LDA']
					memaddr += opCode_len['ORA']
					memaddr += opCode_len['STA']
			elif slop.match(line):
				x = slop.match(line).group(1).lstrip().rstrip()
				if tryInt(x):
					newCode.append('PUSH D')
					newCode.append('MVI E,'+x)
					memaddr += opCode_len['PUSH']
					memaddr += opCode_len['MVI']
					symbol_table[fileName][loopctr] = '#' + str(memaddr)
					loopctr += 1
				# else:
				# 	newCode.append('PUSH E')
				# 	newCode.append('MVI E,'+str(symbol_table[fileName][x]))
				# 	memaddr += opCode_len['PUSH']
				# 	memaddr += opCode_len['MVI']
				# 	symbol_table[fileName][loopctr] = memaddr
				# 	loopctr += 1
			elif elop.match(line):
				newCode.append('MOV A,E')
				newCode.append('SUI 1')
				newCode.append('MOV E,A')
				newCode.append('JNZ '+str(symbol_table[fileName][loopctr-1]))
				newCode.append('POP D')
				loopctr -= 1
				memaddr += opCode_len['MOV']
				memaddr += opCode_len['SUI']
				memaddr += opCode_len['MOV']
				memaddr += opCode_len['JNZ']
				memaddr += opCode_len['POP']
			elif ifgt.match(line):
				x = ifgt.match(line).group(1).lstrip().rstrip()
				y = ifgt.match(line).group(2).lstrip().rstrip()
				newCode.append('LDA '+str(symbol_table[fileName][x]))
				newCode.append('MOV B,A')
				newCode.append('LDA '+str(symbol_table[fileName][y]))
				newCode.append('SUB B')
				newCode.append('JP &&&'+str(ifctr))
				newCode.append('JZ &&&'+str(ifctr))
				ifctr += 1
				memaddr += opCode_len['LDA']
				memaddr += opCode_len['MOV']
				memaddr += opCode_len['LDA']
				memaddr += opCode_len['SUB']
				memaddr += opCode_len['JP']
				memaddr += opCode_len['JZ']
			elif ifeq.match(line):
				x = ifeq.match(line).group(1).lstrip().rstrip()
				y = ifeq.match(line).group(2).lstrip().rstrip()
				newCode.append('LDA '+str(symbol_table[fileName][x]))
				newCode.append('MOV B,A')
				newCode.append('LDA '+str(symbol_table[fileName][y]))
				newCode.append('SUB B')
				newCode.append('JNZ &&&'+str(ifctr))
				ifctr += 1
				memaddr += opCode_len['LDA']
				memaddr += opCode_len['MOV']
				memaddr += opCode_len['LDA']
				memaddr += opCode_len['SUB']
				memaddr += opCode_len['JNZ']
			elif ifgte.match(line):
				ifjmp[ifctr-1] = memaddr
			
		outFile.write('\n'.join(newCode))
		outFile.close()
		file_size[fileName] = memaddr
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