from django.db import models

from django.contrib.auth.models import User

NEW_USERNAME_LENGTH = 1000

def monkey_patch_username():
    username = User._meta.get_field("username")
    username.max_length = NEW_USERNAME_LENGTH
    for v in username.validators:
        if isinstance(v, MaxLengthValidator):
            v.limit_value = NEW_USERNAME_LENGTH


monkey_patch_username()


class UserProfile(models.Model):
    """
    Extension of the basic Django User
    """
    COLLEGES = (
    	('Pa', 'Patel'),
    	('St', 'Strople'),
    	('Le', 'Leung'),
    	('Sc', 'Schaefer'),
    )

    user = models.OneToOneField(User)
    bio = models.CharField(max_length=255, blank=True, null=True, default="")
    college = models.CharField(max_length=3, choices=COLLEGES, default='Pa')
    slug = models.SlugField(max_length=10000)

    def __unicode__(self):
        return "%s" % self.user

class PatelActivity(models.Model):

    TYPE_OF_ACTIVITY = (
        ('R', 'Reading'),
        ('A', 'Assignment'),
    )

    DAY_IT_IS_DUE = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    )

    author = models.ForeignKey(User)
    title = models.CharField(max_length=255, null=False, default="Activity")
    text = models.CharField(max_length=700, null=False, default="Details")
    typeofact = models.CharField(max_length=3, choices=TYPE_OF_ACTIVITY, default='A')
    week = models.IntegerField(default=2)
    duedate = models.CharField(max_length=2, choices=DAY_IT_IS_DUE, default=1)
    slug = models.SlugField(max_length=10000)

    def __unicode__(self):
        return "%s was created by %s for %s on week %s" % (self.title, self.author.first_name, self.duedate, self.week)

class StropleActivity(models.Model):

    TYPE_OF_ACTIVITY = (
        ('R', 'Reading'),
        ('A', 'Assignment'),
    )

    DAY_IT_IS_DUE = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    )

    author = models.ForeignKey(User)
    title = models.CharField(max_length=255, null=False, default="Activity")
    text = models.CharField(max_length=700, null=False, default="Details")
    typeofact = models.CharField(max_length=3, choices=TYPE_OF_ACTIVITY, default='A')
    week = models.IntegerField(default=2)
    duedate = models.CharField(max_length=2, choices=DAY_IT_IS_DUE, default=1)
    slug = models.SlugField(max_length=10000)

    def __unicode__(self):
        return "%s was created by %s for %s on week %s" % (self.title, self.author.first_name, self.duedate, self.week)


class LeungActivity(models.Model):

    TYPE_OF_ACTIVITY = (
        ('R', 'Reading'),
        ('A', 'Assignment'),
    )

    DAY_IT_IS_DUE = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    )

    author = models.ForeignKey(User)
    title = models.CharField(max_length=255, null=False, default="Activity")
    text = models.CharField(max_length=700, null=False, default="Details")
    typeofact = models.CharField(max_length=3, choices=TYPE_OF_ACTIVITY, default='A')
    week = models.IntegerField(default=2)
    duedate = models.CharField(max_length=2, choices=DAY_IT_IS_DUE, default=1)
    slug = models.SlugField(max_length=10000)

    def __unicode__(self):
        return "%s was created by %s for %s on week %s" % (self.title, self.author.first_name, self.duedate, self.week)


class SchaeferActivity(models.Model):

    TYPE_OF_ACTIVITY = (
        ('R', 'Reading'),
        ('A', 'Assignment'),
    )

    
    DAY_IT_IS_DUE = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    )

    author = models.ForeignKey(User)
    title = models.CharField(max_length=255, null=False, default="Activity")
    text = models.CharField(max_length=700, null=False, default="Details")
    typeofact = models.CharField(max_length=3, choices=TYPE_OF_ACTIVITY, default='A')
    week = models.IntegerField(default=2)
    duedate = models.CharField(max_length=2, choices=DAY_IT_IS_DUE, default=1)
    slug = models.SlugField(max_length=10000)

    def __unicode__(self):
        return "%s was created by %s for %s on week %s" % (self.title, self.author.first_name, self.duedate, self.week)

# Create your models here.
