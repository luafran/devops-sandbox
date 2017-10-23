## Prometheus

### Percentage of requests served within 250ms (last 5 minutes)

```text
sum(rate(http_request_duration_seconds_bucket{le="0.25"}[5m])) by (job) / sum(rate(http_request_duration_seconds_count[5m])) by (job)
```

### Response time for 95% of requests

```text
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
```

### References

[Prometheus Best Practices - Histograms](https://prometheus.io/docs/practices/histograms/)


## Grafana

### Dashboard

http://localhost:3000/

### API examples

#### Login and store cookies in file

```shell
curl -v -b /tmp/curl-cookies -X GET -H 'Accept: application/json' 'http://localhost:3000/api/datasources' | python -m json.tool
```

#### Get all data sources

```shell
curl -v -b /tmp/curl-cookies -X GET -H 'Accept: application/json' 'http://localhost:3000/api/datasources' | python -m json.tool
```

#### Create a Prometheus data source

```shell
curl -v -b /tmp/curl-cookies -X POST -H 'Content-Type: application/json' -d '
{
    "access": "direct",
    "database": "",
    "name": "prom-2",
    "type": "prometheus",
    "url": "http://prometheus:9090",
    "withCredentials": false,
    "user": "",
    "password": "",
    "basicAuth": false,
    "basicAuthUser": "",
    "basicAuthPassword": ""
}' 'http://localhost:3000/api/datasources'
```

#### Create a dashboard

```shell
curl -v -b /tmp/curl-cookies -X POST -H 'Content-Type: application/json' -d '
{
	"dashboard": {
		"id": null,
		"title": "SLA",
		"version": 0,
		"schemaVersion": 12,
		"editable": true,
		"gnetId": null,
		"hideControls": false,
		"sharedCrosshair": false,
		"style": "dark",
		"links": [],
		"tags": [],
		"annotations": {
			"list": []
		},
		"templating": {
			"list": []
		},
		"timezone": "browser",
		"refresh": "10s",
		"time": {
			"from": "now-5m",
			"to": "now"
		},
		"timepicker": {
			"refresh_intervals": [
				"5s",
				"10s",
				"30s",
				"1m",
				"5m",
				"15m",
				"30m",
				"1h",
				"2h",
				"1d"
			],
			"time_options": [
				"5m",
				"15m",
				"1h",
				"6h",
				"12h",
				"24h",
				"2d",
				"7d",
				"30d"
			]
		},
		"rows": [{
				"collapse": false,
				"editable": true,
				"height": "250px",
				"panels": [{
					"aliasColors": {},
					"bars": false,
					"datasource": "prom-1",
					"editable": true,
					"error": false,
					"fill": 1,
					"grid": {
						"threshold1": 0.95,
						"threshold1Color": "rgba(216, 200, 27, 0.27)",
						"threshold2": 0.9,
						"threshold2Color": "rgba(234, 112, 112, 0.22)",
						"thresholdLine": true
					},
					"id": 1,
					"isNew": true,
					"legend": {
						"avg": false,
						"current": false,
						"max": false,
						"min": false,
						"show": true,
						"total": false,
						"values": false
					},
					"lines": true,
					"linewidth": 2,
					"links": [],
					"nullPointMode": "connected",
					"percentage": false,
					"pointradius": 5,
					"points": false,
					"renderer": "flot",
					"seriesOverrides": [],
					"span": 12,
					"stack": false,
					"steppedLine": false,
					"targets": [{
						"expr": "sum(rate(http_request_duration_seconds_bucket{le=\"0.25\"}[5m])) by (job) / sum(rate(http_request_duration_seconds_count[5m])) by (job)",
						"intervalFactor": 2,
						"refId": "A",
						"step": 2
					}],
					"timeFrom": null,
					"timeShift": null,
					"title": "Percentage of requests served below 250 ms.",
					"tooltip": {
						"msResolution": true,
						"shared": true,
						"sort": 0,
						"value_type": "cumulative"
					},
					"type": "graph",
					"xaxis": {
						"show": true
					},
					"yaxes": [{
							"format": "percentunit",
							"label": null,
							"logBase": 1,
							"max": 1,
							"min": 0,
							"show": true
						},
						{
							"format": "short",
							"label": null,
							"logBase": 1,
							"max": null,
							"min": null,
							"show": true
						}
					]
				}],
				"title": "Row1"
			},
			{
				"collapse": false,
				"editable": true,
				"height": "250px",
				"panels": [{
					"aliasColors": {},
					"bars": false,
					"datasource": "prom-1",
					"editable": true,
					"error": false,
					"fill": 1,
					"grid": {
						"threshold1": 0.2,
						"threshold1Color": "rgba(216, 200, 27, 0.27)",
						"threshold2": 0.5,
						"threshold2Color": "rgba(234, 112, 112, 0.22)",
						"thresholdLine": true
					},
					"id": 2,
					"isNew": true,
					"legend": {
						"avg": false,
						"current": false,
						"max": false,
						"min": false,
						"show": true,
						"total": false,
						"values": false
					},
					"lines": true,
					"linewidth": 2,
					"links": [],
					"nullPointMode": "connected",
					"percentage": false,
					"pointradius": 5,
					"points": false,
					"renderer": "flot",
					"seriesOverrides": [],
					"span": 12,
					"stack": false,
					"steppedLine": false,
					"targets": [{
						"expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (job, le))",
						"intervalFactor": 2,
						"refId": "A",
						"step": 2
					}],
					"timeFrom": null,
					"timeShift": null,
					"title": "Response time for 95% of requests",
					"tooltip": {
						"msResolution": true,
						"shared": true,
						"sort": 0,
						"value_type": "cumulative"
					},
					"type": "graph",
					"xaxis": {
						"show": true
					},
					"yaxes": [{
							"format": "s",
							"label": null,
							"logBase": 1,
							"max": 1,
							"min": 0,
							"show": true
						},
						{
							"format": "short",
							"label": null,
							"logBase": 1,
							"max": null,
							"min": null,
							"show": true
						}
					]
				}],
				"title": "Row2"
			}
		]
	}
}' 'http://localhost:3000/api/dashboards/db'
```

#### Get a dashboard

```shell
curl -v -b /tmp/curl-cookies -X GET -H 'Accept: application/json' 'http://localhost:3000/api/dashboards/db/sla' | python -m json.tool
```
