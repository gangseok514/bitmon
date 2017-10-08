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

### How to use
Monitoring
```bash
docker-compose up -d
```
and open localhost:3000

ID/PW of grafana is admin/admin

Current exchanges support: Bithumb, Coinone, Korbit

## License
MIT
