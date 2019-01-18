from src.config import entitybase
from sqlalchemy import (Column, Integer, MetaData,BigInteger, SmallInteger,
                        VARCHAR , Integer, DECIMAL, DATETIME, ForeignKey, Boolean)

from sqlalchemy.dialects.mysql import LONGTEXT


class Netflix_detail(entitybase):
    __tablename__ = "netflix_plan2"
    tid = Column(Integer, primary_key=True, autoincrement=True)
    info_tid = Column(Integer, ForeignKey('netflix_page2.tid'))
    locale_id = Column(VARCHAR(100))
    plan_name = Column(VARCHAR(500))
    price_duration = Column(VARCHAR(500))
    currency = Column(VARCHAR(500))
    price = Column(DECIMAL(18, 2))
    num_screens = Column(Integer)
    is_hd_available = Column(Boolean)
    is_ultra_hd_available = Column(Boolean)
    InsertUpdateTime = Column(DATETIME)
    Rundate = Column(DATETIME)



class Netflix_info(entitybase):
    __tablename__ = "netflix_page2"
    tid = Column(Integer, primary_key=True, autoincrement=True)
    locale_id = Column(VARCHAR(500))
    PageSource = Column(LONGTEXT)
    InsertUpdateTime = Column(DATETIME)
    Rundate = Column(DATETIME)