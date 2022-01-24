from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser


from .managers import UserManager


class User(AbstractBaseUser):

    email = models.EmailField('email', unique=True)
    first_name = models.CharField('name', max_length=50, blank=True)
    last_name = models.CharField('surname', max_length=50, blank=True)
    birthday = models.DateField('birthday', null=True)
    phone_number = models.CharField('phone_number', max_length=12)
    date_joined = models.DateTimeField('registered', auto_now_add=True)
    is_active = models.BooleanField('is_active', default=True)
    avatar = models.ForeignKey('Image', on_delete=models.CASCADE)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        full_name = '{} {}'.format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    country = models.CharField('country', max_length=50)
    city = models.CharField('city', max_length=50)
    address = models.CharField('address', max_length=50)
    phone = models.CharField('phone', max_length=12)
    created = models.DateTimeField('created', auto_now_add=True)
    updated = models.DateTimeField('updated', auto_now=True)

    class Meta:
        verbose_name = 'user info'
        verbose_name_plural = 'users info'


class Post(models.Model):

    user = models.ForeignKey(User, verbose_name='author', on_delete=models.CASCADE)
    category = models.ForeignKey('category', on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey('subcategory', on_delete=models.SET_NULL, null=True)
    title = models.CharField('title', max_length=50)
    body = models.TextField('text', blank=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='post')
    created = models.DateTimeField('created', auto_now_add=True)
    updated = models.DateTimeField('updated', auto_now=True)
    image = models.ForeignKey('Image', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        ordering = ['created', 'title']

    def __str__(self):
        return self.title


class Category(models.Model):

    title = models.CharField('title', max_length=50)
    subtitle = models.ManyToManyField('subcategory')
    created = models.DateTimeField('created', auto_now_add=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title


class Subcategory(models.Model):
    title = models.CharField('title', max_length=50)
    created = models.DateTimeField('updated', auto_now_add=True)

    class Meta:
        verbose_name = 'subcategory'
        verbose_name_plural = 'subcategories'

    def __str__(self):
        return self.title


class Tag(models.Model):

    title = models.CharField('title', max_length=50)
    created = models.DateTimeField('updated', auto_now_add=True)

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField('text')
    created = models.DateTimeField('created', auto_now_add=True)
    updated = models.DateTimeField('updated', auto_now=True)

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'


class PostRating(models.Model):

    value = models.SmallIntegerField('value')
    created = models.DateTimeField('created', auto_now_add=True)
    update = models.DateTimeField('updated', auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'rating'
        verbose_name_plural = 'ratings'


class Image(models.Model):

    image_url = models.URLField('image_url', max_length=50)
    length = models.CharField('length', max_length=50)
    width = models.CharField('width', max_length=50)
    created = models.DateTimeField('created', auto_now_add=True)

    class Meta:
        verbose_name = 'image'
        verbose_name_plural = 'images'

