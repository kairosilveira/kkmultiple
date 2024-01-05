# from metrics.crypto_accumulator import CryptoAccumulator
# import polars as pl
# import pytest
# import re


# def test_invalid_init(sample_historical_data, sample_eval_period):
#     possible_methods = CryptoAccumulator.possible_methods
#     with pytest.raises(ValueError,
#                        match="If method is 'kk' a KKMultiple object must be specified"):
#         CryptoAccumulator(sample_historical_data,
#                           sample_eval_period, method='kk')

#     with pytest.raises(ValueError,
#                        match=re.escape(f"The method 'kkk' is not one of the possible methods: {possible_methods}")):
#         CryptoAccumulator(sample_historical_data,
#                           sample_eval_period, method='kkk')


# def test__get_raw_train_data(sample_kkmultiple, sample_historical_data, sample_eval_period):
#     accumulator = CryptoAccumulator(
#         historical_data=sample_historical_data, kkmult=sample_kkmultiple, eval_period=sample_eval_period)

#     train_data = accumulator._get_raw_train_data()

#     assert isinstance(train_data, pl.DataFrame)
#     assert train_data.shape == (2, 2)
#     assert train_data["date"][0] == accumulator.start_date
#     assert train_data["date"][-1] == accumulator.end_date
#     assert "date" in train_data.columns
#     assert "price" in train_data.columns
#     assert pl.Datetime in train_data.dtypes
#     assert pl.Float64 in train_data.dtypes


# def test__get_multiples(sample_kkmultiple, sample_historical_data, sample_eval_period):
#     accumulator = CryptoAccumulator(
#         historical_data=sample_historical_data, kkmult=sample_kkmultiple, eval_period=sample_eval_period)
#     accumulator._get_raw_train_data()

#     multiples = accumulator._get_multiples()

#     assert isinstance(multiples, pl.DataFrame)
#     assert multiples.shape == (2, 1)
#     assert "multiples" in multiples.columns
#     assert multiples.dtypes == [pl.Float64]
#     assert multiples["multiples"][0] == 1.0
#     assert multiples["multiples"][1] == 1.0


# def test__get_buy_percentages(sample_kkmultiple, sample_historical_data, sample_eval_period):
#     accumulator = CryptoAccumulator(
#         historical_data=sample_historical_data, kkmult=sample_kkmultiple, eval_period=sample_eval_period)

#     accumulator._get_raw_train_data()
#     accumulator._get_multiples()

#     buy_percentages = accumulator._get_buy_percentages()

#     assert isinstance(buy_percentages, pl.DataFrame)
#     assert buy_percentages.shape == (2, 1)
#     assert "buy_percentages" in buy_percentages.columns
#     assert buy_percentages.dtypes == [pl.Float64]
#     assert buy_percentages["buy_percentages"][0] == 0.4
#     assert buy_percentages["buy_percentages"][1] == 0.4


# def test_get_train_data(sample_kkmultiple, sample_historical_data, sample_eval_period):
#     accumulator = CryptoAccumulator(
#         historical_data=sample_historical_data, kkmult=sample_kkmultiple, eval_period=sample_eval_period)

#     accumulator._get_raw_train_data()
#     accumulator._get_multiples()
#     accumulator._get_buy_percentages()

#     train_data = accumulator.get_train_data()

#     assert isinstance(train_data, pl.DataFrame)
#     assert train_data.shape == (2, 4)
#     assert "date" in train_data.columns
#     assert "price" in train_data.columns
#     assert "multiples" in train_data.columns
#     assert "buy_percentages" in train_data.columns


# def test_get_accumulated_value(sample_kkmultiple, sample_historical_data, sample_eval_period):
#     accumulator = CryptoAccumulator(
#         historical_data=sample_historical_data, kkmult=sample_kkmultiple, eval_period=sample_eval_period)

#     accumulated_result = accumulator.get_accumulated_value()

#     assert isinstance(accumulated_result, tuple)
#     assert len(accumulated_result) == 2
#     assert isinstance(accumulated_result.amount_accumulated, float)
#     assert isinstance(accumulated_result.remaining_budget, float)
#     assert accumulated_result.amount_accumulated == 0.4*1000/120 + 0.4*1600/130
#     assert accumulated_result.remaining_budget == 2000-(0.4*1000 + 0.4*1600)


# def test_get_accumulated_value_2days(sample_kkmultiple, sample_historical_data):

#     accumulator = CryptoAccumulator(
#         historical_data=sample_historical_data, kkmult=sample_kkmultiple, eval_period=('2022-12-29', '2022-12-30'))

#     accumulated_result = accumulator.get_accumulated_value(
#         remaining_budget=960)

#     assert accumulated_result.amount_accumulated == (
#         960+1000)*0.4/100 + ((960+1000)*0.6+1000)*0.4/100


# def test_get_accumulated_value(sample_historical_data, sample_eval_period):
#     accumulator = CryptoAccumulator(
#         sample_historical_data, sample_eval_period, method="buy_every_day")

#     assert accumulator.get_accumulated_value() == 1000/120+1000/130

# # test for method mayer too
