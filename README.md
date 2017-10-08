# bitmon
(In progress)
Virtual Currency Monitoring, Simulating, Trading platform

This platform is composed with the following components.

- Monitoring
  - Influxdb
  - Fluentd
  - Grafana

- Simulating and Trading(not implemented yet)
  - Django

## How to use
### Monitoring
1. Run docker compose
```bash
docker-compose up -d
```
2. Open localhost:3000(ID/PW of grafana is admin/admin)
3. Import dashboard: monitoring/grafana/bitmon-dashboard.json

Current exchanges support: Bithumb, Coinone, Korbit

## License
MIT
