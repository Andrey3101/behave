import psycopg2
from time import sleep

class BillingRepo():
    def __init__(self, conn_string):
        self.cont_string = conn_string
        pass

    def get_transaction_code(self, id, status):
        try:
            conn = psycopg2.connect(self.cont_string)
        except:
            print("Not connect to the billing database")
            cur = conn.cursor()
            req = "code"
            cur.execute(req)
            rows = cur.fetchall()
            return rows[0]
        pass