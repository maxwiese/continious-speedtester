from pymongo import MongoClient
import speedtest
import datetime

db_url = "mongodb://raspberrypi:27017"

client = MongoClient(db_url)
database = client.speedtest


speedtester = speedtest.Speedtest()
speedtester.get_best_server()

speedtester.download()

speedtester.upload(pre_allocate=False)

results = speedtester.results.dict()

speedtest = {
    'timestamp': datetime.datetime.now().timestamp(),
    'download': str(results['download']),
    'upoload': str(results['upload']),
    'ping': str(results['ping'])
}

result = database.speedtest.insert_one(speedtest)
print("insert speedtest with id {0}".format(result.inserted_id))