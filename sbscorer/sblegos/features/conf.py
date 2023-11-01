import time

from sbscorer.sblegos.features.custom.extract import *

DAY = 3600
WEEK = 7 * DAY
MONTH = 30 * DAY
MONTHS_3 = 3 * MONTH

current_time = time.time()

FC_TSFRESH_TIME = {"approximate_entropy": [{'m': 2, 'r': 0.1},
                                           {'m': 2, 'r': 0.3},
                                           {'m': 2, 'r': 0.5},
                                           {'m': 2, 'r': 0.7},
                                           {'m': 2, 'r': 0.9}], "autocorrelation": [{'lag': 1},
                                                                                    {'lag': 2},
                                                                                    {'lag': 3},
                                                                                    {'lag': 4}], "c3": [{'lag': 0},
                                                                                                        {'lag': 1},
                                                                                                        {'lag': 2},
                                                                                                        {'lag': 3},
                                                                                                        {'lag': 4}],
                   "binned_entropy": [{'max_bins': 5}], "count_above_mean": None, "count_below_mean": None,
                   "has_duplicate": None, "kurtosis": None, "mean": None, "mean_abs_change": None, "mean_change": None,
                   "median": None, "quantile": [{'q': 0.99},
                                                {'q': 0.95},
                                                {'q': 0.90},
                                                {'q': 0.80},
                                                {'q': 0.20}], "ratio_beyond_r_sigma": [{'r': 1},
                                                                                       {'r': 2},
                                                                                       {'r': 6}], "skewness": None,
                   "standard_deviation": None, "variance": None, "variance_larger_than_standard_deviation": None,
                   "variation_coefficient": None, "percentage_of_reoccurring_datapoints_to_all_datapoints": None,
                   "percentage_of_reoccurring_values_to_all_values": None,
                   "permutation_entropy": [{'dimension': 3, 'tau': 1},
                                           {'dimension': 4, 'tau': 1},
                                           {'dimension': 5, 'tau': 1}],
                   "ratio_value_number_to_time_series_length": None,
                   time_since_first: [{'current_time': current_time}],
                   time_since_last: [{'current_time': current_time}],
                   time_last_tx: None, time_first_tx: None,
                   time_max_utc_hour_day: None,
                   time_min_utc_hour_day: None,
                   time_most_active_hour_day: None,
                   time_ratio_tx_time_since_time: [{'current_time': current_time, "time": DAY},
                                                   {'current_time': current_time, "time": WEEK},
                                                   {'current_time': current_time, "time": MONTH},
                                                   {'current_time': current_time, "time": MONTHS_3}],
                   time_ratio_tx_time_since_last_tx: [{"time": DAY},
                                                      {"time": WEEK},
                                                      {"time": MONTH},
                                                      {"time": MONTHS_3}], ratio_above_mean: None}

# add custom features

FC_TSFRESH_VALUE = {
    "sum_values": None,
    "abs_energy": None,
    "approximate_entropy": [{'m': 2, 'r': 0.1},
                            {'m': 2, 'r': 0.3},
                            {'m': 2, 'r': 0.5},
                            {'m': 2, 'r': 0.7},
                            {'m': 2, 'r': 0.9}],
    "autocorrelation": [{'lag': 1},
                        {'lag': 2},
                        {'lag': 3},
                        {'lag': 4}],
    "benford_correlation": None,
    "binned_entropy": [{'max_bins': 5}],
    "count_above_mean": None,
    "count_below_mean": None,
    "has_duplicate": None,
    "maximum": None,
    "mean": None,
    "mean_abs_change": None,
    "mean_change": None,
    "mean_second_derivative_central": None,
    "median": None,
    "minimum": None,
    "skewness": None,
    "standard_deviation": None,
    "variance": None,
    "variance_larger_than_standard_deviation": None,
    "variation_coefficient": None,

    "percentage_of_reoccurring_datapoints_to_all_datapoints": None,
    "percentage_of_reoccurring_values_to_all_values": None,
    "permutation_entropy": [{'dimension': 3, 'tau': 1},
                            {'dimension': 4, 'tau': 1},
                            {'dimension': 5, 'tau': 1}],
    "ratio_beyond_r_sigma": [{'r': 1},
                             {'r': 2},
                             {'r': 6}],
    "ratio_value_number_to_time_series_length": None,
}

FC_TSFRESH_GAS = {
    "sum_values": None,
    "approximate_entropy": [{'m': 2, 'r': 0.1},
                            {'m': 2, 'r': 0.3},
                            {'m': 2, 'r': 0.5},
                            {'m': 2, 'r': 0.7},
                            {'m': 2, 'r': 0.9}],
    "autocorrelation": [{'lag': 1},
                        {'lag': 2},
                        {'lag': 3},
                        {'lag': 4}],
    "benford_correlation": None,
    "binned_entropy": [{'max_bins': 5}],
    "count_above_mean": None,
    "count_below_mean": None,
    "has_duplicate": None,
    "maximum": None,
    "mean": None,
    "mean_abs_change": None,
    "mean_change": None,
    "mean_second_derivative_central": None,
    "median": None,
    "minimum": None,
    "skewness": None,
    "standard_deviation": None,
    "variance": None,
    "variance_larger_than_standard_deviation": None,
    "variation_coefficient": None,

    "percentage_of_reoccurring_datapoints_to_all_datapoints": None,
    "percentage_of_reoccurring_values_to_all_values": None,
    "permutation_entropy": [{'dimension': 3, 'tau': 1},
                            {'dimension': 4, 'tau': 1},
                            {'dimension': 5, 'tau': 1}],
    "ratio_beyond_r_sigma": [{'r': 1},
                             {'r': 2},
                             {'r': 6}],
    "ratio_value_number_to_time_series_length": None,
}

FC_TSFRESH = {
    "block_timestamp": FC_TSFRESH_TIME,
    "value": FC_TSFRESH_VALUE,
    "tx_fee": FC_TSFRESH_VALUE,
    "gas_used": FC_TSFRESH_GAS,
    "gas_limit": FC_TSFRESH_GAS,
}

# ok
FC_TSFRESH_T_V = {
    "block_timestamp": FC_TSFRESH_TIME,
    "value": FC_TSFRESH_VALUE,
    "tx_fee": FC_TSFRESH_VALUE,
}

FC_TSFRESH_GAS_2 = {
    "gas_used": FC_TSFRESH_GAS,
    "gas_limit": FC_TSFRESH_GAS,
}
