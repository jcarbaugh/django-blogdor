from blogdor import utils
from blogdor.models import Post
from django import template
from django.conf import settings
from django.template.loader import render_to_string
import md5
import urllib

register = template.Library()

@register.simple_tag
def recent_posts(count=5, offset=0):
    try:
        index = count + offset
        posts = Post.objects.public()[offset:index]
        return render_to_string("blogdor/post_summary.html", {"posts": posts})
    except IndexError:
        pass

@register.simple_tag
def gravatar(email):
    return render_to_string("blogdor/gravatar_img.html", {"url": utils.gravatar(email)})
