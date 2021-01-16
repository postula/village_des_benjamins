"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token,
)
from members.views import UserViewSet, ChildViewSet, TeamViewSet
from holiday.views import HolidayViewSet, RegistrationViewSet
from site_content.views import ContentViewSet, SiteSectionViewSet
from parent_messages.views import MessageViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"children", ChildViewSet)
router.register(r"team_members", TeamViewSet)
router.register(r"holidays", HolidayViewSet)
router.register(r"registrations", RegistrationViewSet)
router.register(r"contents", ContentViewSet)
router.register(r"sections", SiteSectionViewSet)
router.register(r"messages", MessageViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/jwt/obtain", obtain_jwt_token),
    path("api/jwt/refresh", refresh_jwt_token),
    path("api/jwt/verify", verify_jwt_token),
    path(
        "",
        TemplateView.as_view(template_name="index.html"),
        name="app",
    ),
]
