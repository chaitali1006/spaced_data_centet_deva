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
from .models import Activation, ceo_spaced, cio_spaced, coo_spaced, cto_spaced, doo_spaced, gom_spaced, hom_spaced, hos_spaced, md_spaced

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
def ceo_lix(request):

    #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=ceo_spaced.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    ceo_spaced.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=ceo_spaced.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    ceo_spaced.objects.filter(Row_id=ids).update(contact=0)


    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=ceo_spaced.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    ceo_spaced.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                ceo_spaced.objects.filter(Row_id=ids).delete()



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
            if not ceo_spaced.objects.filter(Profile_Link=column[0]).exists():
                data_dict = {}
                link_lix=ceo_spaced()
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
            ceo_spaced.objects.filter(Profile_Link=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=ceo_spaced.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=ceo_spaced.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="CEO_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=ceo_spaced.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="CEO_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

            displaytopic1=ceo_spaced.objects.filter(
          
              Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            #cur.execute("SELECT * FROM linkedin_lix;")
            
            #displaytopic=ceo_spaced.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="CEO_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            #cur.execute("SELECT * FROM linkedin_lix;")
            displaytopic=ceo_spaced.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="CEO_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'CEO Linkedin (L)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def cio_lix(request):

    #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=cio_spaced.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    cio_spaced.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=cio_spaced.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    cio_spaced.objects.filter(Row_id=ids).update(contact=0)


    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=cio_spaced.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    cio_spaced.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                cio_spaced.objects.filter(Row_id=ids).delete()



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
            if not cio_spaced.objects.filter(Profile_Link=column[0]).exists():
                data_dict = {}
                link_lix=cio_spaced()
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
            cio_spaced.objects.filter(Profile_Link=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=cio_spaced.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=cio_spaced.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="CIO_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=cio_spaced.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="CIO_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

            displaytopic1=cio_spaced.objects.filter(
          
              Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            #cur.execute("SELECT * FROM linkedin_lix;")
            
            #displaytopic=cio_spaced.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="CIO_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            #cur.execute("SELECT * FROM linkedin_lix;")
            displaytopic=cio_spaced.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="CIO_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'CIO Linkedin (L)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )



@login_required
def coo_lix(request):

    #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=coo_spaced.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    coo_spaced.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=coo_spaced.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    coo_spaced.objects.filter(Row_id=ids).update(contact=0)


    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=coo_spaced.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    coo_spaced.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                coo_spaced.objects.filter(Row_id=ids).delete()



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
            if not coo_spaced.objects.filter(Profile_Link=column[0]).exists():
                data_dict = {}
                link_lix=coo_spaced()
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
            coo_spaced.objects.filter(Profile_Link=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=coo_spaced.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=coo_spaced.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="COO_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=coo_spaced.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="COO_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

            displaytopic1=coo_spaced.objects.filter(
          
              Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            #cur.execute("SELECT * FROM linkedin_lix;")
            
            #displaytopic=coo_spaced.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="COO_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            #cur.execute("SELECT * FROM linkedin_lix;")
            displaytopic=coo_spaced.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="COO_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'COO Linkedin (L)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def cto_lix(request):

    #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=cto_spaced.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    cto_spaced.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=cto_spaced.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    cto_spaced.objects.filter(Row_id=ids).update(contact=0)


    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=cto_spaced.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    cto_spaced.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                cto_spaced.objects.filter(Row_id=ids).delete()



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
            if not cto_spaced.objects.filter(Profile_Link=column[0]).exists():
                data_dict = {}
                link_lix=cto_spaced()
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
            cto_spaced.objects.filter(Profile_Link=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=cto_spaced.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=cto_spaced.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="CTO_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=cto_spaced.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="CTO_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

            displaytopic1=cto_spaced.objects.filter(
          
              Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            #cur.execute("SELECT * FROM linkedin_lix;")
            
            #displaytopic=cto_spaced.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="CTO_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            #cur.execute("SELECT * FROM linkedin_lix;")
            displaytopic=cto_spaced.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="CTO_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'CTO Linkedin (L)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def doo_lix(request):

    #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=doo_spaced.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    doo_spaced.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=doo_spaced.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    doo_spaced.objects.filter(Row_id=ids).update(contact=0)


    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=doo_spaced.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    doo_spaced.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                doo_spaced.objects.filter(Row_id=ids).delete()



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
            if not doo_spaced.objects.filter(Profile_Link=column[0]).exists():
                data_dict = {}
                link_lix=doo_spaced()
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
            doo_spaced.objects.filter(Profile_Link=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=doo_spaced.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=doo_spaced.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Director of Operation_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=doo_spaced.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Director of Operation_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

            displaytopic1=doo_spaced.objects.filter(
          
              Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            #cur.execute("SELECT * FROM linkedin_lix;")
            
            #displaytopic=doo_spaced.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Director of Operation_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            #cur.execute("SELECT * FROM linkedin_lix;")
            displaytopic=doo_spaced.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Director of Operation_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Director of Operation Linkedin (L)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def gom_lix(request):

    #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=gom_spaced.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    gom_spaced.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=gom_spaced.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    gom_spaced.objects.filter(Row_id=ids).update(contact=0)


    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=gom_spaced.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    gom_spaced.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                gom_spaced.objects.filter(Row_id=ids).delete()



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
            if not gom_spaced.objects.filter(Profile_Link=column[0]).exists():
                data_dict = {}
                link_lix=gom_spaced()
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
            gom_spaced.objects.filter(Profile_Link=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=gom_spaced.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=gom_spaced.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Growth of Manager_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=gom_spaced.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Growth of Manager_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

            displaytopic1=gom_spaced.objects.filter(
          
              Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            #cur.execute("SELECT * FROM linkedin_lix;")
            
            #displaytopic=gom_spaced.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Growth of Manager_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            #cur.execute("SELECT * FROM linkedin_lix;")
            displaytopic=gom_spaced.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Growth of Manager_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Growth of Manager Linkedin (L)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )

@login_required
def hom_lix(request):

    #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=hom_spaced.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    hom_spaced.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=hom_spaced.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    hom_spaced.objects.filter(Row_id=ids).update(contact=0)


    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=hom_spaced.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    hom_spaced.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                hom_spaced.objects.filter(Row_id=ids).delete()



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
            if not hom_spaced.objects.filter(Profile_Link=column[0]).exists():
                data_dict = {}
                link_lix=hom_spaced()
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
            hom_spaced.objects.filter(Profile_Link=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=hom_spaced.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=hom_spaced.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Head of Marketing_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=hom_spaced.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Head of Marketing_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

            displaytopic1=hom_spaced.objects.filter(
          
              Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            #cur.execute("SELECT * FROM linkedin_lix;")
            
            #displaytopic=hom_spaced.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Head of Marketing_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            #cur.execute("SELECT * FROM linkedin_lix;")
            displaytopic=hom_spaced.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Head of Marketing_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Head of Marketing Linkedin (L)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )



@login_required
def hos_lix(request):

    #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=hos_spaced.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    hos_spaced.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=hos_spaced.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    hos_spaced.objects.filter(Row_id=ids).update(contact=0)


    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=hos_spaced.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    hos_spaced.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                hos_spaced.objects.filter(Row_id=ids).delete()



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
            if not hos_spaced.objects.filter(Profile_Link=column[0]).exists():
                data_dict = {}
                link_lix=hos_spaced()
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
            hos_spaced.objects.filter(Profile_Link=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=hos_spaced.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=hos_spaced.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Head of Sales_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=hos_spaced.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Head of Sales_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

            displaytopic1=hos_spaced.objects.filter(
          
              Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            #cur.execute("SELECT * FROM linkedin_lix;")
            
            #displaytopic=hos_spaced.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Head of Sales_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            #cur.execute("SELECT * FROM linkedin_lix;")
            displaytopic=hos_spaced.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Head of Sales_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Head of Sales Linkedin (L)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def md_lix(request):

    #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=md_spaced.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    md_spaced.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=md_spaced.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    md_spaced.objects.filter(Row_id=ids).update(contact=0)


    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=md_spaced.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    md_spaced.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                md_spaced.objects.filter(Row_id=ids).delete()



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
            if not md_spaced.objects.filter(Profile_Link=column[0]).exists():
                data_dict = {}
                link_lix=md_spaced()
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
            md_spaced.objects.filter(Profile_Link=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=md_spaced.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=md_spaced.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Marketing Director_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=md_spaced.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Marketing Director_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

            displaytopic1=md_spaced.objects.filter(
          
              Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            #cur.execute("SELECT * FROM linkedin_lix;")
            
            #displaytopic=md_spaced.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Marketing Director_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            #cur.execute("SELECT * FROM linkedin_lix;")
            displaytopic=md_spaced.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Marketing Director_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Marketing Director Linkedin (L)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )
