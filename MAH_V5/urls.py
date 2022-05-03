from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from workorder.views import WorkOrderList

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('workorder/', include('workorder.urls')),
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('user/', include('django.contrib.auth.urls')),
]
admin.site.site_header = 'Mercy Affordable Housing Maintenance App'
admin.site.index_title = 'Maintenance App Administration Panel'
