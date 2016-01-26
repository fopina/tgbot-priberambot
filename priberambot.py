#!/usr/bin/env python
# coding=utf-8

import tgbot
from plugins import priberam, intro
import argparse


def setup(db_url=None, token=None):
    tg = tgbot.TGBot(
        token,
        plugins=[
            priberam.PriberamPlugin(),
            intro.IntroPlugin(
                intro_text='''\
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
                markdown=True
            ),
        ],
        no_command=priberam.PriberamPlugin(),
        inline_query=priberam.PriberamPlugin(),
        db_url=db_url,
    )
    return tg


def main():
    parser = build_parser()
    args = parser.parse_args()

    tg = setup(db_url=args.db_url, token=args.token)

    if args.list:
        tg.print_commands()
        return

    if args.create_db:
        tg.setup_db()
        print 'DB created'
        return

    if args.webhook is None:
        tg.run(polling_time=args.polling)
    else:
        tg.run_web(args.webhook[0], host='0.0.0.0', port=int(args.webhook[1]))


def build_parser():
    parser = argparse.ArgumentParser(description='Run PriberamBot')

    parser.add_argument('--polling', '-p', dest='polling', type=float, default=2,
                        help='interval (in seconds) to check for message updates')
    parser.add_argument('--db_url', '-d', dest='db_url', default='sqlite:///bot.sqlite3',
                        help='URL for database (default is sqlite:///bot.sqlite3)')
    parser.add_argument('--list', '-l', dest='list', action='store_const',
                        const=True, default=False,
                        help='plugin method to be used for non-command messages (ex: plugins.simsimi.SimsimiPlugin.simsimi)')
    parser.add_argument('--webhook', '-w', dest='webhook', nargs=2, metavar=('hook_url', 'port'),
                        help='use webhooks (instead of polling) - requires bottle')
    parser.add_argument('--create_db', dest='create_db', action='store_const',
                        const=True, default=False,
                        help='setup database')
    parser.add_argument('--token', '-t', dest='token',
                        help='token provided by @BotFather')

    return parser


if __name__ == '__main__':
    main()
