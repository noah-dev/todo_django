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
from datetime import date, datetime, time, timedelta
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
    form = ItemForm(request.POST)
    if form.is_valid():
        # item = form.cleaned_data
        # user = request.user
        # complete = False
        # priority = -1
        item = form.save(commit = False)
        print(item)
        item.user = request.user
        item.complete = False
        item.priority = -1
        item.due_date += timedelta(days=0, microseconds=999999, seconds=59, minutes=59, hours=23)
        print(item)
        item.save()
    else:
        # If it didn't work, assume the provided data was invalid and
        # request user try again.
        messages.warning(request, "Input Not Valid - Please Try Again")
        HttpResponseRedirect(request.path)
    
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
