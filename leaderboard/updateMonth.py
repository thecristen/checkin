from leaderboard.models import Month
from survey.models import Employer, Commutersurvey
from datetime import date
from operator import itemgetter
from django.template.defaultfilters import slugify

def main():
    surveys = Commutersurvey.objects.all()
    months = []
    for survey in surveys:
        if survey.month not in months:
            months += [survey.month,]
    month_to_digit_conversion = { 'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12 }
    toSortMonth = []
    for month in months:
        year = int(month[-4:])
        imonth = month_to_digit_conversion[month[:-5]]
        toSortMonth += [[date(year, imonth, 1), month],]

    sortedMonths = sorted(toSortMonth, key=itemgetter(0))
    print sortedMonths
    for month in sortedMonths:
        newMonth = Month.objects.create(month=month[1], url_month=slugify(month[1]))
        newMonth.save()
        
