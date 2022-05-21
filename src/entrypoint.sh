#!/bin/sh

main() {
    set -e

    echo "Now in entrypoint for CloudFlare DNS Auto Updater"
    echo "Author:        DaruZero"
    echo "Created:       2022-01-19"
    echo "Started:       $(date '+%F %T')"
    echo ""

    echo "[INFO] - Inspecting enviroment variables"
    echo ""

    if [ -z "$ZONE_ID" ]; then
        echo "[ERROR] - ZONE_ID is empty"
        exit 1
    else
        echo "[INFO] - ZONE_ID ok"
    fi

    if [ -z "$EMAIL" ]; then
        echo "[ERROR] - EMAIL is empty"
        exit 1
    else
        echo "[INFO] - EMAIL ok"
    fi

    if [ -z "$AUTH_KEY" ]; then
        echo "[ERROR] - AUTH_KEY is empty"
        exit 1
    else
        echo "[INFO] - AUTH_KEY ok"
    fi

    if [ -z "$RECORD_ID" ]; then
        echo "[ERROR] - RECORD_ID is empty"
        exit 1
    elif expr "$RECORD_ID" : 'none' >/dev/null; then
        echo "[INFO] - RECORD_ID set to none. The script will check all the A records"
    else
        echo "[INFO] - RECORD_ID ok"
    fi

    if expr "$CHECK_INTERVAL" : '[0-9]*$' >/dev/null; then
        echo "[INFO] - CHECK_INTERVAL ok"
    else
        echo "[ERROR] - CHECK_INTERVAL must be a positive integer"
        exit 1
    fi

    echo ""
    echo "[INFO] - Everything ok!"
    echo ""
    echo "[INFO] - Starting script"
    exec python ./cfautoupdater.py
}

main $@
