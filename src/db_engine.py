# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from stock_data_db import Base, StockDataDb

class DbEngine(object):
    def __init__(self, connection_string):
        self.db_engine = None
        self.connection_string = connection_string
        
    def get_instance(self):
        if not self.db_engine:
            self.db_engine = create_engine(self.connection_string)
        return self.db_engine


class DbSession(object):
    def __init__(self, db_engine):
        self.Session = sessionmaker(bind=db_engine)

    def persist_tick(self, stock_data):
        session = self.Session()
        stock_data_object = StockDataDb(symbol=stock_data.symbol,
                                        date=stock_data.datetime_value,
                                        last_value=stock_data.last_value,
                                        change_value=stock_data.change_value,
                                        change_perc=stock_data.change_perc,
                                        high_value=stock_data.high_value,
                                        low_value=stock_data.low_value,
                                        _52w_change_value=stock_data._52w_change_value,
                                        _52w_change_perc=stock_data._52w_change_perc,
                                        _52w_low=stock_data._52w_low,
                                        _52w_high=stock_data._52w_high,
                                        open_value=stock_data.open_value,
                                        prev_value=stock_data.prev_value,
                                        bid_value=stock_data.bid_value,
                                        bid_amount=stock_data.bid_amount,
                                        ask_value=stock_data.ask_value,
                                        ask_amount=stock_data.ask_amount,
                                        volume_value=stock_data.volume_value,
                                        turnover_value=stock_data.turnover_value,
                                        open_int_value=stock_data.open_int_value,
                                        no_trades_value=stock_data.no_trades_value)
        print(stock_data_object)
        session.add(stock_data_object)
        session.commit()
