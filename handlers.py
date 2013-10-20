# -*- coding: utf-8 -*-

import tornado.web
from random import randint
from math import pow
from time import time
from hashlib import md5
import torndb
import memcache
import os


def cal_E(ra, rb):
    return 1 / (1 + pow(10, (float(ra) - float(rb))/400))


def cal_R(r, e, s):
    return float(r) + 16 * (float(s) - float(e))


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db


    def initialize(self):
        if "SERVER_SOFTWARE" in os.environ:
            from bae.api.memcache import BaeMemcache
            self.cache = BaeMemcache()
        else:
            self.cache = memcache.Client(['127.0.0.1:11211'], debug=True)

    def on_finish(self):
        self.db.close()

    def get_player(self):
        pa = self._get_one_player()
        pb = self._get_one_player()
        while pa.id == pb.id:
            pb = self._get_one_player()

        return [pa, pb]

    def _get_one_player(self):
        total = self.db.get("SELECT count(*) as total FROM player;")
        # 得到两个不重复的 player
        rand = randint(0, total.total)

        result = self.db.get("SELECT * FROM player LIMIT %s, 1;", rand)

        return result

    def compare(self, a, b):
        c = (a["r"] - b["r"]) / 400
        e = pow(10, c)
        ea = 1 / (1 + e)
        rb = 1 / (1 + 1/e)
        r = 32 * ea

        ra = a["r"] + r
        rb = a["r"] - r

        values = [(ra, a["id"]), (rb, b["id"])]
        self.db.updatemany("UPDATE player SET r=%s WHERE id=%s", values)
        self.db.insert("INSERT INTO ip (`ip`) VALUES(%s);", self.request.remote_ip)


class IndexHandler(BaseHandler):
    def get(self):
        player = self.get_player()
        template_values = dict()
        template_values["A"] = player[0]
        template_values["B"] = player[1]
        template_values["total"] = self.db.get("SELECT count(*) as total FROM ip;").total
        # token 防止作弊
        token = "A:%s&B%s;time:%s;key" % (player[0].id, player[1].id, time())
        token = md5(token).hexdigest()
        self.cache.set(token, token, time=180)
        template_values["token"] = token

        self.render("index.html", **template_values)


    def post(self):
        a = self.get_argument("a", None)
        b = self.get_argument("b", None)
        token = self.get_argument("token", None)

        pa = self.db.get("SELECT * FROM player WHERE id=%s;", int(a))
        pb = self.db.get("SELECT * FROM player WHERE id=%s;", int(b))

        if pa is None or pb is None:
            return self.write("非法请求")

        if token is None:
            return self.write("非法请求")
        if self.cache.get(token.encode("utf-8")) is None:
            return self.write("非法请求")

        self.compare(pa, pb)
        self.cache.delete(token.encode("utf-8"))

        self.redirect("/", permanent=True)


class TopHandler(BaseHandler):
    def get(self):

        top = self.db.query("SELECT * FROM player ORDER BY r DESC LIMIT %s;", 10)
        template_values = dict()
        template_values["top"] = top
        template_values["total"] = self.db.get("SELECT count(*) as total FROM ip;").total

        # self.write("%r" % top)
        self.render("top.html", **template_values)


class SetUpHandler(BaseHandler):
    def get(self):
        count = self.db.get("SELECT count(*) as count from player;").count
        if count != 0:
            self.redirect("/", permanent=True)
            return

        path = os.path.join(os.path.dirname(__file__), "static/images")
        # files = list()
        files = os.listdir(path)
        # for name in os.listdir(path):
            # files.append((name))
        self.db.insertmany("INSERT INTO player (`path`) VALUES (%s);", files)

        self.write("%r" % 1)
