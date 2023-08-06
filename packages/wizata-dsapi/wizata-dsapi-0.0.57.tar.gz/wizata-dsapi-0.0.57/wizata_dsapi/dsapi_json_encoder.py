import json
import pandas
import time

from .mlmodel import MLModel
from .script import Script
from .plot import Plot
from .wizard_function import WizardStep, WizardFunction


class DSAPIEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, MLModel):
            json_obj = {
                "model_id": str(obj.model_id),
                "experiment_id": str(obj.experiment_id)
            }
            return json_obj
        if isinstance(obj, Script):
            json_obj = {
                "script_id": str(obj.script_id)
            }
            return json_obj
        if isinstance(obj, Plot):
            json_obj = {
                "plot_id": str(obj.plot_id)
            }
            return json_obj
        if isinstance(obj, pandas.Timestamp):
            return int(time.mktime(obj.timetuple()) * 1000)
        if isinstance(obj, WizardStep):
            json_obj = {
                "id": obj.step_id,
                "order": obj.order
            }
            return json_obj
        if isinstance(obj, WizardFunction):
            json_obj = {
                "title": obj.title,
                "function": obj.function,
                "is_beta": str(obj.is_beta),
                "steps": obj.steps
            }
            return json_obj
        else:
            type_name = obj.__class__.__name__
            raise TypeError("Unexpected type {0}".format(type_name))
