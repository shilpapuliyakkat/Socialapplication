from django.urls import path
from socialweb import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path("register/",views.SignupView.as_view(),name="register"),
    path("login",views.SignInView.as_view(),name="signin"),
    path("home",views.IndexView.as_view(),name="index"),
    path("post/<int:id>/comment/add",views.AddCommentView.as_view(),name="add-comment"),
    path("comments/<int:id>/like/add",views.LikeView.as_view(),name="like"),
    path("profile/add",views.UserProfileCreateView.as_view(),name="profile-add"),
    path("profile/details",views.ProfileDetailView.as_view(),name="profile-detail"),
    path("profile/<int:id>/change",views.ProfileUpdateView.as_view(),name="profile-update"),
    path("post/<int:pk>/remove",views.PostDeleteView.as_view(),name="post-delete"),
    path("comments/<int:id>/dislike/remove",views.DislikeView.as_view(),name="dislike"),
    path("logout",views.SignoutView.as_view(),name="signout")

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)