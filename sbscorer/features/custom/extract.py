from tsfresh.feature_extraction.feature_calculators import set_property

import numpy as np

@set_property("fctype", "simple")
def time_since_first(x, current_time):
    """
    Return the time since the first transaction

    :param x: the time series to calculate the feature of
    :type x: numpy.ndarray
    :param current_time: Current time in seconds
    :type current_time: int
    :return: the value of this feature
    :return type: float
    """
    result = (current_time - np.min(x))
    return result
    
@set_property("fctype", "simple")
def time_since_last(x, current_time):
    """
    Return the time since the last transaction

    :param x: the time series to calculate the feature of
    :type x: numpy.ndarray
    :param current_time: Current time in seconds
    :type current_time: int
    :return: the value of this feature
    :return type: float
    """
    result = (current_time - np.max(x))
    return result


@set_property("fctype", "simple")
def ratio_tx_time_since_time(x, current_time, time):
    """
    Return the ratio of transactions that occured in the time

    :param x: the time series to calculate the feature of
    :type x: numpy.ndarray
    :param current_time: Current time in seconds
    :type current_time: int
    :param time: The time interval in seconds for example 3600 for one day
    :type time: int
    :return: the value of this feature
    :return type: float
    """
    bool_above = x >=  (current_time - time) 
    result = bool_above.sum() / len(x)
    return result

@set_property("fctype", "simple")
def ratio_tx_time_since_last_tx(x, time):
    """
    Return the ratio of transactions that occured in the time before the last transaction

    :param x: the time series to calculate the feature of
    :type x: numpy.ndarray
    :param time: The time interval in seconds for example 3600 for one day
    :type time: int
    :return: the value of this feature
    :return type: float
    """
    last_tx_time = x.max()
    bool_above = x >=  (last_tx_time - time) 
    result = bool_above.sum() / len(x)
    return result

@set_property("fctype", "simple")
def ratio_above_mean(x):
    """
    Return the ratio of values above the mean value

    :param x: the time series to calculate the feature of
    :type x: numpy.ndarray
    :return: the value of this feature
    :return type: float
    """

    bool_above = x >=  x.mean()
    result = bool_above.sum() / len(x)
    return result

@set_property("fctype", "simple") #could be useful for gas
def ratio_above(x, v):
    """
    Return the ratio of values above a definite value (not strinctly)

    :param x: the time series to calculate the feature of
    :type x: numpy.ndarray
    :param v: A value
    :type v: float
    :return: the value of this feature
    :return type: float
    """

    bool_above = x >=  v
    result = bool_above.sum() / len(x)
    return result

@set_property("fctype", "simple") #could be useful for gas
def ratio_between_quantile(x, q1, q2):
    """
    Return the ratio of values above the mean value

    :param x: the time series to calculate the feature of
    :type x: numpy.ndarray
    :param q1: A first quartile between 0 and 1
    :type q1: float
    :param q2: A first quartile between 0 and 1 should be superior to q1
    :type q2: float
    :return: the value of this feature
    :return type: float
    """
    #TODO compute Q1 and Q2 values
    bool_above = x >=  np.quantile(x, q1)
    bool_below = x <= np.quantile(x, q2)
    bool_between = np.logical_and(bool_above, bool_below)
    result = bool_between.sum() / len(x)
    return result


# ratio_above_mean

# distance between quertiles
