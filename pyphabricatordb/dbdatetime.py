from sqlalchemy import types
from datetime import datetime, timedelta
from time import mktime

class dbdatetime(types.TypeDecorator):
    impl = types.Integer

    def process_bind_param(self, value, dialect):
        return int(mktime(value.timetuple()))

    def process_result_value(self, value, dialect):
        return datetime.fromtimestamp(value)
