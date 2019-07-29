import random
from datetime import datetime


def gen_trans_id():
    """ 生成交易的流水 """
    now = datetime.now()
    str_date = now.strftime('%Y%m%d%H%M%S%f')
    return str_date + str(random.randint(1000, 9999))

