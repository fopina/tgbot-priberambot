#!/usr/bin/python

import logging
import os
from priberambot import web_app, file_or_value

logging.basicConfig()


application = web_app(
    file_or_value(os.getenv('TG_TOKEN')),
	file_or_value(os.getenv('TG_DBURL')),
    file_or_value(os.getenv('TG_WH_URL')),
)
