from flask import Flask
from flask import jsonify, make_response
import sqlite3
app = Flask(__name__)

def checkUsername(username):
    con = sqlite3.connect('db.sqlite', check_same_thread=False)
    cur = con.cursor()
    cur.execute('''SELECT * FROM user_scores WHERE username =:user;''', {"user":username})
    result = cur.fetchall()
    cur.close()
    con.close()
    if len(result) == 0:
        return True
    else:
        return False

@app.route('/createUser/<username>')
def createUsername(username):
    con = sqlite3.connect('db.sqlite', check_same_thread=False)
    if checkUsername(username):
        cur = con.cursor()
        resp = cur.execute('''INSERT INTO user_scores VALUES(?,?)''',(username,0)).fetchall()
        con.commit()
        cur.close()
        con.close()
        if len(resp) == 0:
            return "OK"
        else:
            return "ERROR"
    else:
        con.close()
        return "ALREADY USED"

def getUserScore(username):
    con = sqlite3.connect('db.sqlite', check_same_thread=False)
    cur = con.cursor()
    resp = cur.execute('''SELECT scores FROM user_scores WHERE username = ?''',(username,)).fetchall()
    cur.close()
    con.close()
    return resp

@app.route('/getScores')
def getScores():
    con = sqlite3.connect('db.sqlite', check_same_thread=False)
    cur = con.cursor()
    res = cur.execute('''SELECT * FROM user_scores ORDER BY scores DESC ''',).fetchall()
    cur.close()
    con.close()
    string = ""
    for i in res:
        string += i[0]+"|"+str(i[1])+"\n"
    return string


@app.route('/uploadScore/<username>/<score>')
def uploadScore(username,score):
    con = sqlite3.connect('db.sqlite', check_same_thread=False)
    cur = con.cursor()
    current = getUserScore(username)
    current = current[0]
    if int(current[0]) < int(score):
        res = cur.execute('''UPDATE user_scores set scores = ? WHERE username = ?''', (score,username))
    con.commit()
    cur.close()
    con.close()
    return "OK"

@app.route('/resetPlayer/<username>')
def resetPlayer(username):
    con = sqlite3.connect('db.sqlite', check_same_thread=False)
    cur = con.cursor()
    res = cur.execute('''UPDATE user_scores set scores = 0 WHERE username = ?''', (username,)).fetchall()
    cur.close()
    con.close()
    if len(res) == 0:
        return "OK"
    else:
        return "ERROR"

if __name__ == '__main__':
    app.run()
