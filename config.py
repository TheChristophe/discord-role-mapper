import json


class Config:
    data: dict

    def load(self):
        with open("config.json") as file:
            self.data = json.loads(file.read())


config = Config()
