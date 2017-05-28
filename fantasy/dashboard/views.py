from django.shortcuts import render
from django.db.models import Max, Min, Sum, Avg
from .models import FantasyPicks, FantasyPointsTable, FantasyLeaderBoard, PointsSpread
from .forms import EventsForm


def index(request):
    """
    Sends the user to the most recent events page.
    """
    # get max event id (changed to stop_number)
    malesmaxevent = FantasyLeaderBoard.objects.using(
      'fantasydb').filter(sex='m').aggregate(em=Max('stop_number'))['em']
    # females
    femalesmaxevent = FantasyLeaderBoard.objects.using(
      'fantasydb').filter(sex='f').aggregate(em=Max('stop_number'))['em']
    # set context
    context = {'malesmaxevent': malesmaxevent, 
               'femalesmaxevent': femalesmaxevent} 
    # render page
    return render(request, 'dashboard/index.html', context)


# eventid has been changed to "stop_number"
def menstour(request, year, stopnumber):
    # Filter leaderboard 
    # The leaderboard is already structured in such a 
    # way that the table can be filtered on event id  
    leaderboard = FantasyLeaderBoard.objects.using(
      'fantasydb').filter(year=str(year)).filter(
      stop_number=str(stopnumber)).filter(sex='m')

    # filter picks table by event id 
    picks = FantasyPicks.objects.using(
      'fantasydb').filter(year=str(year)).filter(
      stop_number=str(stopnumber)).filter(sex='m')

   # collect list of distinct surfers (from the picks table)
    picks_surfers = picks.values_list('surfer_name',flat=True).distinct()

    # filter points table by event id
    # Further processing is required because the points table needs to be 
    # ordered correctly and rearranged into wide format
    points = FantasyPointsTable.objects.using(
      'fantasydb').filter(year=str(year)).filter(
      stop_number=str(stopnumber)).filter(sex='m').filter(
      surfer_name__in=picks_surfers).order_by('surfer_name', 'round_id')

    # Process points and picks to generate list of lists
    # list 1: surfer name
    # list 2: scores ordered by round 
    # list 3: player names that picked the surfer
    res = []

    # loop over surfers that the players selected 
    for surfer in picks_surfers:
        # Place holders
        scores = []
        players = []
        # loop over points table and filter on the surfer name
        for pt in points.filter(surfer_name=surfer).values_list('round_id','total','bonusflag'):
            #round = pt[0]
            if pt[2] == 'b':
                 score = [pt[1], pt[2]]
            else: 
                 score = [pt[1], 'na']
            scores.append(score)
        # loop over the picks table and filter on the surfer name 
        for pl in picks.filter(surfer_name=surfer).values_list('player_name'):
            players.append(pl[0])
        # Generate list of lists
        results = [surfer, scores, players]
        # pool the results
        res.append(results)

    # Sort function
    def collectLenOfSecond(elem):
      return len(elem[1])

    # Sort the processed table above
    res = sorted(res, key=collectLenOfSecond, reverse=True)

    # Get event information for the summary section
    # Note that the picks table has been filtered on event id 
    # passed in using the url so calling distinct should return only
    # one event name (updated to filter on stop_number - but event_name
    # should still be ok)
    eventname = picks.values_list('event_name',flat=True).distinct()

    # BADGES SECTION   
    # Count surfer picks (total across all events) - this is a badge 
    allpicks = FantasyPicks.objects.using('fantasydb').filter(year=str(year)).filter(
        stop_number__lte=str(stopnumber)).filter(sex='m')

    # Collect surfer names to loop over next
    surferlist = allpicks.values_list('surfer_name',flat=True)

    # Calculate lengths of objects - used to calculate percentage 
    numplayers = len(allpicks.values_list('player_name', flat=True).distinct())
    numevents = len(allpicks.values_list('event_id', flat=True).distinct())
    numselections = numplayers * numevents

    # place holder for results
    mostpickedsurfer = []

    # count each surfer in picks           
    for s in list(picks_surfers):
        mps = [s, round(list(surferlist).count(s)/float(numselections),2)*100]
        mostpickedsurfer.append(mps)

    # sort function
    def SortByMaxPoints(elem):
      return elem[1]

    # sort
    mps = sorted(mostpickedsurfer, key=SortByMaxPoints, reverse=True)


    # Min event points filter
    # This works because the lowest event score is held in the leaderboard
    # NB event totals are not shown in the leaderboard on the dashboard
    minpoints = leaderboard.aggregate(my_min=Min('player_points'))
    try:
        minbadge = FantasyLeaderBoard.objects.using(
          'fantasydb').filter(year=str(year)).filter(
          stop_number=str(stopnumber)).filter(sex='m').get(
          player_points=minpoints['my_min'])
    except:
        minbadge = None

    # highest points
    maxpoints = leaderboard.aggregate(my_max=Max('player_points'))
    try:
        maxbadge = FantasyLeaderBoard.objects.using(
          'fantasydb').filter(year=str(year)).filter(
          stop_number=str(stopnumber)).filter(sex='m').get(
          player_points=maxpoints['my_max'])
    except:
        maxbadge = None

    # create surfer list (from the points table)
    points_surfers = FantasyPointsTable.objects.using(
      'fantasydb').filter(stop_number__lte=str(stopnumber)).filter(
       sex='m').filter(year=str(year)).values_list('surfer_name', flat=True).distinct()

    # iterate over the points table 
    badgeholder = []
    for surfer in points_surfers:
        ptm = FantasyPointsTable.objects.using('fantasydb').filter(sex='m').filter(
            surfer_name=surfer).filter(year=str(year)).filter(
            stop_number__lte=str(stopnumber)).aggregate(ptsum=Sum('total'))['ptsum']
        pta = FantasyPointsTable.objects.using('fantasydb').filter(sex='m').filter(
            surfer_name=surfer).filter(year=str(year)).filter(
            stop_number__lte=str(stopnumber)).aggregate(ptavg=Avg('total'))['ptavg']
        bh = [surfer, ptm, pta]
        badgeholder.append(bh)
    
    # Tour points leader
    sortedbadgeholder = sorted(badgeholder, key=SortByMaxPoints, reverse=True)    
    tourleader = sortedbadgeholder[0]

    # Tour lemon
    tourlemon = [x for x in sortedbadgeholder if x[1] != 0.0][-1]        

    # Top avg heat scores
    def SortByAvgHeat(elem):
      return elem[2]

    # sort
    sortedbadgeholder = sorted(badgeholder, key=SortByAvgHeat, reverse=True)

    # get first element
    heatleader = sortedbadgeholder[0]

    # consolidate results
    tourbadges = [tourleader, tourlemon, heatleader]

    # point spread
    spread = PointsSpread.objects.using('fantasydb').filter(sex='m').filter(
        stop_number=str(stopnumber)).filter(year=str(year))
    pointspread_tourpoints = spread.values('surfer_name', 'tourpoints').order_by(
        '-tourpoints','surfer_name')[0:8]
    pointspread_fantasypoints = spread.values('surfer_name', 'fantasypoints').order_by(
        '-fantasypoints','surfer_name')[0:8]
    pointspread_lasteventfantasypoints = spread.values('surfer_name',
        'lasteventfantasypoints').order_by('-lasteventfantasypoints','surfer_name')[0:8]
    pointspread_tourmaxheatscore = spread.values('surfer_name', 
        'tourmaxheatscore').order_by('-tourmaxheatscore','surfer_name')[0:8]
    pointspread_lasteventmaxheatscore = spread.values('surfer_name',
        'lasteventmaxheatscore').order_by('-lasteventmaxheatscore','surfer_name')[0:8]
    pointspread_results = spread.values('surfer_name',
        'results').order_by('-results','surfer_name')[0:8]

    # build context
    context = {'leaderboard':leaderboard, 
               'picks':picks, 
               'res':res, 
               'eventname':eventname, 
               'minbadge':minbadge,
               'maxbadge':maxbadge,
               'tourbadges':tourbadges,
               'mps':mps,
               'year':year,
               'stopnumber':stopnumber,
               'pointspread_tourpoints':pointspread_tourpoints,
               'pointspread_fantasypoints':pointspread_fantasypoints,
               'pointspread_tourmaxheatscore':pointspread_tourmaxheatscore,
               'pointspread_lasteventfantasypoints':pointspread_lasteventfantasypoints,
               'pointspread_lasteventmaxheatscore':pointspread_lasteventmaxheatscore,
               'pointspread_results':pointspread_results}

    # render page
    return render(request, 'dashboard/mens.html', context)




def womenstour(request, year, stopnumber):
    # Filter leaderboard 
    # The leaderboard is already structured in such a 
    # way that the table can be filtered on event id  
    leaderboard = FantasyLeaderBoard.objects.using(
      'fantasydb').filter(year=str(year)).filter(
      stop_number=str(stopnumber)).filter(sex='f')

    # filter picks table by event id 
    picks = FantasyPicks.objects.using(
      'fantasydb').filter(year=str(year)).filter(
      stop_number=str(stopnumber)).filter(sex='f')

   # collect list of distinct surfers (from the picks table)
    picks_surfers = picks.values_list('surfer_name',flat=True).distinct()

    # filter points table by event id
    # Further processing is required because the points table needs to be 
    # ordered correctly and rearranged into wide format
    points = FantasyPointsTable.objects.using(
      'fantasydb').filter(year=str(year)).filter(
      stop_number=str(stopnumber)).filter(sex='f').filter(
      surfer_name__in=picks_surfers).order_by('surfer_name', 'round_id')

    # Process points and picks to generate list of lists
    # list 1: surfer name
    # list 2: scores ordered by round 
    # list 3: player names that picked the surfer
    res = []

    # loop over surfers that the players selected 
    for surfer in picks_surfers:
        # Place holders
        scores = []
        players = []
        # loop over points table and filter on the surfer name
        for pt in points.filter(surfer_name=surfer).values_list('round_id','total','bonusflag'):
            #round = pt[0]
            if pt[2] == 'b':
                 score = [pt[1], pt[2]]
            else: 
                 score = [pt[1], 'na']
            scores.append(score)
        # loop over the picks table and filter on the surfer name 
        for pl in picks.filter(surfer_name=surfer).values_list('player_name'):
            players.append(pl[0])
        # Generate list of lists
        results = [surfer, scores, players]
        # pool the results
        res.append(results)

    # Sort function
    def collectLenOfSecond(elem):
      return len(elem[1])

    # Sort the processed table above
    res = sorted(res, key=collectLenOfSecond, reverse=True)

    # Get event information for the summary section
    # Note that the picks table has been filtered on event id 
    # passed in using the url so calling distinct should return only
    # one event name (updated to filter on stop_number - but event_name
    # should still be ok)
    eventname = picks.values_list('event_name',flat=True).distinct()

    # BADGES SECTION   
    # Count surfer picks (total across all events) - this is a badge 
    allpicks = FantasyPicks.objects.using('fantasydb').filter(year=str(year)).filter(
        stop_number__lte=str(stopnumber)).filter(sex='f')

    # Collect surfer names to loop over next
    surferlist = allpicks.values_list('surfer_name',flat=True)

    # Calculate lengths of objects - used to calculate percentage 
    numplayers = len(allpicks.values_list('player_name', flat=True).distinct())
    numevents = len(allpicks.values_list('event_id', flat=True).distinct())
    numselections = numplayers * numevents

    # place holder for results
    mostpickedsurfer = []

    # count each surfer in picks           
    for s in list(picks_surfers):
        mps = [s, round(list(surferlist).count(s)/float(numselections),2)*100]
        mostpickedsurfer.append(mps)

    # sort function
    def SortByMaxPoints(elem):
      return elem[1]

    # sort
    mps = sorted(mostpickedsurfer, key=SortByMaxPoints, reverse=True)


    # Min event points filter
    # This works because the lowest event score is held in the leaderboard
    # NB event totals are not shown in the leaderboard on the dashboard
    minpoints = leaderboard.aggregate(my_min=Min('player_points'))
    try:
        minbadge = FantasyLeaderBoard.objects.using(
          'fantasydb').filter(year=str(year)).filter(
          stop_number=str(stopnumber)).filter(sex='f').get(
          player_points=minpoints['my_min'])
    except:
        minbadge = None

    # highest points
    maxpoints = leaderboard.aggregate(my_max=Max('player_points'))
    try:
        maxbadge = FantasyLeaderBoard.objects.using(
          'fantasydb').filter(year=str(year)).filter(
          stop_number=str(stopnumber)).filter(sex='f').get(
          player_points=maxpoints['my_max'])
    except:
        maxbadge = None

    # create surfer list (from the points table)
    points_surfers = FantasyPointsTable.objects.using(
      'fantasydb').filter(stop_number__lte=str(stopnumber)).filter(
       sex='f').filter(year=str(year)).values_list('surfer_name', flat=True).distinct()

    # iterate over the points table 
    badgeholder = []
    for surfer in points_surfers:
        ptm = FantasyPointsTable.objects.using('fantasydb').filter(sex='f').filter(
            surfer_name=surfer).filter(year=str(year)).filter(
            stop_number__lte=str(stopnumber)).aggregate(ptsum=Sum('total'))['ptsum']
        pta = FantasyPointsTable.objects.using('fantasydb').filter(sex='f').filter(
            surfer_name=surfer).filter(year=str(year)).filter(
            stop_number__lte=str(stopnumber)).aggregate(ptavg=Avg('total'))['ptavg']
        bh = [surfer, ptm, pta]
        badgeholder.append(bh)
    
    # Tour points leader
    sortedbadgeholder = sorted(badgeholder, key=SortByMaxPoints, reverse=True)    
    tourleader = sortedbadgeholder[0]

    # Tour lemon
    tourlemon = [x for x in sortedbadgeholder if x[1] != 0.0][-1]        

    # Top avg heat scores
    def SortByAvgHeat(elem):
      return elem[2]

    # sort
    sortedbadgeholder = sorted(badgeholder, key=SortByAvgHeat, reverse=True)

    # get first element
    heatleader = sortedbadgeholder[0]

    # consolidate results
    tourbadges = [tourleader, tourlemon, heatleader]

    # point spread
    spread = PointsSpread.objects.using('fantasydb').filter(sex='f').filter(
        stop_number=str(stopnumber)).filter(year=str(year))
    pointspread_tourpoints = spread.values('surfer_name', 'tourpoints').order_by(
        '-tourpoints','surfer_name')[0:8]
    pointspread_fantasypoints = spread.values('surfer_name', 'fantasypoints').order_by(
        '-fantasypoints','surfer_name')[0:8]
    pointspread_lasteventfantasypoints = spread.values('surfer_name',
        'lasteventfantasypoints').order_by('-lasteventfantasypoints','surfer_name')[0:8]
    pointspread_tourmaxheatscore = spread.values('surfer_name', 
        'tourmaxheatscore').order_by('-tourmaxheatscore','surfer_name')[0:8]
    pointspread_lasteventmaxheatscore = spread.values('surfer_name',
        'lasteventmaxheatscore').order_by('-lasteventmaxheatscore','surfer_name')[0:8]
    pointspread_results = spread.values('surfer_name',
        'results').order_by('-results','surfer_name')[0:8]

    # build context
    context = {'leaderboard':leaderboard, 
               'picks':picks, 
               'res':res, 
               'eventname':eventname, 
               'minbadge':minbadge,
               'maxbadge':maxbadge,
               'tourbadges':tourbadges,
               'mps':mps,
               'year':year,
               'stopnumber':stopnumber,
               'pointspread_tourpoints':pointspread_tourpoints,
               'pointspread_fantasypoints':pointspread_fantasypoints,
               'pointspread_tourmaxheatscore':pointspread_tourmaxheatscore,
               'pointspread_lasteventfantasypoints':pointspread_lasteventfantasypoints,
               'pointspread_lasteventmaxheatscore':pointspread_lasteventmaxheatscore,
               'pointspread_results':pointspread_results}    

    # render page
    return render(request, 'dashboard/womens.html', context)

