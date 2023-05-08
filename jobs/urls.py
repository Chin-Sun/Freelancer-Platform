from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('freelancers/', FreelancerListViews, name='freelancers-list'),
    path('business/', BusinessListViews, name='business-list'),
    path('projects/', ProjectListViews, name='project-list'),
    path('freelancer/create/', FreelancerCreateView.as_view(), name='freelancer-create'),
    path('business/create/', BusinessCreateView.as_view(), name='business-create'),
    path('account/setup', handle_login, name='handle-login'),
    path('profile', profile, name='profile'),
    path('profile/update-freelancer', update_freelancer, name='update-freelancer'),
    path('profile/update-business', update_business, name='update-business'),
    path('business/<int:pk>', view_business_profile, name='view-business-profile'),
    path('freelancer/<int:pk>', view_freelancer_profile, name='view-freelancer-profile'),
    path('search-results/', search, name='search-results'),
    path('freelancer-report/<int:pk>', freelancer_report, name='freelancer-report'),
    path('business-report/<int:pk>', business_report, name='business-report'),
    path('project/create', ProjectCreateView.as_view(), name='project-create'),
    path('project/<int:pk>', view_project_profile, name='project-profile'),
    path('accept-project/<int:pk>', accept_project, name='accept-project'),
    path('send-invitation/', invite, name='send-invitation'),
    path('FAQ/', faq, name='FAQ'),
    path('rate/<int:profile_id>/<int:rating>/', rate),
    path('change-status/<int:profile_id>/<int:project_id>/<int:new_status>/', change_status),
]
