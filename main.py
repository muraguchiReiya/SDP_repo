from flask import Flask, render_template
import psycopg2
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

user= os.getenv('USER_NAME')
pswd= os.getenv('PASS')
db=os.getenv('DBNAME')
host=os.getenv('HOST')

dsn = f"dbname={db} host={host} user={user} password={pswd}"

app = Flask(__name__)

def create_dict(df):
    value=[]
    for i in range(len(df)):
        data={'time':df.iat[i,0],'temp':df.iat[i,1]}
        value.append(data)
    value=list(reversed(value))
    return value

@app.route('/')
def route():
    sql= 'SELECT * FROM temp;'
    conn = psycopg2.connect(dsn)
    df = pd.read_sql(sql=sql, con=conn)
    df['time']=pd.to_datetime(df['time']).dt.strftime('%Y年%m月%d日%H時%M分')
    conn.close()

    data=create_dict(df)

    return render_template('SDP_demo.html',data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

