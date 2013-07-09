# Create your views here.
from survey.models import Commutersurvey, Employer, EmplSector
from leaderboard.models import Month
from django.shortcuts import render, get_object_or_404
from operator import itemgetter
import json

def index(request):
    latest_check_ins = Commutersurvey.objects.order_by('month')[:5]
    context = {'latest_check_ins' : latest_check_ins}
    return render(request, 'leaderboard/index.html', context)

def getTopFiveCompanies(vvp, month, svs, sos):
    emps = []
    if svs == 'all':
        emps = Employer.objects.all()
    elif svs == 'size':
        emps = Employer.objects.filter(size=sos)
    elif svs == 'sector':
        emps = Employer.objects.filter(sector=sos)
    companyList = []
    if vol_v_perc == 'perc':
        for company in emps:
            try:
                companyList += [(company.name, ('%.1f' % (100 * (company.nr_surveys(month) + 0.0)/(company.nr_employees + 0.0)))),]
            except TypeError:
                pass
    else:
        for company in emps:
            companyList += [(company.name, str(company.nr_surveys(month))),]
    topFive = sorted(companyList, key=itemgetter(1), reverse=True)[:5]
    return topFive

def getEmpCheckinMatrix(emp): 
    commuterModes = ['c', 'cp', 'w', 'b', 't', 'tc', 'o']
    checkinMatrix = []
    todayPos = -1
    empCommutes = Commutersurvey.objects.filter(employer__contains=emp.name)
    for todayWM in commuterModes:
        todayPos += 1
        checkinMatrix += [[],]
        for normalWM in commuterModes:
            numTypeCommutes = empCommutes.filter(to_work_today=todayWM, to_work_normally=normalWM).count() + empCommutes.filter(from_work_today=todayWM, from_work_normally=normalWM).count()
            checkinMatrix[todayPos] += [numTypeCommutes,]
    return checkinMatrix

def getBreakdown(emp, month):
    empSurveys = Commutersurvey.objects.filter(employer=emp, month=month)
    unhealthySwitches = 0
    carCommuters = 0
    greenCommuters = 0
    greenSwitches = 0
    for survey in empSurveys:
        if survey.to_work_switch == 1: unhealthySwitches += 1
        elif survey.to_work_switch == 2: carCommuters += 1
        elif survey.to_work_switch == 3: greenSwitches += 1
        elif survey.to_work_switch == 4: greenSwitches += 1
        if survey.from_work_switch == 1: unhealthySwitches += 1
        elif survey.from_work_switch == 2: carCommuters += 1
        elif survey.from_work_switch == 3: greenCommuters += 1
        elif survey.from_work_switch == 4: greenSwitches += 1
    return { 'us': unhealthySwitches, 'cc': carCommuters, 'gc': greenCommuters, 'gs': greenSwitches }

def getMonths(emp):
    return ['March 2013', 'April 2013', 'May 2013', 'June 2013', 'July 2013']

def getCanvasJSChart(emp):
    chartData = getCanvasJSChartData(emp)
    barChart = {
        'title': { 'text': "Walk Ride Day Participation Breakdown and New Checkins Over Time" },
        'data': chartData
    }
    return json.dumps(chartData)

def getCanvasJSChartData(emp):
    chartData = [
        {
            'type': "stackedBar",
            'legendText': "Green Switches",
            'showInLegend': "true",
            'dataPoints': [
            ]
        },
        {
            'type': "stackedBar",
            'legendText': "Green Commutes",
            'showInLegend': "true",
            'dataPoints': [
            ]
        },
        {
            'type': "stackedBar",
            'legendText': "Car Commutes",
            'showInLegend': "true",
            'dataPoints': [
            ]
        },
        {
            'type': "stackedBar",
            'legendText': "Unhealthy Switches",
            'showInLegend': "true",
            'dataPoints': [
            ]
        }
    ]
    intToModeConversion = { 0:'gs', 1:'gc', 2:'cc', 3:'us' }
    for month in getMoths(emp):
        breakDown = getBreakDown(month)
        for i in range(0, 4):
            chartData[i]['dataPoints'] += [{ 'y': month, 'x': breakDown[intToModeConversion[i]]},]
    return chartData

def leaderboard_context(request, vol_v_perc='perc', month='all', svs='all', sos='1', focusEmployer=None):
    topFive = getTopFiveCompanies(vol_v_perc, month, svs, sos)
    if focusEmployer == None and len(topFive) > 0:
        focusEmployer = topFive[0]
    if vol_v_perc == 'vol':
        vvpMsg = ' checkins'
    else:
        vvpMsg = '% participation'
    context = { 'top_five_companies': topFive, 'sectors': sorted(EmplSector.objects.all()), 'months': Month.objects.all(), 'selVVP': vol_v_perc, 'selMonth': month, 'selSOS': sos, 'selSVS': svs, 'vvpMsg': vvpMsg }
    return context

def leaderboard(request, vol_v_perc='all', month='all', svs='all', sos='1', focusEmployer=None):
    context = leaderboard_context(request, vol_v_perc, month, svs, sos, focusEmployer)
    return render(request, 'leaderboard/leaderboard.html', context)

def leaderboard_bare(request, vol_v_perc='all', month='all', svs='all', sos='1', focusEmployer=None):
    context = leaderboard_context(request, vol_v_perc, month, svs, sos, focusEmployer)
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

