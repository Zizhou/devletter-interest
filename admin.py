from django.contrib import admin

from interest.models import UserPollProfile, GamePoll, PollOption, PollAnswer

# Register your models here.

class UserPollProfileAdmin(admin.ModelAdmin):
    fields = ['user', 'voted_on']

class GamePollAdmin(admin.ModelAdmin):
    fields = ['game']

class PollOptionAdmin(admin.ModelAdmin):
    fields = ['option', 'order']
    list_display = ('option', 'order')

class PollAnswerAdmin(admin.ModelAdmin):
    fields = ['user', 'answer', 'game']
    
admin.site.register(UserPollProfile, UserPollProfileAdmin)
admin.site.register(GamePoll, GamePollAdmin)
admin.site.register(PollOption, PollOptionAdmin)
admin.site.register(PollAnswer, PollAnswerAdmin)
