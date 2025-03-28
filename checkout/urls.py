from django.urls import include, path

from checkout.views import LinkAPIView, OrderAPIView

urlpatterns = [
    path("", include("common.urls")),
    path("links/<str:code>", LinkAPIView.as_view()),
    path("orders", OrderAPIView.as_view()),

]
