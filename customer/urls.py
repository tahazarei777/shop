from django.urls import path
from .views import customer_dashboard, delete_customer,export_excel, settle_customer

urlpatterns = [
    path("", customer_dashboard, name="customer_dashboard"),
    path("customer/delete/<int:id>/", delete_customer, name="delete_customer"),
    path("customer/settle/<int:id>/", settle_customer, name="settle_customer"),
    path("customer/export_excel/", export_excel, name="export_excel"),
]
