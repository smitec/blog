#!/usr/bin/env python

# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Elliot Smith'
SITETITLE = 'Elliot Smith'
SITEURL = 'https://smitec.io'
SITESUBTITLE = 'AI & Medicine'
SITEDESCRIPTION = 'Applications of AI in medicine as well as other related work'
SITELOGO = '/images/profile.jpg'

PATH = 'content'

TIMEZONE = 'Australia/Brisbane'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Social widget
SOCIAL = (
        ('github', 'https://github.com/smitec'),
        ('twitter', 'https://twitter.com/smitec'),
        )

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

THEME = '/home/smitec/pelican-themes/Flex/'


DISPLAY_PAGES_ON_MENU = True

LINKS = (('Blog', SITEURL),)


STATIC_PATHS = ['images', 'extra', 'extra/CNAME']

EXTRA_PATH_METADATA = {
        'extra/custom.css': {'path': 'static/custom.css'},
        'extra/CNAME': {'path': 'CNAME'}
}

CUSTOM_CSS = 'static/custom.css'


MARKUP = ('md', 'ipynb')

PLUGIN_PATHS = ('./plugins',)
PLUGINS = ['ipynb.markup']
