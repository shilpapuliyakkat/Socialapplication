from django.shortcuts import render,redirect
from socialweb.forms import RegistrationForm,LoginForm,PostForm,UserProfileForm
from django.views.generic import View,CreateView,FormView,TemplateView,ListView,UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from api.models import Post,Comments,UserProfile
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper
dectr=[signin_required,never_cache]


class SignupView(CreateView):
    model=User
    form_class=RegistrationForm
    template_name="register.html"
    success_url=reverse_lazy("signin")


class SignInView(FormView):
    template_name="login.html"
    form_class=LoginForm
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("index")
            else:
                return render(request,"login.html",{"form":self.form_class})
            
@method_decorator(dectr,name="dispatch")
class IndexView(CreateView,ListView):
    model=Post
    form_class=PostForm
    template_name="index.html"
    success_url=reverse_lazy("index")
    context_object_name="posts"
    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    def get_queryset(self):
        return Post.objects.all().order_by("-date")


# localhost:8000/questions/2/answers/add
@method_decorator(dectr,name="dispatch")
class AddCommentView(View):
    def post(self,request,*args,**kwargs):
        pid=kwargs.get("id")
        pst=Post.objects.get(id=pid)
        usr=request.user
        cmnt=request.POST.get("comments")
        Comments.objects.create(user=usr,
        post=pst,
        comment=cmnt)
        return redirect("index")

# localhost:8000/answers/id/upvote/add
@method_decorator(dectr,name="dispatch")
class LikeView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        ans=Comments.objects.get(id=id)
        ans.like.add(request.user)
        ans.save()
        return redirect("index")
    
@method_decorator(dectr,name="dispatch")
class UserProfileCreateView(CreateView):
    model=UserProfile
    form_class=UserProfileForm
    template_name="profile-add.html"
    success_url=reverse_lazy("index")
    
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    
@method_decorator(dectr,name="dispatch")
class ProfileDetailView(TemplateView):
    template_name="profile-detail.html"

@method_decorator(dectr,name="dispatch")
class ProfileUpdateView(UpdateView):
    model=UserProfile
    form_class=UserProfileForm
    template_name="profile-edit.html"
    success_url=reverse_lazy("index")
    pk_url_kwarg="id"

@method_decorator(dectr,name="dispatch")
class PostDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Post.objects.get(id=id).delete()
        return redirect("index")

@method_decorator(dectr,name="dispatch")
class DislikeView(View):
      def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        ans=Comments.objects.get(id=id)
        ans.like.remove(request.user)
        ans.save()
        return redirect("index")

@method_decorator(dectr,name="dispatch")
class SignoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")
    
