import requests
import json
import getpass
import datetime
from requests.auth import HTTPBasicAuth
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

url = "http://tools.dootax.com.br:8080/jira/rest/tempo-timesheets/4/worklogs/search"


# username_absgp = input("Insira o usuário do absgp : ")
# password_abssgp = input("Insira a senha do absgp : ")

username_absgp = "renan.hartwig@deliverit.com.br"
password_abssgp = "@Bryant2408"


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

    results = []

    for result in response_json:
        results.append({
            "Issue Key": result["issue"]["key"],
            "Start Time": datetime.datetime.strptime(result["started"], "%Y-%m-%d %H:%M:%S.000").strftime("%d/%m/%Y %H:%M"),
            "Time Spent In Seconds": result['timeSpentSeconds'],
        })

    return results

def add_worklog():
    option = Options()
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=option)
    driver.implicitly_wait(5)  # in seconds
    url = "http://gp.absoluta.net/login"

    try:
        driver.get(url)

        element = driver.find_element_by_name("email")
        element.send_keys(username_absgp)

        element = driver.find_element_by_name("password")
        element.send_keys(password_abssgp)

        driver.find_element_by_xpath("//*[@id='login']/button").click()

        errors = driver.find_elements_by_class_name("alert-danger")

        if len(errors) > 0:
            print(errors[0])
            raise Exception(errors[0].text)


    except Exception as identifier:
            print(identifier)
    finally:
        driver.quit()


if __name__ == '__main__':
    add_worklog()


