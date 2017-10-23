import logging
# import socket
import time
from bottle import Bottle, run, request, response
from prometheus_client import generate_latest, REGISTRY, Gauge, Counter, Summary, Histogram

import grafana


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

IN_PROGRESS = Gauge("inprogress_requests", "help")

REQUESTS = Counter('http_requests_total', 'Description of counter', ['method', 'endpoint', 'service'])

REQUEST_TIME = Histogram('http_request_duration_seconds', 'help', ['method', 'endpoint', 'service'])
REQUEST_TIME_TEST = REQUEST_TIME.labels(method='GET', endpoint="test", service='webapp-python')

REQUEST_TIME_NO_LABLES = Histogram('http_request2_duration_seconds', 'Time spent processing request')

# REQUEST_TIME = Summary('request_processing_seconds', 'help', ['method', 'endpoint', 'service'])


@app.route('/always_ok', method='GET')
@app.route('/always_ok/<time_ms>', method='GET')
@IN_PROGRESS.track_inprogress()
def get_ok(time_ms='0'):
    with REQUEST_TIME.labels(method='GET', endpoint="always_ok", service='webapp-python').time():

        logger.info('Processing GET /always_ok/'+time_ms)

        # REQUESTS.labels(method='GET', endpoint="always_ok", service='webapp-python', region='us-west').inc()

        time_to_sleep = int(time_ms) / float(1000)
        time.sleep(time_to_sleep)

        retdata = {
            "status": "OK"
        }

        return retdata


@app.route('/always_500', method='GET')
@app.route('/always_500/<time_ms>', method='GET')
@IN_PROGRESS.track_inprogress()
def get_fail(time_ms='0'):
    with REQUEST_TIME.labels(method='GET', endpoint="always_500", service='webapp-python').time():
        logger.info('Processing GET /always_500')

        time_to_sleep = int(time_ms) / float(1000)
        time.sleep(time_to_sleep)

        retdata = {
            "status": "FAIL"
        }
        response.content_type = 'application/json'
        response.status = 500
    # REQUEST_TIME.labels(method='GET', endpoint="always_500",
    #                    service='webapp-python', region='us-west').observe(time.time() - start_time)
        return retdata


@app.route('/test', method='GET')
@app.route('/test/<time_ms>', method='GET')
@IN_PROGRESS.track_inprogress()
@REQUEST_TIME_TEST.time()
def get_test(time_ms='0'):
    logger.info('Processing GET /test/'+time_ms)

    time_to_sleep = int(time_ms) / float(1000)
    time.sleep(time_to_sleep)

    retdata = {
        "status": "OK"
    }

    return retdata


@IN_PROGRESS.track_inprogress()
@app.route('/metrics')
def metrics():
    return generate_latest(REGISTRY)


'''
RUN APP
'''
# time.sleep(10)
# grafana.create_dashboard()
logger.info('Starting Service on port {0}'.format(LISTEN_PORT))
run(app, host='0.0.0.0', port=LISTEN_PORT, reloader=True)
