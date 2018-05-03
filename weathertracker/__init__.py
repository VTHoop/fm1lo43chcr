from flask import Flask, request, jsonify
from weathertracker.models.measurements.views import measurement_blueprint
from weathertracker.models.stats.views import statistic_blueprint


app = Flask('weathertracker')

app.register_blueprint(measurement_blueprint, url_prefix='/measurements')
app.register_blueprint(statistic_blueprint, url_prefix='/stats')


# TODO: Implement the endpoints in the ATs.
# The below stubs are provided as a starting point.
# You may refactor them however you like, so long as a Flask instance is set
# to `app`

not_implemented = 'Not Implemented\n', 501, { 'Content-Type': 'text/plain' }


# dummy handler so you can tell if the server is running
# e.g. `curl localhost:8000`
@app.route('/')
def root():
    return 'Weather tracker is up and running!\n'


# @app.route('/measurements/<timestamp>', methods=['PUT', 'PATCH', 'DELETE'])
# def update_measurement(timestamp):
    # features/01-measurements/03-update-measurement.feature
    # if request.method == 'PUT':
        # Example:
        # assert timestamp == '2015-09-01T16:20:00.000Z'
        #
        # assert request.get_json() == {
        #     'timestamp': '2015-09-01T16:00:00.000Z',
        #     'temperature': 27.1,
        #     'dewPoint': 16.7,
        #     'precipitation': 15.2
        # }

        # return not_implemented

    # features/01-measurements/03-update-measurement.feature
    # if request.method == 'PATCH':
        # Example:
        # assert timestamp == '2015-09-01T16:20:00.000Z'
        #
        # assert request.get_json() == {
        #     'timestamp': '2015-09-01T16:00:00.000Z',
        #     'precipitation': 15.2
        # }

        # return not_implemented

    # features/01-measurements/04-delete-measurement.feature
    # if request.method == 'DELETE':
        # Example:
        # assert timestamp == '2015-09-01T16:20:00.000Z'

        # return not_implemented

# features/02-stats/01-get-stats.feature
# @app.route('/stats')
# def stats():
    # Example:
    # assert request.args.getlist('metric') == [
    #     'temperature',
    #     'dewPoint'
    # ]
    #
    # assert request.args.getlist('stat') == [
    #     'min',
    #     'max'
    # ]
    #
    # return jsonify([
    #     {
    #         'metric': 'temperature',
    #         'stat': 'min',
    #         'value': 27.1
    #     },
    #     {
    #         'metric': 'temperature',
    #         'stat': 'max',
    #         'value': 27.5
    #     },
    #     {
    #         'metric': 'dewPoint',
    #         'stat': 'min',
    #         'value': 16.9
    #     },
    #     {
    #         'metric': 'dewPoint',
    #         'stat': 'max',
    #         'value': 17.3
    #     }
    # ])

    # return not_implemented
