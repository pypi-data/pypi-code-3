from write import Write

class Contribute(Write):
    def __init__(self, api, table, factual_id, params={}):
        Write.__init__(self, api, table, factual_id, params)

    def values(self, values):
        return self._copy({'values': values})

    def _path(self):
        path = 't/' + self.table
        if self.factual_id:
            path += '/' + self.factual_id
        path += '/contribute'
        return path

    def _copy(self, params):
        return Contribute(self.api, self.table, self.factual_id, self.merge_params(params))
