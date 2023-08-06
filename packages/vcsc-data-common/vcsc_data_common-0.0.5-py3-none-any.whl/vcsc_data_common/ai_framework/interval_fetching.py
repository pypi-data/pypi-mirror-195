from vcsc_data_common.live_price_data import DataFetcher as LiveDataFetcher
from vcsc_data_common.offline_price_data import DataFetcher as OfflineDataFetcher
import pandas as pd
import time


class IntervalFetching:
    offline_data_df: pd.DataFrame
    live_data_df: pd.DataFrame

    def __init__(self, aws_access_key: str, aws_secret_key: str, time_frame: str, interval: int, callback: callable) -> None:
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.time_frame = time_frame
        self.callback = callback
        self.interval = interval

        self.live_data_fetcher = LiveDataFetcher(
            aws_access_key, aws_secret_key, time_frame)

        self.offline_data_fetcher = OfflineDataFetcher(
            aws_access_key, aws_secret_key, time_frame)

    def start(self):
        self.offline_data_df = self.offline_data_fetcher.get_data()

        while True:

            self.live_data_df = self.live_data_fetcher.get_data()

            union_df = pd.concat([self.offline_data_df, self.live_data_df])

            self.callback(union_df)

            time.sleep(self.interval)
