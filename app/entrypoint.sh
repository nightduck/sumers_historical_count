#!/bin/bash
declare -p | grep -Ev 'BASHOPTS|BASH_VERSINFO|EUID|PPID|SHELLOPTS|UID' > /container.env

python /app/app.py &

echo "SHELL=/bin/bash
BASH_ENV=/container.env
*/15 * * * * /usr/local/bin/python /app/scrape_gym.py
# This extra line makes it a valid cron" > scrape_cron.txt

crontab scrape_cron.txt
cron -f