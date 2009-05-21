from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from django.views.generic import date_based, list_detail
from blogdor.models import Post
from tagging.models import Tag
from tagging.views import tagged_object_list

POSTS_PER_PAGE = getattr(settings, "BLOGDOR_POSTS_PER_PAGE", 10)
YEAR_POST_LIST = getattr(settings, "BLOGDOR_YEAR_POST_LIST", False)
WP_PERMALINKS = getattr(settings, "BLOGDOR_WP_PERMALINKS", False)

#
# Post detail views
#
                            
def post(request, year, slug):
    if WP_PERMALINKS:
        try:
            post = Post.objects.get(date_published__year=year, slug=slug)
            month = "%02d" % post.date_published.month
            day = "%02d" % post.date_published.day
            return HttpResponsePermanentRedirect(reverse('blogdor_post_wpcompat', args=(year, month, day, slug)))
        except Post.DoesNotExist:
            return HttpResponseRedirect(reverse('blogdor_archive'))
    else:
        return _post(request, year, slug)

def post_wpcompat(request, year, month, day, slug):
    if WP_PERMALINKS:
        return _post(request, year, slug)
    else:
        return HttpResponsePermanentRedirect(reverse('blogdor_post', args=(year, slug)))

def _post(request, year, slug):
    return list_detail.object_detail(
                    request,
                    queryset=Post.objects.published().filter(date_published__year=year),
                    slug=slug,
                    template_object_name='post')

#
# Post archive views
#
                  
def archive(request):
    return list_detail.object_list(
                    request,
                    queryset=Post.objects.published(),
                    paginate_by=POSTS_PER_PAGE,
                    template_object_name='post',
                    allow_empty=True)

def archive_month(request, year, month):
    return date_based.archive_month(
                    request,
                    queryset=Post.objects.published(),
                    date_field='date_published',
                    year=year,
                    month=month,
                    month_format="%m",
                    template_object_name='post',
                    allow_empty=True)

def archive_year(request, year):
    return date_based.archive_year(
                    request,
                    queryset=Post.objects.published(),
                    date_field='date_published',
                    year=year,
                    template_object_name='post',
                    make_object_list=YEAR_POST_LIST,
                    allow_empty=True)

#
# Post tag views
#

def tag(request, tag):
    return tagged_object_list(
                    request,
                    Post.objects.published(),
                    tag,
                    paginate_by=POSTS_PER_PAGE,
                    template_object_name='post',
                    extra_context={'tag': tag},
                    allow_empty=True)

def tag_list(request):
    ct = ContentType.objects.get_for_model(Post)
    return list_detail.object_list(
                    request,
                    queryset=Tag.objects.filter(items__content_type=ct),
                    paginate_by=POSTS_PER_PAGE,
                    template_name='blogdor/tag_list.html',
                    template_object_name='tag',
                    allow_empty=True)
    