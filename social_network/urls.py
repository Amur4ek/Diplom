"""
URL configuration for social_network project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from posts import views

router_post = DefaultRouter()
router_comment = DefaultRouter()
router_post.register('', views.PostViewSet)
router_comment.register('', views.CommentViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', include(router_post.urls)),
    path('posts/<int:post_id>/comments/', include(router_comment.urls)),
    path('posts/<int:post_id>/likes/', views.LikeView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
