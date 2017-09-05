from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Item

import os
import json
import random
from django.forms.models import model_to_dict

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from datetime import date, datetime, time
import pytz

from django.contrib.auth.models import User

from .forms import ItemForm

@login_required(login_url='/login/')
def index(request):
    '''index will populate the page with items from the database'''
    # I believe this is secure: https://stackoverflow.com/questions/15819937/django-auth-can-request-user-be-exploited-and-point-to-other-user
    user = request.user

    # Split the items based on whether or not the due date has passed
    todo_items = Item.objects\
        .filter(user=user, due_date__gte=timezone.now())\
        .order_by('due_date')
    past_items = Item.objects\
        .filter(user=user, due_date__lt=timezone.now())\
        .order_by('due_date')

    return render(request, 'todo/index.html',
                  {'item_list': todo_items,
                   'past_items': past_items})

@login_required(login_url='/login/')
def show_item(request):
    '''Return a specific item using passed in primary key via ajax request'''
    try:
        item_id = request.GET['id']
        item_select = get_object_or_404(Item, pk=item_id, user=request.user)
    except:
        print("Error at todo.view.show_item")
    
    # Use custom method to turn into python dict
    pre_data = item_select.to_dict()
    # Convert the date fields from datetime objects to strings
    tz = pytz.timezone('America/Chicago')
    
    pre_data['add_date'] = str(pre_data['add_date'].astimezone(tz))
    pre_data['due_date'] = str(pre_data['due_date'].astimezone(tz))
    pre_data['start_date'] = str(pre_data['start_date'].astimezone(tz))

    # User field is not naively serializable and is unneeded. Throw it out
    pre_data.pop('user', None)

    # Dump data and return it
    data = json.dumps(pre_data)
    return JsonResponse(data, safe=False)

@login_required(login_url='/login/')
def complete_item(request):
    '''Update an item's complete status via an ajax request'''
    try:
        item_id = request.GET['id']
        complete = request.GET['complete']
        item = get_object_or_404(Item, pk=item_id)
    except:
        print("Error at todo.view.complete_item")

    if complete == "false":
        bool_complete = False
    elif complete == "true":
        bool_complete = True
    else:
        print("ERROR WITH complete_item")
    # Update the item's compete status and save it to the database
    item.complete = bool_complete
    item.save()

    # Return the JsonResponse - the returned dict is not used for anything
    return JsonResponse({'tmp': 'success'}, safe=False)

@login_required(login_url='/login/')
def add_item(request):
    '''Add a new item from a form via POST method'''
    def convert_date(date_string):
        '''Helper function to convert dates as strings to datetime objects'''
        day = datetime.strptime(date_string, '%m/%d/%Y')
        # If date_string is 8/20/2017, then day will be datetime.datetime(2017, 6, 20, 0, 0)
        # But the due date should not be at the start of the day - it should be the end
        # So set it to datetime.datetime(2017, 6, 20, 23, 59, 59, 999999)
        tz = pytz.timezone('America/Chicago')
        end_day = tz.localize(day).replace(hour=23, minute=59, second=59, microsecond=999999)
        return end_day

    if 'add_button' in request.POST:
        # try:
            # Attempt to fill out a new item and save it to the database
            form = ItemForm(request.POST)
            if form.is_valid:
                form.due_date = timezone.now()
                form.start_date = timezone.now()
                form.user = request.user
                form.complete = False
                form.priority = -1
                print(form.fields)
                form.save()

        # except:
            # If it didn't work, assume the provided data was invalid and
            # request user try again.
            # messages.warning(request, "Input Not Valid - Please Try Again")
            # HttpResponseRedirect(request.path)
    # Used instead of redirect so that back button goes back to todo page
    return HttpResponseRedirect(reverse('todo:index'))

@login_required(login_url='/login/')
def delete_item(request, item_id):
    '''Delete an item upon ajax request'''
    try:
        item = get_object_or_404(Item, pk=item_id, user=request.user)
    except:
        print("Error at todo.view.delete_item")
    # To be honest, I don't know if this is necessary. But it makes me feel better
    item.delete()
    # Return the JsonResponse - the returned dict is not used for anything
    return JsonResponse({'tmp': 'success'}, safe=False)

@login_required(login_url='/login/')
def test_add(request):
    # If the form is valid, attempt to authenticate and login the user
    form = ItemForm(request.POST)
    if form.is_valid():
        item = form.cleaned_data
        item['due_date'] = timezone.now()
        form.start_date = timezone.now()
        form.user = request.user
        form.complete = False
        form.priority = -1
        print(form.cleaned_data)
        form.save()

    # If user is not logged in, show the login page. 
    return render(request, "todo/form.html", {"form":form})