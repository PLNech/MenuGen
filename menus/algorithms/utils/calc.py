__author__ = 'PLNech'


class Calc():
    @staticmethod
    def variance(values, average):
        """
        Calculates the variance of the values
        The variance is the mean of the squared distances between values and average

        :param values: The input values
        :type values list
        :param average: The average of the values
        :type average float
        :return: The variance of the values
        :rtype float
        """
        # Calculate variance
        sum_squares = 0
        for v in values:
            centered_distance = v - average
            squared_difference = centered_distance * centered_distance
            sum_squares += squared_difference
        variance = sum_squares / len(values)
        return variance

    @staticmethod
    def median(values):
        """
        Calculates the median of the values
        The median can be seen as the value partitioning the sorted input in two equal halves

        :param values: The input values
        :type values list
        :return: The median of the values
        :rtype float
        """
        half = int(len(values) / 2)
        sorted_values = sorted(values)
        even = len(sorted_values) % 2 == 0
        median = sorted_values[half] if even else sorted_values[half - 1] + sorted_values[half] / 2
        return median

    @staticmethod
    def median_absolute_deviation(median, values):
        """
        Calculates the median absolute deviation of values
        The median absolute deviation (MAD) is a robust (resistant to rare extreme values) measure of variability

        Example :
        values: [1, 1521.7720318110973, 1560.86343189714, 1620.0020749976825, 1654.949514470738, 1664.9875419401872,
                 1700.198179242014, 1778.0522344274045, 1722.1188253777914, 2024.739253568515]

        Standard deviation of solutions distances: 32.54%.
        Median absolute deviation of solutions distances: 6.11%.

        :param median: The median of the set of values
        :type median float
        :param values: The input values
        :type values list
        :return: The median absolute deviation in the input unit
        :rtype float
        """
        dev_to_med = []
        for v in values:
            # Store absolute deviations to median
            dev_to_med.append(abs(v - median))
        median_absolute_deviation = Calc.median(dev_to_med)
        return median_absolute_deviation


