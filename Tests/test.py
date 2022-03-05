import threading
import time
from unittest import TestCase

import client_for_test
import server_for_test


class Testserver(TestCase):
    def test_init_(self):
        server_thread = threading.Thread(target=self.test_check_server)
        server_thread.start()
        client_thread = threading.Thread(target=self.test_check_client)
        client_thread.start()
        while True:
            try:
                self.assertEqual(self.cl.running, True)
                self.assertEqual(self.cl.wait, False)
                break
            except:
                continue

    def test_check_server(self):
        self.serv = server_for_test.server()

    def test_check_client(self):
        self.cl = client_for_test.client("127.0.0.1", 50500)




