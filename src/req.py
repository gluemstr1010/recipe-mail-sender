import json
import requests
from requests.exceptions import HTTPError

# extracting ingredients + measures from api response
def get_list(actual_res_content, var_name):
    vars_list = []

    for i in range(1,20):
        cur_str = "str" + var_name + str(i)
        el = actual_res_content[cur_str]

        if len(el) > 0:
                    vars_list.append(el)
    return vars_list

def contact_api():
    try:
        response = requests.get("https://www.themealdb.com/api/json/v1/1/random.php")
        response.raise_for_status()
        json = response.json()
        actual_res = json["meals"]
        actual_res_content = actual_res[0]
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

    return actual_res_content