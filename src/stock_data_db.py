#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Date, Float, Integer, String

Base = declarative_base()

#TABLE_ID = Sequence('table_id_seq', start=1000)

class StockDataDb(Base):
    __tablename__ = 'stock_ticks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol=Column(String)
    date = Column(Date)
    last_value = Column(Float)
    change_value = Column(Float)
    change_perc = Column(Float)
    high_value = Column(Float)
    low_value = Column(Float)
    _52w_change_value = Column(Float)
    _52w_change_perc = Column(Float)
    _52w_low = Column(Float)
    _52w_high = Column(Float)
    open_value = Column(Float)
    prev_value = Column(Float)
    bid_value = Column(Float)
    bid_amount = Column(Float)
    ask_value = Column(Float)
    ask_amount = Column(Float)
    volume_value = Column(Float)
    turnover_value = Column(Float)
    open_int_value = Column(Float)
    no_trades_value = Column(Float)

    def __repr__(self):
        return "StockDataDB:" \
               "Symbol value: {symbol}\n" \
               "Last value: {last_value}\n" \
               "Change value: {change_value}\n" \
               "Change percentage: {change_perc}\n" \
               "Date value: {date}\n" \
               "High value: {high_value}\n" \
               "Low value: {low_value}\n" \
               "Change value in 52w: {_52w_change_value}\n" \
               "Change perc in 52w: {_52w_change_perc}\n" \
               "Open value: {open_value}\n" \
               "Previous value: {prev_value}\n" \
               "Bid value: {bid_value}\n" \
               "Bid amount: {bid_amount}\n" \
               "Ask value: {ask_value}\n" \
               "Ask amount: {ask_amount}\n" \
               "Turnover: {turnover}\n" \
               "Open int value: {open_int}\n" \
               "Number of trades: {no_of_trades}\n".format(symbol=self.symbol,
                                                            last_value=self.last_value,
                                                            change_value=self.change_value,
                                                            change_perc=self.change_perc,
                                                            date=self.date,
                                                            high_value=self.high_value,
                                                            low_value=self.low_value,
                                                            _52w_change_value=self._52w_change_value,
                                                            _52w_change_perc=self._52w_change_perc,
                                                            open_value=self.open_value,
                                                            prev_value=self.prev_value,
                                                            bid_value=self.bid_value,
                                                            bid_amount=self.bid_amount,
                                                            ask_value=self.ask_value,
                                                            ask_amount=self.ask_amount,
                                                            turnover=self.turnover_value,
                                                            open_int=self.open_int_value,
                                                            no_of_trades=self.no_trades_value)
