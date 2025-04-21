from flask import Flask, render_template, request
from prometheus_flask_exporter import PrometheusMetrics
import time

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Static information as metric
metrics.info('app_info', 'Application info', version='1.0.3')

# Request count metric
@metrics.counter('http_requests_total', 'Total HTTP requests',
         labels={'method': lambda: request.method, 'endpoint': lambda: request.endpoint})
@app.route('/')
def home():
    return 'Hello World!'

@metrics.counter('example_requests_total', 'Total example endpoint requests')
@app.route('/example')
def example():
    return render_template('example.html')

@metrics.counter('slow_requests_total', 'Total slow endpoint requests')
@metrics.histogram('slow_request_duration_seconds', 'Slow request duration in seconds')
@app.route('/slow')
def slow():
    time.sleep(2)
    return 'Slow Response'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
