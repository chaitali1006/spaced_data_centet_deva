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
from .models import CB_LIX_talk_ads,CManag_LIX_talk_ads,CM_LIX_talk_ads,DC_LIX_talk_ads,CB_phantom_talk_ads,CManag_phantom_talk_ads,CM_phantom_talk_ads,DC_phantom_talk_ads,chatbot_twi_talk_ads,CB_twi_talk_ads,CG_twi_talk_ads,CManag_twi_talk_ads,discordbot_twi_talk_ads,twitter_marketing_twi_talk_ads,web3_community_twi_talk_ads,web3_marketing_twi_talk_ads

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
def cb_lix_ads(request):

    #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=CB_LIX_talk_ads.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    CB_LIX_talk_ads.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=CB_LIX_talk_ads.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    CB_LIX_talk_ads.objects.filter(Row_id=ids).update(contact=0)


    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=CB_LIX_talk_ads.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    CB_LIX_talk_ads.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                CB_LIX_talk_ads.objects.filter(Row_id=ids).delete()



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
            if not CB_LIX_talk_ads.objects.filter(Profile_Link=column[3]).exists():
                data_dict = {}
                link_lix=CB_LIX_talk_ads()
                link_lix.First_Name = column[0]
                link_lix.Last_Name=column[1]
                link_lix.Description=column[2]
                link_lix.Profile_Link=column[3]
                link_lix.Email_id=column[4]
                link_lix.Location=column[5]
                link_lix.Category=column[6]
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
            CB_LIX_talk_ads.objects.filter(Profile_Link=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=CB_LIX_talk_ads.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=CB_LIX_talk_ads.objects.filter(
          
          Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(Description__icontains=query)|Q(Profile_Link__icontains=query)|Q(Email_id__icontains=query)|Q(Location__icontains=query)|Q(Category__icontains=query)
          
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['First Name','Last Name','Description','Profile Link','Email ID','Location','Category']

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
        response['Content-Disposition'] = 'attachment; filename="Community Building LIX Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['First Name','Last Name','Description','Profile Link','Email Id','Location','Category','Contacted'])
        writedata = displaytopic.values_list('First_Name','Last_Name','Description','Profile_Link','Email_id','Location','Category','contact')

        write_list=list()
        for row in writedata:   
            if row[7] ==  1:
                write_contact='Yes'
            else:
                write_contact='No'
            wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],write_contact]

            write_list.append(wlist)

            writer.writerow(wlist)

        return response
        msg_display= f"CSV exported successfully! "


    if 'export_all_ads' in request.POST:
        response =HttpResponse(content_type='text/csv')
        writer=csv.writer(response)
        response['Content-Disposition'] = 'attachment; filename="Community Building LIX Ads Format_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['Email Id','First Name','Last Name','Description','Location'])
        writedata = displaytopic.values_list('Email_id','First_Name','Last_Name','Description','Location')

        write_list=list()
        for row in writedata:   
            wlist=[row[0],row[1],row[2],row[3],row[4]]

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
            displaytopic=CB_LIX_talk_ads.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Community Building LIX Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['First Name','Last Name','Description','Profile Link','Email Id','Location','Category','Contacted'])
            writedata = displaytopic.values_list('First_Name','Last_Name','Description','Profile_Link','Email_id','Location','Category','contact')

            write_list=list()
            for row in writedata:   
                if row[7] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "

        elif sear1=='yes':
            query = request.session['query']

            displaytopic1=CB_LIX_talk_ads.objects.filter(
          
              Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(Description__icontains=query)|Q(Profile_Link__icontains=query)|Q(Email_id_icontains=query)|Q(Location_icontains=query)|Q(Category_icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            #cur.execute("SELECT * FROM linkedin_lix;")
            
            #displaytopic=Venture_capital_LIX.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Community Building LIX Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['First Name','Last Name','Description','Profile Link','Email Id','Location','Category','Contacted'])
            writedata = displaytopic1.values_list('First_Name','Last_Name','Description','Profile_Link','Email_id','Location','Category','contact')
            write_list=list()
            for row in writedata:
                if row[7] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "



        else:
            
            #cur.execute("SELECT * FROM linkedin_lix;")
            displaytopic=CB_LIX_talk_ads.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Community Building LIX Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['First Name','Last Name','Description','Profile Link','Email Id','Location','Category','Contacted'])
            writedata = displaytopic.values_list('First_Name','Last_Name','Description','Profile_Link','Email_id','Location','Category','contact')
            write_list=list()
            for row in writedata:
                if row[7] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        del request.session['query']
        del request.session['sear']

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Community Building Linkedin (L) Ads','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def cmanag_lix_ads(request):

    #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=CManag_LIX_talk_ads.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    CManag_LIX_talk_ads.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=CManag_LIX_talk_ads.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    CManag_LIX_talk_ads.objects.filter(Row_id=ids).update(contact=0)


    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=CManag_LIX_talk_ads.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    CManag_LIX_talk_ads.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                CManag_LIX_talk_ads.objects.filter(Row_id=ids).delete()



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
            if not CManag_LIX_talk_ads.objects.filter(Profile_Link=column[3]).exists():
                data_dict = {}
                link_lix=CManag_LIX_talk_ads()
                link_lix.First_Name = column[0]
                link_lix.Last_Name=column[1]
                link_lix.Description=column[2]
                link_lix.Profile_Link=column[3]
                link_lix.Email_id=column[4]
                link_lix.Location=column[5]
                link_lix.Category=column[6]
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
            CManag_LIX_talk_ads.objects.filter(Profile_Link=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=CManag_LIX_talk_ads.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=CManag_LIX_talk_ads.objects.filter(
          
          Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(Description__icontains=query)|Q(Profile_Link__icontains=query)|Q(Email_id__icontains=query)|Q(Location__icontains=query)|Q(Category__icontains=query)
          
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['First Name','Last Name','Description','Profile Link','Email ID','Location','Category']


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
        response['Content-Disposition'] = 'attachment; filename="Community Management LIX Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['First Name','Last Name','Description','Profile Link','Email Id','Location','Category','Contacted'])
        writedata = displaytopic.values_list('First_Name','Last_Name','Description','Profile_Link','Email_id','Location','Category','contact')

        write_list=list()
        for row in writedata:   
            if row[7] ==  1:
                write_contact='Yes'
            else:
                write_contact='No'
            wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],write_contact]

            write_list.append(wlist)

            writer.writerow(wlist)

        return response
        msg_display= f"CSV exported successfully! "


    if 'export_all_ads' in request.POST:
        response =HttpResponse(content_type='text/csv')
        writer=csv.writer(response)
        response['Content-Disposition'] = 'attachment; filename="Community Management LIX Ads Format_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['Email Id','First Name','Last Name','Description','Location'])
        writedata = displaytopic.values_list('Email_id','First_Name','Last_Name','Description','Location')

        write_list=list()
        for row in writedata:   
            wlist=[row[0],row[1],row[2],row[3],row[4]]

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
            displaytopic=CManag_LIX_talk_ads.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Community Management LIX Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['First Name','Last Name','Description','Profile Link','Email Id','Location','Category','Contacted'])
            writedata = displaytopic.values_list('First_Name','Last_Name','Description','Profile_Link','Email_id','Location','Category','contact')

            write_list=list()
            for row in writedata:   
                if row[7] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "

        elif sear1=='yes':
            query = request.session['query']

            displaytopic1=CManag_LIX_talk_ads.objects.filter(
          
              Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(Description__icontains=query)|Q(Profile_Link__icontains=query)|Q(Email_id_icontains=query)|Q(Location_icontains=query)|Q(Category_icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            #cur.execute("SELECT * FROM linkedin_lix;")
            
            #displaytopic=Venture_capital_LIX.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Community Management LIX Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['First Name','Last Name','Description','Profile Link','Email Id','Location','Category','Contacted'])
            writedata = displaytopic1.values_list('First_Name','Last_Name','Description','Profile_Link','Email_id','Location','Category','contact')
            write_list=list()
            for row in writedata:
                if row[7] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "



        else:
            
            #cur.execute("SELECT * FROM linkedin_lix;")
            displaytopic=CManag_LIX_talk_ads.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Community Management LIX Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['First Name','Last Name','Description','Profile Link','Email Id','Location','Category','Contacted'])
            writedata = displaytopic.values_list('First_Name','Last_Name','Description','Profile_Link','Email_id','Location','Category','contact')
            write_list=list()
            for row in writedata:
                if row[7] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        del request.session['query']
        del request.session['sear']

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Community Management Linkedin (L) Ads','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def cm_lix_ads(request):

    #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=CM_LIX_talk_ads.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    CM_LIX_talk_ads.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=CM_LIX_talk_ads.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    CM_LIX_talk_ads.objects.filter(Row_id=ids).update(contact=0)


    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=CM_LIX_talk_ads.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    CM_LIX_talk_ads.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                CM_LIX_talk_ads.objects.filter(Row_id=ids).delete()



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
            if not CM_LIX_talk_ads.objects.filter(Profile_Link=column[3]).exists():
                data_dict = {}
                link_lix=CM_LIX_talk_ads()
                link_lix.First_Name = column[0]
                link_lix.Last_Name=column[1]
                link_lix.Description=column[2]
                link_lix.Profile_Link=column[3]
                link_lix.Email_id=column[4]
                link_lix.Location=column[5]
                link_lix.Category=column[6]
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
            CM_LIX_talk_ads.objects.filter(Profile_Link=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=CM_LIX_talk_ads.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=CM_LIX_talk_ads.objects.filter(
          
          Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(Description__icontains=query)|Q(Profile_Link__icontains=query)|Q(Email_id__icontains=query)|Q(Location__icontains=query)|Q(Category__icontains=query)
          
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['First Name','Last Name','Description','Profile Link','Email ID','Location','Category']


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
        response['Content-Disposition'] = 'attachment; filename="Community Moderator LIX Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['First Name','Last Name','Description','Profile Link','Email Id','Location','Category','Contacted'])
        writedata = displaytopic.values_list('First_Name','Last_Name','Description','Profile_Link','Email_id','Location','Category','contact')

        write_list=list()
        for row in writedata:   
            if row[7] ==  1:
                write_contact='Yes'
            else:
                write_contact='No'
            wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],write_contact]

            write_list.append(wlist)

            writer.writerow(wlist)

        return response
        msg_display= f"CSV exported successfully! "


    if 'export_all_ads' in request.POST:
        response =HttpResponse(content_type='text/csv')
        writer=csv.writer(response)
        response['Content-Disposition'] = 'attachment; filename="Community Moderator LIX Ads Format_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['Email Id','First Name','Last Name','Description','Location'])
        writedata = displaytopic.values_list('Email_id','First_Name','Last_Name','Description','Location')

        write_list=list()
        for row in writedata:   
            wlist=[row[0],row[1],row[2],row[3],row[4]]

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
            displaytopic=CM_LIX_talk_ads.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Community Moderator LIX Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['First Name','Last Name','Description','Profile Link','Email Id','Location','Category','Contacted'])
            writedata = displaytopic.values_list('First_Name','Last_Name','Description','Profile_Link','Email_id','Location','Category','contact')

            write_list=list()
            for row in writedata:   
                if row[7] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "

        elif sear1=='yes':
            query = request.session['query']

            displaytopic1=CM_LIX_talk_ads.objects.filter(
          
              Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(Description__icontains=query)|Q(Profile_Link__icontains=query)|Q(Email_id_icontains=query)|Q(Location_icontains=query)|Q(Category_icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            #cur.execute("SELECT * FROM linkedin_lix;")
            
            #displaytopic=Venture_capital_LIX.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Community Moderator LIX Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['First Name','Last Name','Description','Profile Link','Email Id','Location','Category','Contacted'])
            writedata = displaytopic1.values_list('First_Name','Last_Name','Description','Profile_Link','Email_id','Location','Category','contact')
            write_list=list()
            for row in writedata:
                if row[7] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "



        else:
            
            #cur.execute("SELECT * FROM linkedin_lix;")
            displaytopic=CM_LIX_talk_ads.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Community Moderator LIX Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['First Name','Last Name','Description','Profile Link','Email Id','Location','Category','Contacted'])
            writedata = displaytopic.values_list('First_Name','Last_Name','Description','Profile_Link','Email_id','Location','Category','contact')
            write_list=list()
            for row in writedata:
                if row[7] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        del request.session['query']
        del request.session['sear']

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Community Moderator Linkedin (L) Ads','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )



@login_required
def dc_lix_ads(request):

    #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=DC_LIX_talk_ads.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    DC_LIX_talk_ads.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=DC_LIX_talk_ads.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    DC_LIX_talk_ads.objects.filter(Row_id=ids).update(contact=0)


    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=DC_LIX_talk_ads.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    DC_LIX_talk_ads.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                DC_LIX_talk_ads.objects.filter(Row_id=ids).delete()



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
            if not DC_LIX_talk_ads.objects.filter(Profile_Link=column[3]).exists():
                data_dict = {}
                link_lix=DC_LIX_talk_ads()
                link_lix.First_Name = column[0]
                link_lix.Last_Name=column[1]
                link_lix.Description=column[2]
                link_lix.Profile_Link=column[3]
                link_lix.Email_id=column[4]
                link_lix.Location=column[5]
                link_lix.Category=column[6]
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
            DC_LIX_talk_ads.objects.filter(Profile_Link=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=DC_LIX_talk_ads.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=DC_LIX_talk_ads.objects.filter(
          
          Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(Description__icontains=query)|Q(Profile_Link__icontains=query)|Q(Email_id__icontains=query)|Q(Location__icontains=query)|Q(Category__icontains=query)
          
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['First Name','Last Name','Description','Profile Link','Email ID','Location','Category']


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
        response['Content-Disposition'] = 'attachment; filename="Discord Community LIX Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['First Name','Last Name','Description','Profile Link','Email Id','Location','Category','Contacted'])
        writedata = displaytopic.values_list('First_Name','Last_Name','Description','Profile_Link','Email_id','Location','Category','contact')

        write_list=list()
        for row in writedata:   
            if row[7] ==  1:
                write_contact='Yes'
            else:
                write_contact='No'
            wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],write_contact]

            write_list.append(wlist)

            writer.writerow(wlist)

        return response
        msg_display= f"CSV exported successfully! "



    if 'export_all_ads' in request.POST:
        response =HttpResponse(content_type='text/csv')
        writer=csv.writer(response)
        response['Content-Disposition'] = 'attachment; filename="Discord Community LIX Ads Format_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['Email Id','First Name','Last Name','Description','Location'])
        writedata = displaytopic.values_list('Email_id','First_Name','Last_Name','Description','Location')

        write_list=list()
        for row in writedata:   
            wlist=[row[0],row[1],row[2],row[3],row[4]]

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
            displaytopic=DC_LIX_talk_ads.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Discord Community LIX Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['First Name','Last Name','Description','Profile Link','Email Id','Location','Category','Contacted'])
            writedata = displaytopic.values_list('First_Name','Last_Name','Description','Profile_Link','Email_id','Location','Category','contact')

            write_list=list()
            for row in writedata:   
                if row[7] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "

        elif sear1=='yes':
            query = request.session['query']

            displaytopic1=DC_LIX_talk_ads.objects.filter(
          
              Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(Description__icontains=query)|Q(Profile_Link__icontains=query)|Q(Email_id_icontains=query)|Q(Location_icontains=query)|Q(Category_icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            #cur.execute("SELECT * FROM linkedin_lix;")
            
            #displaytopic=Venture_capital_LIX.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Discord Community LIX Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['First Name','Last Name','Description','Profile Link','Email Id','Location','Category','Contacted'])
            writedata = displaytopic1.values_list('First_Name','Last_Name','Description','Profile_Link','Email_id','Location','Category','contact')
            write_list=list()
            for row in writedata:
                if row[7] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "



        else:
            
            #cur.execute("SELECT * FROM linkedin_lix;")
            displaytopic=DC_LIX_talk_ads.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Discord Community LIX Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['First Name','Last Name','Description','Profile Link','Email Id','Location','Category','Contacted'])
            writedata = displaytopic.values_list('First_Name','Last_Name','Description','Profile_Link','Email_id','Location','Category','contact')
            write_list=list()
            for row in writedata:
                if row[7] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        del request.session['query']
        del request.session['sear']

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Discord Community Linkedin (L) Ads','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )

    

@login_required
def cb_phantom_ads(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=CB_phantom_talk_ads.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    CB_phantom_talk_ads.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=CB_phantom_talk_ads.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    CB_phantom_talk_ads.objects.filter(Row_id=ids).update(contact=0)



    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=CB_phantom_talk_ads.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    CB_phantom_talk_ads.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                CB_phantom_talk_ads.objects.filter(Row_id=ids).delete()
                


    
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
            if not CB_phantom_talk_ads.objects.filter(profileUrl=column[3]).exists():
                data_dict = {}
                link_search=CB_phantom_talk_ads()
                link_search.First_Name = column[0]
                link_search.Last_Name=column[1]
                link_search.currentJob=column[2]
                link_search.profileUrl=column[3]
                link_search.Category=column[4]
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
            CB_phantom_talk_ads.objects.filter(profileUrl=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION        
 

    displaytopic=CB_phantom_talk_ads.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=CB_phantom_talk_ads.objects.filter(
          
          Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(currentJob__icontains=query)|Q(profileUrl__icontains=query)|Q(Category__icontains=query)
          
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['First Name','Last Name','CurrentJob','Profile URL','Category']


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
        response['Content-Disposition'] = 'attachment; filename="Community Building Phantombuster Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['First Name','Last Name','CurrentJob','Profile URL','Category','Contacted'])
        writedata = displaytopic.values_list('First_Name','Last_Name','currentJob','profileUrl','Category','contact')
        write_list=list()
        for row in writedata:
            if row[5] ==  1:
                write_contact='Yes'
            else:
                write_contact='No'
            wlist=[row[0],row[1],row[2],row[3],row[4],write_contact]

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
            displaytopic=CB_phantom_talk_ads.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Community Building Phantombuster Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['First Name','Last Name','CurrentJob','Profile URL','Category','Contacted'])
            writedata = displaytopic.values_list('First_Name','Last_Name','currentJob','profileUrl','Category','contact')
            write_list=list()
            for row in writedata:
                if row[5] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        elif sear1=='yes':

            query = request.session['query']
            displaytopic1=CB_phantom_talk_ads.objects.filter(
            Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(currentJob__icontains=query)|Q(profileUrl__icontains=query)|Q(Category__icontains=query)
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]
            


            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Community Building Phantombuster Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['First Name','Last Name','CurrentJob','Profile URL','Category','Contacted'])
            writedata = displaytopic1.values_list('First_Name','Last_Name','currentJob','profileUrl','Category','contact')
            write_list=list()
            for row in writedata:
                if row[5] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "

        else:
            
            displaytopic=CB_phantom_talk_ads.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Community Building Phantombuster Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['First Name','Last Name','CurrentJob','Profile URL','Category','Contacted'])
            writedata = displaytopic.values_list('First_Name','Last_Name','currentJob','profileUrl','Category','contact')
            write_list=list()
            for row in writedata:
                if row[5] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "

     
        del request.session['query']
        del request.session['sear']
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Community Building Linkedin (P) Ads','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def cmanag_phantom_ads(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=CManag_phantom_talk_ads.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    CManag_phantom_talk_ads.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=CManag_phantom_talk_ads.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    CManag_phantom_talk_ads.objects.filter(Row_id=ids).update(contact=0)



    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=CManag_phantom_talk_ads.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    CManag_phantom_talk_ads.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                CManag_phantom_talk_ads.objects.filter(Row_id=ids).delete()


    
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
            if not CManag_phantom_talk_ads.objects.filter(profileUrl=column[3]).exists():
                data_dict = {}
                link_search=CManag_phantom_talk_ads()
                link_search.First_Name = column[0]
                link_search.Last_Name=column[1]
                link_search.currentJob=column[2]
                link_search.profileUrl=column[3]
                link_search.Category=column[4]
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
            CManag_phantom_talk_ads.objects.filter(profileUrl=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION        
 

    displaytopic=CManag_phantom_talk_ads.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=CManag_phantom_talk_ads.objects.filter(
          
          Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(currentJob__icontains=query)|Q(profileUrl__icontains=query)|Q(Category__icontains=query)
          
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['First Name','Last Name','CurrentJob','Profile URL','Category']


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
        response['Content-Disposition'] = 'attachment; filename="Community Management Phantombuster Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['First Name','Last Name','CurrentJob','Profile URL','Category','Contacted'])
        writedata = displaytopic.values_list('First_Name','Last_Name','currentJob','profileUrl','Category','contact')
        write_list=list()
        for row in writedata:
            if row[5] ==  1:
                write_contact='Yes'
            else:
                write_contact='No'
            wlist=[row[0],row[1],row[2],row[3],row[4],write_contact]

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
            displaytopic=CManag_phantom_talk_ads.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Community Management Phantombuster Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['First Name','Last Name','CurrentJob','Profile URL','Category','Contacted'])
            writedata = displaytopic.values_list('First_Name','Last_Name','currentJob','profileUrl','Category','contact')
            write_list=list()
            for row in writedata:
                if row[5] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        elif sear1=='yes':

            query = request.session['query']
            displaytopic1=CManag_phantom_talk_ads.objects.filter(
            Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(currentJob__icontains=query)|Q(profileUrl__icontains=query)|Q(Category__icontains=query)
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]
            


            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Community Management Phantombuster Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['First Name','Last Name','CurrentJob','Profile URL','Category','Contacted'])
            writedata = displaytopic1.values_list('First_Name','Last_Name','currentJob','profileUrl','Category','contact')
            write_list=list()
            for row in writedata:
                if row[5] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "

        else:
            
            displaytopic=CManag_phantom_talk_ads.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Community Management Phantombuster Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['First Name','Last Name','CurrentJob','Profile URL','Category','Contacted'])
            writedata = displaytopic.values_list('First_Name','Last_Name','currentJob','profileUrl','Category','contact')
            write_list=list()
            for row in writedata:
                if row[5] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "

     
        del request.session['query']
        del request.session['sear']
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Community Management Linkedin (P) Ads','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def cm_phantom_ads(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=CM_phantom_talk_ads.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    CM_phantom_talk_ads.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=CM_phantom_talk_ads.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    CM_phantom_talk_ads.objects.filter(Row_id=ids).update(contact=0)



    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=CM_phantom_talk_ads.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    CM_phantom_talk_ads.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                CM_phantom_talk_ads.objects.filter(Row_id=ids).delete()


    
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
            if not CM_phantom_talk_ads.objects.filter(profileUrl=column[3]).exists():
                data_dict = {}
                link_search=CM_phantom_talk_ads()
                link_search.First_Name = column[0]
                link_search.Last_Name=column[1]
                link_search.currentJob=column[2]
                link_search.profileUrl=column[3]
                link_search.Category=column[4]
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
            CM_phantom_talk_ads.objects.filter(profileUrl=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION        
 

    displaytopic=CM_phantom_talk_ads.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=CM_phantom_talk_ads.objects.filter(
          
          Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(currentJob__icontains=query)|Q(profileUrl__icontains=query)|Q(Category__icontains=query)
          
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['First Name','Last Name','CurrentJob','Profile URL','Category']


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
        response['Content-Disposition'] = 'attachment; filename="Community Moderator Phantombuster Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['First Name','Last Name','CurrentJob','Profile URL','Category','Contacted'])
        writedata = displaytopic.values_list('First_Name','Last_Name','currentJob','profileUrl','Category','contact')
        write_list=list()
        for row in writedata:
            if row[5] ==  1:
                write_contact='Yes'
            else:
                write_contact='No'
            wlist=[row[0],row[1],row[2],row[3],row[4],write_contact]

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
            displaytopic=CM_phantom_talk_ads.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Community Moderator Phantombuster Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['First Name','Last Name','CurrentJob','Profile URL','Category','Contacted'])
            writedata = displaytopic.values_list('First_Name','Last_Name','currentJob','profileUrl','Category','contact')
            write_list=list()
            for row in writedata:
                if row[5] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        elif sear1=='yes':

            query = request.session['query']
            displaytopic1=CM_phantom_talk_ads.objects.filter(
            Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(currentJob__icontains=query)|Q(profileUrl__icontains=query)|Q(Category__icontains=query)
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]
            


            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Community Moderator Phantombuster Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['First Name','Last Name','CurrentJob','Profile URL','Category','Contacted'])
            writedata = displaytopic1.values_list('First_Name','Last_Name','currentJob','profileUrl','Category','contact')
            write_list=list()
            for row in writedata:
                if row[5] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "

        else:
            
            displaytopic=CM_phantom_talk_ads.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Community Moderator Phantombuster Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['First Name','Last Name','CurrentJob','Profile URL','Category','Contacted'])
            writedata = displaytopic.values_list('First_Name','Last_Name','currentJob','profileUrl','Category','contact')
            write_list=list()
            for row in writedata:
                if row[5] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "

     
        del request.session['query']
        del request.session['sear']
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Community Moderator Linkedin (P) Ads','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def dc_phantom_ads(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=DC_phantom_talk_ads.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    DC_phantom_talk_ads.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=DC_phantom_talk_ads.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    DC_phantom_talk_ads.objects.filter(Row_id=ids).update(contact=0)



    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=DC_phantom_talk_ads.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    DC_phantom_talk_ads.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                DC_phantom_talk_ads.objects.filter(Row_id=ids).delete()


    
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
            if not DC_phantom_talk_ads.objects.filter(profileUrl=column[3]).exists():
                data_dict = {}
                link_search=DC_phantom_talk_ads()
                link_search.First_Name = column[0]
                link_search.Last_Name=column[1]
                link_search.currentJob=column[2]
                link_search.profileUrl=column[3]
                link_search.Category=column[4]
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
            DC_phantom_talk_ads.objects.filter(profileUrl=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION        
 

    displaytopic=DC_phantom_talk_ads.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=DC_phantom_talk_ads.objects.filter(
          
          Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(currentJob__icontains=query)|Q(profileUrl__icontains=query)|Q(Category__icontains=query)
          
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['First Name','Last Name','CurrentJob','Profile URL','Category']


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
        response['Content-Disposition'] = 'attachment; filename="Discord Community Phantombuster Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['First Name','Last Name','CurrentJob','Profile URL','Category','Contacted'])
        writedata = displaytopic.values_list('First_Name','Last_Name','currentJob','profileUrl','Category','contact')
        write_list=list()
        for row in writedata:
            if row[5] ==  1:
                write_contact='Yes'
            else:
                write_contact='No'
            wlist=[row[0],row[1],row[2],row[3],row[4],write_contact]

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
            displaytopic=DC_phantom_talk_ads.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Discord Community Phantombuster Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['First Name','Last Name','CurrentJob','Profile URL','Category','Contacted'])
            writedata = displaytopic.values_list('First_Name','Last_Name','currentJob','profileUrl','Category','contact')
            write_list=list()
            for row in writedata:
                if row[5] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        elif sear1=='yes':

            query = request.session['query']
            displaytopic1=DC_phantom_talk_ads.objects.filter(
            Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(currentJob__icontains=query)|Q(profileUrl__icontains=query)|Q(Category__icontains=query)
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]
            


            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Discord Community Phantombuster Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['First Name','Last Name','CurrentJob','Profile URL','Category','Contacted'])
            writedata = displaytopic1.values_list('First_Name','Last_Name','currentJob','profileUrl','Category','contact')
            write_list=list()
            for row in writedata:
                if row[5] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "

        else:
            
            displaytopic=DC_phantom_talk_ads.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Discord Community Phantombuster Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['First Name','Last Name','CurrentJob','Profile URL','Category','Contacted'])
            writedata = displaytopic.values_list('First_Name','Last_Name','currentJob','profileUrl','Category','contact')
            write_list=list()
            for row in writedata:
                if row[5] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "

     
        del request.session['query']
        del request.session['sear']
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Discord Community Linkedin (P) Ads','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def chatbot_twi_ads(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=chatbot_twi_talk_ads.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    chatbot_twi_talk_ads.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=chatbot_twi_talk_ads.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    chatbot_twi_talk_ads.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
       
            for ids in list_of_input_ids:
                d1=chatbot_twi_talk_ads.objects.filter(Row_id=ids)
            
                if d1.values_list('contact')[0][0] != 2:
                    chatbot_twi_talk_ads.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                chatbot_twi_talk_ads.objects.filter(Row_id=ids).delete()



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
            if not chatbot_twi_talk_ads.objects.filter(User_Id=column[0]).exists():
                data_dict = {}
                fb=chatbot_twi_talk_ads()
                fb.User_Id = column[0]
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
            chatbot_twi_talk_ads.objects.filter(User_Id=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=chatbot_twi_talk_ads.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=chatbot_twi_talk_ads.objects.filter(  
          Q(User_Id__icontains=query)
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['User_Id']


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
        response['Content-Disposition'] = 'attachment; filename="Chat Bots Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['User_Id','Contacted'])
        writedata = displaytopic.values_list('User_Id','contact')
        write_list=list()
        for row in writedata:
            if row[1] ==  1:
                write_contact='Yes'
            else:
                write_contact='No'
            wlist=[row[0],write_contact]

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
            displaytopic=chatbot_twi_talk_ads.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Chat Bots Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['User_Id','Contacted'])
            writedata = displaytopic.values_list('User_Id','contact')
            write_list=list()
            for row in writedata:
                if row[1] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        elif sear1=='yes':
            query = request.session['query']

            displaytopic1=chatbot_twi_talk_ads.objects.filter(
              
              Q(User_Id__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            
            #displaytopic=chatbot_twi_talk_ads.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Chat Bots Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['User_Id','Contacted'])
            writedata = displaytopic1.values_list('User_Id','contact')
            write_list=list()
            for row in writedata:
                if row[1] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        else:
            
            displaytopic=chatbot_twi_talk_ads.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Chat Bots Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['User_Id','Contacted'])
            writedata = displaytopic.values_list('User_Id','contact')
            write_list=list()
            for row in writedata:
                if row[1] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        del request.session['query']
        del request.session['sear']

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Chat Bots Twitter Ads','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def cb_twi_ads(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=CB_twi_talk_ads.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    CB_twi_talk_ads.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=CB_twi_talk_ads.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    CB_twi_talk_ads.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
       
            for ids in list_of_input_ids:
                d1=CB_twi_talk_ads.objects.filter(Row_id=ids)
            
                if d1.values_list('contact')[0][0] != 2:
                    CB_twi_talk_ads.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                CB_twi_talk_ads.objects.filter(Row_id=ids).delete()



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
            if not CB_twi_talk_ads.objects.filter(User_Id=column[0]).exists():
                data_dict = {}
                fb=CB_twi_talk_ads()
                fb.User_Id = column[0]
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
            CB_twi_talk_ads.objects.filter(User_Id=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=CB_twi_talk_ads.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=CB_twi_talk_ads.objects.filter(  
          Q(User_Id__icontains=query)
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['User_Id']


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
        response['Content-Disposition'] = 'attachment; filename="Community Building Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['User_Id','Contacted'])
        writedata = displaytopic.values_list('User_Id','contact')
        write_list=list()
        for row in writedata:
            if row[1] ==  1:
                write_contact='Yes'
            else:
                write_contact='No'
            wlist=[row[0],write_contact]

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
            displaytopic=CB_twi_talk_ads.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Community Building Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['User_Id','Contacted'])
            writedata = displaytopic.values_list('User_Id','contact')
            write_list=list()
            for row in writedata:
                if row[1] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        elif sear1=='yes':
            query = request.session['query']

            displaytopic1=CB_twi_talk_ads.objects.filter(
              
              Q(User_Id__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            
            #displaytopic=CB_twi_talk_ads.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Community Building Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['User_Id','Contacted'])
            writedata = displaytopic1.values_list('User_Id','contact')
            write_list=list()
            for row in writedata:
                if row[1] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        else:
            
            displaytopic=CB_twi_talk_ads.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Community Building Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['User_Id','Contacted'])
            writedata = displaytopic.values_list('User_Id','contact')
            write_list=list()
            for row in writedata:
                if row[1] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        del request.session['query']
        del request.session['sear']

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Community Building Twitter Ads','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def cg_twi_ads(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=CG_twi_talk_ads.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    CG_twi_talk_ads.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=CG_twi_talk_ads.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    CG_twi_talk_ads.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
       
            for ids in list_of_input_ids:
                d1=CG_twi_talk_ads.objects.filter(Row_id=ids)
            
                if d1.values_list('contact')[0][0] != 2:
                    CG_twi_talk_ads.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                CG_twi_talk_ads.objects.filter(Row_id=ids).delete()



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
            if not CG_twi_talk_ads.objects.filter(User_Id=column[0]).exists():
                data_dict = {}
                fb=CG_twi_talk_ads()
                fb.User_Id = column[0]
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
            CG_twi_talk_ads.objects.filter(User_Id=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=CG_twi_talk_ads.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=CG_twi_talk_ads.objects.filter(  
          Q(User_Id__icontains=query)
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['User_Id']


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
        response['Content-Disposition'] = 'attachment; filename="Community Growth Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['User_Id','Contacted'])
        writedata = displaytopic.values_list('User_Id','contact')
        write_list=list()
        for row in writedata:
            if row[1] ==  1:
                write_contact='Yes'
            else:
                write_contact='No'
            wlist=[row[0],write_contact]

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
            displaytopic=CG_twi_talk_ads.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Community Growth Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['User_Id','Contacted'])
            writedata = displaytopic.values_list('User_Id','contact')
            write_list=list()
            for row in writedata:
                if row[1] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        elif sear1=='yes':
            query = request.session['query']

            displaytopic1=CG_twi_talk_ads.objects.filter(
              
              Q(User_Id__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            
            #displaytopic=CG_twi_talk_ads.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Community Growth Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['User_Id','Contacted'])
            writedata = displaytopic1.values_list('User_Id','contact')
            write_list=list()
            for row in writedata:
                if row[1] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        else:
            
            displaytopic=CG_twi_talk_ads.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Community Growth Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['User_Id','Contacted'])
            writedata = displaytopic.values_list('User_Id','contact')
            write_list=list()
            for row in writedata:
                if row[1] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        del request.session['query']
        del request.session['sear']

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Community Growth Twitter Ads','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )

@login_required
def cm_twi_ads(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=CManag_twi_talk_ads.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    CManag_twi_talk_ads.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=CManag_twi_talk_ads.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    CManag_twi_talk_ads.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
       
            for ids in list_of_input_ids:
                d1=CManag_twi_talk_ads.objects.filter(Row_id=ids)
            
                if d1.values_list('contact')[0][0] != 2:
                    CManag_twi_talk_ads.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                CManag_twi_talk_ads.objects.filter(Row_id=ids).delete()



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
            if not CManag_twi_talk_ads.objects.filter(User_Id=column[0]).exists():
                data_dict = {}
                fb=CManag_twi_talk_ads()
                fb.User_Id = column[0]
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
            CManag_twi_talk_ads.objects.filter(User_Id=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=CManag_twi_talk_ads.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=CManag_twi_talk_ads.objects.filter(  
          Q(User_Id__icontains=query)
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['User_Id']


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
        response['Content-Disposition'] = 'attachment; filename="Community Management Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['User_Id','Contacted'])
        writedata = displaytopic.values_list('User_Id','contact')
        write_list=list()
        for row in writedata:
            if row[1] ==  1:
                write_contact='Yes'
            else:
                write_contact='No'
            wlist=[row[0],write_contact]

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
            displaytopic=CManag_twi_talk_ads.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Community Management Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['User_Id','Contacted'])
            writedata = displaytopic.values_list('User_Id','contact')
            write_list=list()
            for row in writedata:
                if row[1] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        elif sear1=='yes':
            query = request.session['query']

            displaytopic1=CManag_twi_talk_ads.objects.filter(
              
              Q(User_Id__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            
            #displaytopic=CManag_twi_talk_ads.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Community Management Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['User_Id','Contacted'])
            writedata = displaytopic1.values_list('User_Id','contact')
            write_list=list()
            for row in writedata:
                if row[1] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        else:
            
            displaytopic=CManag_twi_talk_ads.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Community Management Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['User_Id','Contacted'])
            writedata = displaytopic.values_list('User_Id','contact')
            write_list=list()
            for row in writedata:
                if row[1] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        del request.session['query']
        del request.session['sear']

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Community Management Twitter Ads','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def db_twi_ads(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=discordbot_twi_talk_ads.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    discordbot_twi_talk_ads.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=discordbot_twi_talk_ads.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    discordbot_twi_talk_ads.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
       
            for ids in list_of_input_ids:
                d1=discordbot_twi_talk_ads.objects.filter(Row_id=ids)
            
                if d1.values_list('contact')[0][0] != 2:
                    discordbot_twi_talk_ads.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                discordbot_twi_talk_ads.objects.filter(Row_id=ids).delete()



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
            if not discordbot_twi_talk_ads.objects.filter(User_Id=column[0]).exists():
                data_dict = {}
                fb=discordbot_twi_talk_ads()
                fb.User_Id = column[0]
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
            discordbot_twi_talk_ads.objects.filter(User_Id=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=discordbot_twi_talk_ads.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=discordbot_twi_talk_ads.objects.filter(  
          Q(User_Id__icontains=query)
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['User_Id']


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
        response['Content-Disposition'] = 'attachment; filename="Discord Bots Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['User_Id','Contacted'])
        writedata = displaytopic.values_list('User_Id','contact')
        write_list=list()
        for row in writedata:
            if row[1] ==  1:
                write_contact='Yes'
            else:
                write_contact='No'
            wlist=[row[0],write_contact]

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
            displaytopic=discordbot_twi_talk_ads.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Discord Bots Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['User_Id','Contacted'])
            writedata = displaytopic.values_list('User_Id','contact')
            write_list=list()
            for row in writedata:
                if row[1] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        elif sear1=='yes':
            query = request.session['query']

            displaytopic1=discordbot_twi_talk_ads.objects.filter(
              
              Q(User_Id__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            
            #displaytopic=discordbot_twi_talk_ads.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Discord Bots Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['User_Id','Contacted'])
            writedata = displaytopic1.values_list('User_Id','contact')
            write_list=list()
            for row in writedata:
                if row[1] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        else:
            
            displaytopic=discordbot_twi_talk_ads.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Discord Bots Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['User_Id','Contacted'])
            writedata = displaytopic.values_list('User_Id','contact')
            write_list=list()
            for row in writedata:
                if row[1] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        del request.session['query']
        del request.session['sear']

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Discord Bots Twitter Ads','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )

@login_required
def twi_marketing_twi_ads(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=twitter_marketing_twi_talk_ads.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    twitter_marketing_twi_talk_ads.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=twitter_marketing_twi_talk_ads.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    twitter_marketing_twi_talk_ads.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
       
            for ids in list_of_input_ids:
                d1=twitter_marketing_twi_talk_ads.objects.filter(Row_id=ids)
            
                if d1.values_list('contact')[0][0] != 2:
                    twitter_marketing_twi_talk_ads.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                twitter_marketing_twi_talk_ads.objects.filter(Row_id=ids).delete()



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
            if not twitter_marketing_twi_talk_ads.objects.filter(User_Id=column[0]).exists():
                data_dict = {}
                fb=twitter_marketing_twi_talk_ads()
                fb.User_Id = column[0]
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
            twitter_marketing_twi_talk_ads.objects.filter(User_Id=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=twitter_marketing_twi_talk_ads.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=twitter_marketing_twi_talk_ads.objects.filter(  
          Q(User_Id__icontains=query)
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['User_Id']


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
        response['Content-Disposition'] = 'attachment; filename="Twitter Marketing Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['User_Id','Contacted'])
        writedata = displaytopic.values_list('User_Id','contact')
        write_list=list()
        for row in writedata:
            if row[1] ==  1:
                write_contact='Yes'
            else:
                write_contact='No'
            wlist=[row[0],write_contact]

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
            displaytopic=twitter_marketing_twi_talk_ads.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Twitter Marketing Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['User_Id','Contacted'])
            writedata = displaytopic.values_list('User_Id','contact')
            write_list=list()
            for row in writedata:
                if row[1] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        elif sear1=='yes':
            query = request.session['query']

            displaytopic1=twitter_marketing_twi_talk_ads.objects.filter(
              
              Q(User_Id__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            
            #displaytopic=twitter_marketing_twi_talk_ads.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Twitter Marketing Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['User_Id','Contacted'])
            writedata = displaytopic1.values_list('User_Id','contact')
            write_list=list()
            for row in writedata:
                if row[1] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        else:
            
            displaytopic=twitter_marketing_twi_talk_ads.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Twitter Marketing Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['User_Id','Contacted'])
            writedata = displaytopic.values_list('User_Id','contact')
            write_list=list()
            for row in writedata:
                if row[1] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        del request.session['query']
        del request.session['sear']

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Twitter Marketing Twitter Ads','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def web3_commu_twi_ads(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=web3_community_twi_talk_ads.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    web3_community_twi_talk_ads.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=web3_community_twi_talk_ads.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    web3_community_twi_talk_ads.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
       
            for ids in list_of_input_ids:
                d1=web3_community_twi_talk_ads.objects.filter(Row_id=ids)
            
                if d1.values_list('contact')[0][0] != 2:
                    web3_community_twi_talk_ads.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                web3_community_twi_talk_ads.objects.filter(Row_id=ids).delete()



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
            if not web3_community_twi_talk_ads.objects.filter(User_Id=column[0]).exists():
                data_dict = {}
                fb=web3_community_twi_talk_ads()
                fb.User_Id = column[0]
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
            web3_community_twi_talk_ads.objects.filter(User_Id=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=web3_community_twi_talk_ads.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=web3_community_twi_talk_ads.objects.filter(  
          Q(User_Id__icontains=query)
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['User_Id']


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
        response['Content-Disposition'] = 'attachment; filename="Web3 Community Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['User_Id','Contacted'])
        writedata = displaytopic.values_list('User_Id','contact')
        write_list=list()
        for row in writedata:
            if row[1] ==  1:
                write_contact='Yes'
            else:
                write_contact='No'
            wlist=[row[0],write_contact]

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
            displaytopic=web3_community_twi_talk_ads.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Web3 Community Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['User_Id','Contacted'])
            writedata = displaytopic.values_list('User_Id','contact')
            write_list=list()
            for row in writedata:
                if row[1] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        elif sear1=='yes':
            query = request.session['query']

            displaytopic1=web3_community_twi_talk_ads.objects.filter(
              
              Q(User_Id__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            
            #displaytopic=web3_community_twi_talk_ads.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Web3 Community Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['User_Id','Contacted'])
            writedata = displaytopic1.values_list('User_Id','contact')
            write_list=list()
            for row in writedata:
                if row[1] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        else:
            
            displaytopic=web3_community_twi_talk_ads.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Web3 Community Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['User_Id','Contacted'])
            writedata = displaytopic.values_list('User_Id','contact')
            write_list=list()
            for row in writedata:
                if row[1] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        del request.session['query']
        del request.session['sear']

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Web3 Community Twitter Ads','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )

@login_required
def web3_marketing_twi_ads(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=web3_marketing_twi_talk_ads.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    web3_marketing_twi_talk_ads.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=web3_marketing_twi_talk_ads.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    web3_marketing_twi_talk_ads.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
       
            for ids in list_of_input_ids:
                d1=web3_marketing_twi_talk_ads.objects.filter(Row_id=ids)
            
                if d1.values_list('contact')[0][0] != 2:
                    web3_marketing_twi_talk_ads.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                web3_marketing_twi_talk_ads.objects.filter(Row_id=ids).delete()



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
            if not web3_marketing_twi_talk_ads.objects.filter(User_Id=column[0]).exists():
                data_dict = {}
                fb=web3_marketing_twi_talk_ads()
                fb.User_Id = column[0]
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
            web3_marketing_twi_talk_ads.objects.filter(User_Id=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=web3_marketing_twi_talk_ads.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=web3_marketing_twi_talk_ads.objects.filter(  
          Q(User_Id__icontains=query)
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['User_Id']


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
        response['Content-Disposition'] = 'attachment; filename="Web3 Marketing Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['User_Id','Contacted'])
        writedata = displaytopic.values_list('User_Id','contact')
        write_list=list()
        for row in writedata:
            if row[1] ==  1:
                write_contact='Yes'
            else:
                write_contact='No'
            wlist=[row[0],write_contact]

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
            displaytopic=web3_marketing_twi_talk_ads.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Web3 Marketing Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['User_Id','Contacted'])
            writedata = displaytopic.values_list('User_Id','contact')
            write_list=list()
            for row in writedata:
                if row[1] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        elif sear1=='yes':
            query = request.session['query']

            displaytopic1=web3_marketing_twi_talk_ads.objects.filter(
              
              Q(User_Id__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            
            #displaytopic=web3_marketing_twi_talk_ads.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Web3 Marketing Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['User_Id','Contacted'])
            writedata = displaytopic1.values_list('User_Id','contact')
            write_list=list()
            for row in writedata:
                if row[1] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        else:
            
            displaytopic=web3_marketing_twi_talk_ads.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Web3 Marketing Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['User_Id','Contacted'])
            writedata = displaytopic.values_list('User_Id','contact')
            write_list=list()
            for row in writedata:
                if row[1] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        del request.session['query']
        del request.session['sear']

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Web3 Marketing Twitter Ads','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )

