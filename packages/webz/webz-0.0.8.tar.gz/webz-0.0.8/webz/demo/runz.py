#coding=utf-8
from servers import test
fps = [
    "./test.confz"
]
from webz import config
config.Static.update_time(1)
test.runz(fps)

