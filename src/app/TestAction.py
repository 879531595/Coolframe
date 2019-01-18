from src.core.JobBase import JobBase
from src.app.TestEntity import Netflix_info, Netflix_detail
import re
import json
import datetime

class NetflixAction(JobBase):
    _url = "https://www.netflix.com/signup/planform"

    def __init__(self, *args, **kwargs):
        JobBase.__init__(self, *args, **kwargs)


    def on_run(self):
        self.log.info("started TestAction")
        self.collect_product()
        self.log.info("finished TestAction")


    def collect_product(self):
        sour = self.download_page(self._url, validate="netflix.reactContext")

        info_obj = re.search(r'netflix.reactContext\s*=\s*(.*?)\s*;</script>', sour, re.I | re.S)
        if info_obj:
            info_str = info_obj.group(1).strip()
            regex = re.compile(r'\\(?![/u"])')
            fixed = regex.sub(r"\\\\", info_str)
            json_info = json.loads(fixed)


            locale = json_info.get("models").get("signupContext").get("data").get("geo").get("locale")
            locale_id = locale.get("id")
            self.log.info("localed_id:%s" % (locale_id))

            netflix_info = Netflix_info()
            netflix_info.locale_id = locale_id  # info.locale_id
            netflix_info.PageSource = sour  # info.PageSource
            netflix_info.InsertUpdateTime = datetime.datetime.now()  # info.InsertUpdateTime
            netflix_info.Rundate = self.rundate
            self.dbmanager.add_Entity_to_Session(netflix_info)
            self.dbmanager.save()

            options = json_info.get("models").get("signupContext").get("data").get("flow").get("fields").get(
                "planChoice").get(
                "options")
            for item in options:
                try:
                    netflix_detail = Netflix_detail()
                    detail = item.get("fields")
                    netflix_detail.info_tid = netflix_info.tid
                    netflix_detail.locale_id = locale_id
                    netflix_detail.plan_name = detail.get("localizedPlanName").get("value")
                    netflix_detail.price_duration = detail.get("billingFrequency").get("value")
                    netflix_detail.price = float(detail.get("planPriceAmount").get("value"))
                    netflix_detail.currency = detail.get("planPriceCurrency").get("value")
                    netflix_detail.num_screens = detail.get("planMaxScreenCount").get("value")
                    netflix_detail.is_hd_available = detail.get("planHasHd").get("value")
                    netflix_detail.is_ultra_hd_available = detail.get("planHasUltraHd").get("value")
                    netflix_detail.InsertUpdateTime = datetime.datetime.now()
                    netflix_detail.Rundate = self.rundate

                    self.dbmanager.add_Entity_to_Session(netflix_detail)
                    self.dbmanager.save()
                except Exception as ex:
                    self.log.error(str(ex))








