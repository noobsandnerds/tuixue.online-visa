import os
import time
import traceback
from global_var import SECRET
from notifier import Notifier
from tuixue_mongodb import VisaStatus
from datetime import datetime, timezone


if __name__ == '__main__':
    last_result = []
    admin = SECRET['admin_email_list']
    while True:
        try:
            time.sleep(30)
            result = VisaStatus.find_visa_status_past24h(
                'F', 'bju', datetime.now(timezone.utc), minutes=10)['available_dates']
            if len(last_result) > 0 and len(result) == 0:
                print(f"{time.asctime()} send email to {admin}")
                Notifier.send_email(title="tuixue error",
                                    content=time.asctime(), receivers=admin)
            last_result = result
            os.system("ps aux|grep websocket|grep -v grep|wc -l>log")
            if int(open('log').read()) != 1:
                print(f"{time.asctime()} send email to {admin}")
                Notifier.send_email(title="tuixue error",
                                    content=time.asctime() + '\nwebsocket killed', receivers=admin)
        except KeyboardInterrupt:
            break
        except Exception:
            print(traceback.format_exc())
            if os.system("service mongod status") > 0:
                os.system("service mongod restart")
            print(f"{time.asctime()} send email to {admin}")
            content = f'{time.asctime()}\n{traceback.format_exc()}\n{last_result}\n{result}'
            Notifier.send_email(title="tuixue error",
                                content=content, receivers=admin)
