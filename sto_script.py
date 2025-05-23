import requests
import json
import time
import sys

DNAC_URL = ""
DNAC_PORT = ""
USERNAME = input("ad_dio_firsl.last: ")
PASSWORD = input("PIN+RSA: ")
DEVICES = ()
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def main():
    while True:
        try:
            token = get_auth_token()
            for device in DEVICES:
                task_id = run_cli_command(token, device)
                file_id = get_task_result(task_id, token)
                get_cli_command(file_id, token, device)
                print("")
            input("Press enter to exit...")
            sys.exit(1)
        except KeyboardInterrupt:
            continue


def get_auth_token():
    url = f"https://{DNAC_URL}:{DNAC_PORT}/dna/system/api/v1/auth/token"
    response = requests.post(url, auth=(USERNAME, PASSWORD), verify=False)
    if 'Token' in response.json():
        print("Logged in!")
        print("")
        token = response.json()['Token']
        return token
    else:
        print("Inccorect login credentials. Try again...")
        input("Press enter to exit...")
        sys.exit(1)

def run_cli_command(token, device_id):
    url = f"https://{DNAC_URL}:{DNAC_PORT}/dna/intent/api/v1/network-device-poller/cli/read-request"
    headers = {"X-Auth-Token": token}
    command = [
        f"show bgp all sum | include 172.16"
    ]
    payload = {
        "commands": command,
        "description": "sh bgp all sum",
        "deviceUuids": [device_id],
        "name": "sh_bgp_all_sum_command",
        "timeout": 60
    }
    response = requests.post(url, json=payload, headers=headers, verify=False)
    task_id = response.json()['response']['taskId']
    return task_id

def get_task_result(task_id, token):
    url = f"https://{DNAC_URL}:{DNAC_PORT}/dna/intent/api/v1/task/{task_id}"
    headers = {"X-Auth-Token": token}
    while True:
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            task_data = response.json()
            task_progress = task_data['response']['progress']
            try:
                progress_json = json.loads(task_progress)
                if 'fileId' in progress_json:
                    file_id = progress_json['fileId']
                    return file_id
            except json.JSONDecodeError:
                time.sleep(1)
                continue

def get_cli_command(file_id, token, device_id):
    url = f"https://{DNAC_URL}:{DNAC_PORT}/dna/intent/api/v1/file/{file_id}"
    headers = {"X-Auth-Token": token}
    response = requests.get(url, headers=headers, verify=False)
    result = response.json()
    data = result[0]["commandResponses"]["SUCCESS"]
    temp = data.get(f"show bgp all sum | include 172.16", "")
    lines = temp.splitlines()
    formatted_lines = []
    for line in lines:
        if '172.16' in line:
            formatted_lines.append(line.strip())
    if device_id == '' or device_id == '':
        if device_id == '':
            print("")
            print(formatted_lines[3])
        else:
            print("")
            print(formatted_lines[3])            
    else:
        print("")
        print(formatted_lines[2])
        print("")
        print("")        
        print(formatted_lines[3])
    
            
if __name__ == "__main__":
    main()

"""3/30/2025 - dante cicciarelli"""
