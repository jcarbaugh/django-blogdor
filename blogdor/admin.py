from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User, Group
from blogdor.models import Post
import datetime

AUTHOR_GROUP = getattr(settings, 'BLOGDOR_AUTHOR_GROUP', None)

class PostAdmin(admin.ModelAdmin):
    
    list_display = ('title','is_published','date_published','author','is_favorite','comments_enabled')
    list_display_links = ('title',)
    list_filter = ('is_published','comments_enabled','is_favorite')
    prepopulated_fields = {'slug': ('title',)}
    exclude = ('date_published','is_published',)
    search_fields = ('author','title','content')
    actions = ('publish_posts','recall_posts','enable_comments','disable_comments')
    
    # return filtered author field
    
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        formfield = super(PostAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if AUTHOR_GROUP and db_field.name == 'author':
            try:
                group = Group.objects.get(name=AUTHOR_GROUP)
                authors = User.objects.filter(groups=group).order_by('username')
                formfield.choices = ((author.id, author.username) for author in authors)
            except Group.DoesNotExist:
                pass
        return formfield
    
    # post publishing actions
    
    def publish_posts(self, request, queryset):
        """
        Mark select posts as published and set date_published if it does not exist.
        """
        now = datetime.datetime.now()
        count = queryset.publish()
        self.message_user(request, "%i post(s) published" % count)
    publish_posts.short_description = "Publish posts"
    
    def recall_posts(self, request, queryset):
        """
        Recall published posts, but leave date_published as is.
        """
        count = queryset.recall()
        self.message_user(request, "%i post(s) recalled" % count)
    recall_posts.short_description = "Recall published posts"
    
    # enable or disable comment actions
    
    def enable_comments(self, request, queryset):
        count = queryset.update(comments_enabled=True)
        self.message_user(request, "Comments enabled on %i post(s)" % count)
    enable_comments.short_description = "Enable comments"

    def disable_comments(self, request, queryset):
        count = queryset.update(comments_enabled=False)
        self.message_user(request, "Comments disabled on %i post(s)" % count)
    disable_comments.short_description = "Disable comments"

admin.site.register(Post, PostAdmin)