#!/usr/bin/python

import logging
from priberambot import web_app, file_or_value

logging.basicConfig()


application = web_app(
    file_or_value('TG_TOKEN'),
	file_or_value('TG_DBURL'),
    file_or_value('TG_WH_URL'),
)
