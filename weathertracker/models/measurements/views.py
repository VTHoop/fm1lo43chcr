__author__ = 'hooper-p'

from flask import Blueprint, request, jsonify
from weathertracker.models.measurements.measurement import Measurement

measurement_blueprint = Blueprint('measurements', __name__)


@measurement_blueprint.route('', methods=['POST'])
def create_measurements():
    """
    This function provides the API to create new measurements.
    Error checks include that all appropriate data points were submitted and appropriate data types were provided
    Timestamp should be datetime type
    Temperature, dewPoint, and precipitation should be float
    :return: 201 response object if all checks are passed
            400 response if request has mismatched data types
            400 response if request is missing data
    """
    new_timestamp = request.json['timestamp'] if 'timestamp' in request.json else None
    new_precipitation = request.json['precipitation'] if 'precipitation' in request.json else None
    new_dewPoint = request.json['dewPoint'] if 'dewPoint' in request.json else None
    new_temperature = request.json['temperature'] if 'temperature' in request.json else None

    if 'timestamp' not in request.json:
        resp = jsonify({"Message": "Timestamp not provided"})
        resp.status_code = 400
    elif (not Measurement.check_data_types(request.json)) or (not Measurement.is_timestamp(request.json['timestamp'])):
        resp = jsonify({"Message": "Datatypes are not as expected"})
        resp.status_code = 400
    else:
        measurement = Measurement(timestamp=new_timestamp, temperature=new_temperature,
                                  dewPoint=new_dewPoint, precipitation=new_precipitation)
        measurement.save_new_measurement()
        resp = jsonify(measurement.json())
        resp.headers['location'] = '/measurements/' + new_timestamp
        resp.autocorrect_location_header = False
        resp.status_code = 201
    return resp


@measurement_blueprint.route('/<string:timestamp>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def update_measurements(timestamp):
    """
    This route is provided a timestamp ID that is expected to be in ISO-8061 format.
    The GET request will handle checking of ID in get request.  If OK, then it will provide a list of measures if found,
     otherwise will return 404 error with no measurements found.
    THE PUT and PATCH requests will update the object in the ID of the request if found with the data provided.
    Data checks are performed on the ID and the data provided through the request.
    :param timestamp: timestamp or date of the request
    :return: response object with appropriate code
    """
    if request.method == 'GET':
        # check format of timestamp or date
        if Measurement.is_timestamp(timestamp) or Measurement.is_date(timestamp):
            # if ID provided is in timestamp format, get that measurement by ID
            if Measurement.is_timestamp(timestamp):
                measurement = Measurement.get_measurement_by_timestamp(timestamp)
            # if ID provided is in date format, get list of measurements for that day
            elif Measurement.is_date(timestamp):
                measurement = Measurement.get_measurements_by_date(timestamp)

            if not measurement:
                resp = jsonify({"Message": "No Measurements found"})
                resp.status_code = 404
            else:
                resp = jsonify(measurement)
                resp.status_code = 200
        else:
            resp = jsonify({"Message": "Timestamp or date bad format"})
            resp.status_code = 404
        return resp

    elif request.method in ['PUT', 'PATCH']:
        # handle parameters that may not be passed
        new_timestamp = request.json['timestamp'] if 'timestamp' in request.json else None
        new_precipitation = request.json['precipitation'] if 'precipitation' in request.json else None
        new_dewPoint = request.json['dewPoint'] if 'dewPoint' in request.json else None
        new_temperature = request.json['temperature'] if 'temperature' in request.json else None

        # if a timestamp was provided but does not equal the one provided in URL
        if new_timestamp and (new_timestamp != timestamp):
            resp = jsonify({"Message": "Timestamp in request is inconsistent with ID"})
            resp.status_code = 409
        # if data types are not as expected
        elif (not Measurement.check_data_types(request.json)) or (
                not Measurement.is_timestamp(timestamp)):
            resp = jsonify({"Message": "Datatypes are not as expected"})
            resp.status_code = 400
        # if all checks pass
        else:
            updated_measurement = Measurement.update_measurement(timestamp, new_temperature, new_dewPoint,
                                                                 new_precipitation)
            # measurement found and updated
            if updated_measurement:
                resp = jsonify(updated_measurement)
                resp.status_code = 204
            # no measurements found
            else:
                resp = jsonify({"Message": "Timestamp not found"})
                resp.status_code = 404
        return resp
    elif request.method == 'DELETE':
        deleted_measurement = Measurement.delete_measurement(timestamp)
        # measurement found and successfully deleted
        if deleted_measurement:
            resp = jsonify(deleted_measurement)
            resp.status_code = 204
        # no measurements found
        else:
            resp = jsonify({"Message": "Timestamp not found"})
            resp.status_code = 404
        return resp
