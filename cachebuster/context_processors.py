from django.conf import settings


def cachebuster(request):
    return {'cachebuster_unique_string': settings.CACHEBUSTER_UNIQUE_STRING}
