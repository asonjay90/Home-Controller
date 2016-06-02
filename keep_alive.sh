#!/bin/bash

URL="room-controller/alive"
STATUS=$(curl "$URL" -m 10)

if [[ "$STATUS" == "True" ]]
  then
    echo "Still looks good!"
  else
    /usr/sbin/ssmtp asonjay90@gmail.com < /home/jason/server2/email_notification.txt
    ps aux | grep api | awk '{print $2}' | xargs kill
    echo "killing api and restarting"
    sudo /home/jason/server2/api.py &
fi

