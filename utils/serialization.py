import json
import time
import datetime

from bson.objectid import ObjectId


class AwesomeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return time.mktime(obj.timetuple()) * 1000
        elif isinstance(obj, ObjectId):
            return str(obj)
        else:
            # Lastly, try and coerce into list for serialization of iterators.
            try:
                return super(AwesomeEncoder, self).default(obj)
            except TypeError, exc:
                try:
                    return list(obj)
                except:
                    raise exc


def jsonify(obj, *args, **kwargs):
    return json.dumps(obj, cls=AwesomeEncoder, *args, **kwargs)
