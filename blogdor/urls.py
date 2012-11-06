from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('blogdor.views',

    # comment urls
    url(r'^comment/', include('django.contrib.comments.urls')),

    # tags
    url(r'^tag/(?P<tag>[^/]+)/$', 'tag', name='blogdor_tag'),
    url(r'^tag/$', 'tag_list', name='blogdor_tag_list'),

    # archives
    url(r'^(?P<year>\d{4})/$', 'archive_year', name='blogdor_archive_year'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'archive_month', name='blogdor_archive_month'),
    url(r'^$', 'archive', name='blogdor_archive'),

    # post
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[\w-]+)/$', 'post_wpcompat', name='blogdor_post_wpcompat'),
    url(r'^(?P<year>\d{4})/(?P<slug>[\w-]+)/$', 'post', name='blogdor_post'),

    # author
    url(r'^author/(?P<username>[\w]+)/$', 'author', name='blogdor_author'),

    # preview
    url(r'^preview/(?P<post_id>\d+)/(?P<slug>[\w-]+)/$', 'preview', name='blogdor_preview'),

)

if getattr(settings, 'BLOGDOR_ENABLE_FEEDS', True):

    from blogdor import feeds

    urlpatterns += patterns('',
        url(r'^feeds/latest/$', feeds.LatestPosts()),
        url(r'^feeds/comments/$', feeds.LatestComments()),
        url(r'^feeds/tag/$', feeds.LatestForTag()),
        url(r'^feeds/author/$', feeds.LatestForAuthor()),
    )
