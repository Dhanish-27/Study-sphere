# app/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name='index'),
    #adding Questions, Project and posts
    path('add_question',views.create_question,name="Add a question"),
    path('add_post',views.create_post,name='posts'),
    path('add_project',views.create_project,name='project_videos'),
    #View questions, posts and objects
    path('question/<int:pk>/', views.question_detail, name='question_detail'),
    path('post_video',views.create_project,name='create_post_with_videos'),
    path('all_posts',views.all_posts,name='all_posts'),
    # Language domain category and videos URLs
    path('add_language/', views.add_language, name='add_language'),
    path('add_domain/', views.add_domain, name='add_domain'),
    path('add_category/', views.add_category, name='add_category'),
    path('add_video/', views.add_video, name='add_video'),
    # Professional details
    path('professional_details_form/', views.professional_details, name='professional_details'),
    # Profile page
    path('profile/', views.profile_page, name='profile_page'),
    # My Content pages
    path('my-projects/', views.my_projects, name='my_projects'),
    path('my-posts/', views.my_posts, name='my_posts'),
    path('my-courses/', views.my_courses, name='my_courses'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
