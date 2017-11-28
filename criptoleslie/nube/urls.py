from django.conf.urls import include, url
from . import views

urlpatterns = [
        # index
        url(r'^index/$', views.IndexView.as_view(), name='index'),
        url(r'^profile/$', views.lista, name='profile'),
        url(r'^download/$', views.download, name='download'),
        url(r'^delete/$', views.delete, name='delete'),
        #url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
        #url(r'^subir/$', views.SubirView.as_view(), name='uploads'),
        url(r'^uploads/', views.upload_file, name="uploads"),
        # session
        url(r'^login/$', views.LoginView.as_view(), name='login'),
        url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
        # register
        url(r'^register/$', views.RegisterView.as_view(), name='register'),
        url(r'^register/success/$', views.RegisterSuccessView.as_view(), name='register-success'),
    ]