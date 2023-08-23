from datetime import datetime, timedelta
import plx_jira

def run_ts(FDATE, TDATE, MONTH, YEAR, OS_USERNAME, OS_PASSWORD):
    dateString = YEAR + MONTH + FDATE
    fdate = datetime.strptime(dateString, "%Y%m%d")
    tdate = fdate

    i = int(FDATE)
    while i <= int(TDATE): 
        weekno = tdate.weekday()
        if weekno < 5:
            plx_jira.call_api(tdate, OS_USERNAME, OS_PASSWORD)
        i = i + 1
        tdate = tdate + timedelta(days=1)