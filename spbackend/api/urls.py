from django.urls import path
from . import views

urlpatterns =[
    path('getSchoolList',views.getSchools),
    path('getSchool/<str:school_slug>',views.getSchoolBySlug),
    path('getDevelopmentList',views.getDevelopments),
    path('getDevelopmentBySchool/<str:school_slug>',views.getDevelopmentsBySchool),
    path('getPhilosophersBySchool/<str:school_slug>',views.getPhilosophersBySchool),
    path('getPhilosopher/<str:philosopher_slug>',views.getPhilosopher),
    path('getAffiliations/<str:philosopher_slug>',views.getAffiliations),
    path('getSections/<str:philosopher_slug>',views.getSectionsByPhilosopher),
    path('getRelationsList/<str:philosopher_slug>',views.getRelations),
    path('getTags',views.getTags),
    path('getSectionsByTag/<str:tag_slug>',views.getSectionsByTag),
]