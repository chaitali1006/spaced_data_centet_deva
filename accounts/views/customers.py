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
from .models import Activation,Instagram_talk,Linkedin_lix_talk,Linkedin_group_talk,Linkedin_search_talk,Facebook_talk,Accelerators_talk_new,blank,Wonderverse,Twitter_talk_web3,Twitter_talk_web2,Entrepreneur1,Founder1,Scaleup1,Web_dev_lix,Web_dev_phantom,Entrepreneur_Phantom,Founder_Phantom,Entrepreneurship_fb,Entrepreneurship_insta,Entrepreneurship_twi
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
def accelerators(request):
    #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            lol=list()
            for ids in list_of_input_ids:
                d1=Accelerators_talk_new.objects.filter(Row_id=ids)
                lol.append(d1)
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    Accelerators_talk_new.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=Accelerators_talk_new.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    Accelerators_talk_new.objects.filter(Row_id=ids).update(contact=0)

    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Accelerators_talk_new.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    Accelerators_talk_new.objects.filter(Row_id=ids).update(contact=2)

    #displaytopic=Accelerators.objects.all() 

    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                Accelerators_talk_new.objects.filter(Row_id=ids).delete()




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
            if not Accelerators_talk_new.objects.filter(LinkedIn_Name=column[2],Location=column[9],Organisation=column[8]).exists():
                data_dict = {}
                acc=Accelerators_talk_new()
                acc.Accelerators = column[0]
                acc.ID=column[1]
                acc.LinkedIn_Name=column[2]
                acc.First_Name=column[3]
                acc.Last_Name=column[4]
                acc.Email_Top_Guess=column[5]
                acc.Email_Other_Guesses=column[6]
                acc.Description=column[7]
                acc.Organisation=column[8]
                acc.Location=column[9]
                acc.save()
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
        
        for column in csv.reader(io_string, delimiter=','):
            
            Accelerators_talk_new.objects.filter(LinkedIn_Name=column[0],Location=column[1]).delete()
        msg_display='Delete successfully...'

    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    
    displaytopic=Accelerators_talk_new.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=Accelerators_talk_new.objects.filter(
          
          Q(Accelerators__icontains=query)|Q(ID__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(Email_Top_Guess__icontains=query)|Q(Email_Other_Guesses__icontains=query)|Q(Description__icontains=query)|Q(Organisation__icontains=query)|Q(Location__icontains=query)
          
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['Accelerators','ID','LinkedIn Name','First Name','Last Name','Email Top Guess','Email Other Guesses','Description','Organisation','Location']


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
        response['Content-Disposition'] = 'attachment; filename="accelerators_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['Accelerators','ID','LinkedIn Name','First Name','Last Name','Email Top Guess','Email Other Guesses','Description','Organisation','Location','Contacted'])
        writedata = displaytopic.values_list('Accelerators','ID','LinkedIn_Name','First_Name','Last_Name','Email_Top_Guess','Email_Other_Guesses','Description','Organisation','Location','contact')
        write_list=list()
        for row in writedata:
            if row[10] ==  1:
                write_contact='Yes'
            else:
                write_contact='No'
            wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],write_contact]

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
            displaytopic=Accelerators_talk_new.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id') 
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="accelerators_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Accelerators','ID','LinkedIn Name','First Name','Last Name','Email Top Guess','Email Other Guesses','Description','Organisation','Location','Contacted'])
            writedata = displaytopic.values_list('Accelerators','ID','LinkedIn_Name','First_Name','Last_Name','Email_Top_Guess','Email_Other_Guesses','Description','Organisation','Location','contact')
            write_list=list()
            for row in writedata:
                if row[10] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "

        elif sear1=='yes':
            query = request.session['query']
            
            displaytopic1=Accelerators_talk_new.objects.filter(
              
              Q(Accelerators__icontains=query)|Q(ID__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(Email_Top_Guess__icontains=query)|Q(Email_Other_Guesses__icontains=query)|Q(Description__icontains=query)|Q(Organisation__icontains=query)|Q(Location__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]

            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="accelerators_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Accelerators','ID','LinkedIn Name','First Name','Last Name','Email Top Guess','Email Other Guesses','Description','Organisation','Location','Contacted'])
            writedata = displaytopic.values_list('Accelerators','ID','LinkedIn_Name','First_Name','Last_Name','Email_Top_Guess','Email_Other_Guesses','Description','Organisation','Location','contact')
            write_list=list()
            for row in writedata:
                if row[10] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "


        else:
            
            displaytopic=Accelerators_talk_new.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="accelerators_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Accelerators','ID','LinkedIn Name','First Name','Last Name','Email Top Guess','Email Other Guesses','Description','Organisation','Location','Contacted'])
            writedata = displaytopic.values_list('Accelerators','ID','LinkedIn_Name','First_Name','Last_Name','Email_Top_Guess','Email_Other_Guesses','Description','Organisation','Location','contact')
            write_list=list()
            for row in writedata:
                if row[10] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "

        del request.session['query']
        del request.session['sear']



    if request.GET.get('update'):
        Row_id = int(request.GET.get('Row_id').strip())
        #Accelerators = request.GET.get('Accelerators').strip()
        ID = request.GET.get('ID').strip()
        LinkedIn_Name = request.GET.get('LinkedIn_Name').strip()
        First_Name = request.GET.get('First_Name')
        Last_Name = request.GET.get('Last_Name').strip()
        Email_Top_Guess = request.GET.get('Email_Top_Guess').strip()
        Email_Other_Guesses = request.GET.get('Email_Other_Guesses').strip()
        #Description = request.GET.get('Description').strip()
        #Organisation = request.GET.get('Organisation').strip()
        #Location = request.GET.get('Location').strip()

        Accelerators_talk_new.objects.filter(Row_id=Row_id).update(ID=ID,LinkedIn_Name=LinkedIn_Name,First_Name=First_Name,Last_Name=Last_Name,Email_Top_Guess=Email_Top_Guess,Email_Other_Guesses=Email_Other_Guesses)
        msg_display=f"Updated successfully! "
    
    if request.GET.get('Row_id'):
           post_id = request.GET.get('Row_id').strip()
           ID = request.GET.get('ID').strip()
           LinkedIn_Name=request.GET.get('LinkedIn_Name').strip()
           First_Name = request.GET.get('First_Name')
           Last_Name = request.GET.get('Last_Name').strip()
           Email_Top_Guess = request.GET.get('Email_Top_Guess').strip()
           Email_Other_Guesses = request.GET.get('Email_Other_Guesses').strip()
           Accelerators_talk_new.objects.filter(Row_id=post_id).update(ID=ID,LinkedIn_Name=LinkedIn_Name,First_Name=First_Name,Last_Name=Last_Name,Email_Top_Guess=Email_Top_Guess,Email_Other_Guesses=Email_Other_Guesses)
           
       
    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Accelerators','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display,'merge':'acc'} )


@login_required
def founders(request):

     #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Founder1.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    Founder1.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=Founder1.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    Founder1.objects.filter(Row_id=ids).update(contact=0)


    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Founder1.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    Founder1.objects.filter(Row_id=ids).update(contact=2)



    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                Founder1.objects.filter(Row_id=ids).delete()


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
            if not Founder1.objects.filter(Profile_Link=column[0]).exists():
                data_dict = {}
                link_lix=Founder1()
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
            Founder1.objects.filter(Profile_Link=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=Founder1.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=Founder1.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Founders LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=Founder1.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Founders LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

            displaytopic1=Founder1.objects.filter(
          
              Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            #displaytopic=Entrepreneur1.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Founders LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=Founder1.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Founders LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Founders Linkedin (L)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )



@login_required
def scaleups(request):

     #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Scaleup1.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    Scaleup1.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=Scaleup1.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    Scaleup1.objects.filter(Row_id=ids).update(contact=0)


    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Scaleup1.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    Scaleup1.objects.filter(Row_id=ids).update(contact=2)



    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                Scaleup1.objects.filter(Row_id=ids).delete()



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
            if not Scaleup1.objects.filter(Profile_Link=column[0]).exists():
                data_dict = {}
                link_lix=Scaleup1()
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
            Scaleup1.objects.filter(Profile_Link=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=Scaleup1.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=Scaleup1.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Scaleup_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=Scaleup1.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Scaleup_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

            displaytopic1=Scaleup1.objects.filter(
          
              Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            #displaytopic=Entrepreneur1.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Scaleup_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=Scaleup1.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Scaleup_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Scaleup','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )

@login_required
def entrepreneurs(request):

     #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Entrepreneur1.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    Entrepreneur1.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=Entrepreneur1.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    Entrepreneur1.objects.filter(Row_id=ids).update(contact=0)


    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Entrepreneur1.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    Entrepreneur1.objects.filter(Row_id=ids).update(contact=2)



    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                Entrepreneur1.objects.filter(Row_id=ids).delete()

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
            if not Entrepreneur1.objects.filter(Profile_Link=column[0]).exists():
                data_dict = {}
                link_lix=Entrepreneur1()
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
            Entrepreneur1.objects.filter(Profile_Link=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=Entrepreneur1.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=Entrepreneur1.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Entrepreneur LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=Entrepreneur1.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Entrepreneur LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

            displaytopic1=Linkedin_lix_talk.objects.filter(
          
              Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            #displaytopic=Entrepreneur1.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Entrepreneur LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=Entrepreneur1.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Entrepreneur LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Entrepreneurs Linkedin (L)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )

@login_required
def entrepreneurs_phantom(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Entrepreneur_Phantom.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    Entrepreneur_Phantom.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=Entrepreneur_Phantom.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    Entrepreneur_Phantom.objects.filter(Row_id=ids).update(contact=0)



    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Entrepreneur_Phantom.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    Entrepreneur_Phantom.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                Entrepreneur_Phantom.objects.filter(Row_id=ids).delete()


    
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
            if not Entrepreneur_Phantom.objects.filter(profileUrl=column[0]).exists():
                data_dict = {}
                link_search=Entrepreneur_Phantom()
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
            Entrepreneur_Phantom.objects.filter(profileUrl=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION        
 

    displaytopic=Entrepreneur_Phantom.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=Entrepreneur_Phantom.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Entrepreneur_phantom_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=Entrepreneur_Phantom.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Entrepreneurs_phantom_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic1=Entrepreneur_Phantom.objects.filter(
            Q(profileUrl__icontains=query)|Q(currentJob__icontains=query)|Q(job__icontains=query)|Q(Keyword__icontains=query)|Q(location__icontains=query)|Q(fullName__icontains=query)
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]
            


            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Entrepreneurs_phantom_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=Entrepreneur_Phantom.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Entrepreneurs_phantom_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Entrepreneurs Linkedin (P)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def founders_phantom(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Founder_Phantom.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    Founder_Phantom.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=Founder_Phantom.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    Founder_Phantom.objects.filter(Row_id=ids).update(contact=0)



    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Founder_Phantom.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    Founder_Phantom.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                Founder_Phantom.objects.filter(Row_id=ids).delete()


    
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
            if not Founder_Phantom.objects.filter(profileUrl=column[0]).exists():
                data_dict = {}
                link_search=Founder_Phantom()
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
            Founder_Phantom.objects.filter(profileUrl=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION        
 

    displaytopic=Founder_Phantom.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=Founder_Phantom.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Founders_phantom_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=Founder_Phantom.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Founders_phantom_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic1=Founder_Phantom.objects.filter(
            Q(profileUrl__icontains=query)|Q(currentJob__icontains=query)|Q(job__icontains=query)|Q(Keyword__icontains=query)|Q(location__icontains=query)|Q(fullName__icontains=query)
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]
            


            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Founders_phantom_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=Founder_Phantom.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Founders_phantom_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
        

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Founders Linkedin (P)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )

@login_required
def enter_fb(request):

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Entrepreneurship_fb.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    Entrepreneurship_fb.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=Entrepreneurship_fb.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    Entrepreneurship_fb.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
       
            for ids in list_of_input_ids:
                d1=Entrepreneurship_fb.objects.filter(Row_id=ids)
            
                if d1.values_list('contact')[0][0] != 2:
                    Entrepreneurship_fb.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                Entrepreneurship_fb.objects.filter(Row_id=ids).delete()



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
            if not Entrepreneurship_fb.objects.filter(Profile_URL=column[0]).exists():
                data_dict = {}
                fb=Entrepreneurship_fb()
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
            Entrepreneurship_fb.objects.filter(Profile_URL=column).delete()

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=Entrepreneurship_fb.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=Entrepreneurship_fb.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Entrepreneurship Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=Entrepreneurship_fb.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Entrepreneurship Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

            displaytopic1=Entrepreneurship_fb.objects.filter(
              
              Q(Profile_URL__icontains=query)|Q(Full_Name__icontains=query)|Q(First_Name__icontains=query)|Q(Last_Name__icontains=query)|Q(Education__icontains=query)|Q(Category__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            
            #displaytopic=Entrepreneurship_fb.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Entrepreneurship Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=Entrepreneurship_fb.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Entrepreneurship Facebook_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Entrepreneurs Facebook','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def enter_instagram(request):
    #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Entrepreneurship_insta.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    Entrepreneurship_insta.objects.filter(Row_id=ids).update(contact=1)


    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=Entrepreneurship_insta.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    Entrepreneurship_insta.objects.filter(Row_id=ids).update(contact=0)

    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Entrepreneurship_insta.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    Entrepreneurship_insta.objects.filter(Row_id=ids).update(contact=2)

    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                Entrepreneurship_insta.objects.filter(Row_id=ids).delete()
            
            

    
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
        data_list = []
        for column in csv.reader(io_string, delimiter=','):
            no_rows+=1
            if not Entrepreneurship_insta.objects.filter(profileUrl=column[0]).exists():          
                data_list.append(Entrepreneurship_insta(profileUrl=column[0],
                fullName=column[1],
                query=column[2],
                username=column[3]
                ))
                no_rows_added+=1

        msg = Entrepreneurship_insta.objects.bulk_create(data_list)
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
            Entrepreneurship_insta.objects.filter(profileUrl=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=Entrepreneurship_insta.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=Entrepreneurship_insta.objects.filter(
          
          Q(profileUrl__icontains=query)|Q(fullName__icontains=query)|Q(query__icontains=query)|Q(username__icontains=query)
          
        ).order_by('Row_id')
        
    if 'sear' in request.session:
        sear1='yes'
    else:
        sear1='no'


    column_names=['Profile URL','Full Name','Query','Username']


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
        response['Content-Disposition'] = 'attachment; filename="Entrepreneurs Instagram_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
        writer.writerow(['Profile URL','Full Name','Query','Username','Contacted'])
        write_list=list()
        lol=displaytopic.values_list('profileUrl')
        contact=displaytopic.values_list('contact')

        writedata = displaytopic.values_list('profileUrl', 'fullName', 'query','username','contact')
        write_list=list()
        for row in writedata:   
            if row[4] ==  1:
                write_contact='Yes'
            else:
                write_contact='No'
            wlist=[row[0],row[1],row[2],row[3],write_contact]

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
            displaytopic=Entrepreneurship_insta.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id') 
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Entrepreneurs Instagram_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile URL','Full Name','Query','Username','Contacted'])
            write_list=list()
            lol=displaytopic.values_list('profileUrl')
            contact=displaytopic.values_list('contact')
    
            writedata = displaytopic.values_list('profileUrl', 'fullName', 'query','username','contact')
            write_list=list()
            for row in writedata:   
                if row[4] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            
            return response
            msg_display= f"CSV exported successfully! "



        elif sear1=='yes':
            query = request.session['query']
            

            displaytopic1 = Entrepreneurship_insta.objects.filter(
             Q(profileUrl__icontains=query)|Q(fullName__icontains=query)|Q(query__icontains=query)|Q(username__icontains=query)
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]
            
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Entrepreneurs Instagram_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile URL','Full Name','Query','Username','Contacted'])
            writedata = displaytopic1.values_list('profileUrl', 'fullName', 'query','username','contact')
            write_list=list()
            for row in writedata:
                if row[4] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "


        else:
            
            #cur.execute("SELECT * FROM linkedin_lix;")
            displaytopic=Entrepreneurship_insta.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Entrepreneurs Instagram_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
            writer.writerow(['Profile URL','Full Name','Query','Username','Contacted'])
            writedata = displaytopic.values_list('profileUrl', 'fullName', 'query','username','contact')
            write_list=list()
            for row in writedata:   
                if row[4] ==  1:
                    write_contact='Yes'
                else:
                    write_contact='No'
                wlist=[row[0],row[1],row[2],row[3],write_contact]

                write_list.append(wlist)

                writer.writerow(wlist)

            return response
            msg_display= f"CSV exported successfully! "

        del request.session['query']
        del request.session['sear']

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Entrepreneurs Instagram','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )



@login_required
def enter_twi(request):
    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Entrepreneurship_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    Entrepreneurship_twi.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=Entrepreneurship_twi.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    Entrepreneurship_twi.objects.filter(Row_id=ids).update(contact=0)


    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Entrepreneurship_twi.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    Entrepreneurship_twi.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                Entrepreneurship_twi.objects.filter(Row_id=ids).delete()




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
            if not Entrepreneurship_twi.objects.filter(Profile_Url=column[0]).exists():
                data_dict = {}
                tw=Entrepreneurship_twi()
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
            Entrepreneurship_twi.objects.filter(Profile_Url=column).delete()
            
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

    displaytopic=Entrepreneurship_twi.objects.all().order_by('Row_id')
    if sort == 'ass':
        displaytopic=Entrepreneurship_twi.objects.all().order_by('Followers_Count')
    elif sort == 'dec':
        displaytopic=Entrepreneurship_twi.objects.all().order_by('-Followers_Count')
    

   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=Entrepreneurship_twi.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Entrepreneurs_twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=Entrepreneurship_twi.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Entrepreneurs_twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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


            displaytopic1=Entrepreneurship_twi.objects.filter(
          
              Q(Profile_Url__icontains=query)|Q(Screen_Name__icontains=query)|Q(User_Id__icontains=query)|Q(Name__icontains=query)|Q(Img_Url__icontains=query)|Q(Background_Img__icontains=query)|Q(Bio__icontains=query)|Q(Website__icontains=query)|Q(Location__icontains=query)|Q(Created_At__icontains=query)|Q(Followers_Count__icontains=query)|Q(Friends_Count__icontains=query)|Q(Tweets_Count__icontains=query)|Q(Certified__icontains=query)|Q(Following__icontains=query)|Q(Followed_By__icontains=query)|Q(Query__icontains=query)|Q(Timestamp1__icontains=query)|Q(Screen_Name__icontains=query)|Q(Screen_Name__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]

            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Entrepreneurs_twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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


        elif sort=='ass':
            
            displaytopic=Entrepreneurship_twi.objects.all.order_by('Followers_Count')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Entrepreneurs_twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

        elif sort == 'dec':
            #lol='ds'
            displaytopic1=Entrepreneurship_twi.objects.all.order_by('-Followers_Count')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Entrepreneurs_twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            displaytopic=Entrepreneurship_twi.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Entrepreneurs_twitter_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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


        del request.session['query']
        del request.session['sear']
        del request.session['sort']


    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Entrepreneurs Twitter','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':sort} )
