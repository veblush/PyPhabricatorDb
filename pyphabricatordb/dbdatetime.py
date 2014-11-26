from datetime import datetime, timedelta
from sqlalchemy import Integer, UnicodeText, Float, DateTime, Boolean, types, Table, event

class dbdatetime(types.TypeDecorator):
    impl = types.Integer
    epoch = datetime(1970, 1, 1)

    def process_bind_param(self, value, dialect):
        return int((value - self.epoch).total_seconds())

    def process_result_value(self, value, dialect):
        return datetime.fromtimestamp(value)
