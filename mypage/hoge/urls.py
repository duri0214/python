from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'booking'

urlpatterns = [
    path('', views.StoreList.as_view(), name='store_list'),
    path('store/<int:pk>/staffs/', views.StaffList.as_view(), name='staff_list'),
    path('staff/<int:pk>/calendar/', views.StaffCalendar.as_view(), name='calendar'),
    path('staff/<int:pk>/calendar/<int:year>/<int:month>/<int:day>/', views.StaffCalendar.as_view(), name='calendar'),
]
