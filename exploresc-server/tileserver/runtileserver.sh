#!/bin/bash

# Start the first process
echo 'Start postgresql database'
service postgresql start
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start postgresql: $status"
  exit $status
fi

# Start the second process
echo 'Start apache server'
service apache2 start
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start apache2: $status"
  exit $status
fi
#wait for database to start up :/
echo 'waiting for database...'
sleep 10s

# Start the third process
echo 'Start renderd service'
renderd -c /usr/local/etc/renderd.conf
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start renderd: $status"
  exit $status
fi

#check that all processes are still running otherwise exit
while sleep 60; do
  ps aux | grep postgresql | grep -v grep
  PROCESS_1_STATUS=$?
  ps aux | grep apache2 | grep -v grep
  PROCESS_2_STATUS=$?
  ps aux | grep renderd | grep -v grep
  PROCESS_3_STATUS=$?

  # If the greps above find anything, they exit with 0 status
  # If they are not both 0, then something is wrong
  if [ "$PROCESS_1_STATUS" -ne '0' ] || [ "$PROCESS_2_STATUS" -ne '0' ] || [ "$PROCESS_3_STATUS" -ne '0' ]; then
    echo "One of the processes has already exited."
    exit -1
  fi
done

