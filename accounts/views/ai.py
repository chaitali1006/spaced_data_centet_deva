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
from .models import artificial_intelligence_LIX,machine_learning_LIX,algorithm_LIX,data_mining_LIX,neural_network_LIX,data_prediction_LIX,artificial_intelligence_phantom,machine_learning_phantom,algorithm_phantom,data_mining_phantom,neural_network_phantom,data_prediction_phantom,artificial_intelligence_fb,machine_learning_fb,algorithm_fb,data_mining_fb,neural_network_fb,artificial_intelligence_twi,machine_learning_twi,algorithm_twi,data_mining_twi,neural_network_twi,data_prediction_twi,data_analysis_fb

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
def ai_phantom(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=artificial_intelligence_phantom.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    artificial_intelligence_phantom.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=artificial_intelligence_phantom.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    artificial_intelligence_phantom.objects.filter(Row_id=ids).update(contact=0)



    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=artificial_intelligence_phantom.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    artificial_intelligence_phantom.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                artificial_intelligence_phantom.objects.filter(Row_id=ids).delete()
                


    
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
            if not artificial_intelligence_phantom.objects.filter(profileUrl=column[0]).exists():
                data_dict = {}
                link_search=artificial_intelligence_phantom()
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
            artificial_intelligence_phantom.objects.filter(profileUrl=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION        
 

    displaytopic=artificial_intelligence_phantom.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=artificial_intelligence_phantom.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Artificial Intelligence Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=artificial_intelligence_phantom.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Artificial Intelligence Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic1=artificial_intelligence_phantom.objects.filter(
            Q(profileUrl__icontains=query)|Q(currentJob__icontains=query)|Q(job__icontains=query)|Q(Keyword__icontains=query)|Q(location__icontains=query)|Q(fullName__icontains=query)
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]
            


            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Artificial Intelligence Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=artificial_intelligence_phantom.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Artificial Intelligence Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Artificial Intelligence Linkedin (P)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def ml_phantom(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=machine_learning_phantom.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    machine_learning_phantom.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=machine_learning_phantom.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    machine_learning_phantom.objects.filter(Row_id=ids).update(contact=0)



    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=machine_learning_phantom.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    machine_learning_phantom.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                machine_learning_phantom.objects.filter(Row_id=ids).delete()


    
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
            if not machine_learning_phantom.objects.filter(profileUrl=column[0]).exists():
                data_dict = {}
                link_search=machine_learning_phantom()
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
            machine_learning_phantom.objects.filter(profileUrl=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION        
 

    displaytopic=machine_learning_phantom.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=machine_learning_phantom.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Machine Learning Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=machine_learning_phantom.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Machine Learning Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic1=machine_learning_phantom.objects.filter(
            Q(profileUrl__icontains=query)|Q(currentJob__icontains=query)|Q(job__icontains=query)|Q(Keyword__icontains=query)|Q(location__icontains=query)|Q(fullName__icontains=query)
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]
            


            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Machine Learning Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=machine_learning_phantom.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Machine Learning Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Machine Learning Linkedin (P)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def algo_phantom(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=algorithm_phantom.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    algorithm_phantom.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=algorithm_phantom.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    algorithm_phantom.objects.filter(Row_id=ids).update(contact=0)



    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=algorithm_phantom.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    algorithm_phantom.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                algorithm_phantom.objects.filter(Row_id=ids).delete()


    
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
            if not algorithm_phantom.objects.filter(profileUrl=column[0]).exists():
                data_dict = {}
                link_search=algorithm_phantom()
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
            algorithm_phantom.objects.filter(profileUrl=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION        
 

    displaytopic=algorithm_phantom.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=algorithm_phantom.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Algorithms Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=algorithm_phantom.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Algorithms Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic1=algorithm_phantom.objects.filter(
            Q(profileUrl__icontains=query)|Q(currentJob__icontains=query)|Q(job__icontains=query)|Q(Keyword__icontains=query)|Q(location__icontains=query)|Q(fullName__icontains=query)
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]
            


            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Algorithms Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=algorithm_phantom.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Algorithms Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Algorithms Linkedin (P)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def dm_phantom(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=data_mining_phantom.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    data_mining_phantom.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=data_mining_phantom.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    data_mining_phantom.objects.filter(Row_id=ids).update(contact=0)



    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=data_mining_phantom.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    data_mining_phantom.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                data_mining_phantom.objects.filter(Row_id=ids).delete()


    
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
            if not data_mining_phantom.objects.filter(profileUrl=column[0]).exists():
                data_dict = {}
                link_search=data_mining_phantom()
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
            data_mining_phantom.objects.filter(profileUrl=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION        
 

    displaytopic=data_mining_phantom.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=data_mining_phantom.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Data Mining Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=data_mining_phantom.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Data Mining Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic1=data_mining_phantom.objects.filter(
            Q(profileUrl__icontains=query)|Q(currentJob__icontains=query)|Q(job__icontains=query)|Q(Keyword__icontains=query)|Q(location__icontains=query)|Q(fullName__icontains=query)
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]
            


            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Data Mining Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=data_mining_phantom.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Data Mining Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Data Mining Linkedin (P)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def ann_phantom(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=neural_network_phantom.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    neural_network_phantom.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=neural_network_phantom.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    neural_network_phantom.objects.filter(Row_id=ids).update(contact=0)



    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=neural_network_phantom.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    neural_network_phantom.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                neural_network_phantom.objects.filter(Row_id=ids).delete()


    
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
            if not neural_network_phantom.objects.filter(profileUrl=column[0]).exists():
                data_dict = {}
                link_search=neural_network_phantom()
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
            neural_network_phantom.objects.filter(profileUrl=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION        
 

    displaytopic=neural_network_phantom.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=neural_network_phantom.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Neural Networks Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=neural_network_phantom.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Neural Networks Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic1=neural_network_phantom.objects.filter(
            Q(profileUrl__icontains=query)|Q(currentJob__icontains=query)|Q(job__icontains=query)|Q(Keyword__icontains=query)|Q(location__icontains=query)|Q(fullName__icontains=query)
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]
            


            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Neural Networks Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=neural_network_phantom.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Neural Networks Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Neural Networks Linkedin (P)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def dp_phantom(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=data_prediction_phantom.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    data_prediction_phantom.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=data_prediction_phantom.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    data_prediction_phantom.objects.filter(Row_id=ids).update(contact=0)



    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=data_prediction_phantom.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    data_prediction_phantom.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                data_prediction_phantom.objects.filter(Row_id=ids).delete()


    
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
            if not data_prediction_phantom.objects.filter(profileUrl=column[0]).exists():
                data_dict = {}
                link_search=data_prediction_phantom()
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
            data_prediction_phantom.objects.filter(profileUrl=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION        
 

    displaytopic=data_prediction_phantom.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=data_prediction_phantom.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Data Prediction Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=data_prediction_phantom.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Data Prediction Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic1=data_prediction_phantom.objects.filter(
            Q(profileUrl__icontains=query)|Q(currentJob__icontains=query)|Q(job__icontains=query)|Q(Keyword__icontains=query)|Q(location__icontains=query)|Q(fullName__icontains=query)
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]
            


            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Data Prediction Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=data_prediction_phantom.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Data Prediction Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Data Prediction Linkedin (P)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )



@login_required
def ai_lix(request):

    #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=artificial_intelligence_LIX.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    artificial_intelligence_LIX.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=artificial_intelligence_LIX.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    artificial_intelligence_LIX.objects.filter(Row_id=ids).update(contact=0)


    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=artificial_intelligence_LIX.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    artificial_intelligence_LIX.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                artificial_intelligence_LIX.objects.filter(Row_id=ids).delete()



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
            if not artificial_intelligence_LIX.objects.filter(Profile_Link=column[0]).exists():
                data_dict = {}
                link_lix=artificial_intelligence_LIX()
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
            artificial_intelligence_LIX.objects.filter(Profile_Link=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=artificial_intelligence_LIX.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=artificial_intelligence_LIX.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Artificial Intelligence LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=artificial_intelligence_LIX.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Artificial Intelligence LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

            displaytopic1=artificial_intelligence_LIX.objects.filter(
          
              Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            #cur.execute("SELECT * FROM linkedin_lix;")
            
            #displaytopic=Venture_capital_LIX.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Artificial Intelligence LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=artificial_intelligence_LIX.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Artificial Intelligence LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Artificial Intelligence Linkedin (L)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )

@login_required
def ml_lix(request):

    #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=machine_learning_LIX.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    machine_learning_LIX.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=machine_learning_LIX.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    machine_learning_LIX.objects.filter(Row_id=ids).update(contact=0)


    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=machine_learning_LIX.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    machine_learning_LIX.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                machine_learning_LIX.objects.filter(Row_id=ids).delete()



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
            if not machine_learning_LIX.objects.filter(Profile_Link=column[0]).exists():
                data_dict = {}
                link_lix=machine_learning_LIX()
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
            machine_learning_LIX.objects.filter(Profile_Link=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=machine_learning_LIX.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=machine_learning_LIX.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Machine Learning LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=machine_learning_LIX.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Machine Learning LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

            displaytopic1=machine_learning_LIX.objects.filter(
          
              Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            #cur.execute("SELECT * FROM linkedin_lix;")
            
            #displaytopic=Venture_capital_LIX.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Machine Learning LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=machine_learning_LIX.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Machine Learning LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Machine Learning Linkedin (L)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )

@login_required
def algo_lix(request):

    #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=algorithm_LIX.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    algorithm_LIX.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=algorithm_LIX.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    algorithm_LIX.objects.filter(Row_id=ids).update(contact=0)


    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=algorithm_LIX.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    algorithm_LIX.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                algorithm_LIX.objects.filter(Row_id=ids).delete()



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
            if not algorithm_LIX.objects.filter(Profile_Link=column[0]).exists():
                data_dict = {}
                link_lix=algorithm_LIX()
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
            algorithm_LIX.objects.filter(Profile_Link=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=algorithm_LIX.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=algorithm_LIX.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Algorithms LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=algorithm_LIX.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Algorithms LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

            displaytopic1=algorithm_LIX.objects.filter(
          
              Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            #cur.execute("SELECT * FROM linkedin_lix;")
            
            #displaytopic=Venture_capital_LIX.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Algorithms LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=algorithm_LIX.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Algorithms LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Algorithms Linkedin (L)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def dm_lix(request):

    #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=data_mining_LIX.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    data_mining_LIX.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=data_mining_LIX.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    data_mining_LIX.objects.filter(Row_id=ids).update(contact=0)


    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=data_mining_LIX.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    data_mining_LIX.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                data_mining_LIX.objects.filter(Row_id=ids).delete()



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
            if not data_mining_LIX.objects.filter(Profile_Link=column[0]).exists():
                data_dict = {}
                link_lix=data_mining_LIX()
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
            data_mining_LIX.objects.filter(Profile_Link=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=data_mining_LIX.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=data_mining_LIX.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Data Mining LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=data_mining_LIX.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Data Mining LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

            displaytopic1=data_mining_LIX.objects.filter(
          
              Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            #cur.execute("SELECT * FROM linkedin_lix;")
            
            #displaytopic=Venture_capital_LIX.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Data Mining LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=data_mining_LIX.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Data Mining LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Data Mining Linkedin (L)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )

@login_required
def ann_lix(request):

    #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=neural_network_LIX.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    neural_network_LIX.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=neural_network_LIX.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    neural_network_LIX.objects.filter(Row_id=ids).update(contact=0)


    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=neural_network_LIX.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    neural_network_LIX.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                neural_network_LIX.objects.filter(Row_id=ids).delete()



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
            if not neural_network_LIX.objects.filter(Profile_Link=column[0]).exists():
                data_dict = {}
                link_lix=neural_network_LIX()
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
            neural_network_LIX.objects.filter(Profile_Link=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=neural_network_LIX.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=neural_network_LIX.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Neural Networks LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=neural_network_LIX.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Neural Networks LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

            displaytopic1=neural_network_LIX.objects.filter(
          
              Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            #cur.execute("SELECT * FROM linkedin_lix;")
            
            #displaytopic=Venture_capital_LIX.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Neural Networks LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=neural_network_LIX.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Neural Networks LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Neural Networks Linkedin (L)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def dp_lix(request):

    #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=data_prediction_LIX.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    data_prediction_LIX.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=data_prediction_LIX.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    data_prediction_LIX.objects.filter(Row_id=ids).update(contact=0)


    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=data_prediction_LIX.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    data_prediction_LIX.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                data_prediction_LIX.objects.filter(Row_id=ids).delete()



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
            if not data_prediction_LIX.objects.filter(Profile_Link=column[0]).exists():
                data_dict = {}
                link_lix=data_prediction_LIX()
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
            data_prediction_LIX.objects.filter(Profile_Link=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=data_prediction_LIX.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=data_prediction_LIX.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Data Prediction LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=data_prediction_LIX.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Data Prediction LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

            displaytopic1=data_prediction_LIX.objects.filter(
          
              Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            #cur.execute("SELECT * FROM linkedin_lix;")
            
            #displaytopic=Venture_capital_LIX.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Data Prediction LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=data_prediction_LIX.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Data Prediction LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Data Prediction Linkedin (L)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )

@login_required
def ai_fb(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=artificial_intelligence_fb.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    artificial_intelligence_fb.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=artificial_intelligence_fb.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    artificial_intelligence_fb.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
       
            for ids in list_of_input_ids:
                d1=artificial_intelligence_fb.objects.filter(Row_id=ids)
            
                if d1.values_list('contact')[0][0] != 2:
                    artificial_intelligence_fb.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                artificial_intelligence_fb.objects.filter(Row_id=ids).delete()



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
            if not artificial_intelligence_fb.objects.filter(Profile_URL=column[0]).exists():
                data_dict = {}
                fb=artificial_intelligence_fb()
                fb.Profile_URL = column[0]
                fb.Full_Name=column[1]
                fb.First_Name=column[2]
                fb.Last_Name=column[3]
                fb.Education=column[4]
                fb.Category=column[5]
                fb.save()
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
            artificial_intelligence_fb.objects.filter(Profile_URL=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=artificial_intelligence_fb.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=artificial_intelligence_fb.objects.filter(
          
          Q(Profile_URL__icontains=query)|Q(Full_Name__icontains=query)|Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(Education__icontains=query)|Q(Category__icontains=query)
          
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['Profile URL','Full Name','First Name','Last Name','Education','Category']


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
        response['Content-Disposition'] = 'attachment; filename="Artificial Intelligence Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['Profile URL','Full Name','First Name','Last Name','Education','Category','Contacted'])
        writedata = displaytopic.values_list('Profile_URL','Full_Name','First_Name','Last_Name','Education','Category','contact')
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
            displaytopic=artificial_intelligence_fb.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Artificial Intelligence Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile URL','Full Name','First Name','Last Name','Education','Category','Contacted'])
            writedata = displaytopic.values_list('Profile_URL','Full_Name','First_Name','Last_Name','Education','Category','contact')
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

            displaytopic1=artificial_intelligence_fb.objects.filter(
              
              Q(Profile_URL__icontains=query)|Q(Full_Name__icontains=query)|Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(Education__icontains=query)|Q(Category__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            
            #displaytopic=artificial_intelligence_fb.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Artificial Intelligence Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile URL','Full Name','First Name','Last Name','Education','Category','Contacted'])
            writedata = displaytopic1.values_list('Profile_URL','Full_Name','First_Name','Last_Name','Education','Category','contact')
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
            
            displaytopic=artificial_intelligence_fb.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Artificial Intelligence Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile URL','Full Name','First Name','Last Name','Education','Category','Contacted'])
            writedata = displaytopic.values_list('Profile_URL','Full_Name','First_Name','Last_Name','Education','Category','contact')
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Artificial Intelligence Facebook','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def ml_fb(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=machine_learning_fb.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    machine_learning_fb.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=machine_learning_fb.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    machine_learning_fb.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
       
            for ids in list_of_input_ids:
                d1=machine_learning_fb.objects.filter(Row_id=ids)
            
                if d1.values_list('contact')[0][0] != 2:
                    machine_learning_fb.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                machine_learning_fb.objects.filter(Row_id=ids).delete()



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
            if not machine_learning_fb.objects.filter(Profile_URL=column[0]).exists():
                data_dict = {}
                fb=machine_learning_fb()
                fb.Profile_URL = column[0]
                fb.Full_Name=column[1]
                fb.First_Name=column[2]
                fb.Last_Name=column[3]
                fb.Education=column[4]
                fb.Category=column[5]
                fb.save()
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
            machine_learning_fb.objects.filter(Profile_URL=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=machine_learning_fb.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=machine_learning_fb.objects.filter(
          
          Q(Profile_URL__icontains=query)|Q(Full_Name__icontains=query)|Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(Education__icontains=query)|Q(Category__icontains=query)
          
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['Profile URL','Full Name','First Name','Last Name','Education','Category']


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
        response['Content-Disposition'] = 'attachment; filename="Machine Learning Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['Profile URL','Full Name','First Name','Last Name','Education','Category','Contacted'])
        writedata = displaytopic.values_list('Profile_URL','Full_Name','First_Name','Last_Name','Education','Category','contact')
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
            displaytopic=machine_learning_fb.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Machine Learning Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile URL','Full Name','First Name','Last Name','Education','Category','Contacted'])
            writedata = displaytopic.values_list('Profile_URL','Full_Name','First_Name','Last_Name','Education','Category','contact')
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

            displaytopic1=machine_learning_fb.objects.filter(
              
              Q(Profile_URL__icontains=query)|Q(Full_Name__icontains=query)|Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(Education__icontains=query)|Q(Category__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            
            #displaytopic=machine_learning_fb.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Machine Learning Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile URL','Full Name','First Name','Last Name','Education','Category','Contacted'])
            writedata = displaytopic1.values_list('Profile_URL','Full_Name','First_Name','Last_Name','Education','Category','contact')
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
            
            displaytopic=machine_learning_fb.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Machine Learning Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile URL','Full Name','First Name','Last Name','Education','Category','Contacted'])
            writedata = displaytopic.values_list('Profile_URL','Full_Name','First_Name','Last_Name','Education','Category','contact')
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Machine Learning Facebook','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )

@login_required
def algo_fb(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=algorithm_fb.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    algorithm_fb.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=algorithm_fb.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    algorithm_fb.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
       
            for ids in list_of_input_ids:
                d1=algorithm_fb.objects.filter(Row_id=ids)
            
                if d1.values_list('contact')[0][0] != 2:
                    algorithm_fb.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                algorithm_fb.objects.filter(Row_id=ids).delete()



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
            if not algorithm_fb.objects.filter(Profile_URL=column[0]).exists():
                data_dict = {}
                fb=algorithm_fb()
                fb.Profile_URL = column[0]
                fb.Full_Name=column[1]
                fb.First_Name=column[2]
                fb.Last_Name=column[3]
                fb.Education=column[4]
                fb.Category=column[5]
                fb.save()
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
            algorithm_fb.objects.filter(Profile_URL=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=algorithm_fb.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=algorithm_fb.objects.filter(
          
          Q(Profile_URL__icontains=query)|Q(Full_Name__icontains=query)|Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(Education__icontains=query)|Q(Category__icontains=query)
          
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['Profile URL','Full Name','First Name','Last Name','Education','Category']


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
        response['Content-Disposition'] = 'attachment; filename="Algorithms Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['Profile URL','Full Name','First Name','Last Name','Education','Category','Contacted'])
        writedata = displaytopic.values_list('Profile_URL','Full_Name','First_Name','Last_Name','Education','Category','contact')
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
            displaytopic=algorithm_fb.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Algorithms Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile URL','Full Name','First Name','Last Name','Education','Category','Contacted'])
            writedata = displaytopic.values_list('Profile_URL','Full_Name','First_Name','Last_Name','Education','Category','contact')
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

            displaytopic1=algorithm_fb.objects.filter(
              
              Q(Profile_URL__icontains=query)|Q(Full_Name__icontains=query)|Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(Education__icontains=query)|Q(Category__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            
            #displaytopic=algorithm_fb.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Algorithms Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile URL','Full Name','First Name','Last Name','Education','Category','Contacted'])
            writedata = displaytopic1.values_list('Profile_URL','Full_Name','First_Name','Last_Name','Education','Category','contact')
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
            
            displaytopic=algorithm_fb.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Algorithms Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile URL','Full Name','First Name','Last Name','Education','Category','Contacted'])
            writedata = displaytopic.values_list('Profile_URL','Full_Name','First_Name','Last_Name','Education','Category','contact')
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Algorithms Facebook','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def dm_fb(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=data_mining_fb.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    data_mining_fb.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=data_mining_fb.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    data_mining_fb.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
       
            for ids in list_of_input_ids:
                d1=data_mining_fb.objects.filter(Row_id=ids)
            
                if d1.values_list('contact')[0][0] != 2:
                    data_mining_fb.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                data_mining_fb.objects.filter(Row_id=ids).delete()



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
            if not data_mining_fb.objects.filter(Profile_URL=column[0]).exists():
                data_dict = {}
                fb=data_mining_fb()
                fb.Profile_URL = column[0]
                fb.Full_Name=column[1]
                fb.First_Name=column[2]
                fb.Last_Name=column[3]
                fb.Education=column[4]
                fb.Category=column[5]
                fb.save()
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
            data_mining_fb.objects.filter(Profile_URL=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=data_mining_fb.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=data_mining_fb.objects.filter(
          
          Q(Profile_URL__icontains=query)|Q(Full_Name__icontains=query)|Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(Education__icontains=query)|Q(Category__icontains=query)
          
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['Profile URL','Full Name','First Name','Last Name','Education','Category']


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
        response['Content-Disposition'] = 'attachment; filename="Data Mining Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['Profile URL','Full Name','First Name','Last Name','Education','Category','Contacted'])
        writedata = displaytopic.values_list('Profile_URL','Full_Name','First_Name','Last_Name','Education','Category','contact')
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
            displaytopic=data_mining_fb.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Data Mining Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile URL','Full Name','First Name','Last Name','Education','Category','Contacted'])
            writedata = displaytopic.values_list('Profile_URL','Full_Name','First_Name','Last_Name','Education','Category','contact')
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

            displaytopic1=data_mining_fb.objects.filter(
              
              Q(Profile_URL__icontains=query)|Q(Full_Name__icontains=query)|Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(Education__icontains=query)|Q(Category__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            
            #displaytopic=neural_network_fb.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Data Mining Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile URL','Full Name','First Name','Last Name','Education','Category','Contacted'])
            writedata = displaytopic1.values_list('Profile_URL','Full_Name','First_Name','Last_Name','Education','Category','contact')
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
            
            displaytopic=data_mining_fb.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Data Mining Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile URL','Full Name','First Name','Last Name','Education','Category','Contacted'])
            writedata = displaytopic.values_list('Profile_URL','Full_Name','First_Name','Last_Name','Education','Category','contact')
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Data Mining Facebook','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )

@login_required
def ann_fb(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=neural_network_fb.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    neural_network_fb.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=neural_network_fb.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    neural_network_fb.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
       
            for ids in list_of_input_ids:
                d1=neural_network_fb.objects.filter(Row_id=ids)
            
                if d1.values_list('contact')[0][0] != 2:
                    neural_network_fb.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                neural_network_fb.objects.filter(Row_id=ids).delete()



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
            if not neural_network_fb.objects.filter(Profile_URL=column[0]).exists():
                data_dict = {}
                fb=neural_network_fb()
                fb.Profile_URL = column[0]
                fb.Full_Name=column[1]
                fb.First_Name=column[2]
                fb.Last_Name=column[3]
                fb.Education=column[4]
                fb.Category=column[5]
                fb.save()
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
            neural_network_fb.objects.filter(Profile_URL=column).delete()
            #neural_network_fb.objects.all().delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=neural_network_fb.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=neural_network_fb.objects.filter(
          
          Q(Profile_URL__icontains=query)|Q(Full_Name__icontains=query)|Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(Education__icontains=query)|Q(Category__icontains=query)
          
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['Profile URL','Full Name','First Name','Last Name','Education','Category']


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
        response['Content-Disposition'] = 'attachment; filename="Neural Networks Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['Profile URL','Full Name','First Name','Last Name','Education','Category','Contacted'])
        writedata = displaytopic.values_list('Profile_URL','Full_Name','First_Name','Last_Name','Education','Category','contact')
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
            displaytopic=neural_network_fb.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Neural Networks Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile URL','Full Name','First Name','Last Name','Education','Category','Contacted'])
            writedata = displaytopic.values_list('Profile_URL','Full_Name','First_Name','Last_Name','Education','Category','contact')
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

            displaytopic1=neural_network_fb.objects.filter(
              
              Q(Profile_URL__icontains=query)|Q(Full_Name__icontains=query)|Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(Education__icontains=query)|Q(Category__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            
            #displaytopic=data_mining_fb.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Neural Networks Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile URL','Full Name','First Name','Last Name','Education','Category','Contacted'])
            writedata = displaytopic1.values_list('Profile_URL','Full_Name','First_Name','Last_Name','Education','Category','contact')
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
            
            displaytopic=neural_network_fb.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Neural Networks Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile URL','Full Name','First Name','Last Name','Education','Category','Contacted'])
            writedata = displaytopic.values_list('Profile_URL','Full_Name','First_Name','Last_Name','Education','Category','contact')
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Neural Networks Facebook','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )

@login_required
def ai_twi(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=artificial_intelligence_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    artificial_intelligence_twi.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=artificial_intelligence_twi.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    artificial_intelligence_twi.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=artificial_intelligence_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    artificial_intelligence_twi.objects.filter(Row_id=ids).update(contact=2)



    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                artificial_intelligence_twi.objects.filter(Row_id=ids).delete()




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
            if not artificial_intelligence_twi.objects.filter(Profile_Url=column[0]).exists():
                data_dict = {}
                tw=artificial_intelligence_twi()
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
            artificial_intelligence_twi.objects.filter(Profile_Url=column).delete()
            #Private Investor_talk.objects.all().delete()

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
        displaytopic=artificial_intelligence_twi.objects.all().order_by('Followers_Count')
    elif sort == 'dec':
        displaytopic=artificial_intelligence_twi.objects.all().order_by('-Followers_Count')
    else:
    
        displaytopic=artificial_intelligence_twi.objects.all().order_by('Row_id')

   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=artificial_intelligence_twi.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Artificial Intelligence Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=artificial_intelligence_twi.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Artificial Intelligence Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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


            displaytopic1=artificial_intelligence_twi.objects.filter(
          
              Q(Profile_Url__icontains=query)|Q(Screen_Name__icontains=query)|Q(User_Id__icontains=query)|Q(Name__icontains=query)|Q(Img_Url__icontains=query)|Q(Background_Img__icontains=query)|Q(Bio__icontains=query)|Q(Website__icontains=query)|Q(Location__icontains=query)|Q(Created_At__icontains=query)|Q(Followers_Count__icontains=query)|Q(Friends_Count__icontains=query)|Q(Tweets_Count__icontains=query)|Q(Certified__icontains=query)|Q(Following__icontains=query)|Q(Followed_By__icontains=query)|Q(Query__icontains=query)|Q(Timestamp1__icontains=query)|Q(Screen_Name__icontains=query)|Q(Screen_Name__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]

            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Artificial Intelligence Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=artificial_intelligence_twi.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Artificial Intelligence Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Artificial Intelligence Twitter','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':sort} )

@login_required
def ml_twi(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=machine_learning_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    machine_learning_twi.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=machine_learning_twi.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    machine_learning_twi.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=machine_learning_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    machine_learning_twi.objects.filter(Row_id=ids).update(contact=2)



    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                machine_learning_twi.objects.filter(Row_id=ids).delete()




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
            if not machine_learning_twi.objects.filter(Profile_Url=column[0]).exists():
                data_dict = {}
                tw=machine_learning_twi()
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
            machine_learning_twi.objects.filter(Profile_Url=column).delete()
            #Private Investor_talk.objects.all().delete()

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
        displaytopic=machine_learning_twi.objects.all().order_by('Followers_Count')
    elif sort == 'dec':
        displaytopic=machine_learning_twi.objects.all().order_by('-Followers_Count')
    else:
    
        displaytopic=machine_learning_twi.objects.all().order_by('Row_id')

   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=machine_learning_twi.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Machine Learning Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=machine_learning_twi.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Machine Learning Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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


            displaytopic1=machine_learning_twi.objects.filter(
          
              Q(Profile_Url__icontains=query)|Q(Screen_Name__icontains=query)|Q(User_Id__icontains=query)|Q(Name__icontains=query)|Q(Img_Url__icontains=query)|Q(Background_Img__icontains=query)|Q(Bio__icontains=query)|Q(Website__icontains=query)|Q(Location__icontains=query)|Q(Created_At__icontains=query)|Q(Followers_Count__icontains=query)|Q(Friends_Count__icontains=query)|Q(Tweets_Count__icontains=query)|Q(Certified__icontains=query)|Q(Following__icontains=query)|Q(Followed_By__icontains=query)|Q(Query__icontains=query)|Q(Timestamp1__icontains=query)|Q(Screen_Name__icontains=query)|Q(Screen_Name__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]

            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Machine Learning Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=machine_learning_twi.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Machine Learning Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Machine Learning Twitter','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':sort} )

@login_required
def algo_twi(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=algorithm_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    algorithm_twi.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=algorithm_twi.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    algorithm_twi.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=algorithm_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    algorithm_twi.objects.filter(Row_id=ids).update(contact=2)



    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                algorithm_twi.objects.filter(Row_id=ids).delete()




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
            if not algorithm_twi.objects.filter(Profile_Url=column[0]).exists():
                data_dict = {}
                tw=algorithm_twi()
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
            algorithm_twi.objects.filter(Profile_Url=column).delete()
            #Private Investor_talk.objects.all().delete()

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
        displaytopic=algorithm_twi.objects.all().order_by('Followers_Count')
    elif sort == 'dec':
        displaytopic=algorithm_twi.objects.all().order_by('-Followers_Count')
    else:
    
        displaytopic=algorithm_twi.objects.all().order_by('Row_id')

   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=algorithm_twi.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Algorithms_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=algorithm_twi.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Algorithms Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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


            displaytopic1=algorithm_twi.objects.filter(
          
              Q(Profile_Url__icontains=query)|Q(Screen_Name__icontains=query)|Q(User_Id__icontains=query)|Q(Name__icontains=query)|Q(Img_Url__icontains=query)|Q(Background_Img__icontains=query)|Q(Bio__icontains=query)|Q(Website__icontains=query)|Q(Location__icontains=query)|Q(Created_At__icontains=query)|Q(Followers_Count__icontains=query)|Q(Friends_Count__icontains=query)|Q(Tweets_Count__icontains=query)|Q(Certified__icontains=query)|Q(Following__icontains=query)|Q(Followed_By__icontains=query)|Q(Query__icontains=query)|Q(Timestamp1__icontains=query)|Q(Screen_Name__icontains=query)|Q(Screen_Name__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]

            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Algorithms Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=algorithm_twi.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Algorithms Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Algorithms Twitter','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':sort} )


@login_required
def dm_twi(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=data_mining_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    data_mining_twi.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=data_mining_twi.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    data_mining_twi.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=data_mining_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    data_mining_twi.objects.filter(Row_id=ids).update(contact=2)



    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                data_mining_twi.objects.filter(Row_id=ids).delete()




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
            if not data_mining_twi.objects.filter(Profile_Url=column[0]).exists():
                data_dict = {}
                tw=data_mining_twi()
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
            data_mining_twi.objects.filter(Profile_Url=column).delete()
            #Private Investor_talk.objects.all().delete()

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
        displaytopic=data_mining_twi.objects.all().order_by('Followers_Count')
    elif sort == 'dec':
        displaytopic=data_mining_twi.objects.all().order_by('-Followers_Count')
    else:
    
        displaytopic=data_mining_twi.objects.all().order_by('Row_id')

   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=data_mining_twi.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Data Mining Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=data_mining_twi.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Data Mining Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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


            displaytopic1=data_mining_twi.objects.filter(
          
              Q(Profile_Url__icontains=query)|Q(Screen_Name__icontains=query)|Q(User_Id__icontains=query)|Q(Name__icontains=query)|Q(Img_Url__icontains=query)|Q(Background_Img__icontains=query)|Q(Bio__icontains=query)|Q(Website__icontains=query)|Q(Location__icontains=query)|Q(Created_At__icontains=query)|Q(Followers_Count__icontains=query)|Q(Friends_Count__icontains=query)|Q(Tweets_Count__icontains=query)|Q(Certified__icontains=query)|Q(Following__icontains=query)|Q(Followed_By__icontains=query)|Q(Query__icontains=query)|Q(Timestamp1__icontains=query)|Q(Screen_Name__icontains=query)|Q(Screen_Name__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]

            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Data Mining Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=data_mining_twi.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Data Mining Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Data Mining Twitter','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':sort} )


@login_required
def ann_twi(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=neural_network_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    neural_network_twi.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=neural_network_twi.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    neural_network_twi.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=neural_network_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    neural_network_twi.objects.filter(Row_id=ids).update(contact=2)



    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                neural_network_twi.objects.filter(Row_id=ids).delete()




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
            if not neural_network_twi.objects.filter(Profile_Url=column[0]).exists():
                data_dict = {}
                tw=neural_network_twi()
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
            neural_network_twi.objects.filter(Profile_Url=column).delete()
            #Private Investor_talk.objects.all().delete()

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
        displaytopic=neural_network_twi.objects.all().order_by('Followers_Count')
    elif sort == 'dec':
        displaytopic=neural_network_twi.objects.all().order_by('-Followers_Count')
    else:
    
        displaytopic=neural_network_twi.objects.all().order_by('Row_id')

   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=neural_network_twi.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Neural Networks Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=neural_network_twi.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Neural Networks Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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


            displaytopic1=neural_network_twi.objects.filter(
          
              Q(Profile_Url__icontains=query)|Q(Screen_Name__icontains=query)|Q(User_Id__icontains=query)|Q(Name__icontains=query)|Q(Img_Url__icontains=query)|Q(Background_Img__icontains=query)|Q(Bio__icontains=query)|Q(Website__icontains=query)|Q(Location__icontains=query)|Q(Created_At__icontains=query)|Q(Followers_Count__icontains=query)|Q(Friends_Count__icontains=query)|Q(Tweets_Count__icontains=query)|Q(Certified__icontains=query)|Q(Following__icontains=query)|Q(Followed_By__icontains=query)|Q(Query__icontains=query)|Q(Timestamp1__icontains=query)|Q(Screen_Name__icontains=query)|Q(Screen_Name__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]

            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Neural Networks Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=neural_network_twi.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Neural Networks Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Neural Networks Twitter','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':sort} )


@login_required
def dp_twi(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=data_prediction_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    data_prediction_twi.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=data_prediction_twi.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    data_prediction_twi.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=data_prediction_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    data_prediction_twi.objects.filter(Row_id=ids).update(contact=2)



    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                data_prediction_twi.objects.filter(Row_id=ids).delete()




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
            if not data_prediction_twi.objects.filter(Profile_Url=column[0]).exists():
                data_dict = {}
                tw=data_prediction_twi()
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
            data_prediction_twi.objects.filter(Profile_Url=column).delete()
            #Private Investor_talk.objects.all().delete()

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
        displaytopic=data_prediction_twi.objects.all().order_by('Followers_Count')
    elif sort == 'dec':
        displaytopic=data_prediction_twi.objects.all().order_by('-Followers_Count')
    else:
    
        displaytopic=data_prediction_twi.objects.all().order_by('Row_id')

   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=data_prediction_twi.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Data Prediction Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=data_prediction_twi.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Data Prediction Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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


            displaytopic1=data_prediction_twi.objects.filter(
          
              Q(Profile_Url__icontains=query)|Q(Screen_Name__icontains=query)|Q(User_Id__icontains=query)|Q(Name__icontains=query)|Q(Img_Url__icontains=query)|Q(Background_Img__icontains=query)|Q(Bio__icontains=query)|Q(Website__icontains=query)|Q(Location__icontains=query)|Q(Created_At__icontains=query)|Q(Followers_Count__icontains=query)|Q(Friends_Count__icontains=query)|Q(Tweets_Count__icontains=query)|Q(Certified__icontains=query)|Q(Following__icontains=query)|Q(Followed_By__icontains=query)|Q(Query__icontains=query)|Q(Timestamp1__icontains=query)|Q(Screen_Name__icontains=query)|Q(Screen_Name__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]

            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Data Prediction Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=data_prediction_twi.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Data Prediction Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Data Prediction Twitter','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':sort} )



@login_required
def da_fb(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=data_analysis_fb.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    data_analysis_fb.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=data_analysis_fb.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    data_analysis_fb.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
       
            for ids in list_of_input_ids:
                d1=data_analysis_fb.objects.filter(Row_id=ids)
            
                if d1.values_list('contact')[0][0] != 2:
                    data_analysis_fb.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                data_analysis_fb.objects.filter(Row_id=ids).delete()



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
            if not data_analysis_fb.objects.filter(Profile_URL=column[0]).exists():
                data_dict = {}
                fb=data_analysis_fb()
                fb.Profile_URL = column[0]
                fb.Full_Name=column[1]
                fb.First_Name=column[2]
                fb.Last_Name=column[3]
                fb.Education=column[4]
                fb.Category=column[5]
                fb.save()
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
            data_analysis_fb.objects.filter(Profile_URL=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=data_analysis_fb.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=data_analysis_fb.objects.filter(
          
          Q(Profile_URL__icontains=query)|Q(Full_Name__icontains=query)|Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(Education__icontains=query)|Q(Category__icontains=query)
          
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['Profile URL','Full Name','First Name','Last Name','Education','Category']


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
        response['Content-Disposition'] = 'attachment; filename="Data Analysis Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['Profile URL','Full Name','First Name','Last Name','Education','Category','Contacted'])
        writedata = displaytopic.values_list('Profile_URL','Full_Name','First_Name','Last_Name','Education','Category','contact')
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
            displaytopic=data_analysis_fb.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Data Analysis Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile URL','Full Name','First Name','Last Name','Education','Category','Contacted'])
            writedata = displaytopic.values_list('Profile_URL','Full_Name','First_Name','Last_Name','Education','Category','contact')
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

            displaytopic1=data_analysis_fb.objects.filter(
              
              Q(Profile_URL__icontains=query)|Q(Full_Name__icontains=query)|Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(Education__icontains=query)|Q(Category__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            
            #displaytopic=data_analysis_fb.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Data Analysis Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile URL','Full Name','First Name','Last Name','Education','Category','Contacted'])
            writedata = displaytopic1.values_list('Profile_URL','Full_Name','First_Name','Last_Name','Education','Category','contact')
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
            
            displaytopic=data_analysis_fb.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Data Analysis Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile URL','Full Name','First Name','Last Name','Education','Category','Contacted'])
            writedata = displaytopic.values_list('Profile_URL','Full_Name','First_Name','Last_Name','Education','Category','contact')
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Data Analysis Facebook','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )
