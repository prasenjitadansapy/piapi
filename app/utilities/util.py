from sqlalchemy.ext.declarative import DeclarativeMeta
import json
from datetime import datetime

class AlchemyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:  # noqa: E501
                data = obj.__getattribute__(field)
                try:
                    if field != 'query' and field != 'query_class':
                        #print('field:', field, ' value: ', data)
                        if isinstance(data, datetime):
                            #print('field:', field, ' value: ', data)
                            data = data.isoformat()

                        json.dumps(data)
                        fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)