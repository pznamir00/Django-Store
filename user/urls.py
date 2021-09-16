from . import views
from django.urls import include, path

urlpatterns = [
    path('user/', views.UserDetailAPIView.as_view()),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('password/', include('django.contrib.auth.urls')),
    path('', include('dj_rest_auth.urls'))
]