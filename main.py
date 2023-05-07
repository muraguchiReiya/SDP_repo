from flask import Flask, render_template
import psycopg2
from dotenv import load_dotenv
import os
load_dotenv()

# 環境変数を参照

user= os.getenv('USER_NAME')
pswd= os.getenv('PASS')
db=os.getenv('DBNAME')
host=os.getenv('HOST')

dsn = f"dbname={db} host={host} user={user} password={pswd}"

app = Flask(__name__)

@app.route('/')
def route():

    conn = psycopg2.connect(dsn)  # コネクション
    cur = conn.cursor()
    cur.execute("select * from temp;")
    result=cur.fetchone()
    conn.close()

    return render_template('index.html',data=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


