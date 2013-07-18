# Create your views here.
from survey.models import Employer, Commutersurvey
from leaderboard.views import getBreakDown, getCanvasJSChart, getMonths
from django.shortcuts import render
from leaderboard.models import Month
import json

def getCJSEmplList(month):
    chart = {
        'title': { 'text': 'Alphabetical Employer Breakdown for %s' % (month,), 'fontSize': 20 },
        'creditText': 'gogreenstreets.org',
        'creditHref': 'http://gogreenstreets.org',
        'axisX': {
            'labelFontSize': 12,
            'margin': 0,
        },
        'axisY': {
            'labelFontSize': 12,
        },
        'legend': {
            'fontSize': 12,
        },
        'data': [
            {
                'type': 'stackedBar',
                'color': '#0096FF',
                'legendText': 'Green Switches',
                'showInLegend': 'true',
                'toolTipContent': '{name}: {y}',
                'dataPoints': [
                ]
            },
            {
                'type': 'stackedBar',
                'color': '#65AB4B',
                'legendText': 'Green Commuters',
                'showInLegend': 'true',
                'toolTipContent': '{name}: {y}',
                'dataPoints': [
                ]
            },
            {
                'type': 'stackedBar',
                'color': '#FF2600',
                'legendText': 'Car Commuters',
                'showInLegend': 'true',
                'toolTipContent': '{name}: {y}',
                'dataPoints': [
                ]
            },
            {
                'type': 'stackedBar',
                'color': '#9437FF',
                'legendText': 'Unhealthy Switches',
                'showInLegend': 'true',
                'toolTipContent': '{name}: {y}',
                'dataPoints': [
                ]
            },
        ]
    }
    breakDownTranslator = [ 'gs', 'gc', 'cc', 'us' ]
    longBDT = [ 'Green Switches', 'Green Commuters', 'Car Commuters', 'Unhealthy Switches' ]
    for emp in Employer.objects.filter(active=True).reverse():
        breakDown = getBreakDown(emp, month)
        for i in range(0, 4):
            chart['data'][i]['dataPoints'] += [{ 'label': emp.name, 'name': longBDT[i], 'y': breakDown[breakDownTranslator[i]] },]
    return json.dumps(chart)

def empBreakDown(request, month):
    fullMonth = Month.objects.get(url_month=month)
    context = { 'month': month, 'CHART_DATA': getCJSEmplList(fullMonth.month) }
    return render(request, 'leaderboardlist/leaderboardlist.html', context)
    
def chooseMonth(request):
    months = getMonths()
    context = { 'months': months }
    return render(request, 'leaderboardlist/chooseMonths.html', context)
