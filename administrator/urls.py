from django.urls import include, path

from administrator.views import AmbassadorsAPIView, ProductGenericAPIView

urlpatterns = [
    path("", include("common.urls")),
    path("ambassadors", AmbassadorsAPIView.as_view()),
    path("products", ProductGenericAPIView.as_view()),
    path("products/<str:pk>", ProductGenericAPIView.as_view()),
]

