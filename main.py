import requests
import json
import getpass
import datetime
from requests.auth import HTTPBasicAuth

url = "http://tools.dootax.com.br:8080/jira/rest/tempo-timesheets/4/worklogs/search"


username_absgp = input("Insira o usuário do absgp : ")
password_abssgp = getpass.getpass("Insira a senha do absgp : ")

results = []

def get_worklog():
    username = input("Insira o usuário do jira : ")
    password = getpass.getpass("Insira a sua senha : ")
    initialDate = input("Insira da data inicial (YYYY-MM-DD): ")
    finalDate = input("Insira da data final (YYYY-MM-DD) : ")

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

    for result in response_json:
        results.append({
            "Issue Key": result["issue"]["key"],
            "Start Time": datetime.datetime.strptime(result["started"], "%Y-%m-%d %H:%M:%S.000").strftime("%d/%m/%Y %H:%M"),
            "Time Spent In Seconds": result['timeSpentSeconds'],
        })

    return results

def add_worklog():
    session = requests.Session()
    session.post(
        "http://gp.absoluta.net/login",
        data={
        'email': username_absgp,
        'password': password_abssgp
        }
    )

    response = session.get("http://gp.absoluta.net/api/pm/timesheets/resource-calendars?period=2020-6")

    if response.status_code != 200:
        raise Exception("Credenciais inválidas")

    total = 0

    for result in results:
        if result['Issue Key'] == 'DOON-1089':
            schedule_id = 8156
        elif str(result['Issue Key']).startswith('DOON'):
            schedule_id = 8154
        else:
            schedule_id = 8150

        issue_date = datetime.datetime.strptime(result["Start Time"], "%d/%m/%Y %H:%M")
        start_time = issue_date.strftime("%H:%M")
        time_spent = result['Time Spent In Seconds']
        final_time = issue_date + datetime.timedelta(seconds=time_spent)
        
        payload = json.dumps({
            "date": issue_date.strftime("%Y-%m-%d"),
            "final_time":final_time.strftime("%H:%M"),
            "initial_time":start_time,
            "schedule_id":schedule_id,
            "percentage":10
        })

        response = session.post(
            "http://gp.absoluta.net/api/user/timesheets",
             data=payload,
             headers={
                    "Content-Type": "application/json",
            }
        )

        if response.status_code == 201:
            total += 1

    print("Importados {} registros".format(total))
    

if __name__ == '__main__':
    get_worklog()
    add_worklog()


