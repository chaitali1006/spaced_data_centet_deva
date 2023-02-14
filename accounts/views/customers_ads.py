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
from .models import enterpreneurs_fb_talk_ads_spaced,enterpreneurs_LIX_talk_ads,founder_LIX_talk_ads,enterpreneurs_phantom_talk_ads,founders_phantom_talk_ads,enterpreneurs_twi_talk_ads,entrepreneurs_insta_talk_ads

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
def entrepreneurs_insta_ads(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=entrepreneurs_insta_talk_ads.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    entrepreneurs_insta_talk_ads.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=entrepreneurs_insta_talk_ads.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    entrepreneurs_insta_talk_ads.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
       
            for ids in list_of_input_ids:
                d1=entrepreneurs_insta_talk_ads.objects.filter(Row_id=ids)
            
                if d1.values_list('contact')[0][0] != 2:
                    entrepreneurs_insta_talk_ads.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                entrepreneurs_insta_talk_ads.objects.filter(Row_id=ids).delete()



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
            if not entrepreneurs_insta_talk_ads.objects.filter(uid=column[2]).exists():
                data_dict = {}
                fb=entrepreneurs_insta_talk_ads()
                fb.First_Name = column[0]
                fb.Last_Name=column[1]
                fb.uid=column[2]
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
            entrepreneurs_insta_talk_ads.objects.filter(uid=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=entrepreneurs_insta_talk_ads.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=entrepreneurs_insta_talk_ads.objects.filter(
          
          Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(uid__icontains=query)
          
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['First_Name','Last_Name','uid']


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
        response['Content-Disposition'] = 'attachment; filename="Entrepreneurs Instagram Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['First_Name','Last_Name','uid','Contacted'])
        writedata = displaytopic.values_list('First_Name','Last_Name','uid','contact')
        write_list=list()
        for row in writedata:
            if row[3]==  1:
                write_contact='Yes'
            else:
                write_contact='No'
            wlist=[row[0],row[1],row[2],write_contact]

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
            displaytopic=entrepreneurs_insta_talk_ads.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Entrepreneurs Instagram Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['First_Name','Last_Name','uid','Contacted'])
            writedata = displaytopic.values_list('First_Name','Last_Name','uid','contact')
            write_list=list()
            for row in writedata:
                if row[3]==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        elif sear1=='yes':
            query = request.session['query']

            displaytopic1=entrepreneurs_insta_talk_ads.objects.filter(
              
              Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(uid__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            
            #displaytopic=enterpreneurs_fb_ads.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Entrepreneurs Instagram Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['First_Name','Last_Name','uid','Contacted'])
            writedata = displaytopic1.values_list('First_Name','Last_Name','uid','contact')
            write_list=list()
            for row in writedata:
                if row[3]==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        else:
            
            displaytopic=entrepreneurs_insta_talk_ads.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Entrepreneurs Instagram Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['First_Name','Last_Name','uid','Contacted'])
            writedata = displaytopic.values_list('First_Name','Last_Name','uid','contact')
            write_list=list()
            for row in writedata:
                if row[3] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)
            return response
            msg_display= f"CSV exported successfully! "

        del request.session['query']
        del request.session['sear']

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Entrepreneurs Instagram Ads','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def enterpreneurs_lix__ads(request):

    #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=enterpreneurs_LIX_talk_ads.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    enterpreneurs_LIX_talk_ads.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=enterpreneurs_LIX_talk_ads.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    enterpreneurs_LIX_talk_ads.objects.filter(Row_id=ids).update(contact=0)


    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=enterpreneurs_LIX_talk_ads.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    enterpreneurs_LIX_talk_ads.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                enterpreneurs_LIX_talk_ads.objects.filter(Row_id=ids).delete()



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
            if not enterpreneurs_LIX_talk_ads.objects.filter(Profile_Link=column[3]).exists():
                data_dict = {}
                link_lix=enterpreneurs_LIX_talk_ads()
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
            enterpreneurs_LIX_talk_ads.objects.filter(Profile_Link=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=enterpreneurs_LIX_talk_ads.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=enterpreneurs_LIX_talk_ads.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Entrepreneurs LIX Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
        response['Content-Disposition'] = 'attachment; filename="Entrepreneurs LIX Ads Format_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=enterpreneurs_LIX_talk_ads.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Entrepreneurs LIX Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

            displaytopic1=enterpreneurs_LIX_talk_ads.objects.filter(
          
              Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(Description__icontains=query)|Q(Profile_Link__icontains=query)|Q(Email_id_icontains=query)|Q(Location_icontains=query)|Q(Category_icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            #cur.execute("SELECT * FROM linkedin_lix;")
            
            #displaytopic=Venture_capital_LIX.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Entrepreneurs LIX Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=enterpreneurs_LIX_talk_ads.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Entrepreneurs LIX Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Entrepreneurs Linkedin (L) Ads','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def enterpreneurs_fb_ads(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=enterpreneurs_fb_talk_ads_spaced.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    enterpreneurs_fb_talk_ads_spaced.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=enterpreneurs_fb_talk_ads_spaced.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    enterpreneurs_fb_talk_ads_spaced.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
       
            for ids in list_of_input_ids:
                d1=enterpreneurs_fb_talk_ads_spaced.objects.filter(Row_id=ids)
            
                if d1.values_list('contact')[0][0] != 2:
                    enterpreneurs_fb_talk_ads_spaced.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                enterpreneurs_fb_talk_ads_spaced.objects.filter(Row_id=ids).delete()
                # enterpreneurs_fb_talk_ads_spaced.objects.all().delete()



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
            if not enterpreneurs_fb_talk_ads_spaced.objects.filter(uid=column[3]).exists():
                data_dict = {}
                fb=enterpreneurs_fb_talk_ads_spaced()
                fb.email=column[0]
                fb.First_Name = column[1]
                fb.Last_Name=column[2]
                fb.uid=column[3]
                fb.Category=column[4]
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
            enterpreneurs_fb_talk_ads_spaced.objects.filter(uid=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=enterpreneurs_fb_talk_ads_spaced.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=enterpreneurs_fb_talk_ads_spaced.objects.filter(
          
          Q(email__icontains=query)|Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(uid__icontains=query)|Q(Category__icontains=query)
          
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['Email','First_Name','Last_Name','uid','Category']


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
        response['Content-Disposition'] = 'attachment; filename="Entrepreneurs Facebook Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['Email','First_Name','Last_Name','uid','Category','Contacted'])
        writedata = displaytopic.values_list('email','First_Name','Last_Name','uid','Category','contact')
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

    if 'export_all_ads' in request.POST:
        response =HttpResponse(content_type='text/csv')
        writer=csv.writer(response)
        response['Content-Disposition'] = 'attachment; filename="Entrepreneurs Facebook Ads Format_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['Email','First_Name','Last_Name','uid'])
        writedata = displaytopic.values_list('email','First_Name','Last_Name','uid')

        write_list=list()
        for row in writedata:
            
            wlist=[row[0],row[1],row[2],row[3]]

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
            displaytopic=enterpreneurs_fb_talk_ads_spaced.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Entrepreneurs Facebook Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Email','First_Name','Last_Name','uid','Category','Contacted','Contacted'])
            writedata = displaytopic.values_list('email','First_Name','Last_Name','uid','Category','contact')
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

            displaytopic1=enterpreneurs_fb_talk_ads_spaced.objects.filter(
              
              Q(email__icontains=query)|Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(uid__icontains=query)|Q(Category__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            
            #displaytopic=enterpreneurs_fb_talk_ads_spaced.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Entrepreneurs Facebook Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Email','First_Name','Last_Name','uid','Category','Contacted'])
            writedata = displaytopic1.values_list('email','First_Name','Last_Name','uid','Category','contact')
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
            
            displaytopic=enterpreneurs_fb_talk_ads_spaced.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Entrepreneurs Facebook Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Email','First_Name','Last_Name','uid','Category','Contacted'])
            writedata = displaytopic.values_list('email','First_Name','Last_Name','uid','Category','contact')
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Entrepreneurs Facebook Ads','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )




@login_required
def founder_lix_ads(request):

    #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=founder_LIX_talk_ads.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    founder_LIX_talk_ads.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=founder_LIX_talk_ads.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    founder_LIX_talk_ads.objects.filter(Row_id=ids).update(contact=0)


    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=founder_LIX_talk_ads.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    founder_LIX_talk_ads.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                founder_LIX_talk_ads.objects.filter(Row_id=ids).delete()



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
            if not founder_LIX_talk_ads.objects.filter(Profile_Link=column[3]).exists():
                data_dict = {}
                link_lix=founder_LIX_talk_ads()
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
            founder_LIX_talk_ads.objects.filter(Profile_Link=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=founder_LIX_talk_ads.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=founder_LIX_talk_ads.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Founders LIX Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
        response['Content-Disposition'] = 'attachment; filename="Founders LIX Ads Format_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=founder_LIX_talk_ads.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Founders LIX Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

            displaytopic1=founder_LIX_talk_ads.objects.filter(
          
              Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(Description__icontains=query)|Q(Profile_Link__icontains=query)|Q(Email_id_icontains=query)|Q(Location_icontains=query)|Q(Category_icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            #cur.execute("SELECT * FROM linkedin_lix;")
            
            #displaytopic=Venture_capital_LIX.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Founders LIX Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=founder_LIX_talk_ads.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Founders LIX Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Founders Linkedin (L) Ads','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )
    
@login_required
def enterpreneurs_phantom_ads(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=enterpreneurs_phantom_talk_ads.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    enterpreneurs_phantom_talk_ads.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=enterpreneurs_phantom_talk_ads.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    enterpreneurs_phantom_talk_ads.objects.filter(Row_id=ids).update(contact=0)



    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=enterpreneurs_phantom_talk_ads.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    enterpreneurs_phantom_talk_ads.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                enterpreneurs_phantom_talk_ads.objects.filter(Row_id=ids).delete()


    
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
            if not enterpreneurs_phantom_talk_ads.objects.filter(profileUrl=column[3]).exists():
                data_dict = {}
                link_search=enterpreneurs_phantom_talk_ads()
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
            enterpreneurs_phantom_talk_ads.objects.filter(profileUrl=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION        
 

    displaytopic=enterpreneurs_phantom_talk_ads.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=enterpreneurs_phantom_talk_ads.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Enterpreneurs Phantombuster Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=enterpreneurs_phantom_talk_ads.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Enterpreneurs Phantombuster Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic1=enterpreneurs_phantom_talk_ads.objects.filter(
            Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(currentJob__icontains=query)|Q(profileUrl__icontains=query)|Q(Category__icontains=query)
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]
            


            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Enterpreneurs Phantombuster Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=enterpreneurs_phantom_talk_ads.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Enterpreneurs Phantombuster Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Entrepreneurs Linkedin (P) Ads','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )

@login_required
def founders_phantom_ads(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=founders_phantom_talk_ads.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    founders_phantom_talk_ads.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=founders_phantom_talk_ads.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    founders_phantom_talk_ads.objects.filter(Row_id=ids).update(contact=0)



    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=founders_phantom_talk_ads.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    founders_phantom_talk_ads.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                founders_phantom_talk_ads.objects.filter(Row_id=ids).delete()


    
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
            if not founders_phantom_talk_ads.objects.filter(profileUrl=column[3]).exists():
                data_dict = {}
                link_search=founders_phantom_talk_ads()
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
            founders_phantom_talk_ads.objects.filter(profileUrl=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION        
 

    displaytopic=founders_phantom_talk_ads.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=founders_phantom_talk_ads.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Founders Phantombuster Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=founders_phantom_talk_ads.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Founders Phantombuster Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic1=founders_phantom_talk_ads.objects.filter(
            Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(currentJob__icontains=query)|Q(profileUrl__icontains=query)|Q(Category__icontains=query)
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]
            


            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Founders Phantombuster Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=founders_phantom_talk_ads.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Founders Phantombuster Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Founders Linkedin (P) Ads','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def enterpreneurs_twi_ads(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=enterpreneurs_twi_talk_ads.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    enterpreneurs_twi_talk_ads.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=enterpreneurs_twi_talk_ads.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    enterpreneurs_twi_talk_ads.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
       
            for ids in list_of_input_ids:
                d1=enterpreneurs_twi_talk_ads.objects.filter(Row_id=ids)
            
                if d1.values_list('contact')[0][0] != 2:
                    enterpreneurs_twi_talk_ads.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                enterpreneurs_twi_talk_ads.objects.filter(Row_id=ids).delete()



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
            if not enterpreneurs_twi_talk_ads.objects.filter(User_Id=column[0]).exists():
                data_dict = {}
                fb=enterpreneurs_twi_talk_ads()
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
            enterpreneurs_twi_talk_ads.objects.filter(User_Id=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=enterpreneurs_twi_talk_ads.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=enterpreneurs_twi_talk_ads.objects.filter(  
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
        response['Content-Disposition'] = 'attachment; filename="Enterpreneurs Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=enterpreneurs_twi_talk_ads.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Enterpreneurs Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

            displaytopic1=enterpreneurs_twi_talk_ads.objects.filter(
              
              Q(User_Id__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            
            #displaytopic=enterpreneurs_twi_talk_ads.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Enterpreneurs Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=enterpreneurs_twi_talk_ads.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Enterpreneurs Twitter Ads_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Enterpreneurs Twitter Ads','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )