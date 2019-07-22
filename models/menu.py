
response.title = SETTINGS.title
response.subtitle = SETTINGS.subtitle
response.meta.author = '%(author)s <%(author_email)s>' % SETTINGS
response.meta.keywords = SETTINGS.keywords
response.meta.description = SETTINGS.description

response.menu = get_sub_menu('http://example.org/tbox/kbmsthing', 'kbmsthing')