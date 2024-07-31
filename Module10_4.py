import threading
import time
from queue import Queue


class Table:
    def __init__(self, number):
        self.number = number
        self.busy = False


class Cafe:
    def __init__(self, tables):
        self.tables = tables
        self.queue = Queue()

    def customer_arrival(self):
        customer_number = 1
        while customer_number <= 20:
            print(f'Гость номер {customer_number} прибыл')
            customer_thread = Customer(customer_number, self)
            customer_thread.start()
            customer_number += 1
            time.sleep(1)

    def serve_customer(self, сustomer):
        table_found = False
        for table in self.tables:
            if not table.busy:
                table.busy = True
                print(f"Гость номер {сustomer.number} сел за стол {table.number}.")
                time.sleep(5)  # время обсуживания одного посетителя
                table.busy = False  # освобождение стола после обслужвания
                print(f"Гость номер {сustomer.number} заплатил и ушёл.")
                table_found = True
                break
        if not table_found:
            print(f"Гость номер {сustomer.number} в ожидании свободного стола.")
            self.queue.put(сustomer)
            self.queue.get()


class Customer(threading.Thread):
    def __init__(self, number, cafe):
        super().__init__()
        self.number = number
        self.cafe = cafe

    def run(self):
        self.cafe.serve_customer(self)

table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
tables = [table1, table2, table3]

cafe = Cafe(tables)

customer_arrival_thread = threading.Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()

customer_arrival_thread.join()
