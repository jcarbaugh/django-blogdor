from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.comments.moderation import moderator
from django.db import models
from markupfield.fields import MarkupField
from tagging.fields import TagField
import datetime

COMMENT_FILTERS = getattr(settings, "BLOGDOR_COMMENT_FILTERS", [])
WP_PERMALINKS = getattr(settings, "BLOGDOR_WP_PERMALINKS", False)
DEFAULT_MARKUP = getattr(settings, "BLOGDOR_DEFAULT_MARKUP", "markdown")

class PostQuerySet(models.query.QuerySet):
    
    def publish(self):
        now = datetime.datetime.now()
        count = self.filter(date_published__isnull=False).update(is_published=True)
        count += self.filter(date_published__isnull=True).update(is_published=True, date_published=now)
        return count
        
    def recall(self):
        return self.update(is_published=False)

class PostManager(models.Manager):
    
    use_for_related_fields = True
    
    def published(self):
        return Post.objects.filter(is_published=True)
        
    def get_query_set(self):
        return PostQuerySet(self.model)

class Post(models.Model):
    
    objects = PostManager()
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=64, db_index=True)
    author = models.ForeignKey(User, related_name='posts')
    
    content = MarkupField(default_markup_type=DEFAULT_MARKUP)
    excerpt = MarkupField(markup_type='plain', blank=True, null=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, auto_now_add=True)
    
    date_published = models.DateTimeField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    
    is_favorite = models.BooleanField(default=False)
    
    comments_enabled = models.BooleanField(default=True)
    
    tags = TagField()
    
    class Meta:
        ordering = ['-date_published','-timestamp']
        
    def __unicode__(self):
        return self.title
    
    def save(self):
        self.excerpt.markup_type = self.content.markup_type
        if self.is_published and not self.date_published:
            self.date_published = datetime.datetime.now()
        super(Post, self).save()
    
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
    
    def publish(self):
        self.is_published = True
        self.save()
    
    def recall(self):
        self.is_published = False
        self.save()

#
# setup comment moderation for Post
#

from blogdor.comments import AkismetModerator, BlogdorModerator

if getattr(settings, "AKISMET_KEY", None):
    moderator.register(Post, AkismetModerator)
moderator.register(Post, BlogdorModerator)