#!/usr/bin/env python
# -*- coding: utf-8 -*-

import torndb

db = torndb.Connection("localhost", "facemash", "root", "xws2931336")

print db.get("SELECT count(*) FROM player")

# for i in range(3000):
    # print i
    # db.execute("INSERT INTO player ()VALUES();")
