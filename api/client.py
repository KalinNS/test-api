import requests


class BearClient:

    _s = requests
    host = None

    def __init__(self, host):
        self.host = host

    def create_bear(self, data):
        return self._s.post(self.host + "/bear", json = data)

    def update_bear_id(self, id, data):
        return self._s.put(self.host + "/bear/" + str(id), json = data)

    def delete_all(self):
        return self._s.delete(self.host + "/bear")

    def delete_id(self, id):
        return self._s.delete(self.host + "/bear/" + str(id))

    def info(self):
        return self._s.get(self.host + "/info")

    def read_all(self):
        return self._s.get(self.host + "/bear")

    def read_id(self, id):
        return self._s.get(self.host + "/bear/" + str(id))

    def wrong_ap(self):
        return self._s.get(self.host + "/bears/" )