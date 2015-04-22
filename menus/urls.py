from django.conf.urls import patterns, url

urlpatterns = patterns(
    'menus.views',

    url(r'^$',                           'landing'),

    url(r'^home$',                       'home'),
    url(r'^generate$',                   'generate'),
    url(r'^generate/select_profile$',    'generate_select_profile'),
    url(r'^generate/placements_detail$', 'generate_placements_detail'),
    url(r'^generation',                  'generation'),
    url(r'^menus$',                      'menus'),
    url(r'^friends$',                    'friends'),
    url(r'^statistics$',                 'statistics'),

    url(r'^physiology$',                 'physiology'),
    url(r'^regimes$',                    'regimes'),
    url(r'^tastes$',                     'tastes'),

    url(r'^account$',                    'account'),
    url(r'^sign-in$',                    'sign_in'),
    url(r'^sign-up$',                    'sign_up'),
    url(r'^sign-out$',                   'sign_out'),
)


