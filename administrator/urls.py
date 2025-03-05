from django.urls import path, include

from administrator.views import AmbassadorsAPIView

urlpatterns = [
    path('', include('common.urls')),
    path('ambassadors', AmbassadorsAPIView.as_view())
]