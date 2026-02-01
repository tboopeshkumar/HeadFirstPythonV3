import pymysql

class UseDatabase:
    def __init__(self, config: dict):
        self.config = config

    def __enter__(self):
        self.conn = pymysql.connect(**self.config)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        self.cursor.close()
        self.conn.close()