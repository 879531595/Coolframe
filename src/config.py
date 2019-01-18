from sqlalchemy.ext.declarative import declarative_base
entitybase = declarative_base()
log_config = "mysql+pymysql://root:admin123@127.0.0.1:3306/eventlogs"
DOWNLOAD_SLEEP = 0.5

default_config = {
    "sql_config": "mysql+pymysql://root:admin123@127.0.0.1:3306/test",

    "JobID": "1",

    "project_name": "Netflix",

    "headers": {
        "Host": "www.netflix.com",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Mobile Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
    },
    "cookies": None,

    "proxies": None

}


