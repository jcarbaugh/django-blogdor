from django.core import urlresolvers
from django.conf import settings
from django.contrib.comments.moderation import CommentModerator
from django.contrib.sites.models import Site

AKISMET_KEY = getattr(settings, "AKISMET_KEY", None)

class AkismetModerator(CommentModerator):

    def moderate(self, comment, content_object, request):

        from akismet import Akismet

        a = Akismet(AKISMET_KEY, blog_url='http://%s/' % Site.objects.get_current().domain)

        akismet_data = {
            'user_ip': comment.ip_address,
            'user_agent': request.META['HTTP_USER_AGENT'],
            'comment_author': comment.user_name.encode('ascii','ignore'),
            'comment_author_email': comment.user_email.encode('ascii','ignore'),
            'comment_author_url': comment.user_url.encode('ascii','ignore'),
            'comment_type': 'comment',
        }

        is_spam = a.comment_check(comment.comment.encode('ascii','ignore'), akismet_data)

        return is_spam


class BlogdorModerator(CommentModerator):

    enable_field = 'comments_enabled'

    def email(self, comment, content_object, request):

        from django.core.mail import send_mail

        from_email = getattr(settings, 'BLOGDOR_FROM_EMAIL', None)
        if not from_email:
            from_email = "bounce@%s" % Site.objects.get_current().domain

        subject = "New comment on %s" % content_object.title
        del_link = 'http://%s%s' % (Site.objects.get_current().domain,
            urlresolvers.reverse('admin:comments_comment_delete',
                                 args=(comment.id,)))
        message = '\n\n'.join((comment.get_as_text(), del_link))
        recipient_email = content_object.author.email

        send_mail(subject, message, from_email, (recipient_email,), fail_silently=True)
