FROM python:3.6

EXPOSE 5000

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

RUN apt-get update \
   && apt-get -y install --no-install-recommends cron \
   #
   # Clean up
   && apt-get autoremove -y \
   && apt-get clean -y \
   && rm -rf /var/lib/apt/lists/*

COPY app.py /app
COPY scrape_gym.py /app

COPY entrypoint.sh /entrypoint.sh
CMD /entrypoint.sh