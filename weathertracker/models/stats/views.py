__author__ = 'hooper-p'

from flask import Blueprint, request, jsonify
from weathertracker.models.stats.statistic import Statistic
from weathertracker.models.measurements.measurement import measurements

statistic_blueprint = Blueprint('stat', __name__)

metric_functions = {
    "max": Statistic.get_max_measure,
    "min": Statistic.get_min_measure,
    "average": Statistic.get_average_measure
}


@statistic_blueprint.route('', methods=['GET'])
def stats():
    # clear statistics on each request
    statistic_list = []
    # reduce measurements data by dates if they are provided
    if request.args.get('fromDateTime') and request.args.get('toDateTime'):
        query_measurements = Statistic.select_dates(request.args.get('fromDateTime'), request.args.get('toDateTime'),
                                                    measurements)
    # no dates are provided; query on all measurements
    else:
        query_measurements = measurements
    # get measure for each metric and statistic provided
    for metric in request.args.getlist('metric'):
        for stat in request.args.getlist('stat'):
            new_stats = metric_functions[metric](stat, query_measurements)
            if new_stats:
                statistic_list.append(new_stats)
    return jsonify(statistic_list)
