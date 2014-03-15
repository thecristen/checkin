from django.forms import ModelForm, HiddenInput

from survey.models import Commutersurvey


class CommuterForm(ModelForm):
    class Meta:
        model = Commutersurvey
        exclude = ('walkrideday','ip')
        widgets = {
                   'home_location': HiddenInput(),
                   'work_location': HiddenInput(),
                   'distance': HiddenInput(),
                   'duration': HiddenInput(),
                   }
    
