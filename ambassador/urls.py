
from django.urls import include, path

from ambassador.views import LinkAPIView, ProductBackendAPIView, ProductFrontendAPIView, RankingsAPIView, StatsAPIView

urlpatterns = [
    path("", include("common.urls")),
    path("products/frontend", ProductFrontendAPIView.as_view()),
    path("products/backend", ProductBackendAPIView.as_view()),
    path("links", LinkAPIView.as_view()),
    path("stats", StatsAPIView.as_view()),
    path("rankings", RankingsAPIView.as_view()),

]
