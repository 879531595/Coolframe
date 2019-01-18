from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import entitybase, default_config

class DBUtil(object):
    Base = entitybase()
    config = default_config.get("sql_config")

    def __init__(self):
        self._init_engine_and_Session()
        self._initdb()

    def _init_engine_and_Session(self):
        self._engine = create_engine(self.config, max_overflow=5)
        self._Session = sessionmaker(bind=self._engine)()

    def _initdb(self):
        self.Base.metadata.create_all(self._engine)

    def add_Entity_to_Session(self, entity):
        '''writing in session from an entity'''
        try:
            self._Session.add(entity)
            self.save()
        except Exception as ex:
            self._Session.rollback()
            raise ex
        return True

    def add_Entitys_to_Session(self, entityList):
        '''writing in session from list of EntityList'''

        if entityList:
            for entity in entityList:
                try:
                    self._Session.add(entity)
                except Exception as e:
                    self._Session.rollback()
                    raise e
        else:
            return False

        self.save()
        return True

    def select_by_Session(self, entityclass_name, filter):
        ''' entity is class , is not object()
        filter format: {id:123, name:hello}
        '''
        try:
            result = self._Session.query(entityclass_name).filter_by(**filter).all()
            return result
        except Exception as ex:
            self._Session.rollback()
            raise ex

    def select_by_sql(self, sql):
        try:
            data_query = self._Session.execute(sql)
            result = data_query.fetchall()
            return result
        except Exception as ex:
            self._Session.rollback()
            raise ex

    def update_by_sql(self, sql):
        try:
            if self._Session.execute(sql):
                return True
        except Exception as ex:
            self._Session.rollback()
            raise ex

    def update_by_Session(self):
        # step1: execute select_by_Session return result
        # step2: Direct assignment operation
        pass

    def save(self):
        '''save entitys to db'''
        try:
            self._Session.commit()
        except Exception as ex:
            self._Session.rollback()
            raise ex












