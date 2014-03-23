"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from leaderboard.views import whichSwitch
from survey.models import Commutersurvey

class testSwitch(TestCase):
    def test_green_switch(self):
        greenCommute = Commutersurvey(to_work_today='b', to_work_normally='c', from_work_today='b', from_work_normally='c')
        greenData = whichSwitch(greenCommute)
        self.assertEqual(greenData, (4,4))
    def test_green_commuter(self):
        greenCommute = Commutersurvey(to_work_today='b', to_work_normally='b', from_work_today='b', from_work_normally='b')
        greenData = whichSwitch(greenCommute)
        self.assertEqual(greenData, (3,3))
    def test_car_commuter(self):
        greenCommute = Commutersurvey(to_work_today='c', to_work_normally='c', from_work_today='c', from_work_normally='c')
        greenData = whichSwitch(greenCommute)
        self.assertEqual(greenData, (2,2))
    def test_unhealthy_switch(self):
        greenCommute = Commutersurvey(to_work_today='c', to_work_normally='b', from_work_today='c', from_work_normally='b')
        greenData = whichSwitch(greenCommute)
        self.assertEqual(greenData, (1,1))

