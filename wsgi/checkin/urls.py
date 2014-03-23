from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'checkin.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # Home
    url(r'^$', TemplateView.as_view(template_name='survey/index.html'), name='home'),

    # Commuterform
    url(r'^commuterform/$', 'survey.views.commuter', name='commuterform'),

    url(r'^leaderboard/$', 'leaderboard.views.leaderboard'),
    url(r'^leaderboard-bare/$', 'leaderboard.views.leaderboard_bare'),
    url(r'^test-chart/$', 'leaderboard.views.testchart'),
    url(r'^emplbreakdown/(?P<month>[-\w]+)/$', 'leaderboardlist.views.empBreakDown'),
    url(r'^emplbreakdown/$', 'leaderboardlist.views.chooseMonth'),
    url(r'^nvobreakdown/$', 'leaderboard.views.nvobreakdown'),
    url(r'^nvobreakdown/(?P<selEmpID>[-\w]+)/$', 'leaderboard.views.nvobreakdown'),
    
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
