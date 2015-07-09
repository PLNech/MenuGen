from django.conf.urls import patterns, url

urlpatterns = patterns(
    'menus.views.views',

    url(r'^$', 'landing', name='landing'),
    url(r'^home$', 'home', name='home'),

    url(r'^statistics$', 'statistics', name='statistics'),
    url(r'^account$', 'account', name='account'),
)

"""
    Pre generation
"""
urlpatterns += patterns(
    'menus.views.generation.pre_generation_views',

    url(r'^generate$', 'generate', name='generate'),
    url(r'^generate/select_profile$', 'generate_select_profile', name='generate_select_profile'),
    url(r'^generate/placements_detail$', 'generate_placements_detail', name='generate_placements_detail'),

    url(r'^update_gen_criteria', 'update_gen_criteria', name='update_gen_criteria'),
)

"""
    Post generation
"""
urlpatterns += patterns(
    'menus.views.generation.post_generation_views',

    url(r'^generation$', 'generation', name='generation'),
    url(r'^generation/meal_details$', 'generation_meal_details',
        {'starter_id': 0,
         'main_course_id': 1,
         'dessert_id': 2},
        name='generation_meal_details'),
)

"""
    Authentication
"""
urlpatterns += patterns(
    'menus.views.auth.auth_views',

    url(r'^sign-in$', 'sign_in', name='sign_in'),
    url(r'^sign-up$', 'sign_up', name='sign_up'),
    url(r'^sign-out$', 'sign_out', name='sign_out'),
)

"""
    Profiles
"""
urlpatterns += patterns(
    'menus.views.profiles.profiles_views',

    url(r'^profiles$', 'index', name='profiles'),

    url(r'^profiles/new', 'new', name='profile_new'),
    url(r'^profiles/(?P<profile_id>[0-9]+)/detail$', 'detail', name='profile_detail'),
    url(r'^profiles/(?P<profile_id>[0-9]+)/edit$', 'edit', name='profile_edit'),
    url(r'^profiles/(?P<profile_id>[0-9]+)/remove$', 'remove', name='profile_remove'),

    url(r'^update_physio$', 'update_physio', name='update_physio'),
    url(r'^update_tastes', 'update_tastes', name='update_tastes'),
    url(r'^physiology$', 'physiology', name='physiology'),
    url(r'^regimes$', 'regimes', name='regimes'),
    url(r'^tastes$', 'tastes', name='tastes'),
)

"""
    Profiles
"""
urlpatterns += patterns(
    'menus.views.menus.menus_views',

    url(r'^menus$', 'menus', name='menus'),
    url(r'^menus/new', 'new', name='menu_new'),
)
