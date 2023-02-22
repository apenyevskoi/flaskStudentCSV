from flask import Flask, request, abort

app = Flask('__name__')

studLst = []

def checkId(id):
    print(studLst, id)
    for i in studLst:
        if i['id'] == id:
            return True
    return False


def removeDBduplicates(studL):
    tmpL = studL
    for dict in tmpL:
        if studL.count(dict) > 1:
            studL.pop(studL.index(dict))
    return studL


@app.route('/', methods=['POST'])
def postDataJSON():
    if not request.get_json() or checkId(request.get_json()['id']) == False:
        abort(400)
    content = request.get_json()
    try:
        stud = {
            'id' : int(content['id']),
            'name' : content['name'],
            'class' : content['class']
        }
        studLst.append(stud)
        with open('database.csv', 'a') as dbCSV:
            dbCSV.write( str( stud['id'] ) + ',' + stud['name'] + ',' + stud['class'] + '\n' )
        dbCSV.close()
    except BaseException:
        print('here')
        print('error')
    return 'Ok'


@app.route('/', methods=['PUT'])
def getDataJSON():
    if not request.get_json() or not checkId(request.get_json()['id']):
        return '400, id not in DB'
    try:
        content = request.get_json( )
        for i in studLst:
            if i['id'] == content['id']:
                studLst.pop(studLst.index(i))
                studLst.append(content)
                with open('database.csv', 'w') as dbCSV:
                    for i in studLst:
                        dbCSV.write( str( i['id'] ) + ',' + i['name'] + ',' + i['class'] + '\n' )
                dbCSV.close()
        print(studLst)
        return 'Ok'
    except BaseException:
        print('here3')
        return 'error'


if __name__ == '__main__':
    try:
        with open('database.csv') as dbCSV:
            for line in dbCSV:
                if line not in ['\n', '\r\n']:
                    d = {
                        'id' : int(line.split(',')[0].strip()),
                        'name': line.split( ',' )[1].strip(),
                        'class': line.split( ',' )[2].strip()
                    }
                    studLst.append(d)
        dbCSV.close()
        with open('database.csv', 'w') as dbCSV:
            studLst = removeDBduplicates(studLst)
            for i in studLst:
                dbCSV.write(str(i['id']) + ',' + i['name'] + ',' + i['class'] + '\n')
        dbCSV.close()
    except (ValueError):
        print('error')
    app.run(debug=True)