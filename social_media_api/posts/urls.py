from . import views
from rest_framework.routers import DefaultRouter
from django.urls import path, include

# setup router and its contents
router = DefaultRouter()
router.register(r"post", views.PostViewSet, basename='post')
router.register(r'comments', views.CommentViewSet, basename='comment')


urlpatterns = [
    path("api/", include(router.urls),)
]
