# Statsd + Telegraf + InfluxDB + Grafana


## InfluxDB

### Dashboard

http://localhost:8083/

### Queries

```shell
SELECT derivative(mean("value")) FROM "net_requests" WHERE $timeFilter group by time(10s)
```


## Grafana

### Dashboard

http://localhost:3000/

### API examples

#### Login and store cookies in file

```shell
curl -v -c /tmp/curl-cookies -X POST -H 'Content-Type: application/json' -d '{"user": "admin", "password": "secret"}' 'http://localhost:3000/login'
```

#### Create an InfluxDB data source

```shell
curl -v -b /tmp/curl-cookies -X POST -H 'Content-Type: application/json' -d '{"access":"direct", "database": "telegraf", "name": "ds_influx", "type": "influxdb_08", "url": "http://influxdb:8086", "user": "", "password": ""}' 'http://localhost:3000/api/datasources'
```

#### Get data sources

```shell
curl -v -b /tmp/curl-cookies -X GET -H 'Accept: application/json' 'http://localhost:3000/api/datasources' | python -m json.tool
```

#### Get a dashboard

```shell
curl -v -b /tmp/curl-cookies -X GET -H 'Accept: application/json' 'http://localhost:3000/api/dashboards/db/dashboard-1' | python -m json.tool
```

#### Create a dashboard

```shell
curl -v -b /tmp/curl-cookies -X POST -H 'Content-Type: application/json' -d '{"dashboard": {}}' 'http://localhost:3000/api/dashboards/db'
```

See dashboard example in webapp-python


## TODO

- Move Grafana data source and dashboard creation out of webapp-python
