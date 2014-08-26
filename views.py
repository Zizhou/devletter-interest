from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from interest.models import UserPollProfile, PollAnswerForm, GamePoll
# Create your views here.

@login_required
def main_page(request):
    if request.method == 'POST':
    #TODO
        answer = PollAnswerForm(request.POST)
        print answer
        print '~~~~~~~~~~~'
        print request.POST
        if answer.is_valid():
            answer.save() 
            return HttpResponseRedirect('/interest/')
        else:
            return HttpResponse('you done goofed')

    #TODO
    try:
        user_profile = UserPollProfile.objects.get(user_id = request.user.id)
    except:
        return HttpResponse('something went horribly wrong')
    try:
        game = GamePoll.objects.exclude(game__in = user_profile.voted_on.all()).order_by('?')[0]
    except:
        return HttpResponse('you are probably done with all the games') 

    info = {'game':game, 'user':user_profile}

    poll_answer = PollAnswerForm(initial = info)
    context = {
        #'user_profile' : user_profile,
        'game' : game,
        'poll_answer' : poll_answer,
        
    }
    return render(request, 'interest/poll.html', context) 
