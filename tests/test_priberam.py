# coding=utf-8
from tgbot import plugintest
from tgbot.botapi import Update
from plugins.priberam import PriberamPlugin

from requests.packages import urllib3
urllib3.disable_warnings()


class FakeInlineTelegramBot(plugintest.FakeTelegramBot):
    # TODO - improve this and add it to tgbotplug
    def answer_inline_query(self, inline_query_id, results, cache_time=None, is_personal=None, next_offset=None, **kwargs):
        self._sent_messages.append(([inline_query_id, results], kwargs))
        self._current_message_id += 1
        return FakeInlineTelegramBot.FakeRPCRequest(True)


class PriberamPluginTest(plugintest.PluginTestCase):
    def setUp(self):
        self.bot = FakeInlineTelegramBot(
            '',
            plugins=[PriberamPlugin()],
            inline_query=PriberamPlugin(),
            no_command=PriberamPlugin(),
        )
        self.received_id = 1

    def test_need_reply(self):
        self.receive_message('/priberam')
        self.assertReplied(self.bot, 'Qual palavra?')

        self.receive_message(u'cerveja')
        self.assertReplied(self.bot, u'''\
*cerveja*
_substantivo feminino_
Bebida levemente alcoólica, feita de cevada e lúpulo.
''')

    def test_not_found(self):
        self.receive_message('/priberam Supercalifragilisticexpialidocious')
        self.assertReplied(self.bot, u'Palavra não encontrada')

    def test_complex(self):
        self.receive_message(u'/priberam anão')
        self.assertReplied(self.bot, u'''\
*anão*
_adjectivo_
`1.`Que tem estatura muito menor que a regular.
`2. [Figurado]`Que não é digno de menção.
_substantivo masculino_
`3.`Indivíduo cuja estatura é inferior à dos homens em geral.
''')

    def test_inline(self):
        self.receive_inline(u'bola')
        results = self.last_reply(self.bot)
        self.assertEqual(
            [x.title for x in results],
            [u'bola', u'bola de cristal', u'bola de neve', u'bola-ao-cesto', u'bolacha']
        )

    def test_chat(self):
        self.receive_message(u'cerveja')
        self.assertReplied(self.bot, u'''\
*cerveja*
_substantivo feminino_
Bebida levemente alcoólica, feita de cevada e lúpulo.
''')

    def test_chat_group(self):
        chat = {
            'id': 1,
            'title': 'test group',
            'type': 'group',
        }
        self.receive_message(u'cerveja', chat=chat)
        self.assertReplied(self.bot, u'''\
*cerveja*
_substantivo feminino_
Bebida levemente alcoólica, feita de cevada e lúpulo.
''')

    def test_chat_group_no_text(self):
        chat = {
            'id': 1,
            'title': 'test group',
            'type': 'group',
        }
        self.receive_message(u'', chat=chat)
        # no replies
        self.assertRaises(AssertionError, self.last_reply, self.bot)

    def receive_message(self, text, sender=None, chat=None):
        if sender is None:
            sender = {
                'id': 1,
                'first_name': 'John',
                'last_name': 'Doe',
            }

        if chat is None:
            chat = {'type': 'private'}
            chat.update(sender)

        self.bot.process_update(
            Update.from_dict({
                'update_id': self.received_id,
                'message': {
                    'message_id': self.received_id,
                    'text': text,
                    'chat': chat,
                    'from': sender,
                }
            })
        )

        self.received_id += 1

    def receive_inline(self, query, sender=None):
        if sender is None:
            sender = {
                'id': 1,
                'first_name': 'John',
                'last_name': 'Doe',
            }

        self.bot.process_update(
            Update.from_dict({
                'update_id': self.received_id,
                'message': None,
                'inline_query': {
                    'id': self.received_id,
                    'query': query,
                    'from': sender,
                    'offset': '',
                }
            })
        )

        self.received_id += 1
