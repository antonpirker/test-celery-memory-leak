from celery import Celery

app = Celery("tasks", broker="redis://localhost:6379/0")
app.conf.timezone = "Europe/London"


@app.task
def tell_the_world(msg):
    print("Thats my message to the world: %s" % msg)
