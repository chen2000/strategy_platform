from __future__ import absolute_import

import logging
import sys

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker


logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)
"""
need to revisit kafka logging
_logger = config.get_logger('arnold.scripts.load_dictionary')
"""
engine = create_engine('mysql+pymysql://lchen:tiger@localhost:3306/strategy_platform')
Session = sessionmaker(bind=engine)
session = Session()
"""
need to replace url by config
why clay wrap Session into its package, how clay package know the address for the sessionmaker
"""

def load_price(prices, PriceTable):
    """
    Load data into DailyPrice table
    :param price: a list of namedtuple, price[i] has fields as columns in DialyPrice
    """
        
    if not prices:
        _logger.info('msg: input error, check if the file exists')
        return False
    try:
        for p in prices:
        # find the row with primary keys, if not exist, add keys            
            dp = session.query(PriceTable).filter(
                PriceTable.ind == p.index,
                PriceTable.symbol == p.symbol,
                PriceTable.date == p.date,
            ).first()
            if dp is None:
                dp = PriceTable(ind=p.index, symbol=p.symbol, date=p.date)
                session.add(dp)   # use merge to avoid dup key in same session
            # update non-primary columns
            dp.high = p.high
            dp.low = p.low
            dp.open = p.open
            dp.close = p.close
            dp.volume = p.volume
        # write into database
        session.commit()
        return True
    except OperationalError:
        session.rollback()
        _logger.info("Error: database OperationalError")
        return False
    # except:
    #     session.rollback()
    #     _logger.info("Error: unexpected error" + str(sys.exc_info()[0]))
    #     return False
