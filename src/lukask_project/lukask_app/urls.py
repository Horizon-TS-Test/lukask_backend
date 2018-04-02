from django.conf.urls import url, include
from rest_framework.routers import  DefaultRouter
from . import views

router = DefaultRouter()
router.register("login", views.LoginViewSet, base_name= "login")
router.register("userProfile", views.UserProfileViewSet)
router.register("Person", views.PersonViewSet)


urlpatterns = [
    url(r'', include(router.urls))
    #url(r"^prototype/$", views.PrototypeApiView.as_view()),
    #url(r"^prototype/(?P<user_id>[^/.]+)/$", views.PrototypeApiView.as_view())
]