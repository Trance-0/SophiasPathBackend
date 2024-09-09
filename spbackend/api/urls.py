from django.urls import path
from . import views

urlpatterns =[
    path('getCategoryList',views.getCategories),
    path('getDevelopmentList',views.getDevelopments),
    path('getPages/<int:cate_pk>',views.getPageByCategory),
    path('getSections/<int:page_pk>',views.getSectionByPage),
    path('getRelationsList',views.getRelations),
    path('getTags',views.getTags),
    path('getSectionByTag/<int:tag_pk>',views.getSectionByTag),
]