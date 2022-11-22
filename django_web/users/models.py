from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .validators import validate_no_special_characters, validate_restaurant_link
from place.models import Store
# Create your models here.

class User(AbstractUser):
    nickname = models.CharField(
        max_length=15, 
        unique=True, 
        null=True,
        validators=[validate_no_special_characters],
        error_messages={'unique': '이미 사용중인 닉네임입니다.'},
    )

    profile_pic = models.ImageField(default='images/default_profile.jpg', upload_to='images/users', null=True)

    intro = models.CharField(max_length=60, blank=True)

    following = models.ManyToManyField('self', symmetrical=False, blank=True)

    def __str__(self):
        return self.email

class Review(models.Model):
    title = models.CharField(max_length=40)

    restaurant_name = models.CharField(max_length=40)

    RATING_CHOICES = [
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'),
    ]
    rating = models.IntegerField(choices=RATING_CHOICES, default=None, blank=True, null=True)

    image1 = models.ImageField(upload_to='images/reviews', blank=True, max_length=450)
    image2 = models.ImageField(upload_to='images/reviews', blank=True, max_length=450)
    image3 = models.ImageField(upload_to='images/reviews', blank=True, max_length=450)
    


    content = models.TextField()

    dt_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    dt_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-dt_created']

# class Comment(models.Model):
#     # 댓글 달 때 빈칸 못하게 blank=False
#     content = models.TextField(max_length=500, blank=False)
    
#     dt_created = models.DateTimeField(auto_now_add=True)

#     dt_updated = models.DateTimeField(auto_now=True)

#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     review = models.ForeignKey(Review, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.content[:30]

#     class Meta:
#         ordering = ['-dt_created']

# class Like(models.Model):
#     dt_created = models.DateTimeField(auto_now_add=True)

#     user = models.ForeignKey(User, on_delete=models.CASCADE)

#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

#     object_id = models.PositiveIntegerField()
#     # liked_object = GenericForeignKey('content_type', 'object_id')
#     liked_object = GenericForeignKey()

#     def __str__(self):
#         return f'({self.user}, {self.liked_object})'