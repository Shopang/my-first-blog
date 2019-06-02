from flask import Flask, request, url_for, redirect
from werkzeug import secure_filename
import os.path
import datetime

def getInfos(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    # id, pw = [], []
    infos = []
    for line in lines:
        t = line.split(':')
        infos.append((t[0], t[1]))
        # id.append(t[0])
        # pw.append(t[1])

    return infos

def findId(filename, text):
    infos = getInfos(filename)
    for id in infos:
        if str(id[0]) == text:
            return True
    return False

def checkInfo(filename, id, pw):
    infos = getInfos(filename)
    for info in infos:
        if info[0] == id and info[1][:-1] == pw: # info[1]->비밀번호. 마지막의 '\n' 제거.
            return True
    return False

def writeInfo(filename, id, pw):
    f = open(filename, 'a')
    f.write('{}:{}\n'.format(id, pw))
    f.close()

def readJustLine(filename, i):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    if i+1 > len(lines):
        return 'error\n'
    return lines[i]

def writeString(filename, string):
    f = open(filename, 'a')
    f.write('{}\n'.format(string))
    f.close()

def makeFile(filename):
    if not os.path.isfile(filename): # 파일 확인
        f = open(filename, 'w')
        f.close()

def saveId(filename, id):
    f = open(filename, 'w')
    f.write(id)
    f.close()

filepath = 'c:/test/info_test.txt'
# path_filename = 'c:/test/path_test.txt'
basic_path = 'c:/test/'
sIdPath = basic_path + 'name4Id.txt'
fileSavePath = 'C:/Users/Deep-Learning/PycharmProjects/photo_cloud_flask/uploads/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'C:/Users/Deep-Learning/PycharmProjects/photo_cloud_flask/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
app.config['MAX_CONTENT_PATH'] = 100 * 1024 * 1024

@app.route('/', methods=['GET', 'POST'])
def route():
    a = request.form['id']
    b = request.form['pw']
    # return str(int(a) + int(b))
    return 'basic'

@app.route('/Reg', methods=['POST']) # 회원가입 버튼
def register():
    id = request.form['id']
    pw = request.form['pw']
    print('id: {}, pw: {}'.format(id, pw))

    if findId(filepath, id) == True:
        return 'false'

    writeInfo(filepath, id, pw)
    return 'true'

@app.route('/Login', methods=['POST']) # 로그인 버튼
def login():
    id = request.form['id']
    pw = request.form['pw']

    if checkInfo(filepath, id, pw) == False:
        return 'false'

    # newPath = id + '_path'
    # filepath = makeFile(newPath)
    # filepath = newPath
    makeFile('{0}path_{1}.txt'.format(basic_path, id))

    saveId(sIdPath, id)
    return 'true'

@app.route('/fileUpload', methods = ['GET', 'POST'])
def upload_file():
    # if request.method == 'POST':
    f = request.files['file']
    r = readJustLine(sIdPath, 0)

    # 저장할 경로 + 파일명
    f.save(fileSavePath + r + datetime.datetime.now().strftime('_%Y-%m-%d_%H-%M-%S.jpg'))

    return 'true'

@app.route('/Path', methods = ['POST'])
def savePath():
    path = request.form['path']
    path_filename = request.form['path_filename']
    writeString(path_filename, path)
    return 'true'

@app.route('/PathList', methods=['POST'])
def pathList():
    n = request.form['n']
    path_filename = request.form['path_filename']

    if n != '':
        check = readJustLine(path_filename, int(n))[:-1]
        if 'error' in check:
            return 'false'
        return check
    return ['']

if __name__ == '__main__':
    app.run(host='192.168.10.3', debug=True)


