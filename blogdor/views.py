from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
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
            return HttpResponsePermanentRedirect(post.get_absolute_url())
        except Post.DoesNotExist:
            return HttpResponseRedirect(reverse('blogdor_archive'))
    else:
        return _post(request, year, slug)

def post_wpcompat(request, year, month, day, slug):
    if WP_PERMALINKS:
        return _post(request, year, slug)
    else:
        return HttpResponsePermanentRedirect(post.get_absolute_url())

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

#
# Author views
#

def author(request, username):
    try:
        author = User.objects.get(username=username)
        return list_detail.object_list(
                    request,
                    queryset=Post.objects.published().filter(author=author),
                    paginate_by=POSTS_PER_PAGE,
                    template_object_name='post',
                    extra_context={'author':author},
                    allow_empty=True)
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('blogdor_archive'))

#
# Preview view
#

def preview(request, post_id, slug):
    try:
        post = Post.objects.get(pk=post_id, slug=slug)
        if post.is_published:
            return HttpResponsePermanentRedirect(post.get_absolute_url())
        else:
            return list_detail.object_detail(
                    request,
                    queryset=Post.objects.all(),
                    object_id=post_id,
                    template_object_name='post')
    except Post.DoesNotExist:
        return HttpResponseRedirect(reverse('blogdor_archive'))
