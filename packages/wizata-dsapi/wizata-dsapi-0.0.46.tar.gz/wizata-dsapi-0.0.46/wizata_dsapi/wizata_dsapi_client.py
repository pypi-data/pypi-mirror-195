import json
import uuid
import sys

import dill
import requests
import pickle
import pandas

import sklearn

from .request import Request
from .mlmodel import MLModel
from .script import Script
from .execution import Execution
from .dataframe_toolkit import DataFrameToolkit
from .dsapi_json_encoder import DSAPIEncoder


class WizataDSAPIClient:

    def __init__(self):

        # properties
        self.domain = None
        self.user = None
        self.password = None
        self.protocol = "https"

    def __url(self):
        return self.protocol + "://" + self.user + ":" + self.password + "@" + self.domain + "/dsapi/"

    def __header(self):
        return {'Content-Type': 'application/json'}

    def __request_process(self, method, route, content_json=None, return_type="json", args=None):

        # choosing the right request
        if content_json is None:
            response = requests.request(method, self.__url() + route, headers=self.__header())
        elif method == "GET":
            response = requests.request(method, self.__url() + route,
                                        headers=self.__header(),
                                        data=json.dumps(content_json, cls=DSAPIEncoder))
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

    def simulate(self, dataframe: pandas.DataFrame, ml_model: MLModel) -> pandas.DataFrame:
        simulation_request = {
            "model_id": str(ml_model.model_id),
            "dataset": DataFrameToolkit.convert_to_json(dataframe)
        }
        df_json = self.__request_process("POST", "simulate", simulation_request, "json")
        return DataFrameToolkit.convert_from_json(df_json["result"])

    def get(self, obj):
        if isinstance(obj, MLModel):
            model_bytes = self.__request_process("POST", "get_model", {"model_id": str(obj.model_id)}, "pickle")
            return pickle.loads(model_bytes)
        if isinstance(obj, Script):
            response = requests.request("GET",
                                        self.__url() + "scripts/" + str(obj.script_id) + "/",
                                        headers=self.__header()
                                        )
            if response.status_code == 200:
                script_bytes = response.content
                return dill.loads(script_bytes)
            else:
                raise RuntimeError(str(response.status_code) + " - " + response.reason)
        else:
            raise TypeError("Type not supported.")

    def create(self, obj):
        if isinstance(obj, Script):
            response = requests.post(self.__url() + "scripts/",
                                     headers=self.__header(),
                                     data=dill.dumps(obj.function),
                                     params={"name": obj.name})
            if response.status_code == 200:
                obj.script_id = uuid.UUID(response.json()["script_id"])
                return obj.script_id
            else:
                raise RuntimeError(str(response.status_code) + " - " + response.reason)
        else:
            raise TypeError("Type not supported.")

    def update(self, obj):
        if isinstance(obj, Script):
            response = requests.put(self.__url() + "scripts/" + str(obj.script_id) + "/",
                                    headers=self.__header(),
                                    data=dill.dumps(obj.function),
                                    params={"name": obj.name})
            if response.status_code == 200:
                return
            else:
                raise RuntimeError(str(response.status_code) + " - " + response.reason)
        else:
            raise TypeError("Type not supported.")

    def delete(self, obj):
        if isinstance(obj, Script):
            response = requests.delete(self.__url() + "scripts" + "/" + str(obj.script_id) + "/",
                                       headers=self.__header())
            if response.status_code == 200:
                return
            else:
                raise RuntimeError(str(response.status_code) + " - " + response.reason)
        else:
            raise TypeError("Type not supported.")

    def execute(self, obj):
        if isinstance(obj, Execution):
            response = requests.post(self.__url() + "execute",
                                     headers=self.__header(),
                                     data=json.dumps(obj.to_json()))
            return response.json()
        else:
            raise TypeError("Type not supported.")

