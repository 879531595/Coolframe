from src.utils.logutil import handlerbase
from src.utils.dbutil import DBUtil
import logging
from src.config import default_config, DOWNLOAD_SLEEP
import requests
import time
import urllib3
import datetime
import threading
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # disable insecure  warnings



class JobBase():
    RunID = 0
    MOD_BASE = 5
    project_name = default_config.get("project_name")

    headers = default_config.get("headers")

    cookies = default_config.get("cookies")

    proxies = default_config.get("proxies")

    rundate = datetime.datetime.now()



    def __init__(self, *args, **kwargs):
        self.log = self._init_logger()
        self.dbmanager = DBUtil()
        self.on_run()

    @property
    def _table_name(self):
        return str("event_" + self.__class__.__name__).lower()

    @property
    def _handler(self):
        handler = handlerbase(self.RunID, self._table_name)
        handler.set_class_name(self.__class__.__name__)
        return handler

    def thread_run(self, fun):
        threads = []
        for key in range(self.MOD_BASE):
            t = threading.Thread(target=fun, args=(key,), name=str(key))
            # t.setDaemon(True)
            threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join()

    def _init_logger(self):
        logger = logging.getLogger(self.project_name)
        logger.addHandler(self._handler)
        logger.setLevel(logging.DEBUG)
        return logger

    def on_run(self):
        pass


    def download_page(self,
                      obj_url,
                      data=None,
                      validate='',
                      maxRetry=10):

        sour = ''
        iRetry = 0
        while iRetry <= maxRetry:

            try:
                iRetry += 1

                if iRetry >= 2:
                    self.log.info("retry %s with download" % str(iRetry))

                if data is None:
                    response = requests.get(obj_url, headers=self.headers, cookies=self.cookies, proxies=self.proxies, verify=False)
                else:
                    response = requests.post(obj_url, headers=self.headers, cookies=self.cookies, data=data, proxies=self.proxies, verify=False)

                if not response:
                    self.log.error("did not receive any response!")
                    iRetry += 1
                    continue

                sour = response.text
                time.sleep(DOWNLOAD_SLEEP)

                if response.status_code >= 400:
                    continue

                if (validate is not None) and (validate in sour):
                    return sour

            except Exception as ex:
                    self.log.warn(str(ex))

        self.log.error("download all retry failed ")

        return sour







