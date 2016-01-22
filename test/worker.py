#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: mithril
# @Date:   2016-01-20 09:27:54
# @Last Modified by:   mithril
# @Last Modified time: 2016-01-20 11:25:24

from sqlqueue import Queue

import time

path = 'test.db'
queue = Queue(path)


def run():
    while True:
        # get block the progress
        obj = queue.get()

        # return None when empty
        obj = queue.get_nowait()

        # try:
        #     obj = queue.get()
        # except Exception as e:
        #     print e
        #     time.sleep(0.3)
        #     continue

        print obj


if __name__ == '__main__':
    run()