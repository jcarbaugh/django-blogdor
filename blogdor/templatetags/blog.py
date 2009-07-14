from blogdor import utils
from blogdor.models import Post
from django import template
from django.conf import settings
from django.template.loader import render_to_string
import md5
import urllib

register = template.Library()

class PostsNode(template.Node):
    def __init__(self, queryset, count, offset, varname):
        self.posts = queryset[offset:count+offset]
        self.varname = varname

    def render(self, context):
        context[self.varname] = self.posts
        return ''

class UserPostsNode(template.Node):
    def __init__(self, user, count, offset, varname):
        self.user = template.Variable(user)
        self.count = count
        self.offset = offset
        self.varname = varname

    def render(self, context):
        user = self.user.resolve(context)
        posts = Post.objects.published().filter(author=user)
        context[self.varname] = posts[self.offset:self.count+self.offset]
        return ''


def _simple_get_posts(token, queryset):
    pieces = token.contents.split()
    as_index = pieces.index('as')
    if as_index == -1 or as_index > 3 or len(pieces) != as_index+2:
        raise template.TemplateSyntaxError('%r tag must be in format {%% %r [count [offset]] as varname %%}' %
                                          pieces[0])

    # count & offset
    count = 5
    offset = 0
    if as_index > 1:
        count = int(pieces[1])
        if as_index > 2:
            count = int(pieces[2])

    varname = pieces[as_index+1]

    return PostsNode(queryset, count, offset, varname)

@register.tag
def get_recent_posts(parser, token):
    return _simple_get_posts(token, Post.objects.published())

@register.tag
def get_favorite_posts(parser, token):
   return _simple_get_posts(token, Post.objects.published().filter(is_favorite=True))

@register.tag
def get_user_posts(parser, token):
    pieces = token.contents.split()
    as_index = pieces.index('as')
    if as_index < 2 or as_index > 4 or len(pieces) != as_index+2:
        raise template.TemplateSyntaxError('%r tag must be in format {%% %r user [count [offset]] as varname %%}' %
                                          pieces[0])

    # count & offset
    count = 5
    offset = 0
    if as_index > 2:
        count = int(pieces[2])
        if as_index > 3:
            count = int(pieces[3])

    user = pieces[1]
    varname = pieces[as_index+1]

    return UserPostsNode(user, count, offset, varname)

@register.simple_tag
def gravatar(email):
    return render_to_string("blogdor/gravatar_img.html", {"url": utils.gravatar(email)})
