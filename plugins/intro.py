# coding=utf-8
from tgbot.pluginbase import TGPluginBase, TGCommandBase


class IntroPlugin(TGPluginBase):
    def list_commands(self):
        return (
            TGCommandBase('start', self.start, 'Introduction', printable=False),
        )

    def start(self, message, text):
        self.bot.send_message(
            message.chat.id,
            '''\
*I can help you with that weird Portuguese word you don't know...*

Just write me any word and I'll lookup its definition for you

_Example:_
_Limítrofe_

You can also use me inline in any other chat by just typing *@priberambot WORD*

_Example:_
_@priberambot Limítrofe_

Do not forget to rate me!
https://telegram.me/storebot?start=priberambot

            ''',
            parse_mode='Markdown'
        )
