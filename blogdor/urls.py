from django.conf import settings
from django.conf.urls import patterns, include, url
from blogdor.views import ShowPost
from blogdor.views import ShowPostWP
from blogdor.views import ShowYearArchive
from blogdor.views import ShowMonthArchive
from blogdor.views import ShowArchive
from blogdor.views import AuthorPosts
from blogdor.views import PreviewPost
from blogdor.views import TagList

urlpatterns = patterns('blogdor.views',

    # comment urls
    url(r'^comment/', include('django.contrib.comments.urls')),

    # tags
    url(r'^tag/(?P<tag>[^/]+)/$', 'tag', name='blogdor_tag'),
    url(r'^tag/$', TagList.as_view(), name='blogdor_tag_list'),

    # archives
    url(r'^(?P<year>\d{4})/$', ShowYearArchive.as_view(), name='blogdor_archive_year'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', ShowMonthArchive.as_view(), name='blogdor_archive_month'),
    url(r'^$', ShowArchive.as_view(), name='blogdor_archive'),

    # post
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[\w-]+)/$', ShowPostWP.as_view(), name='blogdor_post_wpcompat'),
    url(r'^(?P<year>\d{4})/(?P<slug>[\w-]+)/$', ShowPost.as_view(), name='blogdor_post'),

    # author
    url(r'^author/(?P<username>[\w]+)/$', AuthorPosts.as_view(), name='blogdor_author'),

    # preview
    url(r'^preview/(?P<post_id>\d+)/(?P<slug>[\w-]+)/$', PreviewPost.as_view(), name='blogdor_preview'),

)

if getattr(settings, 'BLOGDOR_ENABLE_FEEDS', True):

    from blogdor import feeds

    urlpatterns += patterns('',
        url(r'^feeds/latest/$', feeds.LatestPosts()),
        url(r'^feeds/comments/$', feeds.LatestComments()),
        url(r'^feeds/tag/(?P<tag>[\w-]+)/$', feeds.LatestForTag()),
        url(r'^feeds/author/(?P<author>[\w-]+)/$', feeds.LatestForAuthor()),
    )
