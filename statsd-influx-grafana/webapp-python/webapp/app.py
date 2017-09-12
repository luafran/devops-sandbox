import json
import logging
import os
import socket
import time

from bottle import Bottle, run, request, response
import requests
import statsd


LISTEN_PORT = 8080

logger = logging.getLogger('webapp-python')
logger.setLevel(logging.DEBUG)
logger.propagate = False
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

app = Bottle()

stats_client = statsd.StatsClient('telegraf', 8125)


def create_grafana_datasource():

    grafana_host = 'grafana'
    grafana_port = 3000
    grafana_user = 'admin'
    grafana_password = 'secret'
    ifdb_database = 'telegraf'
    datasource_name = 'influxdb-01'
    ifdb_user = ''
    ifdb_password = ''
    ifdb_host = 'influxdb'
    ifdb_port = 8086

    grafana_url = os.path.join('http://', '%s:%u' % (grafana_host, grafana_port))
    session = requests.Session()
    login_post = session.post(
        os.path.join(grafana_url, 'login'),
        data=json.dumps({
            'user': grafana_user,
            'email': '',
            'password': grafana_password}),
        headers={'content-type': 'application/json'})

    # Get list of datasources
    datasources_get = session.get(os.path.join(grafana_url, 'api', 'datasources'))
    datasources = datasources_get.json()

    # Add new datasource
    datasources_post = session.post(
        os.path.join(grafana_url, 'api', 'datasources'),
        data=json.dumps({
            'access': 'direct',
            'database': ifdb_database,
            'name': datasource_name,
            'type': 'influxdb',
            'url': 'http://%s:%u' % (ifdb_host, ifdb_port),
            'basicAuth': False,
            'basicAuthUser': '',
            'basicAuthPassword': '',
            'withCredentials': False,
            'user': '',
            'password': ''}),
        headers={'content-type': 'application/json'})

    dashboard = {
        "dashboard": {
            "id": None,
            "title": "dashboard-1",
            "schemaVersion": 12,
            "version": 0,
            "editable": True,
            "gnetId": None,
            "hideControls": False,
            "sharedCrosshair": False,
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
                "title": "row-1",
                "collapse": False,
                "editable": True,
                "height": "250px",
                "panels": [{
                    "id": 1,
                    "title": "Requests/10s",
                    "isNew": True,
                    "datasource": "influxdb-01",
                    "aliasColors": {},
                    "editable": True,
                    "error": False,
                    "bars": True,
                    "lines": False,
                    "fill": 1,
                    "linewidth": 2,
                    "NonePointMode": "connected",
                    "percentage": False,
                    "pointradius": 5,
                    "points": False,
                    "renderer": "flot",
                    "seriesOverrides": [],
                    "span": 12,
                    "stack": False,
                    "steppedLine": False,
                    "grid": {
                        "threshold1": None,
                        "threshold1Color": "rgba(216, 200, 27, 0.27)",
                        "threshold2": None,
                        "threshold2Color": "rgba(234, 112, 112, 0.22)"
                    },
                    "legend": {
                        "avg": False,
                        "current": False,
                        "max": False,
                        "min": False,
                        "show": True,
                        "total": False,
                        "values": False
                    },
                    "targets": [{
                        "dsType": "influxdb",
                        "groupBy": [{
                            "params": [
                                "$interval"
                            ],
                            "type": "time"
                        },
                            {
                                "params": [
                                    "hostname"
                                ],
                                "type": "tag"
                            },
                            {
                                "params": [
                                    "null"
                                ],
                                "type": "fill"
                            }
                        ],
                        "measurement": "net_requests",
                        "policy": "default",
                        "refId": "A",
                        "resultFormat": "time_series",
                        "select": [
                            [{
                                "params": [
                                    "value"
                                ],
                                "type": "field"
                            },
                                {
                                    "params": [],
                                    "type": "mean"
                                },
                                {
                                    "params": [
                                        "10s"
                                    ],
                                    "type": "derivative"
                                }
                            ]
                        ],
                        "tags": []
                    }],
                    "timeFrom": None,
                    "timeShift": None,
                    "tooltip": {
                        "msResolution": True,
                        "shared": True,
                        "sort": 0,
                        "value_type": "cumulative"
                    },
                    "type": "graph",
                    "xaxis": {
                        "show": True
                    },
                    "yaxes": [{
                        "format": "short",
                        "label": None,
                        "logBase": 1,
                        "max": None,
                        "min": None,
                        "show": True
                        },
                        {
                        "format": "short",
                        "label": None,
                        "logBase": 1,
                        "max": None,
                        "min": None,
                        "show": True
                    }]
                }]
            }]
        }
    }

    dashboard_post = session.post(
        os.path.join(grafana_url, 'api', 'dashboards', 'db'),
        data=json.dumps(dashboard),
        headers={'content-type': 'application/json'})


@app.route('/always_ok', method='GET')
def get_test():
    logger.info('Processing GET /always_ok')

    stats_client.incr('net.requests,hostname={},service=webapp-python,region=us-west'.format(socket.gethostname()))  # Increment counter

    retdata = {
        "status": "OK"
    }
    return retdata


@app.route('/always_500', method='GET')
def get_test():
    logger.info('Processing GET /always_500')

    stats_client.incr('net.requests,service=webapp-python,region=us-west')  # Increment counter

    retdata = {
        "status": "FAIL"
    }
    response.content_type = 'application/json'
    response.status = 500
    return retdata


'''
RUN APP
'''
time.sleep(10)
create_grafana_datasource()
logger.info('Starting Service on port {0}'.format(LISTEN_PORT))
run(app, host='0.0.0.0', port=LISTEN_PORT, reloader=True)
