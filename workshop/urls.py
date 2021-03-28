from django.urls import path

from . import views

# URL-conf
urlpatterns = [
    path('', views.index, name='enter'),
    path('start', views.start, name='start'),
    path('masters', views.masters, name='masters'),
    path('guards', views.guards, name='guards'),
    path('workshops', views.workshops, name='workshops'),
    path('reviews', views.ReviewListView.as_view(), name='review'),
    path('detail/<int:pk>', views.ReviewDetailView.as_view(), name='detail_page'),
    path('make_review', views.ReviewCreateView.as_view(), name = 'make_review'),
    path('login', views.MyprojectLoginView.as_view(), name='login_page'),
    path('register', views.RegisterUserView.as_view(), name='register_page'),
    path('logout', views.MyProjectLogout.as_view(), name = 'logout_page'),
    path('admin_req', views.admin_req, name = 'admin_req')
]
