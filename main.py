import json
import threading
import time
import speedtest
import paho.mqtt.client as mqtt

broker_url = "mosquitto"
time_to_sleep = 60 * 5


class TaskThread(threading.Thread):
    def __init__(self, task, args):
        threading.Thread.__init__(self)
        self.task = task
        self.args = args
        self._stop = threading.Event()

    def run(self):
        while True:
            if self.stopped():
                return
            self.task(*self.args)
            time.sleep(time_to_sleep)

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()


def on_connect(client, userdata, flags, rc):
    taskthread.start()
    pass


def publish_data(client, measures):
    print("publishing")
    client.publish('sensors/internet/speed', json.dumps(measures), qos=0, retain=True)


def measure_internet_connection(speedtester):
    print("measure internet connection")
    speedtester.get_best_server()

    speedtester.download()
    print("download finish")

    speedtester.upload(pre_allocate=False)
    print("upload finish")

    results = speedtester.results.dict()

    return {
        'download': str(results['download']),
        'upoload': str(results['upload']),
        'ping': str(results['ping'])
    }


def task(client, speedtester):
    result = measure_internet_connection(speedtester)
    publish_data(client, result)

if __name__ == "__main__":
    # setup speedtester
    speedtester = speedtest.Speedtest()

    # setup mqtt client
    client = mqtt.Client()
    client.on_connect = on_connect

    # setup worker
    taskthread = TaskThread(task, (client, speedtester))

    # connect to mqtt
    client.connect(broker_url, 1883, 60)

    try:
        client.loop_forever()
    except:
        taskthread.stop()
