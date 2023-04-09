from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count


class Post(models.Model):
    title=models.CharField(max_length=50)
    description=models.CharField(max_length=100)
    image=models.ImageField(upload_to="images",null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.description

    @property
    def post_comments(self):
        return Comments.objects.filter(post=self).annotate(ucount=Count('like')).order_by('-ucount')
    
    

class Comments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    comment=models.CharField(max_length=100)
    like=models.ManyToManyField(User,related_name="comment")

    @property
    def like_count(self):
        return self.like.all().count()
    

class UserProfile(models.Model):
    is_active=models.BooleanField(default=True)
    time_line_pic=models.ImageField(upload_to="images",null=True,blank=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    profile_pic=models.ImageField(upload_to="profile",null=True,blank=True)
    bio=models.CharField(max_length=250)






