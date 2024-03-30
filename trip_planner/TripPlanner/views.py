from .models import Plan
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User, Group
from .forms import LocationForm, TripPlanForm, PlanSelectionForm, ExpenditureForm, SignUpForm, EventForm
from .models import Participant, Location, TripPlan, Event, PlanSelection, Expenditure
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import TripPlan
import traceback
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import TripPlan
from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from .models import TripPlan
from .forms import PlanSelectionForm


class SignUpForm(UserCreationForm):
    is_group_leader = forms.BooleanField(label='Are you a group leader?', required=False)
    team_members = forms.ModelMultipleChoiceField(queryset=User.objects.all(), label='Select team members', required=False)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'is_group_leader', 'team_members')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            is_group_leader = form.cleaned_data.get('is_group_leader')
            if is_group_leader:
                group = Group.objects.get_or_create(name='Group Leader')[0]
                user.groups.add(group)
                team_members = form.cleaned_data.get('team_members')
                for member in team_members:
                    trip_plan = member.participant.trip_plan
                    participant, _ = Participant.objects.get_or_create(user=user, trip_plan=trip_plan)
                    participant.team_member = member
                    participant.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


class LoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = 'homepage'


class LogoutView(LogoutView):
    next_page = 'homepage'


@login_required
def add_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  
    else:
        form = LocationForm()
    return render(request, 'add_location.html', {'form': form})


def create_trip_plan(request):
    if request.method == 'POST':
        form = TripPlanForm(request.POST)
        if form.is_valid():
            trip_plan = form.save(commit=False)
            trip_plan.save()
            return redirect('home')  
    else:
        form = TripPlanForm()
    return render(request, 'create_trip_plan.html', {'form': form})




@login_required
def select_plan(request, trip_plan_id):
    user = request.user
    try:
        trip_plan = TripPlan.objects.get(pk=trip_plan_id)
    except TripPlan.DoesNotExist:
        return HttpResponseNotFound("Trip Plan matching query does not exist")

    plans = trip_plan.plan_set.all()

    if request.method == 'POST':
        form = PlanSelectionForm(request.POST, plans=plans)
        if form.is_valid():
            selected_plan = form.cleaned_data['selected_plan']
            plan_selection, _ = PlanSelection.objects.get_or_create(trip_plan=trip_plan)
            plan_selection.selected_plan = selected_plan
            plan_selection.save()
            return redirect('home')
    else:
        form = PlanSelectionForm(plans=plans)

    return render(request, 'select_plan.html', {'form': form})


@login_required
def add_expenditure(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        form = ExpenditureForm(request.POST)
        if form.is_valid():
            expenditure = form.save(commit=False)
            expenditure.event = event
            expenditure.save()
            return redirect('home')
    else:
        form = ExpenditureForm()
    return render(request, 'add_expenditure.html', {'form': form})


from django.shortcuts import render, get_object_or_404
from .models import TripPlan, PlanSelection, Event


@login_required
def compare_plans(request, trip_plan_id):
    try:
        trip_plan = TripPlan.objects.get(pk=trip_plan_id)
    except TripPlan.DoesNotExist:
        return HttpResponseNotFound("Trip Plan matching query does not exist")

    plan_selections = PlanSelection.objects.filter(trip_plan=trip_plan)
    plan_events = {}

    for plan_selection in plan_selections:
        selected_plan = plan_selection.selected_plan
        events = Event.objects.filter(trip_plan=trip_plan)
        plan_events[selected_plan.name] = events

    return render(request, 'compare_plans.html', {'trip_plan': trip_plan, 'plan_events': plan_events})


def create_event(request, trip_plan_id):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.trip_plan_id = trip_plan_id
            event.creator = request.user
            event.save()
            return redirect('home')
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})




@login_required
def homepage(request):
    user = request.user
    is_group_leader = user.groups.filter(name='Group Leader').exists()

    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
    current_day_events = Event.objects.filter(date=datetime.now().date())
    total_expenditure = Expenditure.objects.aggregate(Sum('amount'))['amount__sum'] or 0

    return render(request, 'homepage.html', {
        'upcoming_events': upcoming_events,
        'current_day_events': current_day_events,
        'total_expenditure': total_expenditure,
        'is_group_leader': is_group_leader,
        'user': user,
    })
