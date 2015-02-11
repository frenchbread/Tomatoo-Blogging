from django.db import models
from time import time
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Count


def get_upload_place(instance, filename):
    return "posts/%s/%s" % (instance.user, str(time()).replace('.', '_')+filename)


class SavedCount(models.Manager):
    def get_query_set(self):
        return super(SavedCount, self).get_query_set().annotate(saveThis=Count('save')).order_by('-timestamp')


class Post(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField("Title", max_length=100)
    body = models.TextField("Text", max_length=1000)
    views = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    with_saved = SavedCount()
    objects = models.Manager()  # default

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post", kwargs={"pk": str(self.id)})


class Save(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)

    def __unicode__(self):
        return "%s saved %s" % (self.user.username, self.post.title)
