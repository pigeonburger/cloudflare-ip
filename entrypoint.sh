#!/bin/sh

main() {
  set -e

  echo "Now in entrypoint for CloudFlare DNS Auto Updater"
  echo "Script        1.1.0 (2022-01-04)"
  echo "User:         '$(whoami)'"
  echo "Group:        '$(id -g -n)'"
  echo "Working dir:  '$(pwd)'"
  echo ""

  echo "Inspecting enviroment variables"
  echo ""

  if [ -z "$ZONE_ID" ]; then
      cat >&2 <<EOF
ZONE_ID is empty
EOF
      exit 1
  else
      echo "ZONE_ID ok"
  fi

  if [ -z "$BEARER_TOKEN" ]; then
      cat >&2 <<EOF
BEARER_TOKEN is empty
EOF
      exit 1
  else
      echo "BEARER_TOKEN ok"
  fi

  if [ -z "$RECORD_ID" ]; then
      cat >&2 <<EOF
  RECORD_ID is empty
  EOF
      exit 1
  else
      echo "RECORD_ID ok"
  fi

  echo ""
  echo "Everything ok!"
  echo ""

  echo "Touching cfauth.ini"
  touch $APP_PATH/cfauth.ini

  echo "Writing cfauth.ini"
  echo "[tokens]" >> $APP_PATH/cfauth.ini
  echo "zone_id=$ZONE_ID" >> $APP_PATH/cfauth.ini
  echo "bearer_token=$BEARER_TOKEN" >> $APP_PATH/cfauth.ini
  echo "record_id=${RECORD_ID}" >> $APP_PATH/cfauth.ini
  echo "Done!"

  echo ""
  echo "Starting script"
  exec python $APP_PATH/cfautoupdater.py
}

main $@
