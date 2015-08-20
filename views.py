from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from interest.models import UserPollProfile, PollAnswerForm, GamePoll, UserSelectForm, PollAnswerForm2
import interest.experiment
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
    #initial data in hidden form
    info = {'game':game, 'user':user_profile}
    #more info from db
    print game.game
    print type(game.game)
    details = game.game

    poll_answer = PollAnswerForm(initial = info)
    context = {
        'game' : game,
        'poll_answer' : poll_answer,
        'details' : details,        
    }
    return render(request, 'interest/poll.html', context) 

@login_required
def poll2(request):
    if request.method == 'POST':
        answer = PollAnswerForm2(request.POST)
        #I am never doing multiple models in a form again if I can help it
        #this is soooooo much nicer
        if answer.is_valid():
            answer.save() 
            return HttpResponseRedirect('/interest/poll2/')

        else:
            return HttpResponse('you done goofed')
    try:
        user_profile = UserPollProfile.objects.get(user_id = request.user.id)
    except:
        return HttpResponse('something went horribly wrong')
    #get current game
    try:
        game = GamePoll.objects.exclude(game__in = user_profile.voted_on.all().values_list('game')).order_by('?')[0]
    except:
        return HttpResponse('you are probably done with all the games') 
    #initial data in hidden form
    info = {'game':game, 'user':user_profile}
    #more info from db
    print game.game
    print type(game.game)
    details = game.game
#ugly UGLY UGLY!!!
#seriously, though, should no be hardcoded 1/2 == yes/no
    poll_yes = PollAnswerForm2(initial = {'game':game, 'user':user_profile, 'answer' : 1})
    poll_no = PollAnswerForm2(initial = {'game':game, 'user':user_profile, 'answer' : 2})

    context = {
        'game' : game,
        'details' : details,
        'poll_yes' : poll_yes,
        'poll_no' : poll_no,
    }
    return render(request, 'interest/poll2.html', context) 

@login_required
def result(request):
    user_list = UserSelectForm()
    if request.method == 'POST':
        selection = UserSelectForm(request.POST)
        if selection.is_valid():
            print selection.cleaned_data
            
            user_select = selection.cleaned_data.get('user_select')
            mutual_games = interest.experiment.run_yes(user_select)
            print mutual_games
            if mutual_games.count() == 0:
                game_list = ['There is nothing that these people can agree upon. NOTHING.']
            else:
                game_list = mutual_games
            context = {
                'user_list': user_list,
                'game_list': game_list,
            }
            return render(request, 'interest/result.html', context)
        else:
            return HttpResponse('what have you done')
    context = {
        'user_list': user_list,
    }
    return render(request, 'interest/result.html', context) 

#Does this page even need to exist? Well...probably not
@login_required
def main_page(request):
    return render(request, 'interest/main.html')
