
from.import views
from django.urls import path
from .views import ChangePwView, PwResetView, PwResetDoneView, PwResetConfirmView, PwResetCompleteView


urlpatterns = [
    path('change-password/', ChangePwView.as_view(), name='change_password'),
    path('password-reset/', PwResetView.as_view(), name='pw_reset'),
    path('password-reset/done/', PwResetDoneView.as_view(), name='pw_reset_done'),
    path('reset/<uidb64>/<token>/', PwResetConfirmView.as_view(), name='pw_reset_confirm'),
    path('reset/done/', PwResetCompleteView.as_view(), name='pw_reset_complete'),
    path('signup', views.signup, name='signup'),
]