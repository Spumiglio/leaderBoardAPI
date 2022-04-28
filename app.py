from flask import Flask
from flask import jsonify, make_response
import sqlite3
app = Flask(__name__)

con = sqlite3.connect('db.sqlite', check_same_thread=False)

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
        return make_response(jsonify({"free":"false"}),200)

@app.route('/getUserScore/<username>')
def getUserScore(username):
    cur = con.cursor()
    resp = cur.execute('''SELECT scores FROM user_scores WHERE username = ?''',(username,)).fetchall()
    cur.close()
    return make_response(jsonify({username:resp[0][0]}))
@app.rout('/getScores/<num>')
def getScores(num):
    cur = con.cursor()
    res = cur.execute('''SELECT * FROM user_scores ORDER BY scores DESC LIMIT ?''',(num,)).fetchall()

    return make_response(jsonify(res))

if __name__ == '__main__':
    app.run()
