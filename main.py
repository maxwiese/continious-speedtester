import speedtest
import datetime
import sqlite3

speedtester = speedtest.Speedtest()
speedtester.get_best_server()

print("test downloading ...")
speedtester.download()

print("test uploading ...")
speedtester.upload()

print("results ...")
results = speedtester.results.dict()

print("download:")
print(results['download'] + " bits/s")

print("upload:")
print(results['upload'] + " bits/s")

print("ping:")
print(results['ping'] " ms")