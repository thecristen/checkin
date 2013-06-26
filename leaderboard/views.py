# Create your views here.
from survey.models import Commutersurvey, Employer, EmplSector
from leaderboard.models import Month
from django.shortcuts import render, get_object_or_404
from operator import itemgetter

def index(request):
    latest_check_ins = Commutersurvey.objects.order_by('month')[:5]
    context = {'latest_check_ins' : latest_check_ins}
    return render(request, 'leaderboard/index.html', context)

def leaderboard_context(request, vol_v_perc='all', month='all', sector='all', size='all', focusEmployer=None):
    companyList = []
    if sector == 'all' and size == 'all':
        emps = Employer.objects.all()
    elif sector == 'all':
        emps = Employer.objects.filter(size_cat=size, month=month)
    elif size == 'all':
        emps = Employer.objects.filter(sector=sector, month=month)
    else:
        emps = Employer.objects.filter(size_cat=size, sector=sector)
    if vol_v_perc == 'perc': 
        for company in emps:
            try:
                companyList += [(company.name, company.nr_surveys/company.nr_employees),]
            except TypeError:
                pass
    else:
        for company in emps:
            companyList += [(company.name, company.nr_surveys),]
    topFive = sorted(companyList, key=itemgetter(1), reverse=True)[:5]
    if focusEmployer == None:
        focusEmployer = topFive[0]
    context = { 'top_five_companies': topFive, 'sectors': EmplSector.objects.all(), 'months': Month.objects.all(), 'selVVP': vol_v_perc, 'selMonth': month, 'selSector': sector, 'selSize': size }
    return context

def leaderboard(request, vol_v_perc='all', month='all', sector='all', size='all', focusEmployer=None):
    context = leaderboard_context(request, vol_v_perc, month, sector, size, focusEmployer)
    return render(request, 'leaderboard/leaderboard.html', context)

def leaderboard_bare(request, vol_v_perc='all', month='all', sector='all', size='all', focusEmployer=None):
    context = leaderboard_context(request, vol_v_perc, month, sector, size, focusEmployer)
    return render(request, 'leaderboard/leaderboard_bare.html', context)


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

