#!/usr/bin/env python

# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Elliot Smith'
SITENAME = 'Elliot Smith'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Australia/Brisbane'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = ()

# Social widget
SOCIAL = (
        ('github', 'https://github.com/smitec'),
        ('twitter', 'https://twitter.com/smitec'),
        )

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

THEME = '/home/smitec/pelican-themes/Flex/'


SIDEBAR_DIGEST = 'Programmer and Web Developer'

DISPLAY_PAGES_ON_MENU = True

TWITTER_USERNAME = 'smitec'

MENUITEMS = (('Blog', SITEURL),)


STATIC_PATHS = ['images', 'extra']

EXTRA_PATH_METADATA = {
        'extra/custom.css': {'path': 'static/custom.css'},
}

CUSTOM_CSS = 'static/custom.css'


MARKUP = ('md', 'ipynb')

PLUGIN_PATHS = ('./plugins',)
PLUGINS = ['ipynb.markup']
