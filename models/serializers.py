from re import search
from sqlalchemy import Table

class JSONSerializeTable(Table):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _foreign_model_json(self, m_key, db_request_result):
        json_fk_obj = {}
        foreign_key = next(iter(self.c[m_key].foreign_keys))
        foreign_table = search('[^\.]+', str(foreign_key.column)).group(0)
        for f_k in db_request_result.keys():
            if foreign_table in f_k:
                json_fk_obj[f_k.replace(f'{foreign_table}_', '')] = db_request_result[f_k]
        return json_fk_obj 

    def db_result_to_json(self, db_request_result, attention=None, error_msg=None, key_values=None):
        json_obj = {}
        if not db_request_result:
            return json_obj
        for k in self.c.keys():
            if key_values and k not in key_values:
                continue
            if self.c[k].foreign_keys:
                json_obj[k] = self._foreign_model_json(k, db_request_result)
                continue
            json_obj[k] = db_request_result[f'{self.name}_{k}']
        return json_obj