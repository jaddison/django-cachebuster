__author__ = 'James Addison'

import posixpath
import datetime
import urllib
import os

from django import template
from django.conf import settings

try:
    # finders won't exist if we're not using Django 1.3+
    from django.contrib.staticfiles import finders
except ImportError:
    finders = None


register = template.Library()


@register.tag(name="media")
def do_media(parser, token):
    return CacheBusterTag(token, True)


@register.tag(name="static")
def do_static(parser, token):
    return CacheBusterTag(token, False)


class CacheBusterTag(template.Node):
    def __init__(self, token, is_media):
        self.is_media = is_media

        try:
            tokens = token.split_contents()
        except ValueError:
            raise template.TemplateSyntaxError, "'%r' tag must have one or two arguments" % token.contents.split()[0]

        self.path = tokens[1]
        self.force_timestamp = len(tokens) == 3 and tokens[2] or False

    def render(self, context):
        # self.path may be a template variable rather than a simple static file string
        try:
            path = template.Variable(self.path).resolve(context)
        except template.VariableDoesNotExist:
            path = self.path

        path = posixpath.normpath(urllib.unquote(path)).lstrip('/')

        if self.is_media:
            url_prepend = settings.MEDIA_URL
            unique_string = self.get_file_modified(os.path.join(settings.MEDIA_ROOT, path))
        else:
            # django versions < 1.3 don't have a STATIC_URL, so fall back to MEDIA_URL
            url_prepend = getattr(settings, "STATIC_URL", settings.MEDIA_URL)
            if settings.DEBUG and finders:
                absolute_path = finders.find(path)
            else:
                # django versions < 1.3 don't have a STATIC_ROOT, so fall back to MEDIA_ROOT
                absolute_path = os.path.join(getattr(settings, 'STATIC_ROOT', settings.MEDIA_ROOT), path)

            if self.force_timestamp:
                unique_string = self.get_file_modified(absolute_path)
            else:
                unique_string = getattr(settings, 'CACHEBUSTER_UNIQUE_STRING', self.get_file_modified(absolute_path))

        return url_prepend + path + '?' + unique_string

    def get_file_modified(self, path):
        return datetime.datetime.fromtimestamp(os.path.getmtime(os.path.abspath(path))).strftime('%S%M%H%d%m%y')

