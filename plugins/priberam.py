# coding=utf-8
from tgbot.pluginbase import TGPluginBase, TGCommandBase
from tgbot.botapi import ForceReply, InlineQueryResultArticle
import requests
import re
import HTMLParser
import xml.etree.ElementTree as ET
from tgbot.tgbot import ChatAction


class PriberamPlugin(TGPluginBase):
    TAG_RE = re.compile(r'<[^>]+>')
    BR_RE = re.compile(r'<span class="varpb">.*?<\/span>', re.DOTALL)
    CLEAN_RE = re.compile(r'<span.*?>Copyright.*?<\/span>')
    FSTDIV_RE = re.compile(r'<div style="background-color:#eee; border-color:#cccccc">.*?<\/div>', re.DOTALL)
    DBL_SPACE_RE = re.compile(r' +')

    def __init__(self):
        super(PriberamPlugin, self).__init__()
        self.unescaper = HTMLParser.HTMLParser()

    def list_commands(self):
        return (
            TGCommandBase('priberam', self.priberam, 'Ver o significado duma palavra'),
        )

    def priberam(self, message, text):
        self.bot.send_chat_action(message.chat.id, ChatAction.TEXT)
        if not text:
            m = self.bot.send_message(
                message.chat.id,
                'Qual palavra?',
                reply_to_message_id=message.message_id,
                reply_markup=ForceReply.create(selective=True)
            ).wait()
            self.need_reply(self.priberam, message, out_message=m, selective=True)
            return

        res = self._lookup(text)

        self.bot.send_message(message.chat.id, res, parse_mode='Markdown')

    def chat(self, message, text):
        if not text:
            return
        if message.chat.type == "private":
            self.priberam(message, text)
        else:
            self.priberam(message, text.replace(self.bot.username, ''))

    def inline_query(self, inline_query):
        if not inline_query.offset and inline_query.query:
            res = requests.get(
                'http://priberam.pt/desktopmodules/EVD_dicionarioshortcut/palavraautocomplete.aspx',
                params={'q': inline_query.query},
            )
            results = []

            for x in res.text.split('\n'):
                if x:
                    x = x.split('|')[0]
                    r = self._lookup(x)
                    if len(r) > 510:
                        r = r[:506] + '\n(...)'
                    results.append(InlineQueryResultArticle(x, x, r))

            self.bot.answer_inline_query(inline_query.id, results, cache_time=1)

    def _lookup(self, word):
        try:
            res = requests.post(
                'http://services.flip.pt/dlpo2transformsac/dlpo_format.asmx',
                data='''\
<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
<soap:Body>
<Define xmlns="http://services.priberam.pt/">
<TextoAPesquisar>%s</TextoAPesquisar>
<Modo>iPhone2</Modo>
<acordo>false</acordo>
<lid>2070</lid></Define>
</soap:Body>
</soap:Envelope>''' % word.encode('ascii', 'xmlcharrefreplace'),
                headers={
                    'Content-Type': 'text/xml; charset=utf-8',
                    'SOAPAction': 'http://services.priberam.pt/Define',
                    'User-Agent': 'Dicionario/2.1.0 CFNetwork/711.4.6 Darwin/14.0.0',
                }
            )

            root = ET.fromstring(res.content)
            res = self.unescaper.unescape(root[0][0][0].text)

            if u'Sugerir a inclusão no dicionário</a> da palavra pesquisada.' in res:
                raise Exception()

            res = PriberamPlugin.FSTDIV_RE.sub('', res)
            res = res.replace('\n', '')
            res = res.replace('<br />', '\n')
            res = res.replace('<span', '\n<span')
            res = res.replace('</Categoria>', '\n')
            res = PriberamPlugin.CLEAN_RE.sub('', res)
            res = PriberamPlugin.BR_RE.sub('', res)
            res = PriberamPlugin.TAG_RE.sub('', res)
            res = PriberamPlugin.DBL_SPACE_RE.sub(' ', res)
            res = res.replace(u'\xa0', '')
            res = res.strip()
            res = re.sub(r'\n\s*\n+', '\n', res)

        except:
            res = u'Palavra não encontrada'

        return res
