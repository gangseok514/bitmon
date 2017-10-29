#!/bin/bash

set -euo pipefail

retry=10
timeouted=false
wait_for_ready() {
    sleep 10
    set +e
    echo "Checking if Grafana is ready"
    while ! response_code=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api/health) || test $response_code != "200"
    do
        sleep 10
        (( retry -= 1 )) || :
        if (( retry == 0 )) ; then
            timeouted=true
            break
        fi
    done
    set -e

    if [ $timeouted = true ] ; then
        echo "Timed out waiting for Grafana to be ready"
    else
        echo "Grafana is ready"
        echo "Add datasource"
        curl 'http://localhost:3000/api/datasources' -u admin:admin -X POST -H "Content-Type: application/json" --data-binary '
        {
            "name":"influxdb",
            "type":"influxdb",
            "url":"http://influxdb:8086",
            "access":"proxy",
            "basicAuth":false,
            "database": "bitmon"
        }'
        return 0
    fi
    exit 1
}

wait_for_ready &
./run.sh