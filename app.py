from flask import Flask
from flask import jsonify, make_response
import sqlite3
app = Flask(__name__)

con = sqlite3.connect('G:\leaderBoardAPI\db.sqlite', check_same_thread=False)

def checkUsername(username):
    cur = con.cursor()
    cur.execute('''SELECT * FROM user_scores WHERE username =:user;''', {"user":username})
    result = cur.fetchall()
    cur.close()
    if len(result) == 0:
        return True
    else:
        return False

@app.route('/createUser/<username>')
def createUsername(username):
    if checkUsername(username):
        cur = con.cursor()
        resp = cur.execute('''INSERT INTO user_scores VALUES(?,?)''',(username,0)).fetchall()
        con.commit()
        cur.close()
        if len(resp) == 0:
            return "OK"
        else:
            return "ERROR"
    else:
        return "ALREADY USED"

def getUserScore(username):
    cur = con.cursor()
    resp = cur.execute('''SELECT scores FROM user_scores WHERE username = ?''',(username,)).fetchall()
    cur.close()
    return resp

@app.route('/getScores')
def getScores():
    cur = con.cursor()
    res = cur.execute('''SELECT * FROM user_scores ORDER BY scores DESC ''',).fetchall()
    cur.close()
    string = ""
    for i in res:
        string += i[0]+"|"+str(i[1])+"\n"
    return string


@app.route('/uploadScore/<username>/<score>')
def uploadScore(username,score):
    cur = con.cursor()
    current = getUserScore(username)
    current = current[0]
    if int(current[0]) < int(score):
        res = cur.execute('''UPDATE user_scores set scores = ? WHERE username = ?''', (score,username))
    con.commit()
    cur.close()
    return "OK"

@app.route('/resetPlayer/<username>')
def resetPlayer(username):
    cur = con.cursor()
    res = cur.execute('''DELETE FROM user_scores WHERE username = ?''', (username,)).fetchall()
    cur.close()
    if len(res) == 0:
        return "OK"
    else:
        return "ERROR"

if __name__ == '__main__':
    app.run()
