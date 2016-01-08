# coding=utf-8
from tgbot.pluginbase import TGPluginBase, TGCommandBase
from twx.botapi import ForceReply
import requests
import re
import HTMLParser
import xml.etree.ElementTree as ET


class PriberamPlugin(TGPluginBase):
    TAG_RE = re.compile(r'<[^>]+>')
    BR_RE = re.compile(r'<span class="varpb">.*?<\/span>')
    CLEAN_RE = re.compile(r'<span.*?>Copyright.*?<\/span>')
    DBL_SPACE_RE = re.compile(r' +')

    def __init__(self):
        super(PriberamPlugin, self).__init__()
        self.unescaper = HTMLParser.HTMLParser()

    def list_commands(self):
        return (
            TGCommandBase('priberam', self.priberam, 'significado duma palavra'),
        )

    def priberam(self, message, text):
        if not text:
            m = self.bot.send_message(
                message.chat.id,
                'Qual palavra?',
                reply_to_message_id=message.message_id,
                reply_markup=ForceReply.create(selective=True)
            ).wait()
            self.need_reply(self.priberam, message, out_message=m, selective=True)
            return

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
</soap:Envelope>''' % text.encode('ascii', 'xmlcharrefreplace'),
            headers={
                'Content-Type': 'text/xml; charset=utf-8',
                'SOAPAction': 'http://services.priberam.pt/Define',
                'User-Agent': 'Dicionario/2.1.0 CFNetwork/711.4.6 Darwin/14.0.0',
            }
        )
        root = ET.fromstring(res.content)
        res = self.unescaper.unescape(root[0][0][0].text)

        if u'Sugerir a inclusão no dicionário</a> da palavra pesquisada.' in res:
            res = u'Palavra não encontrada'
        else:
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

        self.bot.send_message(message.chat.id, res)
