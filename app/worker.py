import os
import sys
import redis
import django

from rq import Worker, Queue, Connection

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
sys.path.insert(0, "..")
sys.path.insert(0, "../..")

django.setup()

listen = ['high', 'default', 'low']

#redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

#conn = redis.from_url(redis_url)

myHostname = "cowtools.redis.cache.windows.net"
myPassword = "WPJVKQt0LVSy1k26RzvrBYalGCGhB4gVqAzCaN8AtNY="
print("Start")
conn = redis.StrictRedis(host=myHostname, port=6380,
                      password=myPassword, ssl=True)
print("End")
if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()