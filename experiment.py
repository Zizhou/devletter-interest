from interest.models import GamePoll, PollOption

def run_yes(input_list):
    user_list = []
    #ugh, this hardcoding is baaaad
    yes = PollOption.objects.get(option = 'Yes')
    yes_plus = PollOption.objects.get(option = 'Yes, and I want an INTERVIEW')
    for user in input_list:
        q = yes.pollanswer_set.filter(user = user)
        qq = yes_plus.pollanswer_set.filter(user = user)
        #magical set unions!
        q = q | qq
        user_list.append(set(q.all().values_list('game')))
    #if there are none, I think this just breaks, but that should never happen
    result = set(user_list[0])
    for user in user_list:
        result = result.intersection(result, user)
    #ah! I finally understand the double underscore here!
    return GamePoll.objects.filter(game__in = result).order_by('game__name')
