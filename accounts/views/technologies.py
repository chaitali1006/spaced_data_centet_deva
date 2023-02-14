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
from .models import Activation,Linkedin_lix_talk,Linkedin_group_talk,Linkedin_search_talk,Facebook_talk,Accelerators_talk_new,blank,Wonderverse,Twitter_talk_web3,Twitter_talk_web2,Entrepreneur1,Founder1,Scaleup1,Web_dev_lix,Web_dev_phantom,LIX_search_talk,Phantom_search_talk,Mobile_dev_lix,Mobile_dev_phantom,CM_LIX_talk,CB_LIX_talk,CManag_LIX_talk,DC_LIX_talk,CM_Phantom_talk,CB_Phantom_talk,CManag_Phantom_talk,DC_Phantom_talk,Entrepreneur_Phantom,Founder_Phantom,Digital_marketing,Product_fit,Software_dev,UIUX,Venture_funding,Data_analysis,Blockchain_LIX,Digital_marketing_phantom,Blockchain_LIX_phantom,Data_analysis_phantom,Venture_funding_phantom,UIUX_phantom,Software_dev_phantom,Product_fit_phantom,cb_twi,cg_twi,cm_twi,twi_marketing,web3_com_twi,web3_marketing_twi,chatbot_twi,discordbot_twi,Venture_capital_LIX,Angle_investor_LIX,Seed_capital_LIX,Fundraising_LIX,Private_investor_LIX,Venture_capital_phantom,Angle_investor_phantom,Seed_capital_phantom,Fundraising_phantom,Private_investor_phantom,venture_capital_fb,angle_investor_fb,pitchdesk_fb,private_investor_fb,business_angle_fb,venture_capital_twi,angle_investor_twi,seed_capital_twi,web3_fund_twi,web3_grants_twi,fundraising_twi,whitepaper_twi,pitchdesk_twi,private_investor_twi,business_angle_twi,web3_investor_twi,d3_design_twi,graphics_design_twi,visual_design_twi,marketing_designer_twi,branding_consultant_twi,d3_design_fb,graphics_design_fb,d3_design_LIX,graphics_design_LIX,visual_design_LIX,marketing_designer_LIX,branding_consultant_LIX,d3_design_phantom,graphics_design_phantom,visual_design_phantom,marketing_designer_phantom,branding_consultant_phantom,artificial_intelligence_LIX,machine_learning_LIX,algorithm_LIX,data_mining_LIX,neural_network_LIX,data_prediction_LIX,artificial_intelligence_phantom,machine_learning_phantom,algorithm_phantom,data_mining_phantom,neural_network_phantom,data_prediction_phantom,artificial_intelligence_fb,machine_learning_fb,algorithm_fb,data_mining_fb,neural_network_fb,artificial_intelligence_twi,machine_learning_twi,algorithm_twi,data_mining_twi,neural_network_twi,data_prediction_twi,Digital_marketing_fb,Blockchain_fb,software_development_fb,data_analysis_fb,UX_fb,Entrepreneurship_fb,UIUX_insta,Entrepreneurship_insta,Digital_marketing_insta,Entrepreneurship_twi,Digital_marketing_twi,uxui_twi,Figma_LIX_talk,Notion_LIX_talk,Slack_LIX_talk,Trello_LIX_talk,Miro_LIX_talk,Figma_twi_talk,Onalytica_twi_talk,Slack_twi_talk,Trello_twi_talk,MicroMentor_insta_talk,MentorPass_insta_talk,Miro_twi_talk,Notion_twi_talk,MicroMentor_twi_talk,MentorPass_twi_talk,Figma_phantom_talk,Notion_phantom_talk,Slack_phantom_talk,Trello_phantom_talk,Brand_Designers_phantom_talk,Brand_Designers_LIX_talk,algorithm_fb_ads,artificial_intelligence_fb_ads,data_analysis_fb_ads,data_mining_fb_ads,machine_learning_fb_ads,neural_network_fb_ads,algorithm_LIX_ads,artificial_intelligence_LIX_ads,data_analysis_LIX_ads,data_mining_LIX_ads,data_prediction_LIX_ads,data_scientist_LIX_ads,machine_learning_LIX_ads,neural_network_LIX_ads,algorithm_phantom_ads,artificial_intelligence_phantom_ads,data_analysis_phantom_ads,data_mining_phantom_ads,data_prediction_phantom_ads,data_scientist_phantom_ads,machine_learning_phantom_ads,neural_network_phantom_ads,algorithm_twi_ads,artificial_intelligence_twi_ads,data_mining_twi_ads,data_prediction_twi_ads,machine_learning_twi_ads,neural_networks_twi_ads,figma_LIX_talk_ads,miro_LIX_talk_ads,notion_LIX_talk_ads,slack_LIX_talk_ads,trello_LIX_talk_ads,figma_phantom_talk_ads,notion_phantom_talk_ads,slack_phantom_talk_ads,trello_phantom_talk_ads,figma_twi_talk_ads,miro_twi_talk_ads,notion_twi_talk_ads,onalytica_twi_talk_ads,slack_twi_talk_ads,trello_twi_talk_ads,CB_LIX_talk_ads,CManag_LIX_talk_ads,CM_LIX_talk_ads,DC_LIX_talk_ads,CB_phantom_talk_ads,CManag_phantom_talk_ads,CM_phantom_talk_ads,DC_phantom_talk_ads,chatbot_twi_talk_ads,CB_twi_talk_ads,CG_twi_talk_ads,CManag_twi_talk_ads,discordbot_twi_talk_ads,twitter_marketing_twi_talk_ads,web3_community_twi_talk_ads,web3_marketing_twi_talk_ads,enterpreneurs_fb_talk_ads,enterpreneurs_LIX_talk_ads,founder_LIX_talk_ads,enterpreneurs_phantom_talk_ads,founders_phantom_talk_ads,enterpreneurs_twi_talk_ads,d3_design_fb_talk_ads,graphic_design_fb_talk_ads,uiux_design_fb_talk_ads,d3_design_LIX_talk_ads,brand_designers_LIX_talk_ads,branding_consultant_LIX_talk_ads,graphic_design_LIX_talk_ads,marketing_designer_LIX_talk_ads,uiux_LIX_talk_ads,visual_design_LIX_talk_ads,d3_design_phantom_talk_ads,brand_designers_phantom_talk_ads,branding_consultant_phantom_talk_ads,graphic_design_phantom_talk_ads,marketing_designer_phantom_talk_ads,uiux_design_phantom_talk_ads,visual_design_phantom_talk_ads,d3_design_twi_talk_ads,branding_consultant_twi_talk_ads,graphic_design_twi_talk_ads,marketing_designer_twi_talk_ads,uiux_design_twi_talk_ads,visual_design_twi_talk_ads,micromentor_twi_talk_ads,mentorpass_twi_talk_ads,digital_marketing_fb_talk_ads,digital_marketing_LIX_talk_ads,digital_marketing_phantom_talk_ads,digital_marketing_twi_talk_ads,pm_fit_LIX_talk_ads,pm_fit_phantom_talk_ads,angle_investor_fb_talk_ads,business_angle_fb_talk_ads,pitchdesk_fb_talk_ads,private_investor_fb_talk_ads,venture_capital_fb_talk_ads,angle_investor_LIX_talk_ads,fundraising_LIX_talk_ads,private_investor_LIX_talk_ads,seed_capital_LIX_talk_ads,venture_capital_LIX_talk_ads,angle_investor_phantom_talk_ads,fundraising_phantom_talk_ads,private_investor_phantom_talk_ads,seed_capital_phantom_talk_ads,venture_capital_phantom_talk_ads,angle_investor_twi_talk_ads,business_angle_twi_talk_ads,fundraising_twi_talk_ads,pitchdesk_twi_talk_ads,private_investor_twi_talk_ads,seed_capital_twi_talk_ads,venture_capital_twi_talk_ads,web3_fund_twi_talk_ads,web3_grants_twi_talk_ads,web3_investor_twi_talk_ads,whitepaper_twi_talk_ads,blockchain_fb_talk_ads,blockchain_LIX_talk_ads,dao_LIX_talk_ads,dapp_LIX_talk_ads,defi_LIX_talk_ads,nft_LIX_talk_ads,yield_farming_LIX_talk_ads,blockchain_phantom_talk_ads,dao_phantom_talk_ads,dapp_phantom_talk_ads,defi_phantom_talk_ads,nft_phantom_talk_ads,yield_farming_phantom_talk_ads,software_development_fb_talk_ads,mobile_development_LIX_talk_ads,software_development_LIX_talk_ads,web_development_LIX_talk_ads,mobile_development_phantom_talk_ads,software_development_phantom_talk_ads,web_development_phantom_talk_ads,entrepreneurs_insta_talk_ads,digital_marketing_insta_talk_ads,uiux_insta_talk_ads,micromente_insta_talk_ads,menterpass_insta_talk_ads,defi_talk_twi,defi_talk_twi_ads,blockchain_LIX_talk_ads_spaced



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
def Web_dev(request):

	 #Contact or not contact update

	if request.GET.get('contact'):
		if request.GET.getlist('ids'):
			list_of_input_ids=request.GET.getlist('ids')
		   
			for ids in list_of_input_ids:
				d1=Web_dev_lix.objects.filter(Row_id=ids)
				
				if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
					Web_dev_lix.objects.filter(Row_id=ids).update(contact=1)

	if request.GET.get('uncontact'):
		if request.GET.getlist('ids'):
			list_of_input_ids=request.GET.getlist('ids')
			
			for ids in list_of_input_ids:
				d1=Web_dev_lix.objects.filter(Row_id=ids)
				if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
					Web_dev_lix.objects.filter(Row_id=ids).update(contact=0)


	
	if request.GET.get('pending'):
		if request.GET.getlist('ids'):
			list_of_input_ids=request.GET.getlist('ids')
		   
			for ids in list_of_input_ids:
				d1=Web_dev_lix.objects.filter(Row_id=ids)
				
				if d1.values_list('contact')[0][0] != 2:
					Web_dev_lix.objects.filter(Row_id=ids).update(contact=2)



	if request.GET.get('deleted'):
		if request.GET.getlist('inputs'):
			list_of_input_ids=request.GET.getlist('inputs')    
			for ids in list_of_input_ids:
				Web_dev_lix.objects.filter(Row_id=ids).delete()



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
			if not Web_dev_lix.objects.filter(Profile_Link=column[0]).exists():
				data_dict = {}
				link_lix=Web_dev_lix()
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
			Web_dev_lix.objects.filter(Profile_Link=column).delete()
			#Web_dev_lix.objects.all().delete()
			

		msg_display='Delete successfully...'




	no_result=request.GET.get('no_result')
	if no_result:
		request.session['no_result'] = request.GET.get('num').strip()    

	if 'no_result' in request.session:
		no_display = request.session['no_result']
	else:
		no_display = 500

	#SEARCH, DISPLAY AND PAGINATION

	displaytopic=Web_dev_lix.objects.all().order_by('Row_id')
   
	query = request.GET.get('q')
	if query:
		request.session['sear']='yes'
		request.session['query']=query
		displaytopic=Web_dev_lix.objects.filter(
		  
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
		response['Content-Disposition'] = 'attachment; filename="Web_development_LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
			displaytopic=Web_dev_lix.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
			response =HttpResponse(content_type='text/csv')
			writer=csv.writer(response)
			response['Content-Disposition'] = 'attachment; filename="Web_development_LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

			displaytopic1=Web_dev_lix.objects.filter(
		  
			  Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
			  
			).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


			#displaytopic=Entrepreneur1.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
			response =HttpResponse(content_type='text/csv')
			writer=csv.writer(response)
			response['Content-Disposition'] = 'attachment; filename="Web_development_LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
			displaytopic=Web_dev_lix.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
			response =HttpResponse(content_type='text/csv')
			writer=csv.writer(response)
			response['Content-Disposition'] = 'attachment; filename="Web_development_LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

	return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Web Development Linkedin (L)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )



@login_required
def web_dev_phantom_display(request):

	if request.GET.get('contact'):
		if request.GET.getlist('ids'):
			list_of_input_ids=request.GET.getlist('ids')
		   
			for ids in list_of_input_ids:
				d1=Web_dev_phantom.objects.filter(Row_id=ids)
				
				if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
					Web_dev_phantom.objects.filter(Row_id=ids).update(contact=1)

	if request.GET.get('uncontact'):
		if request.GET.getlist('ids'):
			list_of_input_ids=request.GET.getlist('ids')
			
			for ids in list_of_input_ids:
				d1=Web_dev_phantom.objects.filter(Row_id=ids)
				if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
					Web_dev_phantom.objects.filter(Row_id=ids).update(contact=0)



	if request.GET.get('pending'):
		if request.GET.getlist('ids'):
			list_of_input_ids=request.GET.getlist('ids')
		   
			for ids in list_of_input_ids:
				d1=Web_dev_phantom.objects.filter(Row_id=ids)
				
				if d1.values_list('contact')[0][0] != 2:
					Web_dev_phantom.objects.filter(Row_id=ids).update(contact=2)


	if request.GET.get('deleted'):
		if request.GET.getlist('inputs'):
			list_of_input_ids=request.GET.getlist('inputs')    
			for ids in list_of_input_ids:
				Web_dev_phantom.objects.filter(Row_id=ids).delete()


	
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
			if not Web_dev_phantom.objects.filter(profileUrl=column[0]).exists():
				data_dict = {}
				link_search=Web_dev_phantom()
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
			Web_dev_phantom.objects.filter(profileUrl=column).delete()

		msg_display='Delete successfully...'




	no_result=request.GET.get('no_result')
	if no_result:
		request.session['no_result'] = request.GET.get('num').strip()    

	if 'no_result' in request.session:
		no_display = request.session['no_result']
	else:
		no_display = 500

	#SEARCH, DISPLAY AND PAGINATION        
 

	displaytopic=Web_dev_phantom.objects.all().order_by('Row_id')
   
	query = request.GET.get('q')
	if query:
		request.session['sear']='yes'
		request.session['query']=query
		displaytopic=Web_dev_phantom.objects.filter(
		  
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
		response['Content-Disposition'] = 'attachment; filename="Web_devlopment_phantom_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
			displaytopic=Web_dev_phantom.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
			response =HttpResponse(content_type='text/csv')
			writer=csv.writer(response)
			response['Content-Disposition'] = 'attachment; filename="Web_devlopment_phantom_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
			displaytopic1=Web_dev_phantom.objects.filter(
			Q(profileUrl__icontains=query)|Q(currentJob__icontains=query)|Q(job__icontains=query)|Q(Keyword__icontains=query)|Q(location__icontains=query)|Q(fullName__icontains=query)
			).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]
			


			response =HttpResponse(content_type='text/csv')
			writer=csv.writer(response)
			response['Content-Disposition'] = 'attachment; filename="Web_devlopment_phantom_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
			
			displaytopic=Web_dev_phantom.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
			response =HttpResponse(content_type='text/csv')
			writer=csv.writer(response)
			response['Content-Disposition'] = 'attachment; filename="Web_devlopment_phantom_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
		

	return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Web Development Linkedin (P)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )



@login_required
def mobile_dev_lix(request):

    #Contact or not contact update

    if request.GET.get('contact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Mobile_dev_lix.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
                    Mobile_dev_lix.objects.filter(Row_id=ids).update(contact=1)

    if request.GET.get('uncontact'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
            
            for ids in list_of_input_ids:
                d1=Mobile_dev_lix.objects.filter(Row_id=ids)
                if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
                    Mobile_dev_lix.objects.filter(Row_id=ids).update(contact=0)


    
    if request.GET.get('pending'):
        if request.GET.getlist('ids'):
            list_of_input_ids=request.GET.getlist('ids')
           
            for ids in list_of_input_ids:
                d1=Mobile_dev_lix.objects.filter(Row_id=ids)
                
                if d1.values_list('contact')[0][0] != 2:
                    Mobile_dev_lix.objects.filter(Row_id=ids).update(contact=2)


    if request.GET.get('deleted'):
        if request.GET.getlist('inputs'):
            list_of_input_ids=request.GET.getlist('inputs')    
            for ids in list_of_input_ids:
                Mobile_dev_lix.objects.filter(Row_id=ids).delete()
                # Mobile_dev_lix.objects.all().delete()




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
            if not Mobile_dev_lix.objects.filter(Profile_Link=column[0]).exists():
                data_dict = {}
                link_lix=Mobile_dev_lix()
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
            Mobile_dev_lix.objects.filter(Profile_Link=column).delete()
            

        msg_display='Delete successfully...'




    no_result=request.GET.get('no_result')
    if no_result:
        request.session['no_result'] = request.GET.get('num').strip()    

    if 'no_result' in request.session:
        no_display = request.session['no_result']
    else:
        no_display = 500

    #SEARCH, DISPLAY AND PAGINATION

    displaytopic=Mobile_dev_lix.objects.all().order_by('Row_id')
   
    query = request.GET.get('q')
    if query:
        request.session['sear']='yes'
        request.session['query']=query
        displaytopic=Mobile_dev_lix.objects.filter(
          
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
        response['Content-Disposition'] = 'attachment; filename="Mobile Development LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            displaytopic=Mobile_dev_lix.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Mobile Development LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

            displaytopic1=Mobile_dev_lix.objects.filter(
          
              Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
              
            ).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


            #cur.execute("SELECT * FROM Mobile Development LIX;")
            
            #displaytopic=Mobile_dev_lix.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Mobile Development LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
            
            #cur.execute("SELECT * FROM Mobile Development LIX;")
            displaytopic=Mobile_dev_lix.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
            response =HttpResponse(content_type='text/csv')
            writer=csv.writer(response)
            response['Content-Disposition'] = 'attachment; filename="Mobile Development LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

    return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Mobile Development Linkedin (L)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def mobile_dev_phantom(request):

	if request.GET.get('contact'):
		if request.GET.getlist('ids'):
			list_of_input_ids=request.GET.getlist('ids')
		   
			for ids in list_of_input_ids:
				d1=Mobile_dev_phantom.objects.filter(Row_id=ids)
				
				if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
					Mobile_dev_phantom.objects.filter(Row_id=ids).update(contact=1)

	if request.GET.get('uncontact'):
		if request.GET.getlist('ids'):
			list_of_input_ids=request.GET.getlist('ids')
			
			for ids in list_of_input_ids:
				d1=Mobile_dev_phantom.objects.filter(Row_id=ids)
				if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
					Mobile_dev_phantom.objects.filter(Row_id=ids).update(contact=0)



	if request.GET.get('pending'):
		if request.GET.getlist('ids'):
			list_of_input_ids=request.GET.getlist('ids')
		   
			for ids in list_of_input_ids:
				d1=Mobile_dev_phantom.objects.filter(Row_id=ids)
				
				if d1.values_list('contact')[0][0] != 2:
					Mobile_dev_phantom.objects.filter(Row_id=ids).update(contact=2)


	if request.GET.get('deleted'):
		if request.GET.getlist('inputs'):
			list_of_input_ids=request.GET.getlist('inputs')    
			for ids in list_of_input_ids:
				Mobile_dev_phantom.objects.filter(Row_id=ids).delete()


	
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
			if not Mobile_dev_phantom.objects.filter(profileUrl=column[0]).exists():
				data_dict = {}
				link_search=Mobile_dev_phantom()
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
			Mobile_dev_phantom.objects.filter(profileUrl=column).delete()
			#Mobile_dev_phantom.objects.all().delete()
		msg_display='Delete successfully...'




	no_result=request.GET.get('no_result')
	if no_result:
		request.session['no_result'] = request.GET.get('num').strip()    

	if 'no_result' in request.session:
		no_display = request.session['no_result']
	else:
		no_display = 500

	#SEARCH, DISPLAY AND PAGINATION        
 

	displaytopic=Mobile_dev_phantom.objects.all().order_by('Row_id')
   
	query = request.GET.get('q')
	if query:
		request.session['sear']='yes'
		request.session['query']=query
		displaytopic=Mobile_dev_phantom.objects.filter(
		  
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
		response['Content-Disposition'] = 'attachment; filename="Mobile_devlopment_phantom_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
			displaytopic=Mobile_dev_phantom.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
			response =HttpResponse(content_type='text/csv')
			writer=csv.writer(response)
			response['Content-Disposition'] = 'attachment; filename="Mobile_devlopment_phantom_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
			displaytopic1=Mobile_dev_phantom.objects.filter(
			Q(profileUrl__icontains=query)|Q(currentJob__icontains=query)|Q(job__icontains=query)|Q(Keyword__icontains=query)|Q(location__icontains=query)|Q(fullName__icontains=query)
			).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]
			


			response =HttpResponse(content_type='text/csv')
			writer=csv.writer(response)
			response['Content-Disposition'] = 'attachment; filename="Mobile_devlopment_phantom_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
			
			displaytopic=Mobile_dev_phantom.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
			response =HttpResponse(content_type='text/csv')
			writer=csv.writer(response)
			response['Content-Disposition'] = 'attachment; filename="Mobile_devlopment_phantom_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
		

	return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Mobile Development Linkedin (P)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )


@login_required
def software(request):

	#Contact or not contact update

	if request.GET.get('contact'):
		if request.GET.getlist('ids'):
			list_of_input_ids=request.GET.getlist('ids')
		   
			for ids in list_of_input_ids:
				d1=Software_dev.objects.filter(Row_id=ids)
				
				if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
					Software_dev.objects.filter(Row_id=ids).update(contact=1)

	if request.GET.get('uncontact'):
		if request.GET.getlist('ids'):
			list_of_input_ids=request.GET.getlist('ids')
			
			for ids in list_of_input_ids:
				d1=Software_dev.objects.filter(Row_id=ids)
				if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
					Software_dev.objects.filter(Row_id=ids).update(contact=0)


	
	if request.GET.get('pending'):
		if request.GET.getlist('ids'):
			list_of_input_ids=request.GET.getlist('ids')
		   
			for ids in list_of_input_ids:
				d1=Software_dev.objects.filter(Row_id=ids)
				
				if d1.values_list('contact')[0][0] != 2:
					Software_dev.objects.filter(Row_id=ids).update(contact=2)


	if request.GET.get('deleted'):
		if request.GET.getlist('inputs'):
			list_of_input_ids=request.GET.getlist('inputs')    
			for ids in list_of_input_ids:
				Software_dev.objects.filter(Row_id=ids).delete()
				



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
			if not Software_dev.objects.filter(Profile_Link=column[0]).exists():
				data_dict = {}
				link_lix=Software_dev()
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
			Software_dev.objects.filter(Profile_Link=column).delete()
			

		msg_display='Delete successfully...'




	no_result=request.GET.get('no_result')
	if no_result:
		request.session['no_result'] = request.GET.get('num').strip()    

	if 'no_result' in request.session:
		no_display = request.session['no_result']
	else:
		no_display = 500

	#SEARCH, DISPLAY AND PAGINATION

	displaytopic=Software_dev.objects.all().order_by('Row_id')
   
	query = request.GET.get('q')
	if query:
		request.session['sear']='yes'
		request.session['query']=query
		displaytopic=Software_dev.objects.filter(
		  
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
		response['Content-Disposition'] = 'attachment; filename="Software Development LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
			displaytopic=Software_dev.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
			response =HttpResponse(content_type='text/csv')
			writer=csv.writer(response)
			response['Content-Disposition'] = 'attachment; filename="Software Development LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

			displaytopic1=Software_dev.objects.filter(
		  
			  Q(Profile_Link__icontains=query)|Q(Category__icontains=query)|Q(Description__icontains=query)|Q(Experience_Title__icontains=query)|Q(LinkedIn_Name__icontains=query)|Q(Location__icontains=query)
			  
			).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]


			#cur.execute("SELECT * FROM linkedin_lix;")
			
			#displaytopic=Linkedin_lix_talk.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
			response =HttpResponse(content_type='text/csv')
			writer=csv.writer(response)
			response['Content-Disposition'] = 'attachment; filename="Software Development LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
			displaytopic=Software_dev.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
			response =HttpResponse(content_type='text/csv')
			writer=csv.writer(response)
			response['Content-Disposition'] = 'attachment; filename="Software Development LIX_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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

	return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Software Development Linkedin (L)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )

@login_required
def software_dev_phantom(request):

	if request.GET.get('contact'):
		if request.GET.getlist('ids'):
			list_of_input_ids=request.GET.getlist('ids')
		   
			for ids in list_of_input_ids:
				d1=Software_dev_phantom.objects.filter(Row_id=ids)
				
				if d1.values_list('contact')[0][0] == 0 or d1.values_list('contact')[0][0] == 2:
					Software_dev_phantom.objects.filter(Row_id=ids).update(contact=1)

	if request.GET.get('uncontact'):
		if request.GET.getlist('ids'):
			list_of_input_ids=request.GET.getlist('ids')
			
			for ids in list_of_input_ids:
				d1=Software_dev_phantom.objects.filter(Row_id=ids)
				if d1.values_list('contact')[0][0] == 1 or d1.values_list('contact')[0][0] == 2:
					Software_dev_phantom.objects.filter(Row_id=ids).update(contact=0)



	if request.GET.get('pending'):
		if request.GET.getlist('ids'):
			list_of_input_ids=request.GET.getlist('ids')
		   
			for ids in list_of_input_ids:
				d1=Software_dev_phantom.objects.filter(Row_id=ids)
				
				if d1.values_list('contact')[0][0] != 2:
					Software_dev_phantom.objects.filter(Row_id=ids).update(contact=2)


	if request.GET.get('deleted'):
		if request.GET.getlist('inputs'):
			list_of_input_ids=request.GET.getlist('inputs')    
			for ids in list_of_input_ids:
				Software_dev_phantom.objects.filter(Row_id=ids).delete()


	
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
			if not Software_dev_phantom.objects.filter(profileUrl=column[0]).exists():
				data_dict = {}
				link_search=Software_dev_phantom()
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
			Software_dev_phantom.objects.filter(profileUrl=column).delete()
			#Mobile_dev_phantom.objects.all().delete()
		msg_display='Delete successfully...'




	no_result=request.GET.get('no_result')
	if no_result:
		request.session['no_result'] = request.GET.get('num').strip()    

	if 'no_result' in request.session:
		no_display = request.session['no_result']
	else:
		no_display = 500

	#SEARCH, DISPLAY AND PAGINATION        
 

	displaytopic=Software_dev_phantom.objects.all().order_by('Row_id')
   
	query = request.GET.get('q')
	if query:
		request.session['sear']='yes'
		request.session['query']=query
		displaytopic=Software_dev_phantom.objects.filter(
		  
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
		response['Content-Disposition'] = 'attachment; filename="Software Development Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
			displaytopic=Software_dev_phantom.objects.filter(Row_id__in=list_of_input_ids).order_by('Row_id')
			response =HttpResponse(content_type='text/csv')
			writer=csv.writer(response)
			response['Content-Disposition'] = 'attachment; filename="Software Development Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
			displaytopic1=Software_dev_phantom.objects.filter(
			Q(profileUrl__icontains=query)|Q(currentJob__icontains=query)|Q(job__icontains=query)|Q(Keyword__icontains=query)|Q(location__icontains=query)|Q(fullName__icontains=query)
			).order_by('Row_id')[int(request.GET.get('start_index'))-1:int(request.GET.get('end_index'))]
			


			response =HttpResponse(content_type='text/csv')
			writer=csv.writer(response)
			response['Content-Disposition'] = 'attachment; filename="Software Development Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
			
			displaytopic=Software_dev_phantom.objects.all().order_by('Row_id')[int(request.GET.get('start_index')):int(request.GET.get('end_index'))]
			response =HttpResponse(content_type='text/csv')
			writer=csv.writer(response)
			response['Content-Disposition'] = 'attachment; filename="Software Development Phantombuster_{}.csv"'.format(pd.datetime.now().strftime("%Y_%m_%d"))
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
		

	return render(request,'accounts/display.html',{'topic':users,'columns':column_names,'title':'Software Development Linkedin (P)','start_index':start_index,'end_index':end_index,'total':paginator.count,'msg':msg_display} )

def display(request):
	emp = Instagram.objects.all()
	return render(request, 'accounts/display1.html',{'emp':emp})
	
def graph_list(request):
	return render(request, 'accounts/graph.html')



def display_count(request):
   
	fb = Facebook_talk.objects.count()
	lix = Linkedin_lix_talk.objects.count()
	dm = Digital_marketing.objects.count()
	group = Linkedin_group_talk.objects.count()
	search = Linkedin_search_talk.objects.count()
	twitter2 = Twitter_talk_web2.objects.count()
	acc = Accelerators_talk_new.objects.count()
	wonder=Wonderverse.objects.count()
	blank1=blank.objects.count()
	twitter3 = Twitter_talk_web3.objects.count()
	enter=Entrepreneur1.objects.count()
	fn=Founder1.objects.count()
	sup=Scaleup1.objects.count()
	web=Web_dev_lix.objects.count()
	web_phantom=Web_dev_phantom.objects.count()
	mobile=Mobile_dev_lix.objects.count()
	mobile_phantom=Mobile_dev_phantom.objects.count()
	ds_phantom=Phantom_search_talk.objects.filter(Keyword='Data Scientist').count()
	nft_phantom=Phantom_search_talk.objects.filter(Keyword='NFT').count()
	defi_phantom=Phantom_search_talk.objects.filter(Keyword='DeFi').count()
	dapp_phantom=Phantom_search_talk.objects.filter(Keyword='DAPP').count()
	dao_phantom=Phantom_search_talk.objects.filter(Keyword='DAO').count()
	yf_phantom=Phantom_search_talk.objects.filter(Keyword='Yield Farming').count()
	ds_lix=LIX_search_talk.objects.filter(Category='Data Scientist').count()
	nft_lix=LIX_search_talk.objects.filter(Category='NFT').count()
	defi_lix=LIX_search_talk.objects.filter(Category='DeFi').count()
	dapp_lix=LIX_search_talk.objects.filter(Category='Dapp').count()
	dao_lix=LIX_search_talk.objects.filter(Category='DAO').count()
	yf_lix=LIX_search_talk.objects.filter(Category='Yield Farming').count()
	cm_phantom=CM_Phantom_talk.objects.count()
	cb_phantom=CB_Phantom_talk.objects.count()
	cman_phantom=CManag_Phantom_talk.objects.count()
	dc_phantom=DC_Phantom_talk.objects.count()
	cm_LIX=CM_LIX_talk.objects.count()
	cb_LIX=CB_LIX_talk.objects.count()
	cman_LIX=CManag_LIX_talk.objects.count()
	dc_LIX=DC_LIX_talk.objects.count()
	block_lix=Blockchain_LIX.objects.count()
	da_lix=Data_analysis.objects.count()
	vf_lix=Venture_funding.objects.count()
	pm_lix=Product_fit.objects.count()
	enter_phantom=Entrepreneur_Phantom.objects.count()
	fn_phantom=Founder_Phantom.objects.count()
	uiux = UIUX.objects.count()
	sw=Software_dev.objects.count()
	sw_phantom=Software_dev_phantom.objects.count()
	block_phantom=Blockchain_LIX_phantom.objects.count()
	digital_marketing_phantom=Digital_marketing_phantom.objects.count()
	da_phantom=Data_analysis_phantom.objects.count()
	vf_phantom=Venture_funding_phantom.objects.count()
	uiux_phantom=UIUX_phantom.objects.count()
	pm_phantom=Product_fit_phantom.objects.count()

	cb_twi_count=cb_twi.objects.count()
	cg_twi_count=cg_twi.objects.count()
	cm_twi_count=cm_twi.objects.count()
	twi_marketing_count=twi_marketing.objects.count()
	web3_com_twi_count=web3_com_twi.objects.count()
	web3_marketing_twi_count=web3_marketing_twi.objects.count()
	chatbot_twi_count=chatbot_twi.objects.count()
	discordbot_twi_count=discordbot_twi.objects.count()

	vnf_lix=Venture_capital_LIX.objects.count()
	ani_lix=Angle_investor_LIX.objects.count()
	sc_lix=Seed_capital_LIX.objects.count()
	fr_lix=Fundraising_LIX.objects.count()
	pi_lix=Private_investor_LIX.objects.count()

	vc_phantom=Venture_capital_phantom.objects.count()
	angle_phantom=Angle_investor_phantom.objects.count()
	sc_phantom=Seed_capital_phantom.objects.count()
	fr_phantom=Fundraising_phantom.objects.count()
	pi_phantom=Private_investor_phantom.objects.count()

	vc_fb=venture_capital_fb.objects.count()
	ai_fb=angle_investor_fb.objects.count()
	pd_fb=pitchdesk_fb.objects.count()
	pi_fb=private_investor_fb.objects.count()
	ba_fb=business_angle_fb.objects.count()

		
	vc_twi=venture_capital_twi.objects.count()
	angel_twi=angle_investor_twi.objects.count()
	sc_twi=seed_capital_twi.objects.count()
	wf_twi=web3_fund_twi.objects.count()
	wg_twi=web3_grants_twi.objects.count()
	wp_twi=whitepaper_twi.objects.count()
	pd_twi=pitchdesk_twi.objects.count()
	pi_twi=private_investor_twi.objects.count()
	ba_twi=business_angle_twi.objects.count()
	wi_twi=web3_investor_twi.objects.count()
	fr_twi=fundraising_twi.objects.count()

	d3_twi=d3_design_twi.objects.count()
	gd_twi=graphics_design_twi.objects.count()
	vd_twi=visual_design_twi.objects.count()
	md_twi=marketing_designer_twi.objects.count()
	bc_twi=branding_consultant_twi.objects.count()

	d3_lix=d3_design_LIX.objects.count()
	gd_lix=graphics_design_LIX.objects.count()
	vd_lix=visual_design_LIX.objects.count()
	md_lix=marketing_designer_LIX.objects.count()
	bc_lix=branding_consultant_LIX.objects.count()

	d3_phantom=d3_design_phantom.objects.count()
	gd_phantom=graphics_design_phantom.objects.count()
	vd_phantom=visual_design_phantom.objects.count()
	md_phantom=marketing_designer_phantom.objects.count()
	bc_phantom=branding_consultant_phantom.objects.count()

	d3_fb=d3_design_fb.objects.count()
	gd_fb=graphics_design_fb.objects.count()

	ai_phantom=artificial_intelligence_phantom.objects.count()
	ml_phantom=machine_learning_phantom.objects.count()
	algo_phantom=algorithm_phantom.objects.count()
	dm_phantom=data_mining_phantom.objects.count()
	ann_phantom=neural_network_phantom.objects.count()
	dp_phantom=data_prediction_phantom.objects.count()

	ai_lix=artificial_intelligence_LIX.objects.count()
	ml_lix=machine_learning_LIX.objects.count()
	algo_lix=algorithm_LIX.objects.count()
	dm_lix=data_mining_LIX.objects.count()
	ann_lix=neural_network_LIX.objects.count()
	dp_lix=data_prediction_LIX.objects.count()

	ai_fb=artificial_intelligence_fb.objects.count()
	ml_fb=machine_learning_fb.objects.count()
	algo_fb=algorithm_fb.objects.count()
	dm_fb=data_mining_fb.objects.count()
	ann_fb=neural_network_fb.objects.count()
	
	ai_twi=artificial_intelligence_twi.objects.count()
	ml_twi=machine_learning_twi.objects.count()
	algo_twi=algorithm_twi.objects.count()
	dm_twi=data_mining_twi.objects.count()
	ann_twi=neural_network_twi.objects.count()
	dp_twi=data_prediction_twi.objects.count()

	digi_fb=Digital_marketing_fb.objects.count()
	block_fb=Blockchain_fb.objects.count()
	sd_fb=software_development_fb.objects.count()
	da_fb=data_analysis_fb.objects.count()
	ux_ui_fb=UX_fb.objects.count()

	enter_fb=Entrepreneurship_fb.objects.count()
	uiux_instagram=UIUX_insta.objects.count()
	enter_insta=Entrepreneurship_insta.objects.count()
	digi_insta=Digital_marketing_insta.objects.count()
	dmar_twi=Digital_marketing_twi.objects.count()
	enter_twi=Entrepreneurship_twi.objects.count()
	uxuidesign_twi=uxui_twi.objects.count()
	


	figma_lix=Figma_LIX_talk.objects.count()
	miro_lix=Miro_LIX_talk.objects.count()
	notion_lix=Notion_LIX_talk.objects.count()
	slack_lix=Slack_LIX_talk.objects.count()
	trello_lix=Trello_LIX_talk.objects.count()

	micromenter_insta=MicroMentor_insta_talk.objects.count()
	menterpass_insta=MentorPass_insta_talk.objects.count()
	micromenter_twi=MicroMentor_twi_talk.objects.count()
	menterpass_twi=MentorPass_twi_talk.objects.count()

	figma_twi=Figma_twi_talk.objects.count()
	onalytica_twi=Onalytica_twi_talk.objects.count()
	slack_twi=Slack_twi_talk.objects.count()
	trello_twi=Trello_twi_talk.objects.count()
	miro_twi=Miro_twi_talk.objects.count()
	notion_twi=Notion_twi_talk.objects.count()

	figma_phantom=Figma_phantom_talk.objects.count()
	notion_phantom=Notion_phantom_talk.objects.count()
	slack_phantom=Slack_phantom_talk.objects.count()
	trello_phantom=Trello_phantom_talk.objects.count()

	bd_design_lix=Brand_Designers_LIX_talk.objects.count()
	bd_design_phantom=Brand_Designers_phantom_talk.objects.count()

	algo_fb_ads= algorithm_fb_ads.objects.count()
	ai_fb_ads= artificial_intelligence_fb_ads.objects.count()
	dataanalysis_fb_ads= data_analysis_fb_ads.objects.count()
	dm_fb_ads= data_mining_fb_ads.objects.count()
	ml_fb_ads= machine_learning_fb_ads.objects.count()
	ann_fb_ads= neural_network_fb_ads.objects.count()
	algo_lix_ads= algorithm_LIX_ads.objects.count()
	ai_lix_ads= artificial_intelligence_LIX_ads.objects.count()
	dataanalysis_lix_ads= data_analysis_LIX_ads.objects.count()
	dm_lix_ads= data_mining_LIX_ads.objects.count()
	dp_lix_ads= data_prediction_LIX_ads.objects.count()
	ds_lix_ads= data_scientist_LIX_ads.objects.count()
	ml_lix_ads= machine_learning_LIX_ads.objects.count()
	ann_lix_ads= neural_network_LIX_ads.objects.count()
	algo_phantom_ads= algorithm_phantom_ads.objects.count()
	ai_phantom_ads= artificial_intelligence_phantom_ads.objects.count()
	dataanalysis_phantom_ads= data_analysis_phantom_ads.objects.count()
	dm_phantom_ads= data_mining_phantom_ads.objects.count()
	dp_phantom_ads= data_prediction_phantom_ads.objects.count()
	ds_phantom_ads= data_scientist_phantom_ads.objects.count()
	ml_phantom_ads= machine_learning_phantom_ads.objects.count()
	ann_phantom_ads= neural_network_phantom_ads.objects.count()
	algo_twi_ads= algorithm_twi_ads.objects.count()
	ai_twi_ads= artificial_intelligence_twi_ads.objects.count()
	dm_twi_ads= data_mining_twi_ads.objects.count()
	dp_twi_ads= data_prediction_twi_ads.objects.count()
	ml_twi_ads= machine_learning_twi_ads.objects.count()
	ann_twi_ads= neural_networks_twi_ads.objects.count()


	figma_lix_ads= figma_LIX_talk_ads.objects.count()
	miro_lix_ads= miro_LIX_talk_ads.objects.count()
	notion_lix_ads= notion_LIX_talk_ads.objects.count()
	slack_lix_ads= slack_LIX_talk_ads.objects.count()
	trello_lix_ads= trello_LIX_talk_ads.objects.count()
	figma_phantom_ads= figma_phantom_talk_ads.objects.count()
	notion_phantom_ads= notion_phantom_talk_ads.objects.count()
	slack_phantom_ads= slack_phantom_talk_ads.objects.count()
	trello_phantom_ads= trello_phantom_talk_ads.objects.count()
	figma_twi_ads= figma_twi_talk_ads.objects.count()
	miro_twi_ads= miro_twi_talk_ads.objects.count()
	notion_twi_ads= notion_twi_talk_ads.objects.count()
	onalytica_twi_ads= onalytica_twi_talk_ads.objects.count()
	slack_twi_ads= slack_twi_talk_ads.objects.count()
	trello_twi_ads= trello_twi_talk_ads.objects.count()

	cb_lix_ads= CB_LIX_talk_ads.objects.count()
	cmanag_lix_ads= CManag_LIX_talk_ads.objects.count()
	cm_lix_ads= CM_LIX_talk_ads.objects.count()
	dc_lix_ads= DC_LIX_talk_ads.objects.count()
	cb_phantom_ads= CB_phantom_talk_ads.objects.count()
	cmanag_phantom_ads= CManag_phantom_talk_ads.objects.count()
	cm_phantom_ads= CM_phantom_talk_ads.objects.count()
	dc_phantom_ads= DC_phantom_talk_ads.objects.count()
	chatbot_twi_ads= chatbot_twi_talk_ads.objects.count()
	cb_twi_ads= CB_twi_talk_ads.objects.count()
	cg_twi_ads= CG_twi_talk_ads.objects.count()
	cm_twi_ads= CManag_twi_talk_ads.objects.count()
	db_twi_ads= discordbot_twi_talk_ads.objects.count()
	twi_marketing_twi_ads= twitter_marketing_twi_talk_ads.objects.count()
	web3_commu_twi_ads= web3_community_twi_talk_ads.objects.count()
	web3_marketing_twi_ads= web3_marketing_twi_talk_ads.objects.count()


	enterpreneurs_fb_ads= enterpreneurs_fb_talk_ads.objects.count()
	enterpreneurs_lix__ads= enterpreneurs_LIX_talk_ads.objects.count()
	founder_lix_ads= founder_LIX_talk_ads.objects.count()
	enterpreneurs_phantom_ads= enterpreneurs_phantom_talk_ads.objects.count()
	founders_phantom_ads= founders_phantom_talk_ads.objects.count()
	enterpreneurs_twi_ads= enterpreneurs_twi_talk_ads.objects.count()

	d3_design_fb_ads= d3_design_fb_talk_ads.objects.count()
	graphic_design_fb_ads= graphic_design_fb_talk_ads.objects.count()
	uiux_design_fb_ads= uiux_design_fb_talk_ads.objects.count()
	d3_design_lix_ads= d3_design_LIX_talk_ads.objects.count()
	brand_designers_lix_ads= brand_designers_LIX_talk_ads.objects.count()
	branding_consultant_lix_ads= branding_consultant_LIX_talk_ads.objects.count()
	graphic_design_lix_ads= graphic_design_LIX_talk_ads.objects.count()
	marketing_designer_lix_ads= marketing_designer_LIX_talk_ads.objects.count()
	uiux_lix_ads= uiux_LIX_talk_ads.objects.count()
	visual_design_lix_ads= visual_design_LIX_talk_ads.objects.count()
	d3_design_phantom_ads= d3_design_phantom_talk_ads.objects.count()
	brand_designers_phantom_ads= brand_designers_phantom_talk_ads.objects.count()
	branding_consultant_phantom_ads= branding_consultant_phantom_talk_ads.objects.count()
	graphic_design_phantom_ads= graphic_design_phantom_talk_ads.objects.count()
	marketing_designer_phantom_ads= marketing_designer_phantom_talk_ads.objects.count()
	uiux_design_phantom_ads= uiux_design_phantom_talk_ads.objects.count()
	visual_design_phantom_ads= visual_design_phantom_talk_ads.objects.count()
	d3_design_twi_ads= d3_design_twi_talk_ads.objects.count()
	branding_consultant_twi_ads= branding_consultant_twi_talk_ads.objects.count()
	graphic_design_twi_ads= graphic_design_twi_talk_ads.objects.count()
	marketing_designer_twi_ads= marketing_designer_twi_talk_ads.objects.count()
	uiux_design_twi_ads= uiux_design_twi_talk_ads.objects.count()
	visual_design_twi_ads= visual_design_twi_talk_ads.objects.count()

	micromentor_twi_ads= micromentor_twi_talk_ads.objects.count()
	mentorpass_twi_ads= mentorpass_twi_talk_ads.objects.count()

	digital_marketing_fb_ads= digital_marketing_fb_talk_ads.objects.count()
	digital_marketing_lix_ads= digital_marketing_LIX_talk_ads.objects.count()
	digital_marketing_phantom_ads= digital_marketing_phantom_talk_ads.objects.count()
	digital_marketing_twi_ads= digital_marketing_twi_talk_ads.objects.count()

	pm_fit_lix_ads= pm_fit_LIX_talk_ads.objects.count()
	pm_fit_phantom_ads= pm_fit_phantom_talk_ads.objects.count()

	software_development_fb_ads= software_development_fb_talk_ads.objects.count()
	mobile_development_lix_ads= mobile_development_LIX_talk_ads.objects.count()
	software_development_lix_ads= software_development_LIX_talk_ads.objects.count()
	web_development_lix_ads= web_development_LIX_talk_ads.objects.count()
	mobile_development_phantom_ads= mobile_development_phantom_talk_ads.objects.count()
	software_development_phantom_ads= software_development_phantom_talk_ads.objects.count()
	web_development_phantom_ads= web_development_phantom_talk_ads.objects.count()

	angle_investor_fb_ads= angle_investor_fb_talk_ads.objects.count()
	business_angle_fb_ads= business_angle_fb_talk_ads.objects.count()
	pitchdesk_fb_ads= pitchdesk_fb_talk_ads.objects.count()
	private_investor_fb_ads= private_investor_fb_talk_ads.objects.count()
	venture_capital_fb_ads= venture_capital_fb_talk_ads.objects.count()
	angle_investor_lix_ads= angle_investor_LIX_talk_ads.objects.count()
	fundraising_lix_ads= fundraising_LIX_talk_ads.objects.count()
	private_investor_lix_ads= private_investor_LIX_talk_ads.objects.count()
	seed_capital_lix_ads= seed_capital_LIX_talk_ads.objects.count()
	venture_capital_lix_ads= venture_capital_LIX_talk_ads.objects.count()
	angle_investor_phantom_ads= angle_investor_phantom_talk_ads.objects.count()
	fundraising_phantom_ads= fundraising_phantom_talk_ads.objects.count()
	private_investor_phantom_ads= private_investor_phantom_talk_ads.objects.count()
	seed_capital_phantom_ads= seed_capital_phantom_talk_ads.objects.count()
	venture_capital_phantom_ads= venture_capital_phantom_talk_ads.objects.count()
	angle_investor_twi_ads= angle_investor_twi_talk_ads.objects.count()
	business_angle_twi_ads= business_angle_twi_talk_ads.objects.count()
	fundraising_twi_ads= fundraising_twi_talk_ads.objects.count()
	pitchdesk_twi_ads= pitchdesk_twi_talk_ads.objects.count()
	private_investor_twi_ads= private_investor_twi_talk_ads.objects.count()
	seed_capital_twi_ads= seed_capital_twi_talk_ads.objects.count()
	venture_capital_twi_ads= venture_capital_twi_talk_ads.objects.count()
	web3_fund_twi_ads= web3_fund_twi_talk_ads.objects.count()
	web3_grants_twi_ads= web3_grants_twi_talk_ads.objects.count()
	web3_investor_twi_ads= web3_investor_twi_talk_ads.objects.count()
	whitepaper_twi_ads= whitepaper_twi_talk_ads.objects.count()

	blockchain_fb_ads= blockchain_fb_talk_ads.objects.count()
	blockchain_lix_ads= blockchain_LIX_talk_ads_spaced.objects.count()
	dao_lix_ads= dao_LIX_talk_ads.objects.count()
	dapp_lix_ads= dapp_LIX_talk_ads.objects.count()
	defi_lix_ads= defi_LIX_talk_ads.objects.count()
	nft_lix_ads= nft_LIX_talk_ads.objects.count()
	yield_farming_lix_ads= yield_farming_LIX_talk_ads.objects.count()
	blockchain_phantom_ads= blockchain_phantom_talk_ads.objects.count()
	dao_phantom_ads= dao_phantom_talk_ads.objects.count()
	dapp_phantom_ads= dapp_phantom_talk_ads.objects.count()
	defi_phantom_ads= defi_phantom_talk_ads.objects.count()
	nft_phantom_ads= nft_phantom_talk_ads.objects.count()
	yield_farming_phantom_ads= yield_farming_phantom_talk_ads.objects.count()

	entrepreneurs_insta_ads= entrepreneurs_insta_talk_ads.objects.count()
	digital_marketing_insta_ads= digital_marketing_insta_talk_ads.objects.count()
	uiux_insta_ads= uiux_insta_talk_ads.objects.count()
	micromente_insta_ads= micromente_insta_talk_ads.objects.count()
	menterpass_insta_ads= menterpass_insta_talk_ads.objects.count()

	defi_twi= defi_talk_twi.objects.count()
	defi_twi_ads= defi_talk_twi_ads.objects.count()




	total_count=fb+lix+group+search+acc+wonder+blank1+twitter3+enter+fn+sup+web+web_phantom+ds_phantom+nft_phantom+defi_phantom+dapp_phantom+dao_phantom+yf_phantom+ds_lix+nft_lix+defi_lix+dapp_lix+dao_lix+yf_lix+mobile+mobile_phantom+enter_phantom+fn_phantom+dm+block_lix+da_lix+vf_lix+uiux+sw+sw_phantom+block_phantom+digital_marketing_phantom+da_phantom+vf_phantom+pm_lix+uiux_phantom+pm_phantom+cb_twi_count+cg_twi_count+cm_twi_count+twi_marketing_count+web3_com_twi_count+web3_marketing_twi_count+chatbot_twi_count+discordbot_twi_count+vnf_lix+ani_lix+sc_lix+fr_lix+pi_lix+vc_phantom+angle_phantom+sc_phantom+fr_phantom+vc_fb+ai_fb+pd_fb+pi_fb+ba_fb+vc_twi+angel_twi+sc_twi+wf_twi+wg_twi+fr_twi+wp_twi+pd_twi+pi_twi+ba_twi+wi_twi+d3_twi+gd_twi+d3_fb+gd_fb+d3_lix+gd_lix+vd_lix+md_lix+bc_lix+d3_phantom+gd_phantom+vd_phantom+md_phantom+bc_phantom+ai_phantom+ml_phantom+algo_phantom+dm_phantom+ann_phantom+dp_phantom+ai_lix+ml_lix+algo_lix+dm_lix+ann_lix+dp_lix+ai_fb+ml_fb+algo_fb+dm_fb+ann_fb+ai_twi+ml_twi+algo_twi+dm_twi+ann_twi+dp_twi+digi_fb+block_fb+sd_fb+da_fb+ux_ui_fb+enter_fb+uiux_instagram+enter_insta+digi_insta+dmar_twi+enter_twi+uxuidesign_twi+figma_lix+miro_lix+notion_lix+slack_lix+trello_lix+micromenter_insta+figma_twi+onalytica_twi+slack_twi+trello_twi+miro_twi+notion_twi+micromenter_twi+menterpass_twi+figma_phantom+notion_phantom+slack_phantom+trello_phantom+bd_design_lix+bd_design_phantom+defi_twi

	total_count_ads=algo_fb_ads+ai_fb_ads+dataanalysis_fb_ads+dm_fb_ads+ml_fb_ads+ann_fb_ads+algo_lix_ads+ai_lix_ads+dataanalysis_lix_ads+dm_lix_ads+dp_lix_ads+ds_lix_ads+ml_lix_ads+ann_lix_ads+algo_phantom_ads+ai_phantom_ads+dataanalysis_phantom_ads+dm_phantom_ads+dp_phantom_ads+ds_phantom_ads+ml_phantom_ads+ann_phantom_ads+algo_twi_ads+ai_twi_ads+dm_twi_ads+dp_twi_ads+ml_twi_ads+ann_twi_ads+figma_lix_ads+miro_lix_ads+notion_lix_ads+slack_lix_ads+trello_lix_ads+figma_phantom_ads+notion_phantom_ads+slack_phantom_ads+trello_phantom_ads+figma_twi_ads+miro_twi_ads+notion_twi_ads+onalytica_twi_ads+slack_twi_ads+trello_twi_ads+ cb_lix_ads+cmanag_lix_ads+cm_lix_ads+dc_lix_ads+cb_phantom_ads+cmanag_phantom_ads+cm_phantom_ads+dc_phantom_ads+chatbot_twi_ads+cb_twi_ads+cg_twi_ads+cm_twi_ads+db_twi_ads+twi_marketing_twi_ads+web3_commu_twi_ads+web3_marketing_twi_ads+enterpreneurs_fb_ads+enterpreneurs_lix__ads+founder_lix_ads+enterpreneurs_phantom_ads+founders_phantom_ads+enterpreneurs_twi_ads+d3_design_fb_ads+graphic_design_fb_ads+uiux_design_fb_ads+d3_design_lix_ads+brand_designers_lix_ads+branding_consultant_lix_ads+graphic_design_lix_ads+marketing_designer_lix_ads+uiux_lix_ads+visual_design_lix_ads+d3_design_phantom_ads+brand_designers_phantom_ads+branding_consultant_phantom_ads+graphic_design_phantom_ads+marketing_designer_phantom_ads+uiux_design_phantom_ads+visual_design_phantom_ads+d3_design_twi_ads+branding_consultant_twi_ads+graphic_design_twi_ads+marketing_designer_twi_ads+uiux_design_twi_ads+visual_design_twi_ads+micromentor_twi_ads+mentorpass_twi_ads+digital_marketing_fb_ads+digital_marketing_lix_ads+digital_marketing_phantom_ads,digital_marketing_twi_ads,pm_fit_lix_ads,pm_fit_phantom_ads+software_development_fb_ads+mobile_development_lix_ads+software_development_lix_ads+web_development_lix_ads+mobile_development_phantom_ads+software_development_phantom_ads+web_development_phantom_ads+angle_investor_fb_ads+business_angle_fb_ads+pitchdesk_fb_ads+private_investor_fb_ads+venture_capital_fb_ads+angle_investor_lix_ads+fundraising_lix_ads+private_investor_lix_ads+seed_capital_lix_ads+venture_capital_lix_ads+angle_investor_phantom_ads+fundraising_phantom_ads+seed_capital_phantom_ads+venture_capital_phantom_ads+angle_investor_twi_ads+business_angle_twi_ads+fundraising_twi_ads+pitchdesk_twi_ads+private_investor_twi_ads+seed_capital_twi_ads,+venture_capital_twi_ads+web3_fund_twi_ads+web3_grants_twi_ads+web3_investor_twi_ads+whitepaper_twi_ads+blockchain_fb_ads+blockchain_lix_ads+dao_lix_ads+dapp_lix_ads+defi_lix_ads+nft_lix_ads+yield_farming_lix_ads+blockchain_phantom_ads+dao_phantom_ads+dapp_phantom_ads+defi_phantom_ads+nft_phantom_ads+yield_farming_phantom_ads+entrepreneurs_insta_ads+digital_marketing_insta_ads+uiux_insta_ads+micromente_insta_ads+menterpass_insta_ads+defi_twi_ads


	return render(request, 'accounts/display_list.html',{'fb':fb,'lix':lix,'group':group,'search':search,'twitter2':twitter2,'acc':acc,'wonder':wonder,'blank':blank1,'twitter3':twitter3,'enter':enter,'fn':fn,'sup':sup,'total':total_count,'web':web,'web_phantom':web_phantom,'ds_phantom':ds_phantom,'nft_phantom':nft_phantom,'defi_phantom':defi_phantom,'dapp_phantom':dapp_phantom,'dao_phantom':dao_phantom,'yf_phantom':yf_phantom,'ds_lix':ds_lix,'nft_lix':nft_lix,'defi_lix':defi_lix,'dapp_lix':dapp_lix,'dao_lix':dao_lix,'yf_lix':yf_lix,'mobile':mobile,'mobile_phantom':mobile_phantom,'cm_phantom':cm_phantom,'cb_phantom':cb_phantom,'cman_phantom':cman_phantom,'dc_phantom':dc_phantom,'cm_LIX':cm_LIX,'cb_LIX':cb_LIX,'cman_LIX':cman_LIX,'dc_LIX':dc_LIX,'enter_phantom':enter_phantom,'fn_phantom':fn_phantom,'dm':dm,'block_lix':block_lix,'da_lix':da_lix,'vf_lix':vf_lix,'uiux':uiux,'sw':sw,'sw_phantom':sw_phantom,'digital_marketing_phantom':digital_marketing_phantom,'dm_phantom':dm_phantom,'da_phantom':da_phantom,'vf_phantom':vf_phantom,'pm_lix':pm_lix,'uiux_phantom':uiux_phantom,'pm_phantom':pm_phantom,'cb_twi_count':cb_twi_count,'cg_twi_count':cg_twi_count,'cm_twi_count':cm_twi_count,'twi_marketing_count':twi_marketing_count,'web3_com_twi_count':web3_com_twi_count,'web3_marketing_twi_count':web3_marketing_twi_count,'chatbot_twi_count':chatbot_twi_count,'discordbot_twi_count':discordbot_twi_count,'vnf_lix':vnf_lix,'ani_lix':ani_lix,'sc_lix':sc_lix,'fr_lix':fr_lix,'pi_lix':pi_lix,'vc_phantom':vc_phantom,'angle_phantom':angle_phantom,'sc_phantom':sc_phantom,'fr_phantom':fr_phantom,'vc_fb':vc_fb,'ai_fb':ai_fb,'pd_fb':pd_fb,'pi_fb':pi_fb,'ba_fb':ba_fb,'vc_twi':vc_twi,'angel_twi':angel_twi,'sc_twi':sc_twi,'wf_twi':wf_twi,'wg_twi':wg_twi,'fr_twi':fr_twi,'wp_twi':wp_twi,'pd_twi':pd_twi,'pi_twi':pi_twi,'ba_twi':ba_twi,'wi_twi':wi_twi,'d3_twi':d3_twi,'gd_twi':gd_twi,'vd_twi':vd_twi,'md_twi':md_twi,'bc_twi':bc_twi,'d3_fb':d3_fb,'gd_fb':gd_fb,'d3_lix':d3_lix,'gd_lix':gd_lix,'vd_lix':vd_lix,'md_lix':md_lix,'bc_lix':bc_lix,'d3_phantom':d3_phantom,'gd_phantom':gd_phantom,'vd_phantom':vd_phantom,'md_phantom':md_phantom,'block_phantom':block_phantom,'ai_phantom':ai_phantom,'ml_phantom':ml_phantom,'algo_phantom':algo_phantom,'dm_phantom':dm_phantom,'ann_phantom':ann_phantom,'dp_phantom':dp_phantom,'ai_lix':ai_lix,'ml_lix':ml_lix,'algo_lix':algo_lix,'dm_lix':dm_lix,'ann_lix':ann_lix,'dp_lix':dp_lix,'ai_fb':ai_fb,'ml_fb':ml_fb,'algo_fb':algo_fb,'dm1_fb':dm_fb,'ann_fb':ann_fb,'ai_twi':ai_twi,'ml_twi':ml_twi,'algo_twi':algo_twi,'dm_twi':dm_twi,'ann_twi':ann_twi,'dp_twi':dp_twi,'digi_fb':digi_fb,'block_fb':block_fb,'sd_fb':sd_fb,'da_fb':da_fb,'ux_ui_fb':ux_ui_fb,'enter_fb':enter_fb,'uiux_instagram':uiux_instagram,'enter_insta':enter_insta,'digi_insta':digi_insta,'dmar_twi':dmar_twi,'enter_twi':enter_twi,'uxuidesign_twi':uxuidesign_twi,'figma_lix':figma_lix,'miro_lix':miro_lix,'notion_lix':notion_lix,'slack_lix':slack_lix,'trello_lix':trello_lix,'micromenter_insta':micromenter_insta,'menterpass_insta':menterpass_insta,'figma_twi':figma_twi,'onalytica_twi':onalytica_twi,'slack_twi':slack_twi,'trello_twi':trello_twi,'miro_twi':miro_twi,'notion_twi':notion_twi,'micromenter_twi':micromenter_twi,'menterpass_twi':menterpass_twi,'figma_phantom':figma_phantom,'notion_phantom':notion_phantom,'slack_phantom':slack_phantom,'trello_phantom':trello_phantom,'bd_design_lix':bd_design_lix,'bd_design_phantom':bd_design_phantom,'algo_fb_ads':algo_fb_ads,'ai_fb_ads':ai_fb_ads,'dataanalysis_fb_ads':dataanalysis_fb_ads,'dm_fb_ads':dm_fb_ads,'ml_fb_ads':ml_fb_ads,'ann_fb_ads':ann_fb_ads,'algo_lix_ads':algo_lix_ads,'ai_lix_ads':ai_lix_ads,'dataanalysis_lix_ads':dataanalysis_lix_ads,'dm_lix_ads':dm_lix_ads,'dp_lix_ads':dp_lix_ads,'ds_lix_ads':ds_lix_ads,'ml_lix_ads':ml_lix_ads,'ann_lix_ads':ann_lix_ads,'algo_phantom_ads':algo_phantom_ads,'ai_phantom_ads':ai_phantom_ads,'dataanalysis_phantom_ads':dataanalysis_phantom_ads,'dm_phantom_ads':dm_phantom_ads,'dp_phantom_ads':dp_phantom_ads,'ds_phantom_ads':ds_phantom_ads,'ml_phantom_ads':ml_phantom_ads,'ann_phantom_ads':ann_phantom_ads,'algo_twi_ads':algo_twi_ads,'ai_twi_ads':ai_twi_ads,'dm_twi_ads':dm_twi_ads,'dp_twi_ads':dp_twi_ads,'ml_twi_ads':ml_twi_ads,'ann_twi_ads':ann_twi_ads,'figma_lix_ads':figma_lix_ads,'miro_lix_ads':miro_lix_ads,'notion_lix_ads':notion_lix_ads,'slack_lix_ads':slack_lix_ads,'trello_lix_ads':trello_lix_ads,'figma_phantom_ads':figma_phantom_ads,'notion_phantom_ads':notion_phantom_ads,'slack_phantom_ads':slack_phantom_ads,'trello_phantom_ads':trello_phantom_ads,'figma_twi_ads':figma_twi_ads,'miro_twi_ads':miro_twi_ads,'notion_twi_ads':notion_twi_ads,'onalytica_twi_ads':onalytica_twi_ads,'slack_twi_ads':slack_twi_ads,'trello_twi_ads':trello_twi_ads,'cb_lix_ads':cb_lix_ads,'cmanag_lix_ads':cmanag_lix_ads,'cm_lix_ads':cm_lix_ads,'dc_lix_ads':dc_lix_ads,'cb_phantom_ads':cb_phantom_ads,'cmanag_phantom_ads':cmanag_phantom_ads,'cm_phantom_ads':cm_phantom_ads,'dc_phantom_ads':dc_phantom_ads,'chatbot_twi_ads':chatbot_twi_ads,'cb_twi_ads':cb_twi_ads,'cg_twi_ads':cg_twi_ads,'cm_twi_ads':cm_twi_ads,'db_twi_ads':db_twi_ads,'twi_marketing_twi_ads':twi_marketing_twi_ads,'web3_commu_twi_ads':web3_commu_twi_ads,'web3_marketing_twi_ads':web3_marketing_twi_ads,'enterpreneurs_fb_ads':enterpreneurs_fb_ads,'enterpreneurs_lix__ads':enterpreneurs_lix__ads,'founder_lix_ads':founder_lix_ads,'enterpreneurs_phantom_ads':enterpreneurs_phantom_ads,'founders_phantom_ads':founders_phantom_ads,'enterpreneurs_twi_ads':enterpreneurs_twi_ads,'d3_design_fb_ads':d3_design_fb_ads,'graphic_design_fb_ads':graphic_design_fb_ads,'uiux_design_fb_ads':uiux_design_fb_ads,'d3_design_lix_ads':d3_design_lix_ads,'brand_designers_lix_ads':brand_designers_lix_ads,'branding_consultant_lix_ads':branding_consultant_lix_ads,'graphic_design_lix_ads':graphic_design_lix_ads,'marketing_designer_lix_ads':marketing_designer_lix_ads,'uiux_lix_ads':uiux_lix_ads,'visual_design_lix_ads':visual_design_lix_ads,'d3_design_phantom_ads':d3_design_phantom_ads,'brand_designers_phantom_ads':brand_designers_phantom_ads,'branding_consultant_phantom_ads':branding_consultant_phantom_ads,'graphic_design_phantom_ads':graphic_design_phantom_ads,'marketing_designer_phantom_ads':marketing_designer_phantom_ads,'uiux_design_phantom_ads':uiux_design_phantom_ads,'visual_design_phantom_ads':visual_design_phantom_ads,'d3_design_twi_ads':d3_design_twi_ads,'branding_consultant_twi_ads':branding_consultant_twi_ads,'graphic_design_twi_ads':graphic_design_twi_ads,'marketing_designer_twi_ads':marketing_designer_twi_ads,'uiux_design_twi_ads':uiux_design_twi_ads,'visual_design_twi_ads':visual_design_twi_ads,'micromentor_twi_ads':micromentor_twi_ads,'mentorpass_twi_ads':mentorpass_twi_ads,'digital_marketing_fb_ads':digital_marketing_fb_ads,'digital_marketing_lix_ads':digital_marketing_lix_ads,'digital_marketing_phantom_ads':digital_marketing_phantom_ads,'digital_marketing_twi_ads':digital_marketing_twi_ads,'pm_fit_lix_ads':pm_fit_lix_ads,'pm_fit_phantom_ads':pm_fit_phantom_ads,'software_development_fb_ads':software_development_fb_ads,'mobile_development_lix_ads':mobile_development_lix_ads,'software_development_lix_ads':software_development_lix_ads,'web_development_lix_ads':web_development_lix_ads,'mobile_development_phantom_ads':mobile_development_phantom_ads,'software_development_phantom_ads':software_development_phantom_ads,'web_development_phantom_ads':web_development_phantom_ads,'angle_investor_fb_ads':angle_investor_fb_ads,'business_angle_fb_ads':business_angle_fb_ads,'pitchdesk_fb_ads':pitchdesk_fb_ads,'private_investor_fb_ads':private_investor_fb_ads,'venture_capital_fb_ads':venture_capital_fb_ads,'angle_investor_lix_ads':angle_investor_lix_ads,'fundraising_lix_ads':fundraising_lix_ads,'private_investor_lix_ads':private_investor_lix_ads,'seed_capital_lix_ads':seed_capital_lix_ads,'venture_capital_lix_ads':venture_capital_lix_ads,'angle_investor_phantom_ads':angle_investor_phantom_ads,'fundraising_phantom_ads':fundraising_phantom_ads,'seed_capital_phantom_ads':seed_capital_phantom_ads,'venture_capital_phantom_ads':venture_capital_phantom_ads,'angle_investor_twi_ads':angle_investor_twi_ads,'business_angle_twi_ads':business_angle_twi_ads,'fundraising_twi_ads':fundraising_twi_ads,'pitchdesk_twi_ads':pitchdesk_twi_ads,'private_investor_twi_ads':private_investor_twi_ads,'seed_capital_twi_ads':seed_capital_twi_ads,'venture_capital_twi_ads':venture_capital_twi_ads,'web3_fund_twi_ads':web3_fund_twi_ads,'web3_grants_twi_ads':web3_grants_twi_ads,'web3_investor_twi_ads':web3_investor_twi_ads,'whitepaper_twi_ads':whitepaper_twi_ads,'blockchain_fb_ads':blockchain_fb_ads,'blockchain_lix_ads':blockchain_lix_ads,'dao_lix_ads':dao_lix_ads,'dapp_lix_ads':dapp_lix_ads,'defi_lix_ads':defi_lix_ads,'nft_lix_ads':nft_lix_ads,'yield_farming_lix_ads':yield_farming_lix_ads,'blockchain_phantom_ads':blockchain_phantom_ads,'dao_phantom_ads':dao_phantom_ads,'dapp_phantom_ads':dapp_phantom_ads,'defi_phantom_ads':defi_phantom_ads,'nft_phantom_ads':nft_phantom_ads,'yield_farming_phantom_ads':yield_farming_phantom_ads,'total_count_ads':total_count_ads,'entrepreneurs_insta_ads':entrepreneurs_insta_ads,'digital_marketing_insta_ads':digital_marketing_insta_ads,'uiux_insta_ads':uiux_insta_ads,'micromente_insta_ads':micromente_insta_ads,'menterpass_insta_ads':menterpass_insta_ads,'defi_twi':defi_twi,'defi_twi_ads':defi_twi_ads})