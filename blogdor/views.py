from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, Http404
from django.shortcuts import render_to_response
from django.views.generic.dates import MonthArchiveView, YearArchiveView
from django.views.generic import ListView, DetailView
from blogdor.models import Post
from tagging.models import Tag
from tagging.views import tagged_object_list

POSTS_PER_PAGE = getattr(settings, "BLOGDOR_POSTS_PER_PAGE", 10)
YEAR_POST_LIST = getattr(settings, "BLOGDOR_YEAR_POST_LIST", False)
WP_PERMALINKS = getattr(settings, "BLOGDOR_WP_PERMALINKS", False)

#
# Post detail views
#
                            
class ShowPost(DetailView):

    model = Post

    def get_queryset(self):
        return Post.objects.published().filter(date_published__year=self.kwargs['year'])


class ShowPostWP(DetailView):

    model = Post

    def get_queryset(self):
        return Post.objects.published().filter(date_published__year=self.kwargs['year'], date_published__month=self.kwargs['month'], date_published__day=self.kwargs['day'])


#
# Post archive views
#

class ShowYearArchive(YearArchiveView):

    queryset = Post.objects.published().select_related()
    date_field = 'date_published'
    make_object_list = YEAR_POST_LIST
    allow_empty = True


class ShowMonthArchive(MonthArchiveView):

    queryset = Post.objects.published().select_related()
    date_field = 'date_published'
    month_format='%m'
    allow_empty = True


class ShowArchive(ListView):

    queryset = Post.objects.published().select_related()
    paginate_by = POSTS_PER_PAGE
    allow_empty = True


#
# Post tag views
#

def tag(request, tag):
    return tagged_object_list(
                    request,
                    Post.objects.published().select_related(),
                    tag,
                    paginate_by=POSTS_PER_PAGE,
                    template_object_name='post',
                    extra_context={'tag': tag},
                    allow_empty=True)


class TagList(ListView):

    model = Tag
    template_name = 'blogdor/tag_list.html'
    template_object_name = 'tag'
    allow_empty = True

    def get_queryset(self):
        if self.request.user.is_staff:
            ct = ContentType.objects.get_for_model(Post)
            return Tag.objects.filter(items__content_type=ct).distinct()
        raise Http404


#
# Author views
#

class AuthorPosts(ListView):

    paginate_by=POSTS_PER_PAGE
    allow_empty=True
    author = None

    def get_queryset(self):
        try:
            self.author = User.objects.get(username=self.kwargs['username'])
        except User.DoesNotExist:
            raise Http404
        queryset = Post.objects.published().select_related().filter(author=self.author)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(AuthorPosts, self).get_context_data(**kwargs)
        context['author'] = self.author
        return context

#
# Preview view
#

class PreviewPost(DetailView):

    def get_queryset(self):
        post = Post.objects.select_related().filter(pk=self.kwargs['post_id'])
        if post and post[0].is_published:
            return HttpResponsePermanentRedirect(post.get_absolute_url())
        else:
            return post
