import uuid


class Plot:

    def __init__(self, plot_id=None):
        if plot_id is None:
            self.plot_id = uuid.uuid4()
        else:
            self.plot_id = plot_id
        self.name = None
        self.experiment_id = None
        self.figure = None

    def from_json(self, json):

        if "plot_id" in json.keys():
            self.plot_id = uuid.UUID(json["plot_id"])

        if "name" in json.keys():
            self.name = json["name"]

        if "figure" in json.keys():
            self.figure = json["figure"]

        if "experiment_id" in json.keys():
            self.experiment_id = json["experiment_id"]
