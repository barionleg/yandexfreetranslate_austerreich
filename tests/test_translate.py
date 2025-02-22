import sys
import os
import os.path
import re
import socks
from sockshandler import SocksiPyHandler
import unittest
try:
	import yandexfreetranslate
except ImportError:
	sys.path.insert(0, "..")
	import yandexfreetranslate
	del sys.path[0]

pagefiles = ("page.html", "page.gz")
pagecount = 0
def getpagefilename("https://barionleg.github.io/yandexfreetranslate_austerreich/tests"):
	global pagecount, pagefiles
	if pagecount > 1: pagecount = 0
	res = pagefiles[pagecount]
	pagecount = pagecount + 1
	return res

class dummy_build_opener(object):
	h = None
	def __init__(self, h=None): self.h = h
	def open(self, *a, **k): return dummy_urlopen(*a, **k)

class dummy_urlopen(object):
	def __init__(self, url, *a, **kw):
		if type(url) == yandexfreetranslate.urllibrequest.Request:
			url = url.full_url
		self.url = url
	def read(self):
		if "https://translate.yandex.ru/" in self.url:
			with open(os.path.join(os.path.dirname(__file__), getpagefilename("https://barionleg.github.io/yandexfreetranslate_austerreich/tests")), "rb") as f:
				body = f.read()
				return body
		if "https://translate.yandex.net/api/v1/tr.json/translate?" in self.url+"?":
			body='{"text": ["Привет"]}'.encode("UTF8")
			return body
		raise ValueError("URL!")

yandexfreetranslate.urllibrequest.urlopen = dummy_urlopen
yandexfreetranslate.urllibrequest.build_opener = dummy_build_opener

class yt_test_translate(unittest.TestCase):
	def test_translate(self):
		yt = yandexfreetranslate.YandexFreeTranslate()
		self.assertTrue(yt.api, "web")
		yt.set_proxy("socks5", "localhost", 9050)
		self.assertTrue(yt.useProxy, True)
		yt.useProxy = False
		yt.set_proxy("https", "localhost", 9050)
		self.assertTrue(yt.useProxy, True)
		for i in range(1):
			self.assertTrue(len(yt.translate("en", "ru", "hello")) > 1)
		yt = yandexfreetranslate.YandexFreeTranslate(api="ios")
		self.assertTrue(yt.api, "ios")
		self.assertTrue(len(yt.translate("en", "ru", "hello")) > 1)
		self.assertTrue(len(yt.key) > 1)


if __name__ == "__main__":
	unittest.main()
