import json
import uuid

import requests
import pickle
import pandas
from .request import Request
from .mlmodel import MLModel
from .dataframe_toolkit import DataFrameToolkit
from .dsapi_json_encoder import DSAPIEncoder

class WizataDSAPIClient:

    def __init__(self):
        self.domain = None
        self.user = None
        self.password = None
        self.protocol = "https"

    def __url(self):
        return self.protocol + "://" + self.user + ":" + self.password + "@" + self.domain + "/dsapi/"

    def __header(self):
        return {'Content-Type': 'application/json'}

    def __request_process(self, method, route, content_json=None, return_type="json"):

        # choosing the right request
        if content_json is None:
            response = requests.request(method, self.__url() + route, headers=self.__header())
        else:
            response = requests.post(self.__url() + route,
                                     headers=self.__header(),
                                     data=json.dumps(content_json, cls=DSAPIEncoder))

        # choosing the right return type
        if response.status_code == 200 and return_type == "json":
            return response.json()
        elif response.status_code == 200 and return_type == "pickle":
            return response.content
        elif response.status_code != 200:
            raise RuntimeError(str(response.status_code) + " - " + response.reason)
        else:
            raise RuntimeError("Cannot find the right action to process the request.")

    def get_infos(self):
        return self.__request_process("GET", "get_infos")

    def get_ds_functions(self):
        return self.__request_process("GET", "get_ds_functions")

    def get_models(self):
        json_models = self.__request_process("GET", "get_models")
        ml_models = []
        for json_model in json_models:
            ml_models.append(MLModel(uuid.UUID(json_model["model_id"])))
        return ml_models

    def get_datas(self, query: Request) -> pandas.DataFrame:
        df_bytes = self.__request_process("POST", "get_datas", query.prepare(), "pickle")
        return pickle.loads(df_bytes)

    def simulate(self, ml_model: MLModel, dataframe: pandas.DataFrame) -> pandas.DataFrame:
        simulation_request = {
            "model_id": str(ml_model.model_id),
            "dataset": DataFrameToolkit.convert_to_json(dataframe)
        }
        df_json = self.__request_process("POST", "simulate", simulation_request, "json")
        return DataFrameToolkit.convert_to_json(df_json)
