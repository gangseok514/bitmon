# bitmon
(In progress)
Virtual Currency Monitoring, Simulating, Trading platform

This platform is composed with the following components.

- Monitoring
  - Collector
  - Influxdb
  - Grafana

- Simulating and Trading(not implemented yet)
  - Django

## How to use
### Monitoring
1. Run docker compose
```bash
bitmon/monitoring$ docker-compose build
bitmon/monitoring$ docker-compose up -d
```
2. Open localhost:3000(ID/PW of grafana is admin/admin)
3. Done!

Current exchanges support: Bithumb, Coinone

## License
MIT
