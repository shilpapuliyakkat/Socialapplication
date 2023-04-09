from api.models import Post,Comments
def activities(request):
    if request.user.is_authenticated:
        cnt=Post.objects.filter(user=request.user).count()
        ccmnt=Comments.objects.filter(user=request.user).count()
        return{"pcnt":cnt,"ccnt":ccmnt}
    else:
        return{"pcnt":0}