from django.conf.urls import patterns, url

urlpatterns = patterns(
    'menus.views',

    url(r'^$', 'landing'),

    url(r'^home$', 'home'),
    url(r'^generate$', 'generate'),
    url(r'^generate/select_profile$', 'generate_select_profile'),
    url(r'^generate/placements_detail$', 'generate_placements_detail'),
    url(r'^generation$', 'generation'),
    url(r'^generation/meal_details$', 'generation_meal_details',
        {'starter_id': 0,
         'main_course_id': 1,
         'dessert_id': 2}),

    url(r'^menus$', 'menus'),
    url(r'^friends$', 'friends'),
    url(r'^profile_infos$', 'profile_infos'),
    url(r'^statistics$', 'statistics'),

    url(r'^update_physio$', 'update_physio'),
    url(r'^update_gen_criteria', 'update_gen_criteria'),
    url(r'^update_tastes', 'update_tastes'),
    url(r'^physiology$', 'physiology'),
    url(r'^regimes$', 'regimes'),
    url(r'^tastes$', 'tastes'),

    url(r'^account$', 'account'),
    url(r'^sign-in$', 'sign_in'),
    url(r'^sign-up$', 'sign_up'),
    url(r'^sign-out$', 'sign_out'),
)


