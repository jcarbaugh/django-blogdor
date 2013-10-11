from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from blogdor.models import Post
from tagging.models import Tag, TaggedItem

ITEMS_PER_FEED = getattr(settings, 'BLOGDOR_ITEMS_PER_FEED', 10)
FEED_TTL = getattr(settings, 'BLOGDOR_FEED_TTL', 120)


#
# Generic blogdor feed
#

class BlogdorFeed(Feed):

    description_template = 'blogdor/feeds/post_description.html'

    def link(self):
        return reverse('blogdor_archive')

    def ttl(self):
        return str(FEED_TTL)


#
# Specific blogdor feeds
#

class LatestPosts(BlogdorFeed):

    title = u"Latest blog posts"
    description = title

    def items(self):
        return Post.objects.published()[:ITEMS_PER_FEED]

    def item_author_name(self, post):
        if post.author:
            return post.author.get_full_name()
        return "Anonymous"

    def item_pubdate(self, post):
        return post.date_published


class LatestComments(BlogdorFeed):

    title_template = 'blogdor/feeds/comment_title.html'
    description_template = 'blogdor/feeds/comment_description.html'

    title = u"Latest blog comments"
    description = title

    def items(self):
        comments = Comment.objects.for_model(Post).filter(is_public=True, is_removed=False)
        return comments.order_by('-submit_date')[:ITEMS_PER_FEED]

    def item_author_name(self, comment):
        return comment.user_name

    def item_pubdate(self, comment):
        return comment.submit_date


class LatestForAuthor(BlogdorFeed):

    feed_title = u"Recent blog posts authored by %s"
    feed_description = feed_title

    def _display_name(self, user):
        if hasattr(user, 'get_full_name'):
            display_name = user.get_full_name()
            if not display_name:
                display_name = user.username
            return display_name
        return user

    def title(self, author):
        return self.feed_title % self._display_name(author)

    def description(self, author):
        return self.feed_description % self._display_name(author)

    def get_object(self, bits, author):
        return User.objects.get(username=author)

    def items(self, author):
        return Post.objects.published().filter(author=author)[:ITEMS_PER_FEED]

    def item_pubdate(self, post):
        return post.date_published


class LatestForTag(BlogdorFeed):

    feed_title = u"Recent blog posts tagged with '%s'"
    feed_description = feed_title

    def title(self, tag):
        return self.feed_title % tag

    def description(self, tag):
        return self.feed_description % tag

    def get_object(self, bits, tag):
        try:
            return Tag.objects.get(name=tag)
        except Tag.DoesNotExist:
            return tag

    def items(self, tag):
        return TaggedItem.objects.get_by_model(Post.objects.published(), tag)[:ITEMS_PER_FEED]

    def item_pubdate(self, post):
        return post.date_published
