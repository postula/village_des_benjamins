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

import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from members.views import UserViewSet, ChildViewSet, TeamViewSet
from holiday.views import HolidayViewSet, RegistrationViewSet
from site_content.views import ContentViewSet, SiteSectionViewSet, NewsViewSet
from parent_messages.views import MessageViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenVerifyView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"children", ChildViewSet)
router.register(r"team_members", TeamViewSet, basename="team_members")
router.register(r"holidays", HolidayViewSet)
router.register(r"registrations", RegistrationViewSet)
router.register(r"contents", ContentViewSet)
router.register(r"sections", SiteSectionViewSet)
router.register(r"messages", MessageViewSet)
router.register(r"news", NewsViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/jwt/obtain", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/jwt/verify", TokenVerifyView.as_view(), name="token_verify"),
    path("api/jwt/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    # path("api/jwt/obtain", obtain_jwt_token),
    # path("api/jwt/refresh", refresh_jwt_token),
    # path("api/jwt/verify", verify_jwt_token),
    path(
        "api/reset-password/",
        include("django_rest_passwordreset.urls", namespace="reset_password"),
    ),
    path("tinymce/", include("tinymce.urls")),
    path(
        "",
        TemplateView.as_view(template_name="index.html"),
        name="app",
    ),
    path("silk/", include("silk.urls", namespace="silk")),
]

if settings.DEBUG:
    urlpatterns.append(
        path("__debug__/", include(debug_toolbar.urls)),
    )
