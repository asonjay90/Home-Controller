#!/bin/bash

API_URL="http://room-controller/alive"
FE_URL="http://room-controller:88"

echo "$1"
if [[ "$1" == "restart" ]]
  then
    echo "Restarting API"
    ps aux | grep api | awk '{print $2}' | xargs kill
fi

API_STATUS=$(curl -Is $API_URL | awk 'NR==1 {print $2}')

if [[ $API_STATUS == 200 ]]
  then
    echo "API Status: Good"
  else
    echo "API Status: Bad"
    /usr/sbin/ssmtp asonjay90@gmail.com < /home/jason/Home-Controller/email_notification.txt
    ps aux | grep api | awk '{print $2}' | sudo xargs kill
    echo "Killing and Restarting API"
    sudo /home/jason/Home-Controller/api.py &
fi

FE_STATUS=$(curl -Is $FE_URL | awk 'NR==1 {print $2}')

if [[ $FE_STATUS == 200 ]]
  then
    echo "Front End Status: Good"
  else
    echo "Front End Status: Bad"
    /usr/sbin/ssmtp asonjay90@gmail.com < /home/jason/Home-Controller/$
    ps aux | grep http | awk '{print $2}' | sudo xargs kill
    echo "Killing HTTP server and restarting"
    sudo python /home/jason/Home-Controller/Front-End/http_server.py &
fi


