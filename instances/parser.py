def parseInstance(fileName):
    '''
    param: the file that must be parsed
    return a tuple containing m, n, l, s, D
    D is a list of lists
    '''

    file = open(fileName, "r")
    content = file.read()
    rows = content.split('\n')
    m = int(rows[0])
    n = int(rows[1])
    l = parseLine(rows[2])
    s = parseLine(rows[3])

    D = []
    for i in range(4, len(rows)-1):
        parsedLine = parseLine(rows[i])
        D.append(parsedLine[:len(parsedLine)-1])

    return (m, n, l, s, D)

def parseLine(line):
    columns = line.split(' ')
    return columns

