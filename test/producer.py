#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mithril
# @Date:   2016-01-20 09:28:03
# @Last Modified by:   mithril
# @Last Modified time: 2017-05-10 10:35:26

from __future__ import unicode_literals, print_function, absolute_import

import time
import random
import os
import unittest
import shutil
from multiprocessing import Process

from sqlqueue import Queue


def produce(queue, count):
    for i in range(count):
        try:
            queue.put(i)
            print('put:%s' % i)
            time.sleep(0.1)
        except Exception as e:
            print(e.__class__.__name__)
            time.sleep(0.1)

def consume(inqueue, outqueue):
    while True:
        # get block the progress
        obj = inqueue.get()
        print('get:%s' % obj)
        outqueue.put(obj)

        # return None when empty
        # obj = queue.get_nowait()

class ProducerTestCase(unittest.TestCase):
    def setUp(self):
        self.inqueue_path = 'inqueue'
        self.outqueue_path = 'outqueue'
        self.inqueue = Queue(self.inqueue_path)
        self.outqueue = Queue(self.outqueue_path)

    def test_consume(self):
        producer_num = random.randint(2, 8)
        consumer_num = random.randint(2, 5)
        count = random.randint(0, 8)

        total_count = producer_num*count
        print('producer_num:%s\n consumer_num:%s\n total_count:%s\n' % (producer_num, consumer_num, total_count))

        producer_threads = []
        consumer_threads = []


        for i in range(producer_num):
            p = Process(target=produce, args=(self.inqueue, count))
            p.start()
            producer_threads.append(p)

        for i in range(consumer_num):
            p = Process(target=consume, args=(self.inqueue, self.outqueue))
            p.start()
            consumer_threads.append(p)

        [p.join() for p in producer_threads]

        while self.inqueue.qsize():
            time.sleep(0.1)

        time.sleep(3)
        [p.terminate() for p in producer_threads]
        [p.terminate() for p in consumer_threads]

        input_values = [j for j in range(i) for i in range(producer_num)].sort()
        output_values = [i for i in self.outqueue].sort()

        self.assertEqual(input_values, output_values)


    def tearDown(self):
        self.inqueue.close()
        self.outqueue.close()
        os.remove(os.path.abspath(self.inqueue_path))
        os.remove(os.path.abspath(self.outqueue_path))



if __name__ == '__main__':
    unittest.main()