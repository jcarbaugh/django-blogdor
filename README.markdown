# django-blogdor

django-blogdor is a project of Sunlight Foundation (c) 2009.
Writen by Jeremy Carbaugh <jcarbaugh@sunlightfoundation.com> and James Turk <jturk@sunlightfoundation.com>

All code is under a BSD-style license, see LICENSE for details.

Source: http://github.com/sunlightlabs/django-blogdor/


## Requirements

python >= 2.5

django >= r10650

django.contrib.comments

django.contrib.markup

tagging >= r155


## Installation

To install run

    python setup.py install

which will install the application into python's site-packages directory.

Add to INSTALLED_APPS:

	'django.contrib.comments',
	'django.contrib.markup',
	'tagging',
	'blogdor',


## Features

### Settings

All settings are optional. The example values are the defaults for each setting.


#### General Settings

The default permalink structure is __year/slug__. A setting of _True_ will use a WordPress compatible permalink structure of __year/month/day/slug__.

	BLOGDOR_WP_PERMALINKS = False

The number of posts to display per list page.

	BLOGDOR_POSTS_PER_PAGE = 10

The default year archive page will display a list of months in the year and links to the month archive pages. A setting of _True_ will display links to the posts as well. If there are a large number of posts per year, this page could take quite some time to render if set to _True_.

	BLOGDOR_YEAR_POST_LIST = False


#### Feed Settings

Use the boring old default feeds if set to _True_. If _False_, you will have to specify the feed URLs yourself, though you may use or extend the Feed classes provided by blogdor (blogdor.feeds.LatestPosts, blogdor.feeds.LatestComments, blogdor.feeds.LatestForTag).

	BLOGDOR_DEFAULT_FEEDS = True

Time-to-live for the feeds. Valid only if _BLOGDOR\_DEFAULT\_FEEDS_ is set to _True_.

	BLOGDOR_FEED_TTL = 120

Number if items to display in feeds. Valid only if _BLOGDOR\_DEFAULT\_FEEDS_ is set to _True_.

	BLOGDOR_ITEMS_PER_FEED = 10


#### Email Settings

Blogdor will sometimes send emails to Post authors. If not specified in settings, __%s__ is replaced by __Site.objects.current_site().domain__.

	BLOGDOR_FROM_EMAIL = 'bounce@%s'


#### Other Settings

Set to your Akismet key if you would like to use Akismet filtering on comments.

	AKISMET_KEY = ''

URL to a default image to show if no Gravatar is found for the email address. If this value is not specified, Gravatar will provide a default image for you.

	GRAVATAR_DEFAULT = ''

The default Gravatar size in pixels. 

	GRAVATAR_SIZE = 96

