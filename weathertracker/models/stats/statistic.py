import datetime
import statistics

__author__ = 'hooper-p'


class Statistic(object):

    @staticmethod
    def get_max_measure(measure, arr):
        """
        Function is executed when "max" metric is submitted in /stats GET request
        :param measure: the appropriate data point of measurement
        :param arr: full or partial (if dates are provided) list of measurements
        :return: object stating the maximum value of the measure provided if at least one is found, otherwise None
        """
        # if at least one measure was found
        if [float(item[measure]) for item in arr if item[measure] is not None]:
            return {
                "metric": measure,
                "stat": "max",
                "value": max([float(item[measure]) for item in arr if item[measure] is not None])
            }
        else:
            return None

    @staticmethod
    def get_min_measure(measure, arr):
        """
        Function is executed when "min" metric is submitted in /stats GET request
        :param measure: the appropriate data point of measurement
        :param arr: full or partial (if dates are provided) list of measurements
        :return: object stating the minimum value of the measure provided if at least one is found, otherwise None
        """
        # if at least one measure was found
        if [float(item[measure]) for item in arr if item[measure] is not None]:
            return {
                "metric": measure,
                "stat": "min",
                "value": min([float(item[measure]) for item in arr if item[measure] is not None])
            }
        else:
            return None

    @staticmethod
    def get_average_measure(measure, arr):
        """
        Function is executed when "average" metric is submitted in /stats GET request
        :param measure: the appropriate data point of measurement
        :param arr: full or partial (if dates are provided) list of measurements
        :return: object stating the average value of the measure provided if at least one is found, otherwise None
        """
        # if at least one measure was found
        if [float(item[measure]) for item in arr if item[measure] is not None]:
            return {
                "metric": measure,
                "stat": "average",
                "value": statistics.mean([float(item[measure]) for item in arr if item[measure] is not None])
            }
        else:
            return None

    @staticmethod
    def select_dates(start_date, end_date, arr):
        """
        Function is invoked when a fromDateTime and toDateTime are provided in /stats GET request
        :param start_date: fromDateTime from /stats GET request in ISO-8061 format
        :param end_date: toDateTime from /stats GET request in ISO-8061 format
        :param arr: full list of measurements captured to date
        :return: reduced list of measurements based on dates provided
        """
        return [measurement for measurement in arr
                if (datetime.datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ")
                    <= datetime.datetime.strptime(measurement['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ")
                    < datetime.datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%fZ"))]
