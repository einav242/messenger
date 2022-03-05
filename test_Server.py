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
                self.assertEqual(self.cl.stop_download, False)
                # print(str(self.cl.running))

                break
            except:
                continue
        # while True:
        #     try:
        #         self.assertEqual(self.cl.bool, False)
        #         # print(str(self.serv.running))
        #         # print(str(self.cl.running))
        #         break
        #     except:
        #         continue

    def test_check_server(self):
        self.serv = server_for_test.server()
        # self.serv = Server.server()

    def test_check_client(self):
        self.cl = client_for_test.client("127.0.0.1", 50500)

    def test_check(self):
        self.assertEqual(True, True)



