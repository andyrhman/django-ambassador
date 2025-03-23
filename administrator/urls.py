from django.urls import include, path

from administrator.views import AmbassadorsAPIView, LinkAPIView, OrderApiView, ProductGenericAPIView

urlpatterns = [
    path("", include("common.urls")),
    path("ambassadors", AmbassadorsAPIView.as_view()),
    path("products", ProductGenericAPIView.as_view()),
    path("products/<str:pk>", ProductGenericAPIView.as_view()),
    path("users/<str:pk>/links", LinkAPIView.as_view()),
    path("orders", OrderApiView.as_view()),
]

