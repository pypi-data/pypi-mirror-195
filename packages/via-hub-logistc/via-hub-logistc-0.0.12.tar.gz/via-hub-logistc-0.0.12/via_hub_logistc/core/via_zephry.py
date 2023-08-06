import requests

from base64 import b64encode

from via_hub_logistc.model.zephry import TestFolder, TestCycle


class TestRunner():
    def __init__(self, url, usr, pwd):
        self.url = url
        self.user = usr
        self.pwd = pwd

    ###Create new folder for test regression ###
    def regression_create_folder(self, date_run: str, projectKey: str):
        uri = self.url + "folder"

        headers = {
            "Authorization": "Basic " + b64encode(f"{self.user}:{self.pwd}".encode('utf-8')).decode("ascii")
        }

        folder_name = f"/ViaOps/{date_run}"

        payload = TestFolder(projectKey, folder_name, "TEST_RUN").__dict__

        requests.request("POST", uri, json=payload, headers=headers)

        return folder_name

    ###Create new cycle for test regression ###
    def regression_create_cycle(self, date_run: str, name_cycle: str, descripption: str, key: str, iteration: str, owner: str, test_plan: str, cycle_date: str, status: str):
        folder_name = self.regression_create_folder(date_run, key)

        payload = TestCycle(
            name_cycle,
            descripption,
            key,
            folder_name,
            iteration,
            owner,
            test_plan,
            cycle_date,
            status,
            []
        ).__dict__

        uri = self.url + "testrun"

        headers = {
            "Authorization": "Basic " + b64encode(f"{self.user}:{self.pwd}".encode('utf-8')).decode("ascii")
        }

        response = requests.request("POST", uri, json=payload, headers=headers)

        return response.json()["key"]

    ### Add scenarios to an existing cycle  ###
    def regression_add_test_result(self, cycle: str, list_scenarios: dict):

        for scenario in list_scenarios:
            uri = self.url + \
                f'testrun/{cycle["id"]}/testcase/{scenario["id"]}/testresult'

            headers = {
                "Authorization": "Basic " +  b64encode(f"{self.user}:{self.pwd}".encode('utf-8')).decode("ascii")
            }

            requests.request('POST', uri, json=scenario["tc"], headers=headers)


class TestCase():
    ### Load info the of created test case ###
    def get_creator_test(self, test_key):

        uri = self.url + f'testcase/{test_key}'

        headers = {
            "Authorization":"Basic " +  b64encode(f"{self.user}:{self.pwd}".encode('utf-8')).decode("ascii")
        }

        response = requests.request("GET", uri, headers=headers)

        return response.json()["owner"]