def loader( files ):
	offset = 0
	fl = files[0].split('.')[0]
	inputFile = open(fl+'.ls','r')
	code = inputFile.read()
	lines = code.split('\n')
	outFile = open(fl+'.8085','w')
	linkCode = []
	for line in lines :
		if '#' in line:
			tag = line.split(' ')[1]
			newtag = str((int(tag.split('#')[1]) + offset))
			linkCode.append(line.replace(tag, newtag))
		else:
			linkCode.append(line)
	linkCode.append('HLT')
	outFile.write('\n'.join(linkCode))
	outFile.close()