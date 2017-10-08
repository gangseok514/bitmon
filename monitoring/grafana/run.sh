docker run \
  -d \
  -p 3000:3000 \
  --link influxdb:influxdb \
  --name=grafana \
  grafana/grafana