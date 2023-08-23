import requests
import json
from datetime import datetime, timedelta

COMPONENTS_ID = "84446"
FORM_TOKEN = "b5b34e59195f8d8ee94556071ba0ce8c27696d7e"

def call_api(pDate, OS_USERNAME, OS_PASSWORD):    
    USER_ASSIGN = OS_USERNAME
    YEAR = pDate.strftime("%Y")
    MONTH = pDate.strftime("%b")
    DATE = pDate.strftime("%d")
    DESC = "Hỗ trợ PLX ngày " + pDate.strftime("%d/%m/%Y")
    START_DATE = int(round(pDate.timestamp())) * 1000

    requests.session().cookies.clear()

    #LOGIN
    API_LOGIN = "https://jira.fis.com.vn/login.jsp"
    data = {"os_username":OS_USERNAME,
            "os_password":OS_PASSWORD}
    resp = requests.post(url=API_LOGIN, data=data)
    COOKIE = resp.cookies.get("JSESSIONID")
    TOKEN = resp.cookies.get("atlassian.xsrf.token")

    #CREATE ISSUE
    API_CREATE_ISSUE = "https://jira.fis.com.vn/secure/QuickCreateIssue.jspa?decorator=none"
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    cookies = {"JSESSIONID": COOKIE, 
               "atlassian.xsrf.token": TOKEN}

    data = {"pid":"32602",
            "issuetype":"3",
            "atl_token":TOKEN,
            "formToken":FORM_TOKEN,
            "summary":DESC,
            "security":"10200",
            "customfield_10700":"",
            "customfield_11202":"",
            "customfield_10800":"",
            "components":COMPONENTS_ID,
            "priority":"2",
            "assignee": OS_USERNAME,
            "reporter":"HungNV67",
            "customfield_10103":DATE + "/" + MONTH + "/" + YEAR,
            "duedate":DATE + "/" + MONTH + "/" + YEAR,
            "customfield_10306":"1d",
            "dnd-dropzone":"",
            "customfield_12400":"",
            "fieldsToRetain":"project",
            "fieldsToRetain":"issuetype",
            "fieldsToRetain":"security",
            "fieldsToRetain":"customfield_10700",
            "fieldsToRetain":"customfield_11202",
            "fieldsToRetain":"customfield_10800",
            "fieldsToRetain":"components",
            "fieldsToRetain":"priority",
            "fieldsToRetain":"assignee",
            "fieldsToRetain":"reporter",
            "fieldsToRetain":"customfield_10103",
            "fieldsToRetain":"duedate",
            "fieldsToRetain":"customfield_10306",
            "fieldsToRetain":"labels",
            "fieldsToRetain":"customfield_12400"}

    resp = requests.post(url=API_CREATE_ISSUE, cookies=cookies, data=data)
    json_resp = resp.json()
    ISSUE_ID = json_resp["createdIssueDetails"]["id"]
    ISSUE_KEY = json_resp["createdIssueDetails"]["key"]

    #IN PROGRESS
    API_IN_PROGRESS = "https://jira.fis.com.vn/secure/WorkflowUIDispatcher.jspa"
    payload = {"id":ISSUE_ID, 
            "action":"11",
            "atl_token":TOKEN,
            "decorator":"dialog",
            "inline":"true"}
    resp = requests.get(url=API_IN_PROGRESS, params=payload, cookies=cookies)

    #WORK LOG
    API_WORK_LOG = "https://jira.fis.com.vn/rest/fis-worklog/1.0/createWorkLog"
    payload = {"issueKey":ISSUE_KEY, 
            "userKey":USER_ASSIGN,
            "period":"false",
            "startDate":START_DATE,
            "endDate":START_DATE,
            "workPerDay":"8",
            "typeOfWork":"Create",
            "desc":DESC,
            "ot":"false",
            "type":"gantt",
            "phaseWorklog":"47"}
    resp = requests.get(url=API_WORK_LOG, params=payload, cookies=cookies)

    #COMPLETE
    API_COMPLETE = "https://jira.fis.com.vn/secure/WorkflowUIDispatcher.jspa"
    payload = {"id":ISSUE_ID, 
            "action":"21",
            "atl_token":TOKEN,
            "decorator":"dialog",
            "inline":"true"}
    resp = requests.get(url=API_COMPLETE, params=payload, cookies=cookies)

