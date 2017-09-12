import logging
import socket
import time

from bottle import Bottle, run, request, response
import statsd

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

stats_client = statsd.StatsClient('telegraf', 8125)


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
grafana.create_dashboard()
logger.info('Starting Service on port {0}'.format(LISTEN_PORT))
run(app, host='0.0.0.0', port=LISTEN_PORT, reloader=True)
