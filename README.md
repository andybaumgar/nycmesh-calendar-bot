# nycmesh-calendar-bot

Automatically create calendar events based on Slack messages

## Dev Setup

Ensure you have Python 3.11
clone repo
cd nycmesh-calendar-bot
Setup venv (generally you can instruct your IDE to do this automatically)
pip install -e .

### Build and Run with Docker Locally

docker build -t calendar-bot .
docker run --env-file=.env calendar-bot

### Push to Dockerhub

login to Dockerhub
docker build -t andybaumgar/nycmesh-calendar-bot .
docker push andybaumgar/nycmesh-calendar-bot
