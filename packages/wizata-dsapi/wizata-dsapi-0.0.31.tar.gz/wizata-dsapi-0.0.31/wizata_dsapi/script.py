import uuid
import dill


class Script:

    def __init__(self, script_id=None):

        # Id of the Script
        if script_id is None:
            script_id = uuid.uuid4()
        self.script_id = script_id

        # Name
        self.name = None

        # Code content of the script (dill format)
        self.code = None

    def to_json(self):
        return {
            "script_id": str(self.script_id),
            "name": str(self.name)
        }

    def from_json(self, json):
        self.name = json["name"]
