from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _


from .managers import UserManager


class User(AbstractBaseUser):

    email = models.EmailField(_('email'), unique=True)
    first_name = models.CharField(_('name'), max_length=50, blank=True)
    last_name = models.CharField(_('surname'), max_length=50, blank=True)
    birthday = models.DateField(_('birthday'), null=True)
    phone_number = models.CharField(_('phone_number'), max_length=12)
    date_joined = models.DateTimeField(_('registered'), auto_now_add=True)
    is_active = models.BooleanField(_('is_active'), default=True)
    avatar = models.ForeignKey('Image', on_delete=models.CASCADE)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        full_name = '{} {}'.format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    country = models.CharField(_('country'), max_length=50)
    city = models.CharField(_('city'), max_length=50)
    address = models.CharField(_('address'), max_length=50)
    phone = models.CharField(_('phone'), max_length=12)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)

    class Meta:
        verbose_name = _('user info')
        verbose_name_plural = _('users info')


class Post(models.Model):

    user = models.ForeignKey(User, verbose_name=_('author'), on_delete=models.CASCADE)
    category = models.ForeignKey('category', on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey('subcategory', on_delete=models.SET_NULL, null=True)
    title = models.CharField(_('title'), max_length=50)
    body = models.TextField('text', blank=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='post')
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    image = models.ForeignKey('Image', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ['created', 'title']

    def __str__(self):
        return self.title


class Category(models.Model):

    title = models.CharField(_('title'), max_length=50)
    subtitle = models.ManyToManyField('subcategory')
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.title


class Subcategory(models.Model):
    title = models.CharField(_('title'), max_length=50)
    created = models.DateTimeField(_('updated'), auto_now_add=True)

    class Meta:
        verbose_name = _('subcategory')
        verbose_name_plural = _('subcategories')

    def __str__(self):
        return self.title


class Tag(models.Model):

    title = models.CharField(_('title'), max_length=50)
    created = models.DateTimeField(_('updated'), auto_now_add=True)

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField('text')
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')


class PostRating(models.Model):

    value = models.SmallIntegerField(_('value'))
    created = models.DateTimeField(_('created'), auto_now_add=True)
    update = models.DateTimeField(_('updated'), auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = _('rating')
        verbose_name_plural = _('ratings')


class Image(models.Model):

    image_url = models.URLField(_('image_url'), max_length=50)
    length = models.CharField(_('length'), max_length=50)
    width = models.CharField(_('width'), max_length=50)
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')

