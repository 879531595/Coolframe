# coding: utf-8
import logging
from sqlalchemy import (Column, Integer, MetaData,
                         Table, create_engine, BigInteger, DATETIME, SmallInteger, VARCHAR)
from sqlalchemy.sql import func
from sqlalchemy.orm import mapper, sessionmaker, clear_mappers
from src.config import default_config, log_config


class LoggerUtil(logging.Handler):
    _mapperflag = False
    Table_args = [
         Column("EventID", BigInteger, primary_key=True, autoincrement=True),
         Column("EventTime", DATETIME, nullable=False, default=func.now()),
         Column("SeverityID", SmallInteger, nullable=False),
         Column("JobID", BigInteger, nullable=False),
         Column("RunID",BigInteger, nullable=False),
         Column("PageID", Integer, default=None),
         Column("Subject", VARCHAR(100), default=''),
         Column("Details", VARCHAR(4000), default=''),
         Column("SourceFile",VARCHAR(100), default=None),
         Column("LineNum", Integer, default=None),
         Column("Class", VARCHAR(200), default=None),
         Column("Method", VARCHAR(200), default=None)]

    table_name = None
    class_name = None
    configdb_str = None
    JobID = None
    PageID = None
    RunID = None

    class LogTable(object):
        pass


    def __init__(self):
        self.config_engine = create_engine(self.configdb_str)
        self.ConfigSession = sessionmaker(bind=self.config_engine)
        self.config_session = self.ConfigSession()
        metadata = MetaData(self.config_engine)
        self.log_table = Table(self.table_name, metadata, *self.Table_args)
        metadata.create_all(self.config_engine)
        self.LogModel = metadata.tables.get(self.table_name)

        logging.Handler.__init__(self)

    def set_class_name(self, class_name):
        self.class_name = class_name


    def emit(self, record):
        if not self._mapperflag:
            mapper(self.LogTable, self.log_table)
            self._mapperflag = True
        log_model = self.LogTable()
        log_model.Class = self.class_name
        log_model.Method = str(record.funcName)
        log_model.SeverityID = record.levelno
        log_model.JobID = self.JobID
        log_model.RunID = self.RunID
        log_model.PageID = self.PageID
        args = record.args
        if args:
            log_model.Details = args[0]

        log_model.Subject = str(record.msg)

        pathname = record.pathname
        if pathname:
            if "/" in pathname:
                log_model.SourceFile = str(pathname).split('/')[-1]
            elif "\\" in pathname:
                log_model.SourceFile = str(pathname).split('\\')[-1]

        log_model.LineNum = record.lineno

        self.config_session.add(log_model)
        try:
            self.config_session.commit()
            # clear_mappers()
        except:
            self.config_session.rollback()

    # def close(self):
    #     try:
    #         self.config_session.commit()
    #     except:
    #         self.config_session.rollback()
    #     self.config_session.close()


class handlerbase(LoggerUtil):
    JobID = default_config.get("JobID")
    configdb_str = log_config

    def __init__(self, RunID, table_name):
        self.RunID = RunID
        self.table_name = table_name
        LoggerUtil.__init__(self)










