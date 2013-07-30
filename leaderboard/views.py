# Create your views here.
from survey.models import Commutersurvey, Employer, EmplSector
from leaderboard.models import Month
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
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
        emps = Employer.objects.filter(size_cat=sos)
    elif svs == 'sector':
        emps = Employer.objects.filter(sector=sos)
    companyList = []
    if vvp == 'perc':
        for company in emps:
            try:
                percent = (100 * float(company.get_nr_surveys(month))/float(company.nr_employees))
                companyList += [(company.name, percent, ('%.1f' % percent)),]
            except TypeError:
                pass
    else:
        for company in emps:
            nr_surveys = company.get_nr_surveys(month)
            companyList += [(company.name, nr_surveys, str(nr_surveys)),]
    topFive = sorted(companyList, key=itemgetter(1), reverse=True)[:5]
    return topFive

def getEmpCheckinMatrix(emp): 
    commuterModes = ['c', 'cp', 'w', 'b', 't', 'tc', 'o']
    checkinMatrix = {}
    todayPos = -1
    empCommutes = Commutersurvey.objects.filter(employer__contains=emp.name)
    for todayWM in commuterModes:
        checkinMatrix[todayWM] = {}
        for normalWM in commuterModes:
            numTypeCommutes = empCommutes.filter(to_work_today=todayWM, to_work_normally=normalWM).count() + empCommutes.filter(from_work_today=todayWM, from_work_normally=normalWM).count()
            checkinMatrix[todayWM][normalWM] = numTypeCommutes
    return checkinMatrix

def getBreakDown(emp, month):
    if month == "all":
        empSurveys = Commutersurvey.objects.filter(employer=emp)
    else:
        empSurveys = Commutersurvey.objects.filter(employer=emp, month=month)
    unhealthySwitches = 0
    carCommuters = 0
    greenCommuters = 0
    greenSwitches = 0
    for survey in empSurveys:
        if survey.to_work_switch == 1: unhealthySwitches += 1
        elif survey.to_work_switch == 2: carCommuters += 1
        elif survey.to_work_switch == 3: greenCommuters += 1
        elif survey.to_work_switch == 4: greenSwitches += 1
        if survey.from_work_switch == 1: unhealthySwitches += 1
        elif survey.from_work_switch == 2: carCommuters += 1
        elif survey.from_work_switch == 3: greenCommuters += 1
        elif survey.from_work_switch == 4: greenSwitches += 1
        #if 
    return { 'us': unhealthySwitches, 'cc': carCommuters, 'gc': greenCommuters, 'gs': greenSwitches, 'total':(len(empSurveys)*2) }

def getMonths(emp):
    return ['April 2013', 'May 2013', 'June 2013', 'July 2013']

def getAllMonths():
    return ['April 2013', 'May 2013', 'June 2013', 'July 2013']

def getCanvasJSChart(emp):
    chartData = getCanvasJSChartData(emp)
    barChart = {
        'title': { 'text': "Walk Ride Day Participation Breakdown and New Checkins Over Time" },
        'colorSet': 'commuterModes',
        'data': chartData
    }
    return json.dumps(barChart)

def getCanvasJSChartData(emp):
    chartData = [
        {
            'type': "stackedColumn",
            'legendText': "Green Switches",
            'showInLegend': "true",
            'dataPoints': [
            ]
        },
        {
            'type': "stackedColumn",
            'legendText': "Green Commutes",
            'showInLegend': "true",
            'dataPoints': [
            ]
        },
        {
            'type': "stackedColumn",
            'legendText': "Car Commutes",
            'showInLegend': "true",
            'dataPoints': [
            ]
        },
        {
            'type': "stackedColumn",
            'legendText': "Unhealthy Switches",
            'showInLegend': "true",
            'dataPoints': [
            ]
        }
    ]
    intToModeConversion = { 0:'gs', 1:'gc', 2:'cc', 3:'us' }
    for month in getMonths(emp):
        breakDown = getBreakDown(emp, month)
        for i in range(0, 4):
            chartData[i]['dataPoints'] += [{ 'label': month, 'y': breakDown[intToModeConversion[i]]},]
    return chartData

def leaderboard_reply_data(vol_v_perc, month, svs, sos, focusEmployer=None):
    topFive = getTopFiveCompanies(vol_v_perc, month, svs, sos)
    if focusEmployer is None and len(topFive) > 0:
        focusEmployer = topFive[0]
        print focusEmployer[0]
        emp = Employer.objects.get(name=focusEmployer[0])
    elif type(focusEmployer) is str:
        emp = Employer.objects.get(name=focusEmployer)
    elif type(focusEmployer) is Employer:
        emp = focusEmployer
    reply_data = { 
            'chart_data': getCanvasJSChart(emp), 
            'top_five_companies': json.dumps(topFive), 
            'checkin_matrix': json.dumps(getEmpCheckinMatrix(emp)),
            'total_breakdown': json.dumps(getBreakDown(emp, "all")),
    }
    return reply_data

def leaderboard_context():
    context = {
            'sectors': sorted(EmplSector.objects.all()), 
            'months': getAllMonths(),
    }
    return context

def leaderboard(request):
    if request.method == "POST":
        reply_data = leaderboard_reply_data(request.POST['selVVP'], request.POST['selMonth'], request.POST['selSVS'], request.POST['selSOS'], request.POST['focusEmployer'])
        response = HttpResponse("")
        for key in reply_data:
            response.__setitem__(key, reply_data[key])
        return response
    else:
        context = leaderboard_context()
        return render(request, 'leaderboard/leaderboard_js.html', context)

def leaderboard_bare(request, vol_v_perc='all', month='all', svs='all', sos='1', focusEmployer=None):
    context = leaderboard_context(request, vol_v_perc, month, svs, sos, focusEmployer)
    return render(request, 'leaderboard/leaderboard_bare.html', context)

def testchart(request):
    context = { 'CHART_DATA': getCanvasJSChart(Employer.objects.get(name="Dana-Farber Cancer Institute")) }
    return render(request, 'leaderboard/testchart.html', context)

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

