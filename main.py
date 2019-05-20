import speedtest
import datetime
import sqlite3

db_conn = sqlite3.connect('speedtest.db')
cursor = db_conn.cursor()

cursor.execute(''' CREATE TABLE IF NOT EXISTS test (timestamp text, download text, upload text, ping text) ''')

speedtester = speedtest.Speedtest()
speedtester.get_best_server()

print("test downloading ...")
speedtester.download()

print("test uploading ...")
speedtester.upload(pre_allocate=False)

print("results ...")
results = speedtester.results.dict()

cursor.execute(''' INSERT INTO test VALUES (?,?,?,?) ''', (str(datetime.datetime.now().timestamp()), str(results['download']), str(results['upload']), str(results['ping'])))
db_conn.commit()
db_conn.close()

print("download:")
print(str(results['download']) + " bits/s")

print("upload:")
print(str(results['upload']) + " bits/s")

print("ping:")
print(str(results['ping']) + " ms")