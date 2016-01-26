# coding=utf-8
from tgbot import plugintest
from plugins.priberam import PriberamPlugin


class PriberamPluginTest(plugintest.PluginTestCase):
    def setUp(self):
        self.bot = self.fake_bot(
            '',
            plugins=[PriberamPlugin()],
            inline_query=PriberamPlugin(),
            no_command=PriberamPlugin(),
        )

    def test_need_reply(self):
        self.receive_message('/priberam')
        self.assertReplied('Qual palavra?')

        self.receive_message(u'cerveja')
        self.assertReplied(u'''\
*cerveja*
_substantivo feminino_
Bebida levemente alcoólica, feita de cevada e lúpulo.
''')

    def test_not_found(self):
        self.receive_message('/priberam Supercalifragilisticexpialidocious')
        self.assertReplied(u'Palavra não encontrada')

    def test_complex(self):
        self.receive_message(u'/priberam anão')
        self.assertReplied(u'''\
*anão*
_adjectivo_
`1.`Que tem estatura muito menor que a regular.
`2. [Figurado]`Que não é digno de menção.
_substantivo masculino_
`3.`Indivíduo cuja estatura é inferior à dos homens em geral.
''')

    def test_inline(self):
        self.receive_inline(u'bola')
        results = self.pop_reply()[1]['results']
        self.assertEqual(
            [x['title'] for x in results],
            [u'bola', u'bola de cristal', u'bola de neve', u'bola-ao-cesto', u'bolacha']
        )

    def test_chat(self):
        self.receive_message(u'cerveja')
        self.assertReplied(u'''\
*cerveja*
_substantivo feminino_
Bebida levemente alcoólica, feita de cevada e lúpulo.
''')

    def test_chat_group(self):
        chat = {
            'id': -1,
            'title': 'test group',
            'type': 'group',
        }
        self.receive_message(u'cerveja', chat=chat)
        self.assertReplied(u'''\
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
        self.assertNoReplies()
