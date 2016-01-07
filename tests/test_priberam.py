# coding=utf-8
from tgbot import plugintest
from twx.botapi import Update
from plugins.priberam import PriberamPlugin


class PriberamPluginTest(plugintest.PluginTestCase):
    def setUp(self):
        self.bot = self.fake_bot('', plugins=[PriberamPlugin()])
        self.received_id = 1

    def receive_message(self, text, sender=None, chat=None):
        if sender is None:
            sender = {
                'id': 1,
                'first_name': 'John',
                'last_name': 'Doe',
            }

        if chat is None:
            chat = sender

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

    def test_need_reply(self):
        self.receive_message('/priberam')
        self.assertReplied(self.bot, 'Qual palavra?')

        self.receive_message(u'cerveja')
        self.assertReplied(self.bot, u'''\
cerveja
 | s. f.
cerveja \n\
 |â ou ê ou âi|
s. f.
Bebida levemente alcoólica, feita de cevada e lúpulo.\
''')

    def test_not_found(self):
        self.receive_message('/priberam Supercalifragilisticexpialidocious')
        self.assertReplied(self.bot, u'Palavra não encontrada')

    def test_complex(self):
        self.receive_message(u'/priberam anão')
        self.assertReplied(self.bot, u'''\
anão
 | adj.
 | s. m.
anão \n\
adj.
adj.
1.
 Que tem estatura muito menor que a regular.
2.
 [Figurado]
 [Figurado]
 Que não é digno de menção.
s. m.
3.
 Indivíduo cuja estatura é inferior à dos homens em geral.
Feminino: anã. Plural: anãos ou anões.\
''')
