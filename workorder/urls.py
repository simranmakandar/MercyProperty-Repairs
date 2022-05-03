from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from workorder.views import WorkOrderList, CreateWorkOrder, UpdateWorkOrder, WorkOrderDetail, DeleteWorkOrder, \
    CreateWorkOrderItems, UpdateWorkOrderItems, DeleteWorkOrderItems, WorkOrderList1, WorkOrderList2

urlpatterns = [
    path('create_workorder.html', CreateWorkOrder.as_view(), name='create_workorder'),
    path('workorder/', WorkOrderList.as_view(), name='workorder_list'),
    path('workorder/list', WorkOrderList1.as_view(), name='workorder_list1'),
    path('workorder/repair_list', WorkOrderList2.as_view(), name='workorder_list2'),
    path('view/<int:pk>/', WorkOrderDetail.as_view(), name='order_detail'),
    path('edit/<int:pk>/', UpdateWorkOrder.as_view(), name='order_update'),
    path('delete/<int:pk>/', DeleteWorkOrder.as_view(), name='order_delete'),
    path('item/<int:work_order_id>/create/', CreateWorkOrderItems.as_view(), name='item_create'),
    path('item/edit/<int:pk>/', UpdateWorkOrderItems.as_view(), name='item_update'),
    path('item/delete/<int:pk>/', DeleteWorkOrderItems.as_view(), name='item_delete'),
    path('export_work_orders/', views.export_work_orders, name='export_work_orders'),
    path('export_PDFwork_orders/', views.export_PDFwork_orders, name='export_PDFwork_orders'),
    path('export_filter_work/', views.export_filter_work, name='export_filter_work'),
    path('export_PDFfilter_work/', views.export_PDFfilter_work, name='export_PDFfilter_work'),
    path('dashboard/', views.dashboardView, name='dashboard'),
    path('view_pdf', views.view_pdf, name='view_pdf'),
    # path('', views.piechart, name='piechart')
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
