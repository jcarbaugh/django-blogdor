from django.contrib import admin
from blogdor.models import Post
import datetime

class PostAdmin(admin.ModelAdmin):
    
    list_display = ('title','author','date_published','is_published','comments_enabled')
    list_display_links = ('title',)
    list_filter = ('author','is_published','comments_enabled')
    prepopulated_fields = {'slug': ('title',)}
    exclude = ('date_published','is_published',)
    search_fields = ('title','content')
    actions = ('publish_posts','recall_posts','enable_comments','disable_comments')
    
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
    
    def enable_comments(self, request, queryset):
        count = queryset.update(comments_enabled=True)
        self.message_user(request, "Comments enabled on %i post(s)" % count)
    enable_comments.short_description = "Enable comments"

    def disable_comments(self, request, queryset):
        count = queryset.update(comments_enabled=False)
        self.message_user(request, "Comments disabled on %i post(s)" % count)
    disable_comments.short_description = "Disable comments"

admin.site.register(Post, PostAdmin)