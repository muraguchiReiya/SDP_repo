from flask import Flask, render_template
import psycopg2
from dotenv import load_dotenv
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import ticker

load_dotenv()

user= os.getenv('USER_NAME')
pswd= os.getenv('PASS')
db=os.getenv('DBNAME')
host=os.getenv('HOST')

dsn = f"dbname={db} host={host} user={user} password={pswd}"

app = Flask(__name__)

def create_image(df):
    time=df['time'].dt.strftime('%Y-%m-%d-%H:%M')
    sns.set()
    fig, ax = plt.subplots(figsize=(15,5))
    ax.plot(time, df['temp'])
    ax.set(xlabel='time', ylabel='temp')
    ax.legend()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
    labels = ax.get_xticklabels()
    plt.setp(labels
             #, rotation=90
     )
    plt.savefig('./static/image/temp.png', bbox_inches='tight', pad_inches=0)

    plt.clf()
    fig, ax = plt.subplots(figsize=(15, 10))
    sns.distplot(df['temp'], kde=False, rug=False)
    plt.savefig('./static/image/hist.png', bbox_inches='tight', pad_inches=0)


def create_dict(df):
    value=[]
    for i in range(len(df)):
        data={'time':df.iat[i,2],'temp':df.iat[i,1]}
        value.append(data)
    value=list(reversed(value))
    return value

@app.route('/')
def route():
    sql= 'SELECT * FROM temp;'
    conn = psycopg2.connect(dsn)
    df = pd.read_sql(sql=sql, con=conn)
    df['time']=pd.to_datetime(df['time'])
    df['view_time']=df['time'].dt.strftime('%Y年%m月%d日%H時%M分')
    conn.close()
    create_image(df)
    data=create_dict(df)

    return render_template('SDP_demo.html',data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

