from django.contrib import messages
from django.contrib.auth import login, authenticate, REDIRECT_FIELD_NAME
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LogoutView as BaseLogoutView, PasswordChangeView as BasePasswordChangeView,
    PasswordResetDoneView as BasePasswordResetDoneView, PasswordResetConfirmView as BasePasswordResetConfirmView,
)
from django.shortcuts import get_object_or_404, redirect
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import View, FormView
from django.conf import settings

from .utils import (
    send_activation_email, send_reset_password_email, send_forgotten_username_email, send_activation_change_email,
)
from .forms import (
    SignInViaUsernameForm, SignInViaEmailOrUsernameForm, SignUpForm,
)
from .models import Activation,Figma_LIX_talk,Notion_LIX_talk,Slack_LIX_talk,Trello_LIX_talk,Miro_LIX_talk,Figma_twi_talk,Onalytica_twi_talk,Slack_twi_talk,Trello_twi_talk,Miro_twi_talk,Notion_twi_talk,Figma_phantom_talk,Notion_phantom_talk,Slack_phantom_talk,Trello_phantom_talk


import sqlite3
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import csv, io
import pandas as pd
from datetime import datetime
from pathlib import Path
import os
from django.http import HttpResponse
from django.db.models import Q


@login_required
def figma_lix(request):

    #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Figma_LIX_talk.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    Figma_LIX_talk.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=Figma_LIX_talk.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    Figma_LIX_talk.objects.filter(Row_id=ids).update(contact=0)


    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Figma_LIX_talk.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    Figma_LIX_talk.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                Figma_LIX_talk.objects.filter(Row_id=ids).delete()



    #UPLOAD CSV FILE
    if 'csv_upload' in request.POST:

        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a .csv file.')

        file_data = csv_file.read().decode("utf-8")  
        io_string = io.StringIO(file_data)
        next(io_string) 
        no_rows=0
        no_rows_added=0
        for column in csv.reader(io_string, delimiter=','):
            no_rows+=1
            if not Figma_LIX_talk.objects.filter(Profile_Link=column[0]).exists():
                data_dict = {}
                link_lix=Figma_LIX_talk()
                link_lix.Profile_Link = column[0]
                link_lix.Category=column[1]
                link_lix.Description=column[2]
                link_lix.Experience_Title=column[3]
                link_lix.LinkedIn_Name=column[4]
                link_lix.Location=column[5]
                link_lix.save()
                no_rows_added+=1
        msg_display=f"Uploaded {no_rows_added} rows out of {no_rows} "

    #DELETE

    elif 'csv_delete' in request.POST:
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a .csv file.')

        file_data = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(file_data)
        next(io_string)
        in_db=list()
        for column in csv.reader(io_string, delimiter=','):
            column=' '.join(map(str, column)) 
            Figma_LIX_talk.objects.filter(Profile_Link=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=Figma_LIX_talk.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=Figma_LIX_talk.objects.filter(
          
          Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
          
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['ProfileLink','Category','Description','Experience Title','LinkedIn Name','Location']


    page = request.GET.get('page', 1)
    paginator = Paginator(displaytopic, no_display)
    try:
        users = paginator.page(page)
        start_index = users.start_index()
        end_index = users.end_index()
    except PageNotAnInteger:
        users = paginator.page(1)
        start_index = users.start_index()
        end_index = users.end_index()
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
        start_index = users.start_index()
        end_index = users.end_index()

    if 'export_all' in request.POST:
        response =HttpResponse(content_type='text/csv')
        writer=csv.writer(response)
        response['Content-Disposition'] = 'attachment; filename="Figma LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['ProfileLink','Category','Description','Experience Title','LinkedIn Name','Location','Contacted'])
        writedata = displaytopic.values_list('Profile_Link','Category','Description','Experience_Title','LinkedIn_Name','Location','contact')

        write_list=list()
        for row in writedata:   
            if row[6] ==  1:
                write_contact='Yes'
            else:
                write_contact='No'
            wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

            write_list.append(wlist)

            writer.writerow(wlist)

        return response
        msg_display= f"CSV exported successfully! "



    if 'csv_upload' in request.POST:
        msg_display2='Uploaded successfully....'
    elif 'csv_delete' in request.POST:
        msg_display='Deleted successfully....'
    else:
        msg_display=''

    import os
    #Export csv
    if request.GET.get('csv_export'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')
            displaytopic=Figma_LIX_talk.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Figma LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['ProfileLink','Category','Description','Experience Title','LinkedIn Name','Location','Contacted'])
            writedata = displaytopic.values_list('Profile_Link','Category','Description','Experience_Title','LinkedIn_Name','Location','contact')

            write_list=list()
            for row in writedata:   
                if row[6] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "

        elif sear1=='yes':
            query = request.session['query']

            displaytopic1=Figma_LIX_talk.objects.filter(
          
              Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            #cur.execute("SELECT * FROM Figma LIX;")
            
            #displaytopic=Figma_LIX_talk.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Figma LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['ProfileLink','Category','Description','Experience Title','LinkedIn Name','Location','Contacted'])
            writedata = displaytopic1.values_list('Profile_Link','Category','Description','Experience_Title','LinkedIn_Name','Location','contact')
            write_list=list()
            for row in writedata:
                if row[6] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "



        else:
            
            #cur.execute("SELECT * FROM Figma LIX;")
            displaytopic=Figma_LIX_talk.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Figma LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['ProfileLink','Category','Description','Experience Title','LinkedIn Name','Location','Contacted'])
            writedata = displaytopic.values_list('Profile_Link','Category','Description','Experience_Title','LinkedIn_Name','Location','contact')
            write_list=list()
            for row in writedata:
                if row[6] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        del request.session['query']
        del request.session['sear']

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Figma Linkedin (L)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def notion_lix(request):

    #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Notion_LIX_talk.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    Notion_LIX_talk.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=Notion_LIX_talk.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    Notion_LIX_talk.objects.filter(Row_id=ids).update(contact=0)


    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Notion_LIX_talk.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    Notion_LIX_talk.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                Notion_LIX_talk.objects.filter(Row_id=ids).delete()
                



    #UPLOAD CSV FILE
    if 'csv_upload' in request.POST:

        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a .csv file.')

        file_data = csv_file.read().decode("utf-8")  
        io_string = io.StringIO(file_data)
        next(io_string) 
        no_rows=0
        no_rows_added=0
        for column in csv.reader(io_string, delimiter=','):
            no_rows+=1
            if not Notion_LIX_talk.objects.filter(Profile_Link=column[0]).exists():
                data_dict = {}
                link_lix=Notion_LIX_talk()
                link_lix.Profile_Link = column[0]
                link_lix.Category=column[1]
                link_lix.Description=column[2]
                link_lix.Experience_Title=column[3]
                link_lix.LinkedIn_Name=column[4]
                link_lix.Location=column[5]
                link_lix.save()
                no_rows_added+=1
        msg_display=f"Uploaded {no_rows_added} rows out of {no_rows} "

    #DELETE

    elif 'csv_delete' in request.POST:
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a .csv file.')

        file_data = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(file_data)
        next(io_string)
        in_db=list()
        for column in csv.reader(io_string, delimiter=','):
            column=' '.join(map(str, column)) 
            Notion_LIX_talk.objects.filter(Profile_Link=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=Notion_LIX_talk.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=Notion_LIX_talk.objects.filter(
          
          Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
          
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['ProfileLink','Category','Description','Experience Title','LinkedIn Name','Location']


    page = request.GET.get('page', 1)
    paginator = Paginator(displaytopic, no_display)
    try:
        users = paginator.page(page)
        start_index = users.start_index()
        end_index = users.end_index()
    except PageNotAnInteger:
        users = paginator.page(1)
        start_index = users.start_index()
        end_index = users.end_index()
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
        start_index = users.start_index()
        end_index = users.end_index()

    if 'export_all' in request.POST:
        response =HttpResponse(content_type='text/csv')
        writer=csv.writer(response)
        response['Content-Disposition'] = 'attachment; filename="Notion LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['ProfileLink','Category','Description','Experience Title','LinkedIn Name','Location','Contacted'])
        writedata = displaytopic.values_list('Profile_Link','Category','Description','Experience_Title','LinkedIn_Name','Location','contact')

        write_list=list()
        for row in writedata:   
            if row[6] ==  1:
                write_contact='Yes'
            else:
                write_contact='No'
            wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

            write_list.append(wlist)

            writer.writerow(wlist)

        return response
        msg_display= f"CSV exported successfully! "



    if 'csv_upload' in request.POST:
        msg_display2='Uploaded successfully....'
    elif 'csv_delete' in request.POST:
        msg_display='Deleted successfully....'
    else:
        msg_display=''

    import os
    #Export csv
    if request.GET.get('csv_export'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')
            displaytopic=Notion_LIX_talk.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Notion LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['ProfileLink','Category','Description','Experience Title','LinkedIn Name','Location','Contacted'])
            writedata = displaytopic.values_list('Profile_Link','Category','Description','Experience_Title','LinkedIn_Name','Location','contact')

            write_list=list()
            for row in writedata:   
                if row[6] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "

        elif sear1=='yes':
            query = request.session['query']

            displaytopic1=Notion_LIX_talk.objects.filter(
          
              Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            #cur.execute("SELECT * FROM Notion LIX;")
            
            #displaytopic=Notion_LIX_talk.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Notion LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['ProfileLink','Category','Description','Experience Title','LinkedIn Name','Location','Contacted'])
            writedata = displaytopic1.values_list('Profile_Link','Category','Description','Experience_Title','LinkedIn_Name','Location','contact')
            write_list=list()
            for row in writedata:
                if row[6] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "



        else:
            
            #cur.execute("SELECT * FROM Notion LIX;")
            displaytopic=Notion_LIX_talk.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Notion LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['ProfileLink','Category','Description','Experience Title','LinkedIn Name','Location','Contacted'])
            writedata = displaytopic.values_list('Profile_Link','Category','Description','Experience_Title','LinkedIn_Name','Location','contact')
            write_list=list()
            for row in writedata:
                if row[6] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        del request.session['query']
        del request.session['sear']

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Notion Linkedin (L)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def slack_lix(request):

    #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Slack_LIX_talk.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    Slack_LIX_talk.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=Slack_LIX_talk.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    Slack_LIX_talk.objects.filter(Row_id=ids).update(contact=0)


    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Slack_LIX_talk.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    Slack_LIX_talk.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                Slack_LIX_talk.objects.filter(Row_id=ids).delete()



    #UPLOAD CSV FILE
    if 'csv_upload' in request.POST:

        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a .csv file.')

        file_data = csv_file.read().decode("utf-8")  
        io_string = io.StringIO(file_data)
        next(io_string) 
        no_rows=0
        no_rows_added=0
        for column in csv.reader(io_string, delimiter=','):
            no_rows+=1
            if not Slack_LIX_talk.objects.filter(Profile_Link=column[0]).exists():
                data_dict = {}
                link_lix=Slack_LIX_talk()
                link_lix.Profile_Link = column[0]
                link_lix.Category=column[1]
                link_lix.Description=column[2]
                link_lix.Experience_Title=column[3]
                link_lix.LinkedIn_Name=column[4]
                link_lix.Location=column[5]
                link_lix.save()
                no_rows_added+=1
        msg_display=f"Uploaded {no_rows_added} rows out of {no_rows} "

    #DELETE

    elif 'csv_delete' in request.POST:
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a .csv file.')

        file_data = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(file_data)
        next(io_string)
        in_db=list()
        for column in csv.reader(io_string, delimiter=','):
            column=' '.join(map(str, column)) 
            Slack_LIX_talk.objects.filter(Profile_Link=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=Slack_LIX_talk.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=Slack_LIX_talk.objects.filter(
          
          Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
          
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['ProfileLink','Category','Description','Experience Title','LinkedIn Name','Location']


    page = request.GET.get('page', 1)
    paginator = Paginator(displaytopic, no_display)
    try:
        users = paginator.page(page)
        start_index = users.start_index()
        end_index = users.end_index()
    except PageNotAnInteger:
        users = paginator.page(1)
        start_index = users.start_index()
        end_index = users.end_index()
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
        start_index = users.start_index()
        end_index = users.end_index()

    if 'export_all' in request.POST:
        response =HttpResponse(content_type='text/csv')
        writer=csv.writer(response)
        response['Content-Disposition'] = 'attachment; filename="Slack LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['ProfileLink','Category','Description','Experience Title','LinkedIn Name','Location','Contacted'])
        writedata = displaytopic.values_list('Profile_Link','Category','Description','Experience_Title','LinkedIn_Name','Location','contact')

        write_list=list()
        for row in writedata:   
            if row[6] ==  1:
                write_contact='Yes'
            else:
                write_contact='No'
            wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

            write_list.append(wlist)

            writer.writerow(wlist)

        return response
        msg_display= f"CSV exported successfully! "



    if 'csv_upload' in request.POST:
        msg_display2='Uploaded successfully....'
    elif 'csv_delete' in request.POST:
        msg_display='Deleted successfully....'
    else:
        msg_display=''

    import os
    #Export csv
    if request.GET.get('csv_export'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')
            displaytopic=Slack_LIX_talk.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Slack LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['ProfileLink','Category','Description','Experience Title','LinkedIn Name','Location','Contacted'])
            writedata = displaytopic.values_list('Profile_Link','Category','Description','Experience_Title','LinkedIn_Name','Location','contact')

            write_list=list()
            for row in writedata:   
                if row[6] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "

        elif sear1=='yes':
            query = request.session['query']

            displaytopic1=Slack_LIX_talk.objects.filter(
          
              Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            #cur.execute("SELECT * FROM Slack LIX;")
            
            #displaytopic=Slack_LIX_talk.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Slack LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['ProfileLink','Category','Description','Experience Title','LinkedIn Name','Location','Contacted'])
            writedata = displaytopic1.values_list('Profile_Link','Category','Description','Experience_Title','LinkedIn_Name','Location','contact')
            write_list=list()
            for row in writedata:
                if row[6] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "



        else:
            
            #cur.execute("SELECT * FROM Slack LIX;")
            displaytopic=Slack_LIX_talk.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Slack LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['ProfileLink','Category','Description','Experience Title','LinkedIn Name','Location','Contacted'])
            writedata = displaytopic.values_list('Profile_Link','Category','Description','Experience_Title','LinkedIn_Name','Location','contact')
            write_list=list()
            for row in writedata:
                if row[6] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        del request.session['query']
        del request.session['sear']

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Slack Linkedin (L)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def trello_lix(request):

    #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Trello_LIX_talk.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    Trello_LIX_talk.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=Trello_LIX_talk.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    Trello_LIX_talk.objects.filter(Row_id=ids).update(contact=0)


    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Trello_LIX_talk.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    Trello_LIX_talk.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                Trello_LIX_talk.objects.filter(Row_id=ids).delete()
                # Trello_LIX_talk.objects.all.delete()



    #UPLOAD CSV FILE
    if 'csv_upload' in request.POST:

        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a .csv file.')

        file_data = csv_file.read().decode("utf-8")  
        io_string = io.StringIO(file_data)
        next(io_string) 
        no_rows=0
        no_rows_added=0
        for column in csv.reader(io_string, delimiter=','):
            no_rows+=1
            if not Trello_LIX_talk.objects.filter(Profile_Link=column[0]).exists():
                data_dict = {}
                link_lix=Trello_LIX_talk()
                link_lix.Profile_Link = column[0]
                link_lix.Category=column[1]
                link_lix.Description=column[2]
                link_lix.Experience_Title=column[3]
                link_lix.LinkedIn_Name=column[4]
                link_lix.Location=column[5]
                link_lix.save()
                no_rows_added+=1
        msg_display=f"Uploaded {no_rows_added} rows out of {no_rows} "

    #DELETE

    elif 'csv_delete' in request.POST:
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a .csv file.')

        file_data = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(file_data)
        next(io_string)
        in_db=list()
        for column in csv.reader(io_string, delimiter=','):
            column=' '.join(map(str, column)) 
            Trello_LIX_talk.objects.filter(Profile_Link=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=Trello_LIX_talk.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=Trello_LIX_talk.objects.filter(
          
          Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
          
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['ProfileLink','Category','Description','Experience Title','LinkedIn Name','Location']


    page = request.GET.get('page', 1)
    paginator = Paginator(displaytopic, no_display)
    try:
        users = paginator.page(page)
        start_index = users.start_index()
        end_index = users.end_index()
    except PageNotAnInteger:
        users = paginator.page(1)
        start_index = users.start_index()
        end_index = users.end_index()
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
        start_index = users.start_index()
        end_index = users.end_index()

    if 'export_all' in request.POST:
        response =HttpResponse(content_type='text/csv')
        writer=csv.writer(response)
        response['Content-Disposition'] = 'attachment; filename="Trello LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['ProfileLink','Category','Description','Experience Title','LinkedIn Name','Location','Contacted'])
        writedata = displaytopic.values_list('Profile_Link','Category','Description','Experience_Title','LinkedIn_Name','Location','contact')

        write_list=list()
        for row in writedata:   
            if row[6] ==  1:
                write_contact='Yes'
            else:
                write_contact='No'
            wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

            write_list.append(wlist)

            writer.writerow(wlist)

        return response
        msg_display= f"CSV exported successfully! "



    if 'csv_upload' in request.POST:
        msg_display2='Uploaded successfully....'
    elif 'csv_delete' in request.POST:
        msg_display='Deleted successfully....'
    else:
        msg_display=''

    import os
    #Export csv
    if request.GET.get('csv_export'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')
            displaytopic=Trello_LIX_talk.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Trello LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['ProfileLink','Category','Description','Experience Title','LinkedIn Name','Location','Contacted'])
            writedata = displaytopic.values_list('Profile_Link','Category','Description','Experience_Title','LinkedIn_Name','Location','contact')

            write_list=list()
            for row in writedata:   
                if row[6] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "

        elif sear1=='yes':
            query = request.session['query']

            displaytopic1=Trello_LIX_talk.objects.filter(
          
              Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            #cur.execute("SELECT * FROM Trello LIX;")
            
            #displaytopic=Trello_LIX_talk.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Trello LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['ProfileLink','Category','Description','Experience Title','LinkedIn Name','Location','Contacted'])
            writedata = displaytopic1.values_list('Profile_Link','Category','Description','Experience_Title','LinkedIn_Name','Location','contact')
            write_list=list()
            for row in writedata:
                if row[6] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "



        else:
            
            #cur.execute("SELECT * FROM Trello LIX;")
            displaytopic=Trello_LIX_talk.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Trello LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['ProfileLink','Category','Description','Experience Title','LinkedIn Name','Location','Contacted'])
            writedata = displaytopic.values_list('Profile_Link','Category','Description','Experience_Title','LinkedIn_Name','Location','contact')
            write_list=list()
            for row in writedata:
                if row[6] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        del request.session['query']
        del request.session['sear']

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Trello Linkedin (L)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )



@login_required
def miro_lix(request):

    #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Miro_LIX_talk.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    Miro_LIX_talk.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=Miro_LIX_talk.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    Miro_LIX_talk.objects.filter(Row_id=ids).update(contact=0)


    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Miro_LIX_talk.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    Miro_LIX_talk.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                Miro_LIX_talk.objects.filter(Row_id=ids).delete()



    #UPLOAD CSV FILE
    if 'csv_upload' in request.POST:

        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a .csv file.')

        file_data = csv_file.read().decode("utf-8")  
        io_string = io.StringIO(file_data)
        next(io_string) 
        no_rows=0
        no_rows_added=0
        for column in csv.reader(io_string, delimiter=','):
            no_rows+=1
            if not Miro_LIX_talk.objects.filter(Profile_Link=column[0]).exists():
                data_dict = {}
                link_lix=Miro_LIX_talk()
                link_lix.Profile_Link = column[0]
                link_lix.Category=column[1]
                link_lix.Description=column[2]
                link_lix.Experience_Title=column[3]
                link_lix.LinkedIn_Name=column[4]
                link_lix.Location=column[5]
                link_lix.save()
                no_rows_added+=1
        msg_display=f"Uploaded {no_rows_added} rows out of {no_rows} "

    #DELETE

    elif 'csv_delete' in request.POST:
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a .csv file.')

        file_data = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(file_data)
        next(io_string)
        in_db=list()
        for column in csv.reader(io_string, delimiter=','):
            column=' '.join(map(str, column)) 
            Miro_LIX_talk.objects.filter(Profile_Link=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=Miro_LIX_talk.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=Miro_LIX_talk.objects.filter(
          
          Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
          
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['ProfileLink','Category','Description','Experience Title','LinkedIn Name','Location']


    page = request.GET.get('page', 1)
    paginator = Paginator(displaytopic, no_display)
    try:
        users = paginator.page(page)
        start_index = users.start_index()
        end_index = users.end_index()
    except PageNotAnInteger:
        users = paginator.page(1)
        start_index = users.start_index()
        end_index = users.end_index()
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
        start_index = users.start_index()
        end_index = users.end_index()

    if 'export_all' in request.POST:
        response =HttpResponse(content_type='text/csv')
        writer=csv.writer(response)
        response['Content-Disposition'] = 'attachment; filename="Miro LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['ProfileLink','Category','Description','Experience Title','LinkedIn Name','Location','Contacted'])
        writedata = displaytopic.values_list('Profile_Link','Category','Description','Experience_Title','LinkedIn_Name','Location','contact')

        write_list=list()
        for row in writedata:   
            if row[6] ==  1:
                write_contact='Yes'
            else:
                write_contact='No'
            wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

            write_list.append(wlist)

            writer.writerow(wlist)

        return response
        msg_display= f"CSV exported successfully! "



    if 'csv_upload' in request.POST:
        msg_display2='Uploaded successfully....'
    elif 'csv_delete' in request.POST:
        msg_display='Deleted successfully....'
    else:
        msg_display=''

    import os
    #Export csv
    if request.GET.get('csv_export'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')
            displaytopic=Miro_LIX_talk.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Miro LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['ProfileLink','Category','Description','Experience Title','LinkedIn Name','Location','Contacted'])
            writedata = displaytopic.values_list('Profile_Link','Category','Description','Experience_Title','LinkedIn_Name','Location','contact')

            write_list=list()
            for row in writedata:   
                if row[6] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "

        elif sear1=='yes':
            query = request.session['query']

            displaytopic1=Miro_LIX_talk.objects.filter(
          
              Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            #cur.execute("SELECT * FROM Miro LIX;")
            
            #displaytopic=Miro_LIX_talk.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Miro LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['ProfileLink','Category','Description','Experience Title','LinkedIn Name','Location','Contacted'])
            writedata = displaytopic1.values_list('Profile_Link','Category','Description','Experience_Title','LinkedIn_Name','Location','contact')
            write_list=list()
            for row in writedata:
                if row[6] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "



        else:
            
            #cur.execute("SELECT * FROM Miro LIX;")
            displaytopic=Miro_LIX_talk.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Miro LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['ProfileLink','Category','Description','Experience Title','LinkedIn Name','Location','Contacted'])
            writedata = displaytopic.values_list('Profile_Link','Category','Description','Experience_Title','LinkedIn_Name','Location','contact')
            write_list=list()
            for row in writedata:
                if row[6] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        del request.session['query']
        del request.session['sear']

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Miro LIX','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )



@login_required
def figma_twi(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Figma_twi_talk.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    Figma_twi_talk.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=Figma_twi_talk.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    Figma_twi_talk.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Figma_twi_talk.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    Figma_twi_talk.objects.filter(Row_id=ids).update(contact=2)



    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                Figma_twi_talk.objects.filter(Row_id=ids).delete()




    #UPLOAD CSV FILE
    if 'csv_upload' in request.POST:

        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a .csv file.')

        file_data = csv_file.read().decode("utf-8")  
        io_string = io.StringIO(file_data)
        next(io_string) 
        no_rows=0
        no_rows_added=0
        for column in csv.reader(io_string, delimiter=','):
            no_rows+=1
            if not Figma_twi_talk.objects.filter(Profile_Url=column[0]).exists():
                data_dict = {}
                tw=Figma_twi_talk()
                tw.Profile_Url = column[0]
                tw.Screen_Name=column[1]
                tw.User_Id=column[2]
                tw.Name=column[3]
                tw.Img_Url=column[4]
                tw.Background_Img=column[5]
                tw.Bio=column[6]
                tw.Website=column[7]
                tw.Location=column[8]
                tw.Created_At=column[9]
                tw.Followers_Count=column[10]
                tw.Friends_Count=column[11]
                tw.Tweets_Count=column[12]
                tw.Certified=column[13]
                tw.Following=column[14]
                tw.Followed_By=column[15]
                tw.Query=column[16]
                tw.Timestamp1=column[17]
                tw.save()
                no_rows_added+=1

        msg_display=f"Uploaded {no_rows_added} rows out of {no_rows}"

    #DELETE

    elif 'csv_delete' in request.POST:
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a .csv file.')

        file_data = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(file_data)
        next(io_string)
        in_db=list()
        for column in csv.reader(io_string, delimiter=','):
            column=' '.join(map(str, column))  
            Figma_twi_talk.objects.filter(Profile_Url=column).delete()
            #Figma_twi_talk.objects.all().delete()

        msg_display='Delete successfully...'



    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SET SESSION FOR SORTING
    
    if request.GET.get('ass'):
        request.session['sort'] = 'ass' 
    elif request.GET.get('dec'):
        request.session['sort'] = 'dec'  

    if 'sort' in request.session:
        sort = request.session['sort']
    elif 'no_result' in request.session and 'sort' in request.session:
        sort = request.session['sort']

    else:
        sort = " "




    #SEARCH, DISPLAY AND PAGINATION

        

    if sort == 'ass':
        displaytopic=Figma_twi_talk.objects.all().order_by('Followers_Count')
    elif sort == 'dec':
        displaytopic=Figma_twi_talk.objects.all().order_by('-Followers_Count')
    else:
    
        displaytopic=Figma_twi_talk.objects.all().order_by('Row_id')

   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=Figma_twi_talk.objects.filter(
          
          Q(Profile_Url__icontains=query)|Q(Screen_Name__icontains=query)|Q(User_Id__icontains=query)|Q(Name__icontains=query)|Q(Img_Url__icontains=query)|Q(Background_Img__icontains=query)|Q(Bio__icontains=query)|Q(Website__icontains=query)|Q(Location__icontains=query)|Q(Created_At__icontains=query)|Q(Followers_Count__icontains=query)|Q(Friends_Count__icontains=query)|Q(Tweets_Count__icontains=query)|Q(Certified__icontains=query)|Q(Following__icontains=query)|Q(Followed_By__icontains=query)|Q(Query__icontains=query)|Q(Timestamp1__icontains=query)|Q(Screen_Name__icontains=query)|Q(Screen_Name__icontains=query)
          
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['Profile Url', 'Screen Name','User Id','Name','Img Url','Background Img','Bio','Website','Location','Created At', 'Followers Count','Friends Count','Tweets Count','Certified','Following','Followed By','Query','Timestamp1']
    
    page = request.GET.get('page', 1)
    paginator = Paginator(displaytopic, no_display)
    try:
        users = paginator.page(page)
        start_index = users.start_index()
        end_index = users.end_index()
    except PageNotAnInteger:
        users = paginator.page(1)
        start_index = users.start_index()
        end_index = users.end_index()
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
        start_index = users.start_index()
        end_index = users.end_index()

    if 'export_all' in request.POST:
        response =HttpResponse(content_type='text/csv')
        writer=csv.writer(response)
        response['Content-Disposition'] = 'attachment; filename="twFigma_twi_talkitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['Profile Url', 'Screen Name','User Id','Name','Img Url','Background Img','Bio','Website','Location','Created At', 'Followers Count','Friends Count','Tweets Count','Certified','Following','Followed By','Query','Timestamp1','Contacted'])
        writedata = displaytopic.values_list('Profile_Url', 'Screen_Name','User_Id','Name','Img_Url','Background_Img','Bio','Website','Location','Created_At', 'Followers_Count','Friends_Count','Tweets_Count','Certified','Following','Followed_By','Query','Timestamp1','contact')
        write_list=list()
        for row in writedata:
            if row[18] ==  1:
                write_contact='Yes'
            else:
                write_contact='No'
            wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],write_contact]

            write_list.append(wlist)

            writer.writerow(wlist)
        return response
        msg_display= f"CSV exported successfully! "

    
   
    if 'csv_upload' in request.POST:
        msg_display2='Uploaded successfully....'
    elif 'csv_delete' in request.POST:
        msg_display='Deleted successfully....'
    else:
        msg_display=''

    import os
    #Export csv
    if request.GET.get('csv_export'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')
            displaytopic=Figma_twi_talk.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="twFigma_twi_talkitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile Url', 'Screen Name','User Id','Name','Img Url','Background Img','Bio','Website','Location','Created At', 'Followers Count','Friends Count','Tweets Count','Certified','Following','Followed By','Query','Timestamp1','Contacted'])
            writedata = displaytopic.values_list('Profile_Url', 'Screen_Name','User_Id','Name','Img_Url','Background_Img','Bio','Website','Location','Created_At', 'Followers_Count','Friends_Count','Tweets_Count','Certified','Following','Followed_By','Query','Timestamp1','contact')
            write_list=list()
            for row in writedata:
                if row[18] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        elif sear1=='yes':
            
            
            query = request.session['query']


            displaytopic1=Figma_twi_talk.objects.filter(
          
              Q(Profile_Url__icontains=query)|Q(Screen_Name__icontains=query)|Q(User_Id__icontains=query)|Q(Name__icontains=query)|Q(Img_Url__icontains=query)|Q(Background_Img__icontains=query)|Q(Bio__icontains=query)|Q(Website__icontains=query)|Q(Location__icontains=query)|Q(Created_At__icontains=query)|Q(Followers_Count__icontains=query)|Q(Friends_Count__icontains=query)|Q(Tweets_Count__icontains=query)|Q(Certified__icontains=query)|Q(Following__icontains=query)|Q(Followed_By__icontains=query)|Q(Query__icontains=query)|Q(Timestamp1__icontains=query)|Q(Screen_Name__icontains=query)|Q(Screen_Name__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]

            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile Url', 'Screen Name','User Id','Name','Img Url','Background Img','Bio','Website','Location','Created At', 'Followers Count','Friends Count','Tweets Count','Certified','Following','Followed By','Query','Timestamp1','Contacted'])
            writedata = displaytopic1.values_list('Profile_Url', 'Screen_Name','User_Id','Name','Img_Url','Background_Img','Bio','Website','Location','Created_At', 'Followers_Count','Friends_Count','Tweets_Count','Certified','Following','Followed_By','Query','Timestamp1','contact')
            write_list=list()
            for row in writedata:
                if row[18] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "




        else:
            
            displaytopic=Figma_twi_talk.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile Url', 'Screen Name','User Id','Name','Img Url','Background Img','Bio','Website','Location','Created At', 'Followers Count','Friends Count','Tweets Count','Certified','Following','Followed By','Query','Timestamp1','Contacted'])
            writedata = displaytopic.values_list('Profile_Url', 'Screen_Name','User_Id','Name','Img_Url','Background_Img','Bio','Website','Location','Created_At', 'Followers_Count','Friends_Count','Tweets_Count','Certified','Following','Followed_By','Query','Timestamp1','contact')
            write_list=list()
            for row in writedata:
                if row[18] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "

        del request.session['sort']
        del request.session['query']
        del request.session['sear']
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Figma Twitter','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':sort} )

@login_required
def onalytica_twi(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Onalytica_twi_talk.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    Onalytica_twi_talk.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=Onalytica_twi_talk.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    Onalytica_twi_talk.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Onalytica_twi_talk.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    Onalytica_twi_talk.objects.filter(Row_id=ids).update(contact=2)



    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                Onalytica_twi_talk.objects.filter(Row_id=ids).delete()




    #UPLOAD CSV FILE
    if 'csv_upload' in request.POST:

        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a .csv file.')

        file_data = csv_file.read().decode("utf-8")  
        io_string = io.StringIO(file_data)
        next(io_string) 
        no_rows=0
        no_rows_added=0
        for column in csv.reader(io_string, delimiter=','):
            no_rows+=1
            if not Onalytica_twi_talk.objects.filter(Profile_Url=column[0]).exists():
                data_dict = {}
                tw=Onalytica_twi_talk()
                tw.Profile_Url = column[0]
                tw.Screen_Name=column[1]
                tw.User_Id=column[2]
                tw.Name=column[3]
                tw.Img_Url=column[4]
                tw.Background_Img=column[5]
                tw.Bio=column[6]
                tw.Website=column[7]
                tw.Location=column[8]
                tw.Created_At=column[9]
                tw.Followers_Count=column[10]
                tw.Friends_Count=column[11]
                tw.Tweets_Count=column[12]
                tw.Certified=column[13]
                tw.Following=column[14]
                tw.Followed_By=column[15]
                tw.Query=column[16]
                tw.Timestamp1=column[17]
                tw.save()
                no_rows_added+=1

        msg_display=f"Uploaded {no_rows_added} rows out of {no_rows}"

    #DELETE

    elif 'csv_delete' in request.POST:
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a .csv file.')

        file_data = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(file_data)
        next(io_string)
        in_db=list()
        for column in csv.reader(io_string, delimiter=','):
            column=' '.join(map(str, column))  
            Onalytica_twi_talk.objects.filter(Profile_Url=column).delete()
            #Onalytica_twi_talk.objects.all().delete()

        msg_display='Delete successfully...'



    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SET SESSION FOR SORTING
    
    if request.GET.get('ass'):
        request.session['sort'] = 'ass' 
    elif request.GET.get('dec'):
        request.session['sort'] = 'dec'  

    if 'sort' in request.session:
        sort = request.session['sort']
    elif 'no_result' in request.session and 'sort' in request.session:
        sort = request.session['sort']

    else:
        sort = " "




    #SEARCH, DISPLAY AND PAGINATION

        

    if sort == 'ass':
        displaytopic=Onalytica_twi_talk.objects.all().order_by('Followers_Count')
    elif sort == 'dec':
        displaytopic=Onalytica_twi_talk.objects.all().order_by('-Followers_Count')
    else:
    
        displaytopic=Onalytica_twi_talk.objects.all().order_by('Row_id')

   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=Onalytica_twi_talk.objects.filter(
          
          Q(Profile_Url__icontains=query)|Q(Screen_Name__icontains=query)|Q(User_Id__icontains=query)|Q(Name__icontains=query)|Q(Img_Url__icontains=query)|Q(Background_Img__icontains=query)|Q(Bio__icontains=query)|Q(Website__icontains=query)|Q(Location__icontains=query)|Q(Created_At__icontains=query)|Q(Followers_Count__icontains=query)|Q(Friends_Count__icontains=query)|Q(Tweets_Count__icontains=query)|Q(Certified__icontains=query)|Q(Following__icontains=query)|Q(Followed_By__icontains=query)|Q(Query__icontains=query)|Q(Timestamp1__icontains=query)|Q(Screen_Name__icontains=query)|Q(Screen_Name__icontains=query)
          
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['Profile Url', 'Screen Name','User Id','Name','Img Url','Background Img','Bio','Website','Location','Created At', 'Followers Count','Friends Count','Tweets Count','Certified','Following','Followed By','Query','Timestamp1']
    
    page = request.GET.get('page', 1)
    paginator = Paginator(displaytopic, no_display)
    try:
        users = paginator.page(page)
        start_index = users.start_index()
        end_index = users.end_index()
    except PageNotAnInteger:
        users = paginator.page(1)
        start_index = users.start_index()
        end_index = users.end_index()
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
        start_index = users.start_index()
        end_index = users.end_index()

    if 'export_all' in request.POST:
        response =HttpResponse(content_type='text/csv')
        writer=csv.writer(response)
        response['Content-Disposition'] = 'attachment; filename="twOnalytica_twi_talkitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['Profile Url', 'Screen Name','User Id','Name','Img Url','Background Img','Bio','Website','Location','Created At', 'Followers Count','Friends Count','Tweets Count','Certified','Following','Followed By','Query','Timestamp1','Contacted'])
        writedata = displaytopic.values_list('Profile_Url', 'Screen_Name','User_Id','Name','Img_Url','Background_Img','Bio','Website','Location','Created_At', 'Followers_Count','Friends_Count','Tweets_Count','Certified','Following','Followed_By','Query','Timestamp1','contact')
        write_list=list()
        for row in writedata:
            if row[18] ==  1:
                write_contact='Yes'
            else:
                write_contact='No'
            wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],write_contact]

            write_list.append(wlist)

            writer.writerow(wlist)
        return response
        msg_display= f"CSV exported successfully! "

    
   
    if 'csv_upload' in request.POST:
        msg_display2='Uploaded successfully....'
    elif 'csv_delete' in request.POST:
        msg_display='Deleted successfully....'
    else:
        msg_display=''

    import os
    #Export csv
    if request.GET.get('csv_export'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')
            displaytopic=Onalytica_twi_talk.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="twOnalytica_twi_talkitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile Url', 'Screen Name','User Id','Name','Img Url','Background Img','Bio','Website','Location','Created At', 'Followers Count','Friends Count','Tweets Count','Certified','Following','Followed By','Query','Timestamp1','Contacted'])
            writedata = displaytopic.values_list('Profile_Url', 'Screen_Name','User_Id','Name','Img_Url','Background_Img','Bio','Website','Location','Created_At', 'Followers_Count','Friends_Count','Tweets_Count','Certified','Following','Followed_By','Query','Timestamp1','contact')
            write_list=list()
            for row in writedata:
                if row[18] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        elif sear1=='yes':
            
            
            query = request.session['query']


            displaytopic1=Onalytica_twi_talk.objects.filter(
          
              Q(Profile_Url__icontains=query)|Q(Screen_Name__icontains=query)|Q(User_Id__icontains=query)|Q(Name__icontains=query)|Q(Img_Url__icontains=query)|Q(Background_Img__icontains=query)|Q(Bio__icontains=query)|Q(Website__icontains=query)|Q(Location__icontains=query)|Q(Created_At__icontains=query)|Q(Followers_Count__icontains=query)|Q(Friends_Count__icontains=query)|Q(Tweets_Count__icontains=query)|Q(Certified__icontains=query)|Q(Following__icontains=query)|Q(Followed_By__icontains=query)|Q(Query__icontains=query)|Q(Timestamp1__icontains=query)|Q(Screen_Name__icontains=query)|Q(Screen_Name__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]

            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile Url', 'Screen Name','User Id','Name','Img Url','Background Img','Bio','Website','Location','Created At', 'Followers Count','Friends Count','Tweets Count','Certified','Following','Followed By','Query','Timestamp1','Contacted'])
            writedata = displaytopic1.values_list('Profile_Url', 'Screen_Name','User_Id','Name','Img_Url','Background_Img','Bio','Website','Location','Created_At', 'Followers_Count','Friends_Count','Tweets_Count','Certified','Following','Followed_By','Query','Timestamp1','contact')
            write_list=list()
            for row in writedata:
                if row[18] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "




        else:
            
            displaytopic=Onalytica_twi_talk.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile Url', 'Screen Name','User Id','Name','Img Url','Background Img','Bio','Website','Location','Created At', 'Followers Count','Friends Count','Tweets Count','Certified','Following','Followed By','Query','Timestamp1','Contacted'])
            writedata = displaytopic.values_list('Profile_Url', 'Screen_Name','User_Id','Name','Img_Url','Background_Img','Bio','Website','Location','Created_At', 'Followers_Count','Friends_Count','Tweets_Count','Certified','Following','Followed_By','Query','Timestamp1','contact')
            write_list=list()
            for row in writedata:
                if row[18] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "

        del request.session['sort']
        del request.session['query']
        del request.session['sear']
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Onalytica Twitter','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':sort} )

@login_required
def slack_twi(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Slack_twi_talk.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    Slack_twi_talk.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=Slack_twi_talk.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    Slack_twi_talk.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Slack_twi_talk.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    Slack_twi_talk.objects.filter(Row_id=ids).update(contact=2)



    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                Slack_twi_talk.objects.filter(Row_id=ids).delete()




    #UPLOAD CSV FILE
    if 'csv_upload' in request.POST:

        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a .csv file.')

        file_data = csv_file.read().decode("utf-8")  
        io_string = io.StringIO(file_data)
        next(io_string) 
        no_rows=0
        no_rows_added=0
        for column in csv.reader(io_string, delimiter=','):
            no_rows+=1
            if not Slack_twi_talk.objects.filter(Profile_Url=column[0]).exists():
                data_dict = {}
                tw=Slack_twi_talk()
                tw.Profile_Url = column[0]
                tw.Screen_Name=column[1]
                tw.User_Id=column[2]
                tw.Name=column[3]
                tw.Img_Url=column[4]
                tw.Background_Img=column[5]
                tw.Bio=column[6]
                tw.Website=column[7]
                tw.Location=column[8]
                tw.Created_At=column[9]
                tw.Followers_Count=column[10]
                tw.Friends_Count=column[11]
                tw.Tweets_Count=column[12]
                tw.Certified=column[13]
                tw.Following=column[14]
                tw.Followed_By=column[15]
                tw.Query=column[16]
                tw.Timestamp1=column[17]
                tw.save()
                no_rows_added+=1

        msg_display=f"Uploaded {no_rows_added} rows out of {no_rows}"

    #DELETE

    elif 'csv_delete' in request.POST:
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a .csv file.')

        file_data = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(file_data)
        next(io_string)
        in_db=list()
        for column in csv.reader(io_string, delimiter=','):
            column=' '.join(map(str, column))  
            Slack_twi_talk.objects.filter(Profile_Url=column).delete()
            #Slack_twi_talk.objects.all().delete()

        msg_display='Delete successfully...'



    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SET SESSION FOR SORTING
    
    if request.GET.get('ass'):
        request.session['sort'] = 'ass' 
    elif request.GET.get('dec'):
        request.session['sort'] = 'dec'  

    if 'sort' in request.session:
        sort = request.session['sort']
    elif 'no_result' in request.session and 'sort' in request.session:
        sort = request.session['sort']

    else:
        sort = " "




    #SEARCH, DISPLAY AND PAGINATION

        

    if sort == 'ass':
        displaytopic=Slack_twi_talk.objects.all().order_by('Followers_Count')
    elif sort == 'dec':
        displaytopic=Slack_twi_talk.objects.all().order_by('-Followers_Count')
    else:
    
        displaytopic=Slack_twi_talk.objects.all().order_by('Row_id')

   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=Slack_twi_talk.objects.filter(
          
          Q(Profile_Url__icontains=query)|Q(Screen_Name__icontains=query)|Q(User_Id__icontains=query)|Q(Name__icontains=query)|Q(Img_Url__icontains=query)|Q(Background_Img__icontains=query)|Q(Bio__icontains=query)|Q(Website__icontains=query)|Q(Location__icontains=query)|Q(Created_At__icontains=query)|Q(Followers_Count__icontains=query)|Q(Friends_Count__icontains=query)|Q(Tweets_Count__icontains=query)|Q(Certified__icontains=query)|Q(Following__icontains=query)|Q(Followed_By__icontains=query)|Q(Query__icontains=query)|Q(Timestamp1__icontains=query)|Q(Screen_Name__icontains=query)|Q(Screen_Name__icontains=query)
          
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['Profile Url', 'Screen Name','User Id','Name','Img Url','Background Img','Bio','Website','Location','Created At', 'Followers Count','Friends Count','Tweets Count','Certified','Following','Followed By','Query','Timestamp1']
    
    page = request.GET.get('page', 1)
    paginator = Paginator(displaytopic, no_display)
    try:
        users = paginator.page(page)
        start_index = users.start_index()
        end_index = users.end_index()
    except PageNotAnInteger:
        users = paginator.page(1)
        start_index = users.start_index()
        end_index = users.end_index()
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
        start_index = users.start_index()
        end_index = users.end_index()

    if 'export_all' in request.POST:
        response =HttpResponse(content_type='text/csv')
        writer=csv.writer(response)
        response['Content-Disposition'] = 'attachment; filename="twSlack_twi_talkitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['Profile Url', 'Screen Name','User Id','Name','Img Url','Background Img','Bio','Website','Location','Created At', 'Followers Count','Friends Count','Tweets Count','Certified','Following','Followed By','Query','Timestamp1','Contacted'])
        writedata = displaytopic.values_list('Profile_Url', 'Screen_Name','User_Id','Name','Img_Url','Background_Img','Bio','Website','Location','Created_At', 'Followers_Count','Friends_Count','Tweets_Count','Certified','Following','Followed_By','Query','Timestamp1','contact')
        write_list=list()
        for row in writedata:
            if row[18] ==  1:
                write_contact='Yes'
            else:
                write_contact='No'
            wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],write_contact]

            write_list.append(wlist)

            writer.writerow(wlist)
        return response
        msg_display= f"CSV exported successfully! "

    
   
    if 'csv_upload' in request.POST:
        msg_display2='Uploaded successfully....'
    elif 'csv_delete' in request.POST:
        msg_display='Deleted successfully....'
    else:
        msg_display=''

    import os
    #Export csv
    if request.GET.get('csv_export'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')
            displaytopic=Slack_twi_talk.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="twSlack_twi_talkitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile Url', 'Screen Name','User Id','Name','Img Url','Background Img','Bio','Website','Location','Created At', 'Followers Count','Friends Count','Tweets Count','Certified','Following','Followed By','Query','Timestamp1','Contacted'])
            writedata = displaytopic.values_list('Profile_Url', 'Screen_Name','User_Id','Name','Img_Url','Background_Img','Bio','Website','Location','Created_At', 'Followers_Count','Friends_Count','Tweets_Count','Certified','Following','Followed_By','Query','Timestamp1','contact')
            write_list=list()
            for row in writedata:
                if row[18] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        elif sear1=='yes':
            
            
            query = request.session['query']


            displaytopic1=Slack_twi_talk.objects.filter(
          
              Q(Profile_Url__icontains=query)|Q(Screen_Name__icontains=query)|Q(User_Id__icontains=query)|Q(Name__icontains=query)|Q(Img_Url__icontains=query)|Q(Background_Img__icontains=query)|Q(Bio__icontains=query)|Q(Website__icontains=query)|Q(Location__icontains=query)|Q(Created_At__icontains=query)|Q(Followers_Count__icontains=query)|Q(Friends_Count__icontains=query)|Q(Tweets_Count__icontains=query)|Q(Certified__icontains=query)|Q(Following__icontains=query)|Q(Followed_By__icontains=query)|Q(Query__icontains=query)|Q(Timestamp1__icontains=query)|Q(Screen_Name__icontains=query)|Q(Screen_Name__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]

            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile Url', 'Screen Name','User Id','Name','Img Url','Background Img','Bio','Website','Location','Created At', 'Followers Count','Friends Count','Tweets Count','Certified','Following','Followed By','Query','Timestamp1','Contacted'])
            writedata = displaytopic1.values_list('Profile_Url', 'Screen_Name','User_Id','Name','Img_Url','Background_Img','Bio','Website','Location','Created_At', 'Followers_Count','Friends_Count','Tweets_Count','Certified','Following','Followed_By','Query','Timestamp1','contact')
            write_list=list()
            for row in writedata:
                if row[18] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "




        else:
            
            displaytopic=Slack_twi_talk.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile Url', 'Screen Name','User Id','Name','Img Url','Background Img','Bio','Website','Location','Created At', 'Followers Count','Friends Count','Tweets Count','Certified','Following','Followed By','Query','Timestamp1','Contacted'])
            writedata = displaytopic.values_list('Profile_Url', 'Screen_Name','User_Id','Name','Img_Url','Background_Img','Bio','Website','Location','Created_At', 'Followers_Count','Friends_Count','Tweets_Count','Certified','Following','Followed_By','Query','Timestamp1','contact')
            write_list=list()
            for row in writedata:
                if row[18] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "

        del request.session['sort']
        del request.session['query']
        del request.session['sear']
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Slack Twitter','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':sort} )


@login_required
def trello_twi(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Trello_twi_talk.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    Trello_twi_talk.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=Trello_twi_talk.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    Trello_twi_talk.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Trello_twi_talk.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    Trello_twi_talk.objects.filter(Row_id=ids).update(contact=2)



    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                Trello_twi_talk.objects.filter(Row_id=ids).delete()
                # Trello_twi_talk.objects.all().delete()




    #UPLOAD CSV FILE
    if 'csv_upload' in request.POST:

        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a .csv file.')

        file_data = csv_file.read().decode("utf-8")  
        io_string = io.StringIO(file_data)
        next(io_string) 
        no_rows=0
        no_rows_added=0
        for column in csv.reader(io_string, delimiter=','):
            no_rows+=1
            if not Trello_twi_talk.objects.filter(Profile_Url=column[0]).exists():
                data_dict = {}
                tw=Trello_twi_talk()
                tw.Profile_Url = column[0]
                tw.Screen_Name=column[1]
                tw.User_Id=column[2]
                tw.Name=column[3]
                tw.Img_Url=column[4]
                tw.Background_Img=column[5]
                tw.Bio=column[6]
                tw.Website=column[7]
                tw.Location=column[8]
                tw.Created_At=column[9]
                tw.Followers_Count=column[10]
                tw.Friends_Count=column[11]
                tw.Tweets_Count=column[12]
                tw.Certified=column[13]
                tw.Following=column[14]
                tw.Followed_By=column[15]
                tw.Query=column[16]
                tw.Timestamp1=column[17]
                tw.save()
                no_rows_added+=1

        msg_display=f"Uploaded {no_rows_added} rows out of {no_rows}"

    #DELETE

    elif 'csv_delete' in request.POST:
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a .csv file.')

        file_data = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(file_data)
        next(io_string)
        in_db=list()
        for column in csv.reader(io_string, delimiter=','):
            column=' '.join(map(str, column))  
            Trello_twi_talk.objects.filter(Profile_Url=column).delete()
            #Trello_twi_talk.objects.all().delete()

        msg_display='Delete successfully...'



    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SET SESSION FOR SORTING
    
    if request.GET.get('ass'):
        request.session['sort'] = 'ass' 
    elif request.GET.get('dec'):
        request.session['sort'] = 'dec'  

    if 'sort' in request.session:
        sort = request.session['sort']
    elif 'no_result' in request.session and 'sort' in request.session:
        sort = request.session['sort']

    else:
        sort = " "




    #SEARCH, DISPLAY AND PAGINATION

        

    if sort == 'ass':
        displaytopic=Trello_twi_talk.objects.all().order_by('Followers_Count')
    elif sort == 'dec':
        displaytopic=Trello_twi_talk.objects.all().order_by('-Followers_Count')
    else:
    
        displaytopic=Trello_twi_talk.objects.all().order_by('Row_id')

   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=Trello_twi_talk.objects.filter(
          
          Q(Profile_Url__icontains=query)|Q(Screen_Name__icontains=query)|Q(User_Id__icontains=query)|Q(Name__icontains=query)|Q(Img_Url__icontains=query)|Q(Background_Img__icontains=query)|Q(Bio__icontains=query)|Q(Website__icontains=query)|Q(Location__icontains=query)|Q(Created_At__icontains=query)|Q(Followers_Count__icontains=query)|Q(Friends_Count__icontains=query)|Q(Tweets_Count__icontains=query)|Q(Certified__icontains=query)|Q(Following__icontains=query)|Q(Followed_By__icontains=query)|Q(Query__icontains=query)|Q(Timestamp1__icontains=query)|Q(Screen_Name__icontains=query)|Q(Screen_Name__icontains=query)
          
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['Profile Url', 'Screen Name','User Id','Name','Img Url','Background Img','Bio','Website','Location','Created At', 'Followers Count','Friends Count','Tweets Count','Certified','Following','Followed By','Query','Timestamp1']
    
    page = request.GET.get('page', 1)
    paginator = Paginator(displaytopic, no_display)
    try:
        users = paginator.page(page)
        start_index = users.start_index()
        end_index = users.end_index()
    except PageNotAnInteger:
        users = paginator.page(1)
        start_index = users.start_index()
        end_index = users.end_index()
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
        start_index = users.start_index()
        end_index = users.end_index()

    if 'export_all' in request.POST:
        response =HttpResponse(content_type='text/csv')
        writer=csv.writer(response)
        response['Content-Disposition'] = 'attachment; filename="twTrello_twi_talkitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['Profile Url', 'Screen Name','User Id','Name','Img Url','Background Img','Bio','Website','Location','Created At', 'Followers Count','Friends Count','Tweets Count','Certified','Following','Followed By','Query','Timestamp1','Contacted'])
        writedata = displaytopic.values_list('Profile_Url', 'Screen_Name','User_Id','Name','Img_Url','Background_Img','Bio','Website','Location','Created_At', 'Followers_Count','Friends_Count','Tweets_Count','Certified','Following','Followed_By','Query','Timestamp1','contact')
        write_list=list()
        for row in writedata:
            if row[18] ==  1:
                write_contact='Yes'
            else:
                write_contact='No'
            wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],write_contact]

            write_list.append(wlist)

            writer.writerow(wlist)
        return response
        msg_display= f"CSV exported successfully! "

    
   
    if 'csv_upload' in request.POST:
        msg_display2='Uploaded successfully....'
    elif 'csv_delete' in request.POST:
        msg_display='Deleted successfully....'
    else:
        msg_display=''

    import os
    #Export csv
    if request.GET.get('csv_export'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')
            displaytopic=Trello_twi_talk.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="twTrello_twi_talkitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile Url', 'Screen Name','User Id','Name','Img Url','Background Img','Bio','Website','Location','Created At', 'Followers Count','Friends Count','Tweets Count','Certified','Following','Followed By','Query','Timestamp1','Contacted'])
            writedata = displaytopic.values_list('Profile_Url', 'Screen_Name','User_Id','Name','Img_Url','Background_Img','Bio','Website','Location','Created_At', 'Followers_Count','Friends_Count','Tweets_Count','Certified','Following','Followed_By','Query','Timestamp1','contact')
            write_list=list()
            for row in writedata:
                if row[18] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        elif sear1=='yes':
            
            
            query = request.session['query']


            displaytopic1=Trello_twi_talk.objects.filter(
          
              Q(Profile_Url__icontains=query)|Q(Screen_Name__icontains=query)|Q(User_Id__icontains=query)|Q(Name__icontains=query)|Q(Img_Url__icontains=query)|Q(Background_Img__icontains=query)|Q(Bio__icontains=query)|Q(Website__icontains=query)|Q(Location__icontains=query)|Q(Created_At__icontains=query)|Q(Followers_Count__icontains=query)|Q(Friends_Count__icontains=query)|Q(Tweets_Count__icontains=query)|Q(Certified__icontains=query)|Q(Following__icontains=query)|Q(Followed_By__icontains=query)|Q(Query__icontains=query)|Q(Timestamp1__icontains=query)|Q(Screen_Name__icontains=query)|Q(Screen_Name__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]

            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile Url', 'Screen Name','User Id','Name','Img Url','Background Img','Bio','Website','Location','Created At', 'Followers Count','Friends Count','Tweets Count','Certified','Following','Followed By','Query','Timestamp1','Contacted'])
            writedata = displaytopic1.values_list('Profile_Url', 'Screen_Name','User_Id','Name','Img_Url','Background_Img','Bio','Website','Location','Created_At', 'Followers_Count','Friends_Count','Tweets_Count','Certified','Following','Followed_By','Query','Timestamp1','contact')
            write_list=list()
            for row in writedata:
                if row[18] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "




        else:
            
            displaytopic=Trello_twi_talk.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile Url', 'Screen Name','User Id','Name','Img Url','Background Img','Bio','Website','Location','Created At', 'Followers Count','Friends Count','Tweets Count','Certified','Following','Followed By','Query','Timestamp1','Contacted'])
            writedata = displaytopic.values_list('Profile_Url', 'Screen_Name','User_Id','Name','Img_Url','Background_Img','Bio','Website','Location','Created_At', 'Followers_Count','Friends_Count','Tweets_Count','Certified','Following','Followed_By','Query','Timestamp1','contact')
            write_list=list()
            for row in writedata:
                if row[18] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "

        del request.session['sort']
        del request.session['query']
        del request.session['sear']
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Trello Twitter','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':sort} )


@login_required
def miro_twi(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Miro_twi_talk.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    Miro_twi_talk.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=Miro_twi_talk.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    Miro_twi_talk.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Miro_twi_talk.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    Miro_twi_talk.objects.filter(Row_id=ids).update(contact=2)



    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                Miro_twi_talk.objects.filter(Row_id=ids).delete()




    #UPLOAD CSV FILE
    if 'csv_upload' in request.POST:

        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a .csv file.')

        file_data = csv_file.read().decode("utf-8")  
        io_string = io.StringIO(file_data)
        next(io_string) 
        no_rows=0
        no_rows_added=0
        for column in csv.reader(io_string, delimiter=','):
            no_rows+=1
            if not Miro_twi_talk.objects.filter(Profile_Url=column[0]).exists():
                data_dict = {}
                tw=Miro_twi_talk()
                tw.Profile_Url = column[0]
                tw.Screen_Name=column[1]
                tw.User_Id=column[2]
                tw.Name=column[3]
                tw.Img_Url=column[4]
                tw.Background_Img=column[5]
                tw.Bio=column[6]
                tw.Website=column[7]
                tw.Location=column[8]
                tw.Created_At=column[9]
                tw.Followers_Count=column[10]
                tw.Friends_Count=column[11]
                tw.Tweets_Count=column[12]
                tw.Certified=column[13]
                tw.Following=column[14]
                tw.Followed_By=column[15]
                tw.Query=column[16]
                tw.Timestamp1=column[17]
                tw.save()
                no_rows_added+=1

        msg_display=f"Uploaded {no_rows_added} rows out of {no_rows}"

    #DELETE

    elif 'csv_delete' in request.POST:
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a .csv file.')

        file_data = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(file_data)
        next(io_string)
        in_db=list()
        for column in csv.reader(io_string, delimiter=','):
            column=' '.join(map(str, column))  
            Miro_twi_talk.objects.filter(Profile_Url=column).delete()
            #Miro_twi_talk.objects.all().delete()

        msg_display='Delete successfully...'



    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SET SESSION FOR SORTING
    
    if request.GET.get('ass'):
        request.session['sort'] = 'ass' 
    elif request.GET.get('dec'):
        request.session['sort'] = 'dec'  

    if 'sort' in request.session:
        sort = request.session['sort']
    elif 'no_result' in request.session and 'sort' in request.session:
        sort = request.session['sort']

    else:
        sort = " "




    #SEARCH, DISPLAY AND PAGINATION

        

    if sort == 'ass':
        displaytopic=Miro_twi_talk.objects.all().order_by('Followers_Count')
    elif sort == 'dec':
        displaytopic=Miro_twi_talk.objects.all().order_by('-Followers_Count')
    else:
    
        displaytopic=Miro_twi_talk.objects.all().order_by('Row_id')

   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=Miro_twi_talk.objects.filter(
          
          Q(Profile_Url__icontains=query)|Q(Screen_Name__icontains=query)|Q(User_Id__icontains=query)|Q(Name__icontains=query)|Q(Img_Url__icontains=query)|Q(Background_Img__icontains=query)|Q(Bio__icontains=query)|Q(Website__icontains=query)|Q(Location__icontains=query)|Q(Created_At__icontains=query)|Q(Followers_Count__icontains=query)|Q(Friends_Count__icontains=query)|Q(Tweets_Count__icontains=query)|Q(Certified__icontains=query)|Q(Following__icontains=query)|Q(Followed_By__icontains=query)|Q(Query__icontains=query)|Q(Timestamp1__icontains=query)|Q(Screen_Name__icontains=query)|Q(Screen_Name__icontains=query)
          
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['Profile Url', 'Screen Name','User Id','Name','Img Url','Background Img','Bio','Website','Location','Created At', 'Followers Count','Friends Count','Tweets Count','Certified','Following','Followed By','Query','Timestamp1']
    
    page = request.GET.get('page', 1)
    paginator = Paginator(displaytopic, no_display)
    try:
        users = paginator.page(page)
        start_index = users.start_index()
        end_index = users.end_index()
    except PageNotAnInteger:
        users = paginator.page(1)
        start_index = users.start_index()
        end_index = users.end_index()
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
        start_index = users.start_index()
        end_index = users.end_index()

    if 'export_all' in request.POST:
        response =HttpResponse(content_type='text/csv')
        writer=csv.writer(response)
        response['Content-Disposition'] = 'attachment; filename="miro_twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['Profile Url', 'Screen Name','User Id','Name','Img Url','Background Img','Bio','Website','Location','Created At', 'Followers Count','Friends Count','Tweets Count','Certified','Following','Followed By','Query','Timestamp1','Contacted'])
        writedata = displaytopic.values_list('Profile_Url', 'Screen_Name','User_Id','Name','Img_Url','Background_Img','Bio','Website','Location','Created_At', 'Followers_Count','Friends_Count','Tweets_Count','Certified','Following','Followed_By','Query','Timestamp1','contact')
        write_list=list()
        for row in writedata:
            if row[18] ==  1:
                write_contact='Yes'
            else:
                write_contact='No'
            wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],write_contact]

            write_list.append(wlist)

            writer.writerow(wlist)
        return response
        msg_display= f"CSV exported successfully! "

    
   
    if 'csv_upload' in request.POST:
        msg_display2='Uploaded successfully....'
    elif 'csv_delete' in request.POST:
        msg_display='Deleted successfully....'
    else:
        msg_display=''

    import os
    #Export csv
    if request.GET.get('csv_export'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')
            displaytopic=Miro_twi_talk.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="miro_twitterr_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile Url', 'Screen Name','User Id','Name','Img Url','Background Img','Bio','Website','Location','Created At', 'Followers Count','Friends Count','Tweets Count','Certified','Following','Followed By','Query','Timestamp1','Contacted'])
            writedata = displaytopic.values_list('Profile_Url', 'Screen_Name','User_Id','Name','Img_Url','Background_Img','Bio','Website','Location','Created_At', 'Followers_Count','Friends_Count','Tweets_Count','Certified','Following','Followed_By','Query','Timestamp1','contact')
            write_list=list()
            for row in writedata:
                if row[18] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        elif sear1=='yes':
            
            
            query = request.session['query']


            displaytopic1=Miro_twi_talk.objects.filter(
          
              Q(Profile_Url__icontains=query)|Q(Screen_Name__icontains=query)|Q(User_Id__icontains=query)|Q(Name__icontains=query)|Q(Img_Url__icontains=query)|Q(Background_Img__icontains=query)|Q(Bio__icontains=query)|Q(Website__icontains=query)|Q(Location__icontains=query)|Q(Created_At__icontains=query)|Q(Followers_Count__icontains=query)|Q(Friends_Count__icontains=query)|Q(Tweets_Count__icontains=query)|Q(Certified__icontains=query)|Q(Following__icontains=query)|Q(Followed_By__icontains=query)|Q(Query__icontains=query)|Q(Timestamp1__icontains=query)|Q(Screen_Name__icontains=query)|Q(Screen_Name__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]

            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="miro_twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile Url', 'Screen Name','User Id','Name','Img Url','Background Img','Bio','Website','Location','Created At', 'Followers Count','Friends Count','Tweets Count','Certified','Following','Followed By','Query','Timestamp1','Contacted'])
            writedata = displaytopic1.values_list('Profile_Url', 'Screen_Name','User_Id','Name','Img_Url','Background_Img','Bio','Website','Location','Created_At', 'Followers_Count','Friends_Count','Tweets_Count','Certified','Following','Followed_By','Query','Timestamp1','contact')
            write_list=list()
            for row in writedata:
                if row[18] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "




        else:
            
            displaytopic=Miro_twi_talk.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="miro_twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile Url', 'Screen Name','User Id','Name','Img Url','Background Img','Bio','Website','Location','Created At', 'Followers Count','Friends Count','Tweets Count','Certified','Following','Followed By','Query','Timestamp1','Contacted'])
            writedata = displaytopic.values_list('Profile_Url', 'Screen_Name','User_Id','Name','Img_Url','Background_Img','Bio','Website','Location','Created_At', 'Followers_Count','Friends_Count','Tweets_Count','Certified','Following','Followed_By','Query','Timestamp1','contact')
            write_list=list()
            for row in writedata:
                if row[18] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "

        del request.session['sort']
        del request.session['query']
        del request.session['sear']
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Miro Twitter','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':sort} )



@login_required
def notion_twi(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Notion_twi_talk.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    Notion_twi_talk.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=Notion_twi_talk.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    Notion_twi_talk.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Notion_twi_talk.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    Notion_twi_talk.objects.filter(Row_id=ids).update(contact=2)



    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                Notion_twi_talk.objects.filter(Row_id=ids).delete()




    #UPLOAD CSV FILE
    if 'csv_upload' in request.POST:

        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a .csv file.')

        file_data = csv_file.read().decode("utf-8")  
        io_string = io.StringIO(file_data)
        next(io_string) 
        no_rows=0
        no_rows_added=0
        for column in csv.reader(io_string, delimiter=','):
            no_rows+=1
            if not Notion_twi_talk.objects.filter(Profile_Url=column[0]).exists():
                data_dict = {}
                tw=Notion_twi_talk()
                tw.Profile_Url = column[0]
                tw.Screen_Name=column[1]
                tw.User_Id=column[2]
                tw.Name=column[3]
                tw.Img_Url=column[4]
                tw.Background_Img=column[5]
                tw.Bio=column[6]
                tw.Website=column[7]
                tw.Location=column[8]
                tw.Created_At=column[9]
                tw.Followers_Count=column[10]
                tw.Friends_Count=column[11]
                tw.Tweets_Count=column[12]
                tw.Certified=column[13]
                tw.Following=column[14]
                tw.Followed_By=column[15]
                tw.Query=column[16]
                tw.Timestamp1=column[17]
                tw.save()
                no_rows_added+=1

        msg_display=f"Uploaded {no_rows_added} rows out of {no_rows}"

    #DELETE

    elif 'csv_delete' in request.POST:
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a .csv file.')

        file_data = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(file_data)
        next(io_string)
        in_db=list()
        for column in csv.reader(io_string, delimiter=','):
            column=' '.join(map(str, column))  
            Notion_twi_talk.objects.filter(Profile_Url=column).delete()
            #Notion_twi_talk.objects.all().delete()

        msg_display='Delete successfully...'



    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SET SESSION FOR SORTING
    
    if request.GET.get('ass'):
        request.session['sort'] = 'ass' 
    elif request.GET.get('dec'):
        request.session['sort'] = 'dec'  

    if 'sort' in request.session:
        sort = request.session['sort']
    elif 'no_result' in request.session and 'sort' in request.session:
        sort = request.session['sort']

    else:
        sort = " "




    #SEARCH, DISPLAY AND PAGINATION

        

    if sort == 'ass':
        displaytopic=Notion_twi_talk.objects.all().order_by('Followers_Count')
    elif sort == 'dec':
        displaytopic=Notion_twi_talk.objects.all().order_by('-Followers_Count')
    else:
    
        displaytopic=Notion_twi_talk.objects.all().order_by('Row_id')

   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=Notion_twi_talk.objects.filter(
          
          Q(Profile_Url__icontains=query)|Q(Screen_Name__icontains=query)|Q(User_Id__icontains=query)|Q(Name__icontains=query)|Q(Img_Url__icontains=query)|Q(Background_Img__icontains=query)|Q(Bio__icontains=query)|Q(Website__icontains=query)|Q(Location__icontains=query)|Q(Created_At__icontains=query)|Q(Followers_Count__icontains=query)|Q(Friends_Count__icontains=query)|Q(Tweets_Count__icontains=query)|Q(Certified__icontains=query)|Q(Following__icontains=query)|Q(Followed_By__icontains=query)|Q(Query__icontains=query)|Q(Timestamp1__icontains=query)|Q(Screen_Name__icontains=query)|Q(Screen_Name__icontains=query)
          
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['Profile Url', 'Screen Name','User Id','Name','Img Url','Background Img','Bio','Website','Location','Created At', 'Followers Count','Friends Count','Tweets Count','Certified','Following','Followed By','Query','Timestamp1']
    
    page = request.GET.get('page', 1)
    paginator = Paginator(displaytopic, no_display)
    try:
        users = paginator.page(page)
        start_index = users.start_index()
        end_index = users.end_index()
    except PageNotAnInteger:
        users = paginator.page(1)
        start_index = users.start_index()
        end_index = users.end_index()
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
        start_index = users.start_index()
        end_index = users.end_index()

    if 'export_all' in request.POST:
        response =HttpResponse(content_type='text/csv')
        writer=csv.writer(response)
        response['Content-Disposition'] = 'attachment; filename="notion_twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['Profile Url', 'Screen Name','User Id','Name','Img Url','Background Img','Bio','Website','Location','Created At', 'Followers Count','Friends Count','Tweets Count','Certified','Following','Followed By','Query','Timestamp1','Contacted'])
        writedata = displaytopic.values_list('Profile_Url', 'Screen_Name','User_Id','Name','Img_Url','Background_Img','Bio','Website','Location','Created_At', 'Followers_Count','Friends_Count','Tweets_Count','Certified','Following','Followed_By','Query','Timestamp1','contact')
        write_list=list()
        for row in writedata:
            if row[18] ==  1:
                write_contact='Yes'
            else:
                write_contact='No'
            wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],write_contact]

            write_list.append(wlist)

            writer.writerow(wlist)
        return response
        msg_display= f"CSV exported successfully! "

    
   
    if 'csv_upload' in request.POST:
        msg_display2='Uploaded successfully....'
    elif 'csv_delete' in request.POST:
        msg_display='Deleted successfully....'
    else:
        msg_display=''

    import os
    #Export csv
    if request.GET.get('csv_export'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')
            displaytopic=Notion_twi_talk.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="notion_twitterr_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile Url', 'Screen Name','User Id','Name','Img Url','Background Img','Bio','Website','Location','Created At', 'Followers Count','Friends Count','Tweets Count','Certified','Following','Followed By','Query','Timestamp1','Contacted'])
            writedata = displaytopic.values_list('Profile_Url', 'Screen_Name','User_Id','Name','Img_Url','Background_Img','Bio','Website','Location','Created_At', 'Followers_Count','Friends_Count','Tweets_Count','Certified','Following','Followed_By','Query','Timestamp1','contact')
            write_list=list()
            for row in writedata:
                if row[18] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        elif sear1=='yes':
            
            
            query = request.session['query']


            displaytopic1=Notion_twi_talk.objects.filter(
          
              Q(Profile_Url__icontains=query)|Q(Screen_Name__icontains=query)|Q(User_Id__icontains=query)|Q(Name__icontains=query)|Q(Img_Url__icontains=query)|Q(Background_Img__icontains=query)|Q(Bio__icontains=query)|Q(Website__icontains=query)|Q(Location__icontains=query)|Q(Created_At__icontains=query)|Q(Followers_Count__icontains=query)|Q(Friends_Count__icontains=query)|Q(Tweets_Count__icontains=query)|Q(Certified__icontains=query)|Q(Following__icontains=query)|Q(Followed_By__icontains=query)|Q(Query__icontains=query)|Q(Timestamp1__icontains=query)|Q(Screen_Name__icontains=query)|Q(Screen_Name__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]

            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="notion_twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile Url', 'Screen Name','User Id','Name','Img Url','Background Img','Bio','Website','Location','Created At', 'Followers Count','Friends Count','Tweets Count','Certified','Following','Followed By','Query','Timestamp1','Contacted'])
            writedata = displaytopic1.values_list('Profile_Url', 'Screen_Name','User_Id','Name','Img_Url','Background_Img','Bio','Website','Location','Created_At', 'Followers_Count','Friends_Count','Tweets_Count','Certified','Following','Followed_By','Query','Timestamp1','contact')
            write_list=list()
            for row in writedata:
                if row[18] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "




        else:
            
            displaytopic=Notion_twi_talk.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="notion_twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile Url', 'Screen Name','User Id','Name','Img Url','Background Img','Bio','Website','Location','Created At', 'Followers Count','Friends Count','Tweets Count','Certified','Following','Followed By','Query','Timestamp1','Contacted'])
            writedata = displaytopic.values_list('Profile_Url', 'Screen_Name','User_Id','Name','Img_Url','Background_Img','Bio','Website','Location','Created_At', 'Followers_Count','Friends_Count','Tweets_Count','Certified','Following','Followed_By','Query','Timestamp1','contact')
            write_list=list()
            for row in writedata:
                if row[18] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "

        del request.session['sort']
        del request.session['query']
        del request.session['sear']
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Notion Twitter','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':sort} )



@login_required
def figma_phantom(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Figma_phantom_talk.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    Figma_phantom_talk.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=Figma_phantom_talk.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    Figma_phantom_talk.objects.filter(Row_id=ids).update(contact=0)



    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Figma_phantom_talk.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    Figma_phantom_talk.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                Figma_phantom_talk.objects.filter(Row_id=ids).delete()


    
    #UPLOAD CSV FILE
    if 'csv_upload' in request.POST:

        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a .csv file.')

        file_data = csv_file.read().decode("utf-8")  
        io_string = io.StringIO(file_data)
        next(io_string) 
        no_rows=0
        no_rows_added=0
        for column in csv.reader(io_string, delimiter=','):
            no_rows+=1
            if not Figma_phantom_talk.objects.filter(profileUrl=column[0]).exists():
                data_dict = {}
                link_search=Figma_phantom_talk()
                link_search.profileUrl = column[0]
                link_search.currentJob=column[1]
                link_search.job=column[2]
                link_search.Keyword=column[3]
                link_search.location=column[4]
                link_search.fullName=column[5]
                link_search.save()
                no_rows_added+=1
        msg_display=f"Uploaded {no_rows_added} rows out of {no_rows}"

    #DELETE

    elif 'csv_delete' in request.POST:
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a .csv file.')

        file_data = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(file_data)
        next(io_string)
        in_db=list()
        for column in csv.reader(io_string, delimiter=','):
            column=' '.join(map(str, column))  
            Figma_phantom_talk.objects.filter(profileUrl=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION        
 

    displaytopic=Figma_phantom_talk.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=Figma_phantom_talk.objects.filter(
          
          Q(profileUrl__icontains=query)|Q(currentJob__icontains=query)|Q(job__icontains=query)|Q(Keyword__icontains=query)|Q(location__icontains=query)|Q(fullName__icontains=query)
          
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['Profile URL','CurrentJob','Job','Keyword','Location','Full Name']


    page = request.GET.get('page', 1)
    paginator = Paginator(displaytopic, no_display)
    try:
        users = paginator.page(page)
        start_index = users.start_index()
        end_index = users.end_index()
    except PageNotAnInteger:
        users = paginator.page(1)
        start_index = users.start_index()
        end_index = users.end_index()
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
        start_index = users.start_index()
        end_index = users.end_index()

    if 'export_all' in request.POST:
        response =HttpResponse(content_type='text/csv')
        writer=csv.writer(response)
        response['Content-Disposition'] = 'attachment; filename="Figma Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['Profile URL','CurrentJob','Job','Keyword','Location',
            'Full Name','Contacted'])
        writedata = displaytopic.values_list('profileUrl','currentJob','job','Keyword','location','fullName','contact')
        write_list=list()
        for row in writedata:
            if row[6] ==  1:
                write_contact='Yes'
            else:
                write_contact='No'
            wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

            write_list.append(wlist)

            writer.writerow(wlist)
        return response
        msg_display= f"CSV exported successfully! "



    if 'csv_upload' in request.POST:
        msg_display2='Uploaded successfully....'
    elif 'csv_delete' in request.POST:
        msg_display='Deleted successfully....'
    else:
        msg_display=''

    import os
    #Export csv
    if request.GET.get('csv_export'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')
            displaytopic=Figma_phantom_talk.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Figma Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile URL','CurrentJob','Job','Keyword','Location',
                'Full Name','Contacted'])
            writedata = displaytopic.values_list('profileUrl','currentJob','job','Keyword','location','fullName','contact')
            write_list=list()
            for row in writedata:
                if row[6] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        elif sear1=='yes':

            query = request.session['query']
            displaytopic1=Figma_phantom_talk.objects.filter(
            Q(profileUrl__icontains=query)|Q(currentJob__icontains=query)|Q(job__icontains=query)|Q(Keyword__icontains=query)|Q(location__icontains=query)|Q(fullName__icontains=query)
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]
            


            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Figma Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile URL','CurrentJob','Job','Keyword','Location',
               'Full Name','Contacted'])
            writedata = displaytopic1.values_list('profileUrl','currentJob','job','Keyword','location','fullName','contact')
            write_list=list()
            for row in writedata:
                if row[6] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "

        else:
            
            displaytopic=Figma_phantom_talk.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Figma Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile URL','CurrentJob','Job','Keyword','Location',
                'Full Name','Contacted'])
            writedata = displaytopic.values_list('profileUrl','currentJob','job','Keyword','location','fullName','contact')
            write_list=list()
            for row in writedata:
                if row[6] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "

     
        del request.session['query']
        del request.session['sear']
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Figma Linkedin (P)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )




@login_required
def notion_phantom(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Notion_phantom_talk.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    Notion_phantom_talk.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=Notion_phantom_talk.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    Notion_phantom_talk.objects.filter(Row_id=ids).update(contact=0)



    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Notion_phantom_talk.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    Notion_phantom_talk.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                Notion_phantom_talk.objects.filter(Row_id=ids).delete()


    
    #UPLOAD CSV FILE
    if 'csv_upload' in request.POST:

        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a .csv file.')

        file_data = csv_file.read().decode("utf-8")  
        io_string = io.StringIO(file_data)
        next(io_string) 
        no_rows=0
        no_rows_added=0
        for column in csv.reader(io_string, delimiter=','):
            no_rows+=1
            if not Notion_phantom_talk.objects.filter(profileUrl=column[0]).exists():
                data_dict = {}
                link_search=Notion_phantom_talk()
                link_search.profileUrl = column[0]
                link_search.currentJob=column[1]
                link_search.job=column[2]
                link_search.Keyword=column[3]
                link_search.location=column[4]
                link_search.fullName=column[5]
                link_search.save()
                no_rows_added+=1
        msg_display=f"Uploaded {no_rows_added} rows out of {no_rows}"

    #DELETE

    elif 'csv_delete' in request.POST:
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a .csv file.')

        file_data = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(file_data)
        next(io_string)
        in_db=list()
        for column in csv.reader(io_string, delimiter=','):
            column=' '.join(map(str, column))  
            Notion_phantom_talk.objects.filter(profileUrl=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION        
 

    displaytopic=Notion_phantom_talk.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=Notion_phantom_talk.objects.filter(
          
          Q(profileUrl__icontains=query)|Q(currentJob__icontains=query)|Q(job__icontains=query)|Q(Keyword__icontains=query)|Q(location__icontains=query)|Q(fullName__icontains=query)
          
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['Profile URL','CurrentJob','Job','Keyword','Location','Full Name']


    page = request.GET.get('page', 1)
    paginator = Paginator(displaytopic, no_display)
    try:
        users = paginator.page(page)
        start_index = users.start_index()
        end_index = users.end_index()
    except PageNotAnInteger:
        users = paginator.page(1)
        start_index = users.start_index()
        end_index = users.end_index()
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
        start_index = users.start_index()
        end_index = users.end_index()

    if 'export_all' in request.POST:
        response =HttpResponse(content_type='text/csv')
        writer=csv.writer(response)
        response['Content-Disposition'] = 'attachment; filename="Notion Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['Profile URL','CurrentJob','Job','Keyword','Location',
            'Full Name','Contacted'])
        writedata = displaytopic.values_list('profileUrl','currentJob','job','Keyword','location','fullName','contact')
        write_list=list()
        for row in writedata:
            if row[6] ==  1:
                write_contact='Yes'
            else:
                write_contact='No'
            wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

            write_list.append(wlist)

            writer.writerow(wlist)
        return response
        msg_display= f"CSV exported successfully! "



    if 'csv_upload' in request.POST:
        msg_display2='Uploaded successfully....'
    elif 'csv_delete' in request.POST:
        msg_display='Deleted successfully....'
    else:
        msg_display=''

    import os
    #Export csv
    if request.GET.get('csv_export'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')
            displaytopic=Notion_phantom_talk.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Notion Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile URL','CurrentJob','Job','Keyword','Location',
                'Full Name','Contacted'])
            writedata = displaytopic.values_list('profileUrl','currentJob','job','Keyword','location','fullName','contact')
            write_list=list()
            for row in writedata:
                if row[6] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        elif sear1=='yes':

            query = request.session['query']
            displaytopic1=Notion_phantom_talk.objects.filter(
            Q(profileUrl__icontains=query)|Q(currentJob__icontains=query)|Q(job__icontains=query)|Q(Keyword__icontains=query)|Q(location__icontains=query)|Q(fullName__icontains=query)
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]
            


            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Notion Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile URL','CurrentJob','Job','Keyword','Location',
               'Full Name','Contacted'])
            writedata = displaytopic1.values_list('profileUrl','currentJob','job','Keyword','location','fullName','contact')
            write_list=list()
            for row in writedata:
                if row[6] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "

        else:
            
            displaytopic=Notion_phantom_talk.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Notion Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile URL','CurrentJob','Job','Keyword','Location',
                'Full Name','Contacted'])
            writedata = displaytopic.values_list('profileUrl','currentJob','job','Keyword','location','fullName','contact')
            write_list=list()
            for row in writedata:
                if row[6] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "

     
        del request.session['query']
        del request.session['sear']
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Notion Linkedin (P)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def slack_phantom(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Slack_phantom_talk.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    Slack_phantom_talk.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=Slack_phantom_talk.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    Slack_phantom_talk.objects.filter(Row_id=ids).update(contact=0)



    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Slack_phantom_talk.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    Slack_phantom_talk.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                Slack_phantom_talk.objects.filter(Row_id=ids).delete()


    
    #UPLOAD CSV FILE
    if 'csv_upload' in request.POST:

        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a .csv file.')

        file_data = csv_file.read().decode("utf-8")  
        io_string = io.StringIO(file_data)
        next(io_string) 
        no_rows=0
        no_rows_added=0
        for column in csv.reader(io_string, delimiter=','):
            no_rows+=1
            if not Slack_phantom_talk.objects.filter(profileUrl=column[0]).exists():
                data_dict = {}
                link_search=Slack_phantom_talk()
                link_search.profileUrl = column[0]
                link_search.currentJob=column[1]
                link_search.job=column[2]
                link_search.Keyword=column[3]
                link_search.location=column[4]
                link_search.fullName=column[5]
                link_search.save()
                no_rows_added+=1
        msg_display=f"Uploaded {no_rows_added} rows out of {no_rows}"

    #DELETE

    elif 'csv_delete' in request.POST:
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a .csv file.')

        file_data = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(file_data)
        next(io_string)
        in_db=list()
        for column in csv.reader(io_string, delimiter=','):
            column=' '.join(map(str, column))  
            Slack_phantom_talk.objects.filter(profileUrl=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION        
 

    displaytopic=Slack_phantom_talk.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=Slack_phantom_talk.objects.filter(
          
          Q(profileUrl__icontains=query)|Q(currentJob__icontains=query)|Q(job__icontains=query)|Q(Keyword__icontains=query)|Q(location__icontains=query)|Q(fullName__icontains=query)
          
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['Profile URL','CurrentJob','Job','Keyword','Location','Full Name']


    page = request.GET.get('page', 1)
    paginator = Paginator(displaytopic, no_display)
    try:
        users = paginator.page(page)
        start_index = users.start_index()
        end_index = users.end_index()
    except PageNotAnInteger:
        users = paginator.page(1)
        start_index = users.start_index()
        end_index = users.end_index()
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
        start_index = users.start_index()
        end_index = users.end_index()

    if 'export_all' in request.POST:
        response =HttpResponse(content_type='text/csv')
        writer=csv.writer(response)
        response['Content-Disposition'] = 'attachment; filename="Slack Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['Profile URL','CurrentJob','Job','Keyword','Location',
            'Full Name','Contacted'])
        writedata = displaytopic.values_list('profileUrl','currentJob','job','Keyword','location','fullName','contact')
        write_list=list()
        for row in writedata:
            if row[6] ==  1:
                write_contact='Yes'
            else:
                write_contact='No'
            wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

            write_list.append(wlist)

            writer.writerow(wlist)
        return response
        msg_display= f"CSV exported successfully! "



    if 'csv_upload' in request.POST:
        msg_display2='Uploaded successfully....'
    elif 'csv_delete' in request.POST:
        msg_display='Deleted successfully....'
    else:
        msg_display=''

    import os
    #Export csv
    if request.GET.get('csv_export'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')
            displaytopic=Slack_phantom_talk.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Slack Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile URL','CurrentJob','Job','Keyword','Location',
                'Full Name','Contacted'])
            writedata = displaytopic.values_list('profileUrl','currentJob','job','Keyword','location','fullName','contact')
            write_list=list()
            for row in writedata:
                if row[6] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        elif sear1=='yes':

            query = request.session['query']
            displaytopic1=Slack_phantom_talk.objects.filter(
            Q(profileUrl__icontains=query)|Q(currentJob__icontains=query)|Q(job__icontains=query)|Q(Keyword__icontains=query)|Q(location__icontains=query)|Q(fullName__icontains=query)
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]
            


            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Slack Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile URL','CurrentJob','Job','Keyword','Location',
               'Full Name','Contacted'])
            writedata = displaytopic1.values_list('profileUrl','currentJob','job','Keyword','location','fullName','contact')
            write_list=list()
            for row in writedata:
                if row[6] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "

        else:
            
            displaytopic=Slack_phantom_talk.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Slack Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile URL','CurrentJob','Job','Keyword','Location',
                'Full Name','Contacted'])
            writedata = displaytopic.values_list('profileUrl','currentJob','job','Keyword','location','fullName','contact')
            write_list=list()
            for row in writedata:
                if row[6] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "

     
        del request.session['query']
        del request.session['sear']
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Slack Linkedin (P)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )



@login_required
def trello_phantom(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Trello_phantom_talk.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    Trello_phantom_talk.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=Trello_phantom_talk.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    Trello_phantom_talk.objects.filter(Row_id=ids).update(contact=0)



    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Trello_phantom_talk.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    Trello_phantom_talk.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                Trello_phantom_talk.objects.filter(Row_id=ids).delete()


    
    #UPLOAD CSV FILE
    if 'csv_upload' in request.POST:

        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a .csv file.')

        file_data = csv_file.read().decode("utf-8")  
        io_string = io.StringIO(file_data)
        next(io_string) 
        no_rows=0
        no_rows_added=0
        for column in csv.reader(io_string, delimiter=','):
            no_rows+=1
            if not Trello_phantom_talk.objects.filter(profileUrl=column[0]).exists():
                data_dict = {}
                link_search=Trello_phantom_talk()
                link_search.profileUrl = column[0]
                link_search.currentJob=column[1]
                link_search.job=column[2]
                link_search.Keyword=column[3]
                link_search.location=column[4]
                link_search.fullName=column[5]
                link_search.save()
                no_rows_added+=1
        msg_display=f"Uploaded {no_rows_added} rows out of {no_rows}"

    #DELETE

    elif 'csv_delete' in request.POST:
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a .csv file.')

        file_data = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(file_data)
        next(io_string)
        in_db=list()
        for column in csv.reader(io_string, delimiter=','):
            column=' '.join(map(str, column))  
            Trello_phantom_talk.objects.filter(profileUrl=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION        
 

    displaytopic=Trello_phantom_talk.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=Trello_phantom_talk.objects.filter(
          
          Q(profileUrl__icontains=query)|Q(currentJob__icontains=query)|Q(job__icontains=query)|Q(Keyword__icontains=query)|Q(location__icontains=query)|Q(fullName__icontains=query)
          
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['Profile URL','CurrentJob','Job','Keyword','Location','Full Name']


    page = request.GET.get('page', 1)
    paginator = Paginator(displaytopic, no_display)
    try:
        users = paginator.page(page)
        start_index = users.start_index()
        end_index = users.end_index()
    except PageNotAnInteger:
        users = paginator.page(1)
        start_index = users.start_index()
        end_index = users.end_index()
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
        start_index = users.start_index()
        end_index = users.end_index()

    if 'export_all' in request.POST:
        response =HttpResponse(content_type='text/csv')
        writer=csv.writer(response)
        response['Content-Disposition'] = 'attachment; filename="Trello Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['Profile URL','CurrentJob','Job','Keyword','Location',
            'Full Name','Contacted'])
        writedata = displaytopic.values_list('profileUrl','currentJob','job','Keyword','location','fullName','contact')
        write_list=list()
        for row in writedata:
            if row[6] ==  1:
                write_contact='Yes'
            else:
                write_contact='No'
            wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

            write_list.append(wlist)

            writer.writerow(wlist)
        return response
        msg_display= f"CSV exported successfully! "



    if 'csv_upload' in request.POST:
        msg_display2='Uploaded successfully....'
    elif 'csv_delete' in request.POST:
        msg_display='Deleted successfully....'
    else:
        msg_display=''

    import os
    #Export csv
    if request.GET.get('csv_export'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')
            displaytopic=Trello_phantom_talk.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Trello Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile URL','CurrentJob','Job','Keyword','Location',
                'Full Name','Contacted'])
            writedata = displaytopic.values_list('profileUrl','currentJob','job','Keyword','location','fullName','contact')
            write_list=list()
            for row in writedata:
                if row[6] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        elif sear1=='yes':

            query = request.session['query']
            displaytopic1=Trello_phantom_talk.objects.filter(
            Q(profileUrl__icontains=query)|Q(currentJob__icontains=query)|Q(job__icontains=query)|Q(Keyword__icontains=query)|Q(location__icontains=query)|Q(fullName__icontains=query)
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]
            


            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Trello Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile URL','CurrentJob','Job','Keyword','Location',
               'Full Name','Contacted'])
            writedata = displaytopic1.values_list('profileUrl','currentJob','job','Keyword','location','fullName','contact')
            write_list=list()
            for row in writedata:
                if row[6] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "

        else:
            
            displaytopic=Trello_phantom_talk.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Trello Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile URL','CurrentJob','Job','Keyword','Location',
                'Full Name','Contacted'])
            writedata = displaytopic.values_list('profileUrl','currentJob','job','Keyword','location','fullName','contact')
            write_list=list()
            for row in writedata:
                if row[6] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "

     
        del request.session['query']
        del request.session['sear']
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Trello Linkedin (P)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )





