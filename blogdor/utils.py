from django.conf import settings
import urllib
try:
    from hashlib import md5
except ImportError:
    from md5 import md5

GRAVATAR_DEFAULT = getattr(settings, "GRAVATAR_DEFAULT", None)
GRAVATAR_SIZE = getattr(settings, "GRAVATAR_SIZE", 50)
GRAVATAR_URL = "http://www.gravatar.com/avatar.php"

def gravatar(email):
    params = { 'gravatar_id': md5(email).hexdigest() }
    if GRAVATAR_SIZE:
        params['size'] = GRAVATAR_SIZE
    if GRAVATAR_DEFAULT:
        params['default'] = GRAVATAR_DEFAULT
    return "%s?%s" % (GRAVATAR_URL, urllib.urlencode(params))
