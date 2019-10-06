from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'front'
urlpatterns = [
                  path('', views.show, name='show'),
                  path('show_model/', views.show_model, name='show_model'),
                  path('reduce_fogy/', views.reduce_fogy, name='reduce_fogy'),
                  path('seam_carving/', views.seam_carving, name='seam_carving'),
                  path('sift/', views.sift, name='sift'),
                  path('filter/', views.flr_set, name='filter'),
                  path('route/', views.al_route, name='route'),
                  path('route_alo/', views.al_route_alo, name='route_alo'),
                  path('BP/', views.BP, name='BP'),
                  path('add_pay/', views.android_pay, name='add_pay'),
                  path('add_pay_web/', views.add_pay_web, name='add_pay_web'),
                  path('show_pay_web/', views.show_pay_web, name='show_pay_web'),
                  path('android_login_api/', views.android_login_api, name='android_login_api'),
                  path('android_register_api/', views.android_register_api, name='android_register_api'),
                  path('android_get_password_back/', views.android_get_password_back, name='android_get_password_back'),
                  path('android_get_password_back_db_operation/', views.android_get_password_back_db_operation, name='android_get_password_back_db_operation'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
