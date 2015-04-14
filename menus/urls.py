from django.conf.urls import patterns, url

urlpatterns = patterns(
    'menus.views',

    url(r'^$',              'home',         name='home'),
    url(r'^generate$',      'generate',     name='generate'),
    url(r'^menus$',         'menus',        name='menus'),
    url(r'^friends$',       'friends',      name='friends'),
    url(r'^statistics$',    'statistics',   name='statistics'),

    url(r'^preferences$',   'preferences',  name='preferences'),
    url(r'^regimes$',       'regimes',      name='regimes'),
    url(r'^tastes$',        'tastes',       name='tastes'),

    url(r'^account$',       'account',      name='account'),
    url(r'^sign-in$',       'sign_in',      name='sign-in'),
    url(r'^sign-up$',       'sign_up',      name='sign-up'),
    url(r'^sign-out$',      'sign_out',     name='sign-out'),
)


