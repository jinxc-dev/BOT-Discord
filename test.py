
import  requests
import hq
# from date import datetime
import time
from datetime import date, datetime
hq_inst = hq.HQ()
# print(hq_inst.generator_name(3))
hq_inst.authenticate('+19132574252')
sms_code = input('Enter SMS code sent: ')
sms_code.strip()
vv = hq_inst.verification(sms_code)
print(str(vv))

# print(str(hq_inst.get_user('bPrice212')))
# user = hq_inst.create_referrel('testestst')
# print(str(user))

# info = hq_inst.get_show_info()
# print(str(info))
# datetime.now()
# print(time.strftime("%Y-%m-%dT%H:%M:%S:%Z", time.gmtime()))
datetime.strptime('2018-06-27T00:00:00.000Z', '%Y-%m-%dT%H:%M:%S.000Z')
#date.fromtimestamp('2018-06-27T00:00:00.000Z')
# print(str(test))