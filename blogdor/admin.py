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
    actions = ('publish_posts','recall_posts')
    
    def publish_posts(self, request, queryset):
        """
        Mark select posts as published and set date_published if it does not exist.
        """
        now = datetime.datetime.now()
        published_count = queryset.publish()
        s = published_count == 1 and 'posts' or 'post'
        self.message_user(request, "%i %s published" % (published_count, s))
    publish_posts.short_description = "Publish posts"
    
    def recall_posts(self, request, queryset):
        """
        Recall published posts, but leave date_published as is.
        """
        recalled_count = queryset.recall()
        s = recalled_count == 1 and 'posts' or 'post'
        self.message_user(request, "%i %s recalled" % (recalled_count, s))
    recall_posts.short_description = "Recall published posts"

admin.site.register(Post, PostAdmin)