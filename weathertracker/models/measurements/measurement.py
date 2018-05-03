import datetime

__author__ = 'hooper-p'

# global variable to keep all measurements in memory
measurements = []


class Measurement(object):
    def __init__(self, timestamp, temperature=None, dewPoint=None, precipitation=None):
        self.timestamp = timestamp
        self.temperature = temperature
        self.dewPoint = dewPoint
        self.precipitation = precipitation

    @staticmethod
    def measurement_data_points():
        """
        :return: Object returning the data types of the properties for Measurement object
        """
        return ["temperature", "dewPoint", "precipitation"]

    @staticmethod
    def is_timestamp(timestamp):
        """
        Timestamps are expected to be passed in an ISO-8061 format specifically.  This checks whether the input
        can be translated from that format
        :param timestamp: timestamp from JSON request
        :return: True if timestamp is ISO-8061 format, otherwise False
        """
        try:
            # expecting timestamp to be in ISO-8061
            datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
            return True
        except ValueError:
            return False

    @staticmethod
    def is_date(timestamp):
        """
        Dates can be passed in to return an list or measurements on a date.  They must be passed in with the following
        format (YYYY-MM-DD)
        :param timestamp: timestamp from JSON request
        :return: True if timestamp is in YYYY-MM-DD format, otherwise false
        """
        try:
            datetime.datetime.strptime(timestamp, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    @staticmethod
    def check_data_types(json_request):
        """
        This function will perform a try to determine if a float object was passed.  It will raise an exception if it
        fails.
        :param json_request: dict from request
        :return: True if all measurements are float, False otherwise
        """
        try:
            for obj_prop in Measurement.measurement_data_points():
                if obj_prop in list(json_request.keys()):
                    float(json_request[obj_prop])
            return True
        except ValueError:
            return False

    @staticmethod
    def get_measurement_by_timestamp(timestamp):
        """
        Return an object if found with the timestamp passed in, otherwise return False so that API can send error
        :param timestamp: ID from GET request
        :return: object if found, otherwise False
        """
        measurement = [measurement for measurement in measurements if measurement['timestamp'] == timestamp]
        if len(measurement) == 0:
            return False
        else:
            return measurement[0]

    @staticmethod
    def get_measurements_by_date(date):
        """
        Return an object(s) are found with the date string passed in, otherwise return False so that API can send error
        :param timestamp: Date ID from GET request
        :return: object(s) if found, otherwise False
        """
        measurement_by_date = [measurement for measurement in measurements if measurement['timestamp'][:10] == date]
        if len(measurement_by_date) == 0:
            return False
        else:
            return measurement_by_date

    def save_new_measurement(self):
        """
        append dict to measurements variable
        :return: True
        """
        measurements.append(self.json())
        return True

    @staticmethod
    def update_measurement(timestamp, temperature, dewPoint, precipitation):
        """
        function parameters are scrubbed before they reach this stage.  If they were left blank, then Nones are passed
        in.  If a value was provided, then it will be updated in the object
        :param timestamp: ID from GET request
        :param temperature: temperature provided in JSON object if provided, else None
        :param dewPoint: dewPoint provided in JSON object if provided, else None
        :param precipitation: precipitation provided in JSON object if provided, else None
        :return: updated object if object was found by timestamp provided, otherwise False so API can return error
        """
        measurement = Measurement.get_measurement_by_timestamp(timestamp)
        if measurement:
            if temperature:
                measurement['temperature'] = temperature
            if dewPoint:
                measurement['dewPoint'] = dewPoint
            if precipitation:
                measurement['precipitation'] = precipitation
            return measurement
        else:
            return False

    @staticmethod
    def delete_measurement(timestamp):
        """
        function will remove object from list if it is found, otherwise it will return False
        :param timestamp: ID from GET request
        :return: object to return to requester, other False so that API can return error
        """
        measurement = Measurement.get_measurement_by_timestamp(timestamp)
        if measurement:
            measurements.remove(measurement)
            return measurement
        else:
            return False

    def json(self):
        """
        :return: json notation of python object
        """
        return {
            "timestamp": self.timestamp,
            "temperature": self.temperature,
            "dewPoint": self.dewPoint,
            "precipitation": self.precipitation
        }
