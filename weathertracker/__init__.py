from flask import Flask, request, jsonify
from weathertracker.models.measurements.views import measurement_blueprint
from weathertracker.models.stats.views import statistic_blueprint


app = Flask('weathertracker')

app.register_blueprint(measurement_blueprint, url_prefix='/measurements')
app.register_blueprint(statistic_blueprint, url_prefix='/stats')


@app.route('/')
def root():
    return 'Weather tracker is up and running!\n'
