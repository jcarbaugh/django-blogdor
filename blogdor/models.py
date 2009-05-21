from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.comments.moderation import moderator
from django.db import models
from tagging.fields import TagField

COMMENT_FILTERS = getattr(settings, "BLOGDOR_COMMENT_FILTERS", [])
WP_PERMALINKS = getattr(settings, "BLOGDOR_WP_PERMALINKS", False)

MARKUP_CHOICES = (
    ('none', 'plain text or HTML'),
    ('textile', 'Textile'),
    ('markdown', 'Markdown'),
    ('restructuredtext', 'ReST'),
)

class PostManager(models.Manager):
    def published(self):
        return Post.objects.filter(is_published=True)
        
class Post(models.Model):
    
    objects = PostManager()
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=64, db_index=True)
    author = models.ForeignKey(User, related_name='posts')
    
    content = models.TextField()
    excerpt = models.TextField(blank=True, null=True)
    markup = models.CharField(max_length=32, choices=MARKUP_CHOICES, default='none')
    
    timestamp = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, auto_now_add=True)
    
    date_published = models.DateTimeField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    
    comments_enabled = models.BooleanField(default=True)
    
    tags = TagField()
    
    class Meta:
        ordering = ['-date_published','-timestamp']
        
    def __unicode__(self):
        return self.title
    
    @models.permalink
    def get_absolute_url(self):        
        params = {
            'year': self.date_published.year,
            'slug': self.slug,
        }
        urlname = 'blogdor_post'
        if WP_PERMALINKS:
            urlname += '_wpcompat'
            params['month'] = "%02d" % self.date_published.month,
            params['day'] = "%02d" % self.date_published.day
        return (urlname, (), params)

#
# setup comment moderation for Post
#

from blogdor.comments import AkismetModerator, BlogdorModerator

if getattr(settings, "AKISMET_KEY", None):
    moderator.register(Post, AkismetModerator)
moderator.register(Post, BlogdorModerator)