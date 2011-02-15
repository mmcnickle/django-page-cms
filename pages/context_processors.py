"""Context processors for Page CMS."""
from pages import settings
from pages.models import Page


def media(request):
    """Adds media-related variables to the `context`."""
    return {
        'PAGES_MEDIA_URL': settings.PAGES_MEDIA_URL,
        'PAGE_USE_SITE_ID': settings.PAGE_USE_SITE_ID,
        'PAGE_HIDE_SITES': settings.PAGE_HIDE_SITES,
        'PAGE_LANGUAGES': settings.PAGE_LANGUAGES,
    }


def pages_navigation(request):
    """Adds essential pages variables to the `context`."""
    pages = Page.objects.navigation().order_by("tree_id")
    return {
        'pages_navigation': pages,
        'current_page': None
    }

def current_page(request):
    """ 
    Return a page object with the current path.
    
    If it doesn't exist, return the page of the nearest whut
    
    change request 2
    parent.
    
    So if a page exists with the slug '/pages/test-page'
    it will be returned.
    
    If the path requested is '/pages/test-page/application/page'
    it will try:
    
    '/pages/test-page/application/page'
    '/pages/test-page/application/'
    '/pages/test-page/'
    '/pages/'
    
    And return the first one that exists
    """
    
    page = None
    bits = request.path.split('/')
    i = len(bits)
    
    while page == None or i == 0:
        path = '/'.join(bits[:i])
        page = Page.objects.from_path(path, None)
        i -= 1
    
    return {'current_page': page}
