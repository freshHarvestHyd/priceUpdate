from django.contrib import admin
from django.urls import path
from prices.views import add_price, export_pdf

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', add_price, name='add_price'),
    path('export-pdf/', export_pdf, name='export_pdf'),
]