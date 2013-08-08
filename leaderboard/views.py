# Create your views here.
from survey.models import Commutersurvey, Employer, EmplSector
from leaderboard.models import Month, getMonths
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from operator import itemgetter, attrgetter
import json

def index(request):
    latest_check_ins = Commutersurvey.objects.order_by('month')[:5]
    context = {'latest_check_ins' : latest_check_ins}
    return render(request, 'leaderboard/index.html', context)

def getSectorNum(sector):
    if sector.name[1] == ' ':
        return int(sector.name[0])
    elif sector.name[2] == ' ':
        return int(sector.name[:2])
    else:
        return int(sector.name[:3])

def getTopCompanies(vvp, month, svs, sos):
    emps = Employer.objects.filter(active=True, sector__in=EmplSector.objects.filter(parent=None))
    if svs == 'size':
        emps = emps.filter(size=sos)
    elif svs == 'sector':
        sector = EmplSector.objects.get(pk=sos)
        if sector.parent != None:
            emps = Employer.objects.filter(active=True, sector=sos)
        else:
            emps = emps.filter(sector=sos)
    elif svs == 'name':
        nameList = []
        for emp in sorted(emps, key=attrgetter('name')):
            nameList += [(emp.name, 0, 0),]
        return nameList
    companyList = []
    if vvp == 'perc':
        for company in emps:
            try:
                percent = (100 * float(company.get_nr_surveys(month))/float(company.nr_employees))
                if month == 'all':
                    percent /= len(getMonths())
                companyList += [(company.name, percent, ('%.1f' % percent)),]
            except TypeError:
                pass
    else:
        for company in emps:
            nr_surveys = company.get_nr_surveys(month)
            companyList += [(company.name, nr_surveys, str(nr_surveys)),]
    topEmps = sorted(companyList, key=itemgetter(1), reverse=True)
    return topEmps

def getEmpCheckinMatrix(emp): 
    commuterModes = ['c', 'cp', 'w', 'b', 't', 'tc', 'o']
    checkinMatrix = []
    todayPos = -1
    empCommutes = emp.get_surveys('all')
    for todayWM in commuterModes:
        todayPos += 1
        checkinMatrix += [[],]
        for normalWM in commuterModes:
            numTypeCommutes = empCommutes.filter(to_work_today=todayWM, to_work_normally=normalWM).count() + empCommutes.filter(from_work_today=todayWM, from_work_normally=normalWM).count()
            checkinMatrix[todayPos] += [numTypeCommutes,]
    return checkinMatrix

def getBreakDown(emp, month):
    empSurveys = emp.get_surveys(month)
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

def getCanvasJSChart(emp):
    chartData = getCanvasJSChartData(emp)
    barChart = {
        'title': { 
            'text': "Walk Ride Day Participation Over Time",
            'fontSize': 20 },
        'colorSet': 'commuterModes',
        'data': chartData
    }
    return barChart

def getCanvasJSChartData(emp):
    chartData = [
        {
            'type': "stackedColumn",
            'color': '#0096FF',
            'legendText': "Green Switches",
            'showInLegend': "true",
            'toolTipContent': '{name}: {y}',
            'dataPoints': [
            ]
        },
        {
            'type': "stackedColumn",
            'color': '#65AB4B',
            'legendText': "Green Commutes",
            'showInLegend': "true",
            'toolTipContent': '{name}: {y}',
            'dataPoints': [
            ]
        },
        {
            'type': "stackedColumn",
            'color': '#FF2600',
            'legendText': "Car Commutes",
            'showInLegend': "true",
            'toolTipContent': '{name}: {y}',
            'dataPoints': [
            ]
        },
        {
            'type': "stackedColumn",
            'color': '#9437FF',
            'legendText': "Other",
            'showInLegend': "true",
            'toolTipContent': '{name}: {y}',
            'dataPoints': [
            ]
        }
    ]
    intToModeConversion = ['gs', 'gc', 'cc', 'us']
    iTMSConv = ['Green Switches','Green Commutes', 'Car Commutes', 'Other']
    for month in getMonths():
        breakDown = getBreakDown(emp, month)
        for i in range(0, 4):
            chartData[i]['dataPoints'] += [{ 'label': month, 'y': breakDown[intToModeConversion[i]], 'name': iTMSConv[i] },]
    return chartData

def leaderboard_reply_data(vol_v_perc, month, svs, sos, focusEmployer=None):
    topEmps = getTopCompanies(vol_v_perc, month, svs, sos) 
    if focusEmployer is None and len(topEmps) > 0:
        focusEmployer = topEmps[0]
        emp = Employer.objects.get(name=focusEmployer[0])
    elif type(focusEmployer) is str:
        emp = Employer.objects.get(name=focusEmployer)
    elif type(focusEmployer) is Employer:
        emp = focusEmployer
    reply_data = { 
            'chart_data': getCanvasJSChart(emp), 
            'top_companies': topEmps, 
            'checkin_matrix': getEmpCheckinMatrix(emp),
            'total_breakdown': getBreakDown(emp, "all"),
            'vol_v_perc': vol_v_perc,
            'month': month,
            'svs': svs,
            'sos': sos,
    }
    return reply_data

def leaderboard_company_detail(empName):
    emp = Employer.objects.get(name=empName)
    reply_data = {
            'chart_data': getCanvasJSChart(emp),
            'checkin_matrix': getEmpCheckinMatrix(emp),
            'total_breakdown': getBreakDown(emp, "all"),
    }
    return reply_data

def leaderboard_context():
    context = {
            'sectors': sorted(EmplSector.objects.all(), key=getSectorNum), 
            'months': Month.objects.filter(active=True),
    }
    return context

def leaderboard(request):
    if request.method == "POST":
        if request.POST['just_emp'] == 'false':
            reply_data = leaderboard_reply_data(request.POST['selVVP'], request.POST['selMonth'], request.POST['selSVS'], request.POST['selSOS'],)
        else:
            reply_data = leaderboard_company_detail(request.POST['focusEmployer'])
        response = HttpResponse(json.dumps(reply_data), content_type='application/json')
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

