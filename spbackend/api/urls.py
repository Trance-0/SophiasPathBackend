from django.urls import path
from . import views

urlpatterns =[
    path('getSchoolList',views.getSchools),
    path('getSchool/<str:school_slug>',views.getSchoolBySlug),
    path('getDevelopmentList',views.getDevelopments),
    path('getDevelopmentBySchool/<str:school_slug>',views.getDevelopmentsBySchool),
    path('getPhilosophersBySchool/<str:school_slug>',views.getPhilosophersBySchool),
    path('getPage/<str:page_slug>',views.getPage),
    path('getAffiliations/<str:page_slug>',views.getAffiliations),
    path('getSections/<str:page_slug>',views.getSections),
    path('getRelationsList/<str:page_slug>',views.getRelations),
    path('getTags',views.getTags),
    path('getSectionsByTag/<str:tag_slug>',views.getSectionsByTag),
    path('search',views.search),
]