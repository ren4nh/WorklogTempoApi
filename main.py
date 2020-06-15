import requests
import pandas as pd
import json
import getpass
import datetime
from requests.auth import HTTPBasicAuth

url = "http://tools.dootax.com.br:8080/jira/rest/tempo-timesheets/4/worklogs/search"

username = input("Insira o usuário do jira :")
password = getpass.getpass("Insira a sua senha :")
initialDate = input("Insira da data inicial (YYYY-MM-DD):")
finalDate = input("Insira da data final (YYYY-MM-DD) :")

request_body = json.dumps({
    "from": initialDate,
    "to": finalDate
})

response = requests.post(
    url,
    data=request_body,
    auth=HTTPBasicAuth(username, password),
    headers={
        "Content-Type": "application/json",
    }
)

if response.status_code != 200:
    print("Não foi possivel logar")


response_json = response.json()

results = []

for result in response_json:
    results.append({
        "Issue Key": result["issue"]["key"],
        "Start Time": datetime.datetime.strptime(result["started"], "%Y-%m-%d %H:%M:%S.000").strftime("%d/%m/%Y %H:%M"),
        "Time Spent In Seconds": result['timeSpentSeconds'],
    })

df = pd.DataFrame.from_dict(results)

df.to_csv('worklog.csv', index=False, sep=';')


