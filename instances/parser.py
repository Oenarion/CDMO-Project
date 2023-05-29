def parseInstance(fileName):
    '''
    param: the file that must be parsed
    return a tuple containing m, n, l, s, D
    D is a list of lists
    '''
    # try:
    #     file = open(fileName, "r")
    # except:
    #     print("error, file not found")
    try:
        file = open(f"instances/{fileName}", "r")
    except:
        print("error, file not found")
        exit(0)
    content = file.read()
    rows = content.split('\n')
    m = int(rows[0])
    n = int(rows[1])
    l = parseLine(rows[2])
    s = parseLine(rows[3])

    D = []
    for i in range(4, len(rows)-1):
        parsedLine = parseLine(rows[i])
        D.append(parsedLine)

    return (m, n, l, s, D)

def parseLine(line):
    columns = line.split(' ')
    res = []
    for x in columns:
        if x != '':
            res.append(int(x))
    return res

def getMinizincInstance(fileName):
    m, n, l, s, D = parseInstance(fileName)
    res = f"m={m};n={n};l={l};s={s};D=\n["
    for i in range(len(D)):
        for j in range(len(D[i])):
            if j == 0:
                res += f"|"
            res += f"{D[i][j]}"
            if j != len(D[i])-1:
                res += f"," 
            if i == len(D)-1 and j == len(D[i])-1:
                res += f"|];"
        res += f"\n"
    return res

def main():
    print(parseInstance('inst01.dat'))

if __name__ == "__main__":
    main()
    
