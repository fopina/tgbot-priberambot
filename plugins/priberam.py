# coding=utf-8
from tgbot.pluginbase import TGPluginBase, TGCommandBase
from tgbot.botapi import ForceReply, InlineQueryResultArticle
import requests
import HTMLParser
import re
import xml.etree.ElementTree as ET
from tgbot.tgbot import ChatAction


class PriberamPlugin(TGPluginBase):
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
                    # do not include words without definition...
                    if r == u'Palavra não encontrada':
                        continue
                    if len(r) > 510:
                        r = r[:506] + '\n(...)'
                    results.append(InlineQueryResultArticle(x, x, r, parse_mode='Markdown'))
                    # limit to 5 results to avoid looking up too many definitions...
                    if len(results) == 5:
                        break

            self.bot.answer_inline_query(inline_query.id, results, cache_time=3600)

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

            res = self._parse(res.encode('utf-16'))

        except:
            res = u'Palavra não encontrada'

        return res

    def _parse(self, xml):
        root = ET.fromstring(xml)
        word = root[3][0][0][0].text

        def _clear_node(n):
            n.attrib = {}
            n._children = []
            n.text = ''

        map(_clear_node, root.findall('.//*[@class="varpb"]'))
        map(_clear_node, root.findall('.//*[@class="dAO"]'))

        for n in root.findall('.//*[@style]'):
            if 'visibility:hidden' in n.attrib['style']:
                _clear_node(n)

        t = ''
        tag = ''
        for c in root[3][0][1:]:
            if c.tag == 'span':
                if len(c) > 0:
                    t += '_%s_\n' % c[0].attrib.get('title')
            elif c.tag == 'div':
                if c.text:
                    t += '%s\n' % c.text.strip()
                else:
                    prefix = ''
                    tail = ''
                    for d in c:
                        if tail:
                            tail += ' ' + ' '.join(x.strip() for x in d.itertext())
                        else:
                            prefix += ' '.join(x.strip() for x in d.itertext()) + ' '

                        if d.tail:
                            tail += d.tail.strip()

                    if prefix:
                        t += '`%s`' % re.sub('\s+', ' ', prefix.strip())

                    t += '%s\n' % re.sub('\s+', ' ', tail.strip())
            else:
                tag += ' '.join(x.strip() for x in c.itertext()) + ' '
                if c.tail:
                    tag += c.tail.strip() + ' '

        f = '*%s*\n' % (word)
        if tag.strip():
            f += tag + '\n'
        f += t
        return f
