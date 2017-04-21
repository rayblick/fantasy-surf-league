from django.shortcuts import render
from django.db.models import Max, Min, Sum, Avg
from .models import FantasyPicks, FantasyPointsTable, FantasyLeaderBoard
from .forms import EventsForm


def index(request):
    """
    Sends the user to the most recent events page.
    """
    # get max event id
    maxevent = FantasyLeaderBoard.objects.using(
      'fantasydb').aggregate(em=Max('event_id'))['em']
    return championshiptour(request, maxevent)


def championshiptour(request, eventid):
    # Filter leaderboard 
    # The leaderboard is already structured in such a 
    # way that the table can be filtered on event id  
    leaderboard = FantasyLeaderBoard.objects.using(
      'fantasydb').filter(event_id=str(eventid))

    # filter picks table by event id 
    picks = FantasyPicks.objects.using(
      'fantasydb').filter(event_id=str(eventid))

   # collect list of distinct surfers (from the picks table)
    picks_surfers = picks.values_list('surfer_name',flat=True).distinct()

    # filter points table by event id
    # Further processing is required because the points table needs to be 
    # ordered correctly and rearranged into wide format
    points = FantasyPointsTable.objects.using('fantasydb').filter(
      event_id=str(eventid)).filter(surfer_name__in=picks_surfers).order_by(
      'surfer_name', 'round_id')

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
            round = pt[0]
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
    # one event name
    eventname = picks.values_list('event_name',flat=True).distinct()

    # BADGES SECTION   
    # Count surfer picks (total across all events) - this is a badge 
    allpicks = FantasyPicks.objects.using('fantasydb').filter(
        event_id__lte=str(eventid))

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
        mps = [s, (list(surferlist).count(s)/numselections)*100]
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
    minbadge = FantasyLeaderBoard.objects.using('fantasydb').get(
                   player_points=str(minpoints['my_min']))
    
    # highest points
    maxpoints = leaderboard.aggregate(my_max=Max('player_points'))
    maxbadge = FantasyLeaderBoard.objects.using('fantasydb').get(
                   player_points=str(maxpoints['my_max']))
    
    # create surfer list (from the points table)
    points_surfers = FantasyPointsTable.objects.using(
      'fantasydb').filter(event_id__lte=str(eventid)).values_list(
      'surfer_name', flat=True).distinct()

    # iterate over the points table 
    badgeholder = []
    for surfer in points_surfers:
        ptm = FantasyPointsTable.objects.using('fantasydb').filter(
            surfer_name=surfer).filter(event_id__lte=str(eventid)).aggregate(
            ptsum=Sum('total'))['ptsum']
        pta = FantasyPointsTable.objects.using('fantasydb').filter(
            surfer_name=surfer).filter(event_id__lte=str(eventid)).aggregate(
            ptavg=Avg('total'))['ptavg']
        bh = [surfer, ptm, pta]
        badgeholder.append(bh)
    
    # Tour points leader
    sortedbadgeholder = sorted(badgeholder, key=SortByMaxPoints, reverse=True)    
    tourleader = sortedbadgeholder[0]

    # Tour lemon
    tourlemon = sortedbadgeholder[-1]

    # Top avg heat scores
    def SortByAvgHeat(elem):
      return elem[2]

    # sort
    sortedbadgeholder = sorted(badgeholder, key=SortByAvgHeat, reverse=True)

    # get first element
    heatleader = sortedbadgeholder[0]

    # consolidate results
    tourbadges = [tourleader, tourlemon, heatleader]

    # build context
    context = {'leaderboard':leaderboard, 
               'picks':picks, 
               'res':res, 
               'eventname':eventname, 
               'minbadge':minbadge,
               'maxbadge':maxbadge,
               'tourbadges':tourbadges,
               'mps':mps,
               'eventid':eventid}

    # render page
    return render(request, 'dashboard/index.html', context)

