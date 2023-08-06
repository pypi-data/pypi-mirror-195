import uuid
import dill


class Script:

    def __init__(self, script_id=None):

        # Id
        if script_id is None:
            script_id = uuid.uuid4()
        self.script_id = script_id

        # Name
        self.name = None

        # Function properties
        self.function = None

    def to_json(self):
        return {
            "script_id": str(self.script_id),
            "name": str(self.name)
        }

    def from_json(self, json):

        if "script_id" in json.keys():
            self.script_id = uuid.UUID(json["script_id"])

        if "name" in json.keys():
            self.name = json["name"]

    def copy(self, myfunction):
        self.function = Function()
        self.function.code = myfunction.__code__


class Function:

    def __init__(self):
        self.code = None
