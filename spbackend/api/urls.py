from django.urls import path
from . import views

urlpatterns =[
    path('getSchoolList',views.getSchools),
    path('getDevelopmentList',views.getDevelopments),
    path('getPhilosophers/<int:school_pk>',views.getPhilosophersBySchool),
    path('getAffiliations/<int:philosopher_pk>',views.getAffiliations),
    path('getSections/<int:philosopher_pk>',views.getSectionsByPhilosopher),
    path('getRelationsList/<int:philosopher_pk>',views.getRelations),
    path('getTags',views.getTags),
    path('getSectionsByTag/<int:tag_pk>',views.getSectionsByTag),
]