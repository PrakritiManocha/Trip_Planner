from django import forms
from .models import Location, TripPlan, Event, PlanSelection, Expenditure, ExpenditureSplit
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import Participant,Plan

class SignUpForm(UserCreationForm):
    is_group_leader = forms.BooleanField(label='Are you a group leader?', required=False)
    team_members = forms.ModelMultipleChoiceField(queryset=User.objects.none(), label='Select team members', required=False)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'is_group_leader', 'team_members')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['team_members'].queryset = User.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        is_group_leader = cleaned_data.get('is_group_leader')

        if is_group_leader:
            self.fields['team_members'].queryset = User.objects.all()
        else:
            self.cleaned_data['team_members'] = None

        return cleaned_data

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        if commit:
            user.save()
            is_group_leader = self.cleaned_data.get('is_group_leader')
            if is_group_leader:
                team_members = self.cleaned_data.get('team_members')
                group = Group.objects.get(name='Group Leader')
                user.groups.add(group)
                # Associate group leader with selected team members
                for member in team_members:
                    participant, _ = Participant.objects.get_or_create(user=user, group=group)
                    participant.team_member = member
                    participant.save()
        return user

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name']

class TripPlanForm(forms.ModelForm):
    class Meta:
        model = TripPlan
        fields = ['name', 'destination', 'start_date', 'end_date', 'group']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['location', 'activities', 'estimated_cost', 'start_time', 'end_time', 'date']

from django import forms
from .models import PlanSelection, Plan

class PlanSelectionForm(forms.ModelForm):
    selected_plan = forms.ModelChoiceField(queryset=Plan.objects.none())

    def __init__(self, *args, **kwargs):
        plans = kwargs.pop('plans', None)
        super(PlanSelectionForm, self).__init__(*args, **kwargs)
        if plans:
            self.fields['selected_plan'].queryset = plans

    class Meta:
        model = PlanSelection
        fields = ['selected_plan']

class ExpenditureForm(forms.ModelForm):
    class Meta:
        model = Expenditure
        fields = ['amount', 'split_type']
        widgets = {
            'split_type': forms.Select(choices=[('Equal', 'Equal'), ('Custom', 'Custom')])
        }

class ExpenditureSplitForm(forms.ModelForm):
    class Meta:
        model = ExpenditureSplit
        fields = ['user', 'share']
