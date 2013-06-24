# Create your views here.
from survey.models import Commutersurvey, Employer
from django.shortcuts import render, get_object_or_404
from operator import itemgetter

def index(request):
    latest_check_ins = Commutersurvey.objects.order_by('month')[:5]
    context = {'latest_check_ins' : latest_check_ins}
    return render(request, 'leaderboard/index.html', context)

def topfive(request, vol_v_perc): #top five companies by specs
    #specs is a dictionary containing 'vol_v_perc', 'month', 'sector', and 'size'
    companyList = []
    if vol_v_perc == 'perc': 
        for company in Employer.objects.all():
            try:
                companyList += [(company.name, (len(Commutersurvey.objects.filter(employer=company.name))+0.0)/company.nr_employees),]
            except TypeError:
                pass
    else:
        for company in Employer.objects.all():
            companyList += [(company.name, len(Commutersurvey.objects.filter(employer=company.name))),]
    context = {'top_five_companies' : sorted(companyList, key=itemgetter(1), reverse=True)[:5], 'vvp' : vol_v_perc}
    return render(request, 'leaderboard/topfive.html', context)

def topfivebv(request):
    return topfive(request, 'vol')

def topfivebp(request):
    return topfive(request, 'perc')

def topfivesector(request, vol_v_perc, sector, *month): #top five companies by sector
    pass
    #stuff!

def topfivesize(request, vol_v_perc, size, *month):
    pass
    #more stuff!

def whichSwitch(checkin): # 1=Unhealthy, 2=Car Commuter, 3=Green Commuter, 4=Green Switch
    """returns a tuple of (to_work, from_work)"""
    if checkin.to_work_today == 'c': tw = 1
    else: tw = 3
    if checkin.to_work_normally == 'c': tw += 1
    if checkin.from_work_today == 'c': fw = 1
    else: fw = 3
    if checkin.from_work_normally == 'c': fw += 1
    return (tw, fw)
    
def numNewCheckins(company, month1, month2):
    month1Checkins = Commutersurvey.objects.filter(employer=company, month=month1)
    month2Checkins = Commutersurvey.objects.filter(employer=company, month=month2)
    month1emails = []
    newCount = 0
    for checkin in month1Checkins:
        month1emails += checkin.email
    for checkin in month2Checkins:
        if checkin.email not in month1emails:
            newCount += 1
            month1emails += checkin.email
    return str(round(((newCount*1.0)/(len(month1emails)*1.0))*100, 2)) + "%"

