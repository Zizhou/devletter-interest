from django.db import models
from submit.models import Game
from django.contrib.auth.models import User

from django.db.models.signals import post_save

# Create your models here.

class UserPollProfile(models.Model):
    user = models.OneToOneField(User, unique = True)
    #keep track of answered polls?
    voted_on = models.ManyToManyField('GamePoll', blank = True)
    
    def __unicode__(self):
        return self.user.username

class GamePoll(models.Model):
    game = models.OneToOneField(Game, unique = True)
    def __unicode__(self):
        return self.game.name

#individual answers linked to user profiles
class PollAnswer(models.Model):
    user = models.ForeignKey(UserPollProfile)
    answer = models.ForeignKey(PollOption)
    game = models.ForeignKey(GamePoll)
    def __unicode__(self):
        return     

#define options for poll answers
class PollOption(models.Model):
    option = models.CharField(max_length = 100)
    def __unicode__(self):
        return self.option

###auto create models for users/games with signal magic

def userpoll_create(sender, instance, created, **kwargs):
    if created == True:
        u = UserPollProfile()
        u.user = instance
        u.save()

post_save.connect(userpoll_create, sender = User)

def gamepoll_create(sender, instance, created, **kwargs):
    if created == True:
        g = GamePoll()
        g.game = instance
        g.save()

post_save.connect(gamepoll_create, sender = Game)
