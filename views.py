from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from interest.models import UserPollProfile, PollAnswerForm, GamePoll, UserSelectForm
# Create your views here.

@login_required
def poll(request):
    if request.method == 'POST':
        answer = PollAnswerForm(request.POST)
        #I am never doing multiple models in a form again if I can help it
        #this is soooooo much nicer
        if answer.is_valid():
            answer.save() 
            return HttpResponseRedirect('/interest/poll/')

        else:
            return HttpResponse('you done goofed')
    #get initial user
    #this is a terrible way to handle user, should be on POST side
    try:
        user_profile = UserPollProfile.objects.get(user_id = request.user.id)
    except:
        return HttpResponse('something went horribly wrong')
    #get current game
    try:
        game = GamePoll.objects.exclude(game__in = user_profile.voted_on.all().values_list('game')).order_by('?')[0]
    except:
        return HttpResponse('you are probably done with all the games') 

    info = {'game':game, 'user':user_profile}

    poll_answer = PollAnswerForm(initial = info)
    context = {
        'game' : game,
        'poll_answer' : poll_answer,
        
    }
    return render(request, 'interest/poll.html', context) 


@login_required
def result(request):
    if request.method == 'POST':
        selection = UserSelectForm(request.POST)
        if selection.is_valid():
            print selection.cleaned_data
            
            #TODO: query goes here

            context = {
            
            }
            return render(request, 'interest/result.html', context)
        else:
            return HttpResponse('what have you done')
    user_list = UserSelectForm()
    context = {
        'user_list': user_list,
    }
    return render(request, 'interest/result.html', context) 

#Does this page even need to exist? Well...probably not
@login_required
def main_page(request):
    return render(request, 'interest/main.html')
