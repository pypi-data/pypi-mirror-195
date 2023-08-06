import json
from .mlmodel import MLModel


class DSAPIEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, MLModel):
            json_obj = {
                "model_id": str(obj.model_id),
                "experiment_id": str(obj.experiment_id)
            }
            return json_obj
        else:
            type_name = obj.__class__.__name__
            raise TypeError("Unexpected type {0}".format(type_name))