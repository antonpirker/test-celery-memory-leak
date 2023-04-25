
## Setup

cd demo-cookiecutter-flask
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt


## Starting (in seperate shells)

./run-gunicorn.sh 
# note the PID

./run-celery.sh

psrecord <PID_OF_GUNICORN> --interval 1 --plot plot1.png

locust
# point browser to http://localhost:8089/
# start load test with 200 users to http://localhost:5000


After some time ctrl+c psrecord and look at plot1.png
