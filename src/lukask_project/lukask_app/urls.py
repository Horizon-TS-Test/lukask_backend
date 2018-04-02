from django.conf.urls import url, include
from rest_framework.routers import  DefaultRouter
from . import views

router = DefaultRouter()
router.register("login", views.LoginViewSet, base_name= "login")
router.register("userProfile", views.UserProfileViewSet)
router.register("Person", views.PersonViewSet)
router.register("TypeAction", views.TypeActionViewSet)
router.register("action", views.ActionViewSet)
router.register("prioPub", views.PriorityPublicationViewSet)
router.register("typePub", views.TypePublicationViewSet)
router.register("publication", views.PublicationViewSet)
router.register("tracing", views.TracingViewSet)
router.register("activity", views.ActivityViewSet)
router.register("multimedia", views.MultimediaViewSet)



urlpatterns = [
    url(r'', include(router.urls))
    #url(r"^prototype/$", views.PrototypeApiView.as_view()),
    #url(r"^prototype/(?P<user_id>[^/.]+)/$", views.PrototypeApiView.as_view())
]