'''
Members Choose their names during registration.
A valid name is used as the slug for their profile page.
In order to allow short profile URLs, with the member name
after the FQDN, we need to make sure no one has the same name
as any slug in the paths in lookaway.urls.
Returns a list of blacklisted names.
'''
bad_names = [
    'admin',
    'members',
    'multimedia',
    'zine',
    'posts',
    'music',
    'art',
    'crypto',
    'invite',
    'login',
    'logout',
    'change-password',
    'reset-password/',
    'reset-password-done',
    'reset-password-complete',
    'static',
    'media',
]
