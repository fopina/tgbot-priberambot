# coding=utf-8

from tgbot import plugintest, webserver
import webtest
import priberambot


class WebTest(plugintest.PluginTestCase):
    def setUp(self):
        self.bot = self.prepare_bot(priberambot.setup('sqlite:///:memory:', '123'))
        self.bot.setup_db()
        self.webapp = webtest.TestApp(webserver.wsgi_app([self.bot]))

    def test_web(self):
        self.webapp.post_json('/update/123', params=self.build_message(u'Supercalifragilisticexpialidocious'))
        self.assertReplied(u'Palavra não encontrada')
