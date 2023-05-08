import datetime

dt_now = datetime.datetime.now()
dt_now=dt_now.strftime('%Y%m%d%H%M')
sql=f'INSERT INTO temp VALUES("{dt_now}",20)'