import logging

from bottle import Bottle, run, request, response


LISTEN_PORT = 8080

logger = logging.getLogger('webapp-python')
logger.setLevel(logging.DEBUG)
logger.propagate = False
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

app = Bottle()


@app.route('/always_ok', method='GET')
def get_test():
    logger.info('Processing GET /always_ok')

    retdata = {
        "status": "OK"
    }

    logger.info('status: OK')
    return retdata


@app.route('/always_500', method='GET')
def get_test():
    logger.info('Processing GET /always_500')

    retdata = {
        "status": "FAIL"
    }

    response.content_type = 'application/json'
    response.status = 500
    logger.error('status: FAIL')
    return retdata


'''
RUN APP
'''
logger.info('Starting Service on port {0}'.format(LISTEN_PORT))
run(app, host='0.0.0.0', port=LISTEN_PORT, reloader=True)
