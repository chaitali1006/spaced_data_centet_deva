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
from .models import Activation,Instagram_talk,Linkedin_lix_talk,Linkedin_group_talk,Linkedin_search_talk,Facebook_talk,Accelerators_talk_new,blank,Wonderverse,Twitter_talk_web3,Twitter_talk_web2,Entrepreneur1,Founder1,Scaleup1,Web_dev_lix,Web_dev_phantom,Venture_capital_LIX,Angle_investor_LIX,Seed_capital_LIX,Fundraising_LIX,Private_investor_LIX,Venture_capital_phantom,Angle_investor_phantom,Seed_capital_phantom,Fundraising_phantom,Private_investor_phantom,venture_capital_fb,angle_investor_fb,pitchdesk_fb,private_investor_fb,business_angle_fb,venture_capital_twi,angle_investor_twi,seed_capital_twi,web3_fund_twi,web3_grants_twi,fundraising_twi,whitepaper_twi,pitchdesk_twi,private_investor_twi,business_angle_twi,web3_investor_twi
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
def vc_lix(request):

    #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Venture_capital_LIX.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    Venture_capital_LIX.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=Venture_capital_LIX.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    Venture_capital_LIX.objects.filter(Row_id=ids).update(contact=0)


    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Venture_capital_LIX.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    Venture_capital_LIX.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                Venture_capital_LIX.objects.filter(Row_id=ids).delete()



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
            if not Venture_capital_LIX.objects.filter(Profile_Link=column[0]).exists():
                data_dict = {}
                link_lix=Venture_capital_LIX()
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
            Venture_capital_LIX.objects.filter(Profile_Link=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=Venture_capital_LIX.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=Venture_capital_LIX.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Venture Capital_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=Venture_capital_LIX.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Venture Capital_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

            displaytopic1=Venture_capital_LIX.objects.filter(
          
              Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            #cur.execute("SELECT * FROM linkedin_lix;")
            
            #displaytopic=Venture_capital_LIX.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Venture Capital_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=Venture_capital_LIX.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Venture Capital_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Venture Capital Linkedin (L)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def angel_lix(request):

    #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Angle_investor_LIX.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    Angle_investor_LIX.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=Angle_investor_LIX.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    Angle_investor_LIX.objects.filter(Row_id=ids).update(contact=0)


    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Angle_investor_LIX.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    Angle_investor_LIX.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                Angle_investor_LIX.objects.filter(Row_id=ids).delete()



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
            if not Angle_investor_LIX.objects.filter(Profile_Link=column[0]).exists():
                data_dict = {}
                link_lix=Angle_investor_LIX()
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
            Angle_investor_LIX.objects.filter(Profile_Link=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=Angle_investor_LIX.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=Angle_investor_LIX.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Angel Investor_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=Angle_investor_LIX.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Angel Investor_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

            displaytopic1=Angle_investor_LIX.objects.filter(
          
              Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            #cur.execute("SELECT * FROM linkedin_lix;")
            
            #displaytopic=Venture_capital_LIX.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Angel Investor_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=Angle_investor_LIX.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Angel Investor_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Angel Investor Linkedin (L)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def sc_lix(request):

    #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Seed_capital_LIX.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    Seed_capital_LIX.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=Seed_capital_LIX.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    Seed_capital_LIX.objects.filter(Row_id=ids).update(contact=0)


    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Seed_capital_LIX.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    Seed_capital_LIX.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                Seed_capital_LIX.objects.filter(Row_id=ids).delete()



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
            if not Seed_capital_LIX.objects.filter(Profile_Link=column[0]).exists():
                data_dict = {}
                link_lix=Seed_capital_LIX()
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
            Seed_capital_LIX.objects.filter(Profile_Link=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=Seed_capital_LIX.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=Seed_capital_LIX.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Seed Capital_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=Seed_capital_LIX.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Seed Capital_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

            displaytopic1=Seed_capital_LIX.objects.filter(
          
              Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            #cur.execute("SELECT * FROM linkedin_lix;")
            
            #displaytopic=Venture_capital_LIX.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Seed Capital_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=Seed_capital_LIX.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Seed Capital_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Seed Capital Linkedin (L)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )

@login_required
def fr_lix(request):

    #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Fundraising_LIX.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    Fundraising_LIX.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=Fundraising_LIX.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    Fundraising_LIX.objects.filter(Row_id=ids).update(contact=0)


    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Fundraising_LIX.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    Fundraising_LIX.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                Fundraising_LIX.objects.filter(Row_id=ids).delete()



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
            if not Fundraising_LIX.objects.filter(Profile_Link=column[0]).exists():
                data_dict = {}
                link_lix=Fundraising_LIX()
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
            Fundraising_LIX.objects.filter(Profile_Link=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=Fundraising_LIX.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=Fundraising_LIX.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Fundraising_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=Fundraising_LIX.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Fundraising_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

            displaytopic1=Fundraising_LIX.objects.filter(
          
              Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            #cur.execute("SELECT * FROM linkedin_lix;")
            
            #displaytopic=Venture_capital_LIX.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Fundraising_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=Fundraising_LIX.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Fundraising_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Fundraising Linkedin (L)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )

@login_required
def pi_lix(request):

    #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Fundraising_LIX.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    Fundraising_LIX.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=Private_investor_LIX.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    Private_investor_LIX.objects.filter(Row_id=ids).update(contact=0)


    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Private_investor_LIX.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    Private_investor_LIX.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                Private_investor_LIX.objects.filter(Row_id=ids).delete()



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
            if not Private_investor_LIX.objects.filter(Profile_Link=column[0]).exists():
                data_dict = {}
                link_lix=Private_investor_LIX()
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
            Private_investor_LIX.objects.filter(Profile_Link=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=Private_investor_LIX.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=Private_investor_LIX.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Private Investor_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=Private_investor_LIX.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Private Investor_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

            displaytopic1=Private_investor_LIX.objects.filter(
          
              Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            #cur.execute("SELECT * FROM linkedin_lix;")
            
            #displaytopic=Venture_capital_LIX.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Private Investor_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=Private_investor_LIX.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Private Investor_lix_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Private Investor Linkedin (L)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def vc_phantom(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Venture_capital_phantom.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    Venture_capital_phantom.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=Venture_capital_phantom.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    Venture_capital_phantom.objects.filter(Row_id=ids).update(contact=0)



    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Venture_capital_phantom.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    Venture_capital_phantom.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                Venture_capital_phantom.objects.filter(Row_id=ids).delete()


    
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
            if not Venture_capital_phantom.objects.filter(profileUrl=column[0]).exists():
                data_dict = {}
                link_search=Venture_capital_phantom()
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
            Venture_capital_phantom.objects.filter(profileUrl=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION        
 

    displaytopic=Venture_capital_phantom.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=Venture_capital_phantom.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Venture Capital Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=Venture_capital_phantom.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Venture Capital Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic1=Venture_capital_phantom.objects.filter(
            Q(profileUrl__icontains=query)|Q(currentJob__icontains=query)|Q(job__icontains=query)|Q(Keyword__icontains=query)|Q(location__icontains=query)|Q(fullName__icontains=query)
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]
            


            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Venture Capital Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=Venture_capital_phantom.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Venture Capital Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Venture Capital Linkedin (P)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )

@login_required
def angel_phantom(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Angle_investor_phantom.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    Angle_investor_phantom.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=Angle_investor_phantom.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    Angle_investor_phantom.objects.filter(Row_id=ids).update(contact=0)



    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Angle_investor_phantom.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    Angle_investor_phantom.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                Angle_investor_phantom.objects.filter(Row_id=ids).delete()


    
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
            if not Angle_investor_phantom.objects.filter(profileUrl=column[0]).exists():
                data_dict = {}
                link_search=Angle_investor_phantom()
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
            Angle_investor_phantom.objects.filter(profileUrl=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION        
 

    displaytopic=Angle_investor_phantom.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=Angle_investor_phantom.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Angel Investor Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=Angle_investor_phantom.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Angel Investor Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic1=Angle_investor_phantom.objects.filter(
            Q(profileUrl__icontains=query)|Q(currentJob__icontains=query)|Q(job__icontains=query)|Q(Keyword__icontains=query)|Q(location__icontains=query)|Q(fullName__icontains=query)
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]
            


            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Angel Investor Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=Angle_investor_phantom.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Angel Investor Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Angel Investor Linkedin (P)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def sc_phantom(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Seed_capital_phantom.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    Seed_capital_phantom.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=Seed_capital_phantom.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    Seed_capital_phantom.objects.filter(Row_id=ids).update(contact=0)



    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Seed_capital_phantom.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    Seed_capital_phantom.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                Seed_capital_phantom.objects.filter(Row_id=ids).delete()


    
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
            if not Seed_capital_phantom.objects.filter(profileUrl=column[0]).exists():
                data_dict = {}
                link_search=Seed_capital_phantom()
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
            Seed_capital_phantom.objects.filter(profileUrl=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION        
 

    displaytopic=Seed_capital_phantom.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=Seed_capital_phantom.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Seed Capital Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=Seed_capital_phantom.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Seed Capital Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic1=Seed_capital_phantom.objects.filter(
            Q(profileUrl__icontains=query)|Q(currentJob__icontains=query)|Q(job__icontains=query)|Q(Keyword__icontains=query)|Q(location__icontains=query)|Q(fullName__icontains=query)
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]
            


            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Seed Capital Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=Seed_capital_phantom.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Seed Capital Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Seed Capital Linkedin (P)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def fr_phantom(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Fundraising_phantom.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    Fundraising_phantom.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=Fundraising_phantom.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    Fundraising_phantom.objects.filter(Row_id=ids).update(contact=0)



    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Fundraising_phantom.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    Fundraising_phantom.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                Fundraising_phantom.objects.filter(Row_id=ids).delete()


    
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
            if not Fundraising_phantom.objects.filter(profileUrl=column[0]).exists():
                data_dict = {}
                link_search=Fundraising_phantom()
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
            Fundraising_phantom.objects.filter(profileUrl=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION        
 

    displaytopic=Fundraising_phantom.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=Fundraising_phantom.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Fundraising Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=Fundraising_phantom.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Fundraising Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic1=Fundraising_phantom.objects.filter(
            Q(profileUrl__icontains=query)|Q(currentJob__icontains=query)|Q(job__icontains=query)|Q(Keyword__icontains=query)|Q(location__icontains=query)|Q(fullName__icontains=query)
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]
            


            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Fundraising Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=Fundraising_phantom.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Fundraising Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Fundraising Linkedin (P)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def pi_phantom(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Private_investor_phantom.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    Private_investor_phantom.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=Private_investor_phantom.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    Private_investor_phantom.objects.filter(Row_id=ids).update(contact=0)



    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Private_investor_phantom.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    Private_investor_phantom.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                Private_investor_phantom.objects.filter(Row_id=ids).delete()


    
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
            if not Private_investor_phantom.objects.filter(profileUrl=column[0]).exists():
                data_dict = {}
                link_search=Private_investor_phantom()
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
            Private_investor_phantom.objects.filter(profileUrl=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION        
 

    displaytopic=Private_investor_phantom.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=Private_investor_phantom.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Private Investor Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=Private_investor_phantom.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Private Investor Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic1=Private_investor_phantom.objects.filter(
            Q(profileUrl__icontains=query)|Q(currentJob__icontains=query)|Q(job__icontains=query)|Q(Keyword__icontains=query)|Q(location__icontains=query)|Q(fullName__icontains=query)
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]
            


            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Private Investor Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=Private_investor_phantom.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Private Investor Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Private Investor Linkedin (P)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )



@login_required
def vc_fb(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=venture_capital_fb.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    venture_capital_fb.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=venture_capital_fb.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    venture_capital_fb.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
       
            for ids in list_of_input_ids:
                d1=venture_capital_fb.objects.filter(Row_id=ids)
            
                if d1.values_list('contact')[0][0] != 2:
                    venture_capital_fb.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                venture_capital_fb.objects.filter(Row_id=ids).delete()



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
            if not venture_capital_fb.objects.filter(Profile_URL=column[0]).exists():
                data_dict = {}
                fb=venture_capital_fb()
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
            venture_capital_fb.objects.filter(Profile_URL=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=venture_capital_fb.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=venture_capital_fb.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Venture Capital Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=venture_capital_fb.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Venture Capital Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

            displaytopic1=venture_capital_fb.objects.filter(
              
              Q(Profile_URL__icontains=query)|Q(Full_Name__icontains=query)|Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(Education__icontains=query)|Q(Category__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            
            #displaytopic=venture_capital_fb.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Venture Capital Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=venture_capital_fb.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Venture Capital Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Venture Capital Facebook','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def angle_investor_fb_view(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=angle_investor_fb.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    angle_investor_fb.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=angle_investor_fb.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    angle_investor_fb.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
       
            for ids in list_of_input_ids:
                d1=angle_investor_fb.objects.filter(Row_id=ids)
            
                if d1.values_list('contact')[0][0] != 2:
                    angle_investor_fb.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                angle_investor_fb.objects.filter(Row_id=ids).delete()



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
            if not angle_investor_fb.objects.filter(Profile_URL=column[0]).exists():
                data_dict = {}
                fb=angle_investor_fb()
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
            angle_investor_fb.objects.filter(Profile_URL=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=angle_investor_fb.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=angle_investor_fb.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Angel Investor Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=angle_investor_fb.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Angel Investor Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

            displaytopic1=angle_investor_fb.objects.filter(
              
              Q(Profile_URL__icontains=query)|Q(Full_Name__icontains=query)|Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(Education__icontains=query)|Q(Category__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            
            #displaytopic=angle_investor_fb.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Angel Investor Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=angle_investor_fb.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Angel Investor Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Angel Investor Facebook','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def pd_fb(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=pitchdesk_fb.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    pitchdesk_fb.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=pitchdesk_fb.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    pitchdesk_fb.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
       
            for ids in list_of_input_ids:
                d1=pitchdesk_fb.objects.filter(Row_id=ids)
            
                if d1.values_list('contact')[0][0] != 2:
                    pitchdesk_fb.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                pitchdesk_fb.objects.filter(Row_id=ids).delete()



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
            if not pitchdesk_fb.objects.filter(Profile_URL=column[0]).exists():
                data_dict = {}
                fb=pitchdesk_fb()
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
            pitchdesk_fb.objects.filter(Profile_URL=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=pitchdesk_fb.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=pitchdesk_fb.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Pitchdeck Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=pitchdesk_fb.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Pitchdeck Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

            displaytopic1=pitchdesk_fb.objects.filter(
              
              Q(Profile_URL__icontains=query)|Q(Full_Name__icontains=query)|Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(Education__icontains=query)|Q(Category__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            
            #displaytopic=pitchdesk_fb.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Pitchdeck Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=pitchdesk_fb.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Pitchdeck Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Pitchdeck Facebook','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )

@login_required
def pi_fb(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=private_investor_fb.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    private_investor_fb.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=private_investor_fb.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    private_investor_fb.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
       
            for ids in list_of_input_ids:
                d1=private_investor_fb.objects.filter(Row_id=ids)
            
                if d1.values_list('contact')[0][0] != 2:
                    private_investor_fb.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                private_investor_fb.objects.filter(Row_id=ids).delete()



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
            if not private_investor_fb.objects.filter(Profile_URL=column[0]).exists():
                data_dict = {}
                fb=private_investor_fb()
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
            private_investor_fb.objects.filter(Profile_URL=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=private_investor_fb.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=private_investor_fb.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Private Investor Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=private_investor_fb.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Private Investor Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

            displaytopic1=private_investor_fb.objects.filter(
              
              Q(Profile_URL__icontains=query)|Q(Full_Name__icontains=query)|Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(Education__icontains=query)|Q(Category__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            
            #displaytopic=private_investor_fb.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Private Investor Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=private_investor_fb.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Private Investor Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Private Investor Facebook','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )

@login_required
def ba_fb(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=business_angle_fb.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    business_angle_fb.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=business_angle_fb.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    business_angle_fb.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
       
            for ids in list_of_input_ids:
                d1=business_angle_fb.objects.filter(Row_id=ids)
            
                if d1.values_list('contact')[0][0] != 2:
                    business_angle_fb.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                business_angle_fb.objects.filter(Row_id=ids).delete()



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
            if not business_angle_fb.objects.filter(Profile_URL=column[0]).exists():
                data_dict = {}
                fb=business_angle_fb()
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
            business_angle_fb.objects.filter(Profile_URL=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=business_angle_fb.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=business_angle_fb.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Business Angel Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=business_angle_fb.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Business Angel Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

            displaytopic1=business_angle_fb.objects.filter(
              
              Q(Profile_URL__icontains=query)|Q(Full_Name__icontains=query)|Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(Education__icontains=query)|Q(Category__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            
            #displaytopic=business_angle_fb.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Business Angel Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=business_angle_fb.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Business Angel Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Business Angel Facebook','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )

@login_required
def vc_twi(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=venture_capital_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    venture_capital_twi.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=venture_capital_twi.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    venture_capital_twi.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=venture_capital_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    venture_capital_twi.objects.filter(Row_id=ids).update(contact=2)



    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                venture_capital_twi.objects.filter(Row_id=ids).delete()




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
            if not venture_capital_twi.objects.filter(Profile_Url=column[0]).exists():
                data_dict = {}
                tw=venture_capital_twi()
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
            venture_capital_twi.objects.filter(Profile_Url=column).delete()
            #Venture Capital Twitter_talk.objects.all().delete()

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
        displaytopic=venture_capital_twi.objects.all().order_by('Followers_Count')
    elif sort == 'dec':
        displaytopic=venture_capital_twi.objects.all().order_by('-Followers_Count')
    else:
    
        displaytopic=venture_capital_twi.objects.all().order_by('Row_id')

   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=venture_capital_twi.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Venture Capital Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=venture_capital_twi.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Venture Capital Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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


            displaytopic1=venture_capital_twi.objects.filter(
          
              Q(Profile_Url__icontains=query)|Q(Screen_Name__icontains=query)|Q(User_Id__icontains=query)|Q(Name__icontains=query)|Q(Img_Url__icontains=query)|Q(Background_Img__icontains=query)|Q(Bio__icontains=query)|Q(Website__icontains=query)|Q(Location__icontains=query)|Q(Created_At__icontains=query)|Q(Followers_Count__icontains=query)|Q(Friends_Count__icontains=query)|Q(Tweets_Count__icontains=query)|Q(Certified__icontains=query)|Q(Following__icontains=query)|Q(Followed_By__icontains=query)|Q(Query__icontains=query)|Q(Timestamp1__icontains=query)|Q(Screen_Name__icontains=query)|Q(Screen_Name__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]

            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Venture Capital Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=venture_capital_twi.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Venture Capital Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Venture Capital Twitter','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':sort} )

@login_required
def angeli_twi(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=angle_investor_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    angle_investor_twi.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=angle_investor_twi.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    angle_investor_twi.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=angle_investor_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    angle_investor_twi.objects.filter(Row_id=ids).update(contact=2)



    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                angle_investor_twi.objects.filter(Row_id=ids).delete()




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
            if not angle_investor_twi.objects.filter(Profile_Url=column[0]).exists():
                data_dict = {}
                tw=angle_investor_twi()
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
            angle_investor_twi.objects.filter(Profile_Url=column).delete()
            #Angel Investor Twitter_talk.objects.all().delete()

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
        displaytopic=angle_investor_twi.objects.all().order_by('Followers_Count')
    elif sort == 'dec':
        displaytopic=angle_investor_twi.objects.all().order_by('-Followers_Count')
    else:
    
        displaytopic=angle_investor_twi.objects.all().order_by('Row_id')

   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=angle_investor_twi.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Angel Investor Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=angle_investor_twi.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Angel Investor Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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


            displaytopic1=angle_investor_twi.objects.filter(
          
              Q(Profile_Url__icontains=query)|Q(Screen_Name__icontains=query)|Q(User_Id__icontains=query)|Q(Name__icontains=query)|Q(Img_Url__icontains=query)|Q(Background_Img__icontains=query)|Q(Bio__icontains=query)|Q(Website__icontains=query)|Q(Location__icontains=query)|Q(Created_At__icontains=query)|Q(Followers_Count__icontains=query)|Q(Friends_Count__icontains=query)|Q(Tweets_Count__icontains=query)|Q(Certified__icontains=query)|Q(Following__icontains=query)|Q(Followed_By__icontains=query)|Q(Query__icontains=query)|Q(Timestamp1__icontains=query)|Q(Screen_Name__icontains=query)|Q(Screen_Name__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]

            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Angel Investor Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=angle_investor_twi.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Angel Investor Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Angel Investor Twitter','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':sort} )

@login_required
def sc_twi(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=seed_capital_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    seed_capital_twi.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=seed_capital_twi.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    seed_capital_twi.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=seed_capital_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    seed_capital_twi.objects.filter(Row_id=ids).update(contact=2)



    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                seed_capital_twi.objects.filter(Row_id=ids).delete()




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
            if not seed_capital_twi.objects.filter(Profile_Url=column[0]).exists():
                data_dict = {}
                tw=seed_capital_twi()
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
            seed_capital_twi.objects.filter(Profile_Url=column).delete()
            #Seed Capital Twitter_talk.objects.all().delete()

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
        displaytopic=seed_capital_twi.objects.all().order_by('Followers_Count')
    elif sort == 'dec':
        displaytopic=seed_capital_twi.objects.all().order_by('-Followers_Count')
    else:
    
        displaytopic=seed_capital_twi.objects.all().order_by('Row_id')

   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=seed_capital_twi.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Seed Capital Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=seed_capital_twi.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Seed Capital Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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


            displaytopic1=seed_capital_twi.objects.filter(
          
              Q(Profile_Url__icontains=query)|Q(Screen_Name__icontains=query)|Q(User_Id__icontains=query)|Q(Name__icontains=query)|Q(Img_Url__icontains=query)|Q(Background_Img__icontains=query)|Q(Bio__icontains=query)|Q(Website__icontains=query)|Q(Location__icontains=query)|Q(Created_At__icontains=query)|Q(Followers_Count__icontains=query)|Q(Friends_Count__icontains=query)|Q(Tweets_Count__icontains=query)|Q(Certified__icontains=query)|Q(Following__icontains=query)|Q(Followed_By__icontains=query)|Q(Query__icontains=query)|Q(Timestamp1__icontains=query)|Q(Screen_Name__icontains=query)|Q(Screen_Name__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]

            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Seed Capital Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=seed_capital_twi.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Seed Capital Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Seed Capital Twitter','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':sort} )

@login_required
def wf_twi(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=web3_fund_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    web3_fund_twi.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=web3_fund_twi.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    web3_fund_twi.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=web3_fund_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    web3_fund_twi.objects.filter(Row_id=ids).update(contact=2)



    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                web3_fund_twi.objects.filter(Row_id=ids).delete()




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
            if not web3_fund_twi.objects.filter(Profile_Url=column[0]).exists():
                data_dict = {}
                tw=web3_fund_twi()
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
            web3_fund_twi.objects.filter(Profile_Url=column).delete()
            #Seed Capital Twitter_talk.objects.all().delete()

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
        displaytopic=web3_fund_twi.objects.all().order_by('Followers_Count')
    elif sort == 'dec':
        displaytopic=web3_fund_twi.objects.all().order_by('-Followers_Count')
    else:
    
        displaytopic=web3_fund_twi.objects.all().order_by('Row_id')

   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=web3_fund_twi.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Web3 Fund Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=web3_fund_twi.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Web3 Fund Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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


            displaytopic1=web3_fund_twi.objects.filter(
          
              Q(Profile_Url__icontains=query)|Q(Screen_Name__icontains=query)|Q(User_Id__icontains=query)|Q(Name__icontains=query)|Q(Img_Url__icontains=query)|Q(Background_Img__icontains=query)|Q(Bio__icontains=query)|Q(Website__icontains=query)|Q(Location__icontains=query)|Q(Created_At__icontains=query)|Q(Followers_Count__icontains=query)|Q(Friends_Count__icontains=query)|Q(Tweets_Count__icontains=query)|Q(Certified__icontains=query)|Q(Following__icontains=query)|Q(Followed_By__icontains=query)|Q(Query__icontains=query)|Q(Timestamp1__icontains=query)|Q(Screen_Name__icontains=query)|Q(Screen_Name__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]

            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Web3 Fund Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=web3_fund_twi.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Web3 Fund Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Web3 Fund Twitter','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':sort} )



@login_required
def wg_twi(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=web3_grants_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    web3_grants_twi.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=web3_grants_twi.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    web3_grants_twi.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=web3_grants_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    web3_grants_twi.objects.filter(Row_id=ids).update(contact=2)



    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                web3_grants_twi.objects.filter(Row_id=ids).delete()




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
            if not web3_grants_twi.objects.filter(Profile_Url=column[0]).exists():
                data_dict = {}
                tw=web3_grants_twi()
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
            web3_grants_twi.objects.filter(Profile_Url=column).delete()
            #Seed Capital Twitter_talk.objects.all().delete()

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
        displaytopic=web3_grants_twi.objects.all().order_by('Followers_Count')
    elif sort == 'dec':
        displaytopic=web3_grants_twi.objects.all().order_by('-Followers_Count')
    else:
    
        displaytopic=web3_grants_twi.objects.all().order_by('Row_id')

   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=web3_grants_twi.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Web3 Grants Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=web3_grants_twi.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Web3 Grants Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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


            displaytopic1=web3_grants_twi.objects.filter(
          
              Q(Profile_Url__icontains=query)|Q(Screen_Name__icontains=query)|Q(User_Id__icontains=query)|Q(Name__icontains=query)|Q(Img_Url__icontains=query)|Q(Background_Img__icontains=query)|Q(Bio__icontains=query)|Q(Website__icontains=query)|Q(Location__icontains=query)|Q(Created_At__icontains=query)|Q(Followers_Count__icontains=query)|Q(Friends_Count__icontains=query)|Q(Tweets_Count__icontains=query)|Q(Certified__icontains=query)|Q(Following__icontains=query)|Q(Followed_By__icontains=query)|Q(Query__icontains=query)|Q(Timestamp1__icontains=query)|Q(Screen_Name__icontains=query)|Q(Screen_Name__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]

            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Web3 Grants Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=web3_grants_twi.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Web3 Grants Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Web3 Grants Twitter','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':sort} )



@login_required
def fr_twi(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=fundraising_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    fundraising_twi.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=fundraising_twi.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    fundraising_twi.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=fundraising_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    fundraising_twi.objects.filter(Row_id=ids).update(contact=2)



    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                fundraising_twi.objects.filter(Row_id=ids).delete()




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
            if not fundraising_twi.objects.filter(Profile_Url=column[0]).exists():
                data_dict = {}
                tw=fundraising_twi()
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
            fundraising_twi.objects.filter(Profile_Url=column).delete()
            #Web3 Grants Twitter_talk.objects.all().delete()

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
        displaytopic=fundraising_twi.objects.all().order_by('Followers_Count')
    elif sort == 'dec':
        displaytopic=fundraising_twi.objects.all().order_by('-Followers_Count')
    else:
    
        displaytopic=fundraising_twi.objects.all().order_by('Row_id')

   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=fundraising_twi.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Fundraising Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=fundraising_twi.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Fundraising Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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


            displaytopic1=fundraising_twi.objects.filter(
          
              Q(Profile_Url__icontains=query)|Q(Screen_Name__icontains=query)|Q(User_Id__icontains=query)|Q(Name__icontains=query)|Q(Img_Url__icontains=query)|Q(Background_Img__icontains=query)|Q(Bio__icontains=query)|Q(Website__icontains=query)|Q(Location__icontains=query)|Q(Created_At__icontains=query)|Q(Followers_Count__icontains=query)|Q(Friends_Count__icontains=query)|Q(Tweets_Count__icontains=query)|Q(Certified__icontains=query)|Q(Following__icontains=query)|Q(Followed_By__icontains=query)|Q(Query__icontains=query)|Q(Timestamp1__icontains=query)|Q(Screen_Name__icontains=query)|Q(Screen_Name__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]

            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Fundraising Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=fundraising_twi.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Fundraising Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Fundraising Twitter','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':sort} )

@login_required
def wp_twi(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=whitepaper_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    whitepaper_twi.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=whitepaper_twi.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    whitepaper_twi.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=whitepaper_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    whitepaper_twi.objects.filter(Row_id=ids).update(contact=2)



    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                whitepaper_twi.objects.filter(Row_id=ids).delete()




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
            if not whitepaper_twi.objects.filter(Profile_Url=column[0]).exists():
                data_dict = {}
                tw=whitepaper_twi()
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
            whitepaper_twi.objects.filter(Profile_Url=column).delete()
            #Whitepaper Twitter_talk.objects.all().delete()

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
        displaytopic=whitepaper_twi.objects.all().order_by('Followers_Count')
    elif sort == 'dec':
        displaytopic=whitepaper_twi.objects.all().order_by('-Followers_Count')
    else:
    
        displaytopic=whitepaper_twi.objects.all().order_by('Row_id')

   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=whitepaper_twi.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Whitepaper Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=whitepaper_twi.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Whitepaper Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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


            displaytopic1=whitepaper_twi.objects.filter(
          
              Q(Profile_Url__icontains=query)|Q(Screen_Name__icontains=query)|Q(User_Id__icontains=query)|Q(Name__icontains=query)|Q(Img_Url__icontains=query)|Q(Background_Img__icontains=query)|Q(Bio__icontains=query)|Q(Website__icontains=query)|Q(Location__icontains=query)|Q(Created_At__icontains=query)|Q(Followers_Count__icontains=query)|Q(Friends_Count__icontains=query)|Q(Tweets_Count__icontains=query)|Q(Certified__icontains=query)|Q(Following__icontains=query)|Q(Followed_By__icontains=query)|Q(Query__icontains=query)|Q(Timestamp1__icontains=query)|Q(Screen_Name__icontains=query)|Q(Screen_Name__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]

            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Whitepaper Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=whitepaper_twi.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Whitepaper Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Whitepaper Twitter','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':sort} )



@login_required
def pd_twi(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=pitchdesk_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    pitchdesk_twi.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=pitchdesk_twi.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    pitchdesk_twi.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=pitchdesk_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    pitchdesk_twi.objects.filter(Row_id=ids).update(contact=2)



    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                pitchdesk_twi.objects.filter(Row_id=ids).delete()




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
            if not pitchdesk_twi.objects.filter(Profile_Url=column[0]).exists():
                data_dict = {}
                tw=pitchdesk_twi()
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
            pitchdesk_twi.objects.filter(Profile_Url=column).delete()
            #Pitchdeck_talk.objects.all().delete()

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
        displaytopic=pitchdesk_twi.objects.all().order_by('Followers_Count')
    elif sort == 'dec':
        displaytopic=pitchdesk_twi.objects.all().order_by('-Followers_Count')
    else:
    
        displaytopic=pitchdesk_twi.objects.all().order_by('Row_id')

   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=pitchdesk_twi.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Pitchdeck Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=pitchdesk_twi.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Pitchdeck Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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


            displaytopic1=pitchdesk_twi.objects.filter(
          
              Q(Profile_Url__icontains=query)|Q(Screen_Name__icontains=query)|Q(User_Id__icontains=query)|Q(Name__icontains=query)|Q(Img_Url__icontains=query)|Q(Background_Img__icontains=query)|Q(Bio__icontains=query)|Q(Website__icontains=query)|Q(Location__icontains=query)|Q(Created_At__icontains=query)|Q(Followers_Count__icontains=query)|Q(Friends_Count__icontains=query)|Q(Tweets_Count__icontains=query)|Q(Certified__icontains=query)|Q(Following__icontains=query)|Q(Followed_By__icontains=query)|Q(Query__icontains=query)|Q(Timestamp1__icontains=query)|Q(Screen_Name__icontains=query)|Q(Screen_Name__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]

            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Pitchdeck Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=pitchdesk_twi.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Pitchdeck Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Pitchdeck Twitter','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':sort} )



@login_required
def pi_twi(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=private_investor_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    private_investor_twi.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=private_investor_twi.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    private_investor_twi.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=private_investor_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    private_investor_twi.objects.filter(Row_id=ids).update(contact=2)



    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                private_investor_twi.objects.filter(Row_id=ids).delete()




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
            if not private_investor_twi.objects.filter(Profile_Url=column[0]).exists():
                data_dict = {}
                tw=private_investor_twi()
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
            private_investor_twi.objects.filter(Profile_Url=column).delete()
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
        displaytopic=private_investor_twi.objects.all().order_by('Followers_Count')
    elif sort == 'dec':
        displaytopic=private_investor_twi.objects.all().order_by('-Followers_Count')
    else:
    
        displaytopic=private_investor_twi.objects.all().order_by('Row_id')

   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=private_investor_twi.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Private Investor Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=private_investor_twi.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Private Investor Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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


            displaytopic1=private_investor_twi.objects.filter(
          
              Q(Profile_Url__icontains=query)|Q(Screen_Name__icontains=query)|Q(User_Id__icontains=query)|Q(Name__icontains=query)|Q(Img_Url__icontains=query)|Q(Background_Img__icontains=query)|Q(Bio__icontains=query)|Q(Website__icontains=query)|Q(Location__icontains=query)|Q(Created_At__icontains=query)|Q(Followers_Count__icontains=query)|Q(Friends_Count__icontains=query)|Q(Tweets_Count__icontains=query)|Q(Certified__icontains=query)|Q(Following__icontains=query)|Q(Followed_By__icontains=query)|Q(Query__icontains=query)|Q(Timestamp1__icontains=query)|Q(Screen_Name__icontains=query)|Q(Screen_Name__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]

            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Private Investor Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=private_investor_twi.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Privates Investor Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Private Investor Twitter','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':sort} )



@login_required
def ba_twi(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=business_angle_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    business_angle_twi.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=business_angle_twi.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    business_angle_twi.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=business_angle_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    business_angle_twi.objects.filter(Row_id=ids).update(contact=2)



    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                business_angle_twi.objects.filter(Row_id=ids).delete()




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
            if not business_angle_twi.objects.filter(Profile_Url=column[0]).exists():
                data_dict = {}
                tw=business_angle_twi()
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
            business_angle_twi.objects.filter(Profile_Url=column).delete()
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
        displaytopic=business_angle_twi.objects.all().order_by('Followers_Count')
    elif sort == 'dec':
        displaytopic=business_angle_twi.objects.all().order_by('-Followers_Count')
    else:
    
        displaytopic=business_angle_twi.objects.all().order_by('Row_id')

   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=business_angle_twi.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Business Angel Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=business_angle_twi.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Business Angel Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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


            displaytopic1=business_angle_twi.objects.filter(
          
              Q(Profile_Url__icontains=query)|Q(Screen_Name__icontains=query)|Q(User_Id__icontains=query)|Q(Name__icontains=query)|Q(Img_Url__icontains=query)|Q(Background_Img__icontains=query)|Q(Bio__icontains=query)|Q(Website__icontains=query)|Q(Location__icontains=query)|Q(Created_At__icontains=query)|Q(Followers_Count__icontains=query)|Q(Friends_Count__icontains=query)|Q(Tweets_Count__icontains=query)|Q(Certified__icontains=query)|Q(Following__icontains=query)|Q(Followed_By__icontains=query)|Q(Query__icontains=query)|Q(Timestamp1__icontains=query)|Q(Screen_Name__icontains=query)|Q(Screen_Name__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]

            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Business Angel Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=business_angle_twi.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Business Angel Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Business Angel Twitter','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':sort} )



@login_required
def wi_twi(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=web3_investor_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    web3_investor_twi.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=web3_investor_twi.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    web3_investor_twi.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=web3_investor_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    web3_investor_twi.objects.filter(Row_id=ids).update(contact=2)



    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                web3_investor_twi.objects.filter(Row_id=ids).delete()




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
            if not web3_investor_twi.objects.filter(Profile_Url=column[0]).exists():
                data_dict = {}
                tw=web3_investor_twi()
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
            web3_investor_twi.objects.filter(Profile_Url=column).delete()
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
        displaytopic=web3_investor_twi.objects.all().order_by('Followers_Count')
    elif sort == 'dec':
        displaytopic=web3_investor_twi.objects.all().order_by('-Followers_Count')
    else:
    
        displaytopic=web3_investor_twi.objects.all().order_by('Row_id')

   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=web3_investor_twi.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Web3 Investor Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=web3_investor_twi.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Web3 Investor Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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


            displaytopic1=web3_investor_twi.objects.filter(
          
              Q(Profile_Url__icontains=query)|Q(Screen_Name__icontains=query)|Q(User_Id__icontains=query)|Q(Name__icontains=query)|Q(Img_Url__icontains=query)|Q(Background_Img__icontains=query)|Q(Bio__icontains=query)|Q(Website__icontains=query)|Q(Location__icontains=query)|Q(Created_At__icontains=query)|Q(Followers_Count__icontains=query)|Q(Friends_Count__icontains=query)|Q(Tweets_Count__icontains=query)|Q(Certified__icontains=query)|Q(Following__icontains=query)|Q(Followed_By__icontains=query)|Q(Query__icontains=query)|Q(Timestamp1__icontains=query)|Q(Screen_Name__icontains=query)|Q(Screen_Name__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]

            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Web3 Investor Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=web3_investor_twi.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Web3 Investor Twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Web3 Investor Twitter','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':sort} )
