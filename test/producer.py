#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mithril
# @Date:   2016-01-20 09:28:03
# @Last Modified by:   mithril
# @Last Modified time: 2016-01-20 10:19:23

from sqlqueue import Queue
import time
import random

path = 'test.db'
queue = Queue(path)

def run():
    i = 0
    while True:
        try:
            obj = queue.put(i)
            print 'put:%s' % i
            i +=1
            time.sleep(1)
        except Exception as e:
            print e.__class__.__name__
            time.sleep(1)



if __name__ == '__main__':
    run()