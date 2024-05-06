from django.urls import path
from api import views


urlpatterns = [
    path('vendors/', views.VendorsListViews.as_view(), name='vendors'),
    path('vendors/<int:pk>/', views.VendorViews.as_view(), name='vendor'),
    path('purchase_orders/', views.PurchaseOrdersListViews.as_view(), name='purchase-orders'),
    path('purchase_orders/<int:pk>/', views.PurchaseOrderViews.as_view(), name='purchase-order'),
    path('vendors/<int:pk>/performance/', views.VendorPerformanceViews.as_view(), name='vendor-performance'),
    path('purchase_orders/<int:pk>/acknowledgement/', views.Acknowledgement.as_view(), name = 'acknowledgement')
    
]