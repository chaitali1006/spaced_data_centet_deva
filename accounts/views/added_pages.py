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
from .models import Activation,Accelerators_talk_new,Entrepreneurship_fb,enterpreneurs_fb_talk_ads,Entrepreneur1,enterpreneurs_LIX_talk_ads,Founder1,founder_LIX_talk_ads,Entrepreneur_Phantom,enterpreneurs_phantom_talk_ads,Founder_Phantom,founders_phantom_talk_ads,Digital_marketing_fb,digital_marketing_fb_talk_ads_spaced,Digital_marketing_insta, digital_marketing_insta_talk_ads,Digital_marketing,digital_marketing_LIX_talk_ads,Digital_marketing_phantom,digital_marketing_phantom_talk_ads,Digital_marketing_twi,digital_marketing_twi_talk_ads,d3_animation_talk,d3_modeling_talk,blogging_talk,content_marketing_talk,email_marketing_talk,figma_design_talk,graphic_design_talk,infographics_talk,marketing_video_talk,poadcasting_talk,instagram_marketing_talk,social_media_marketing_talk,tiktok_marketing_talk,video_marketing_talk,youtube_marketing_talk,d3_animation_fb_ads_spaced,d3_modeling_fb_ads_spaced,blogging_fb_ads_spaced,content_marketing_fb_ads_spaced,email_marketing_fb_ads_spaced,figma_design_fb_ads_spaced,graphic_design_fb_ads_spaced,infographics_fb_ads_spaced,marketing_video_fb_ads_spaced,poadcasting_fb_ads_spaced,instagram_marketing_fb_ads_spaced,social_media_marketing_fb_ads_spaced,tiktok_marketing_fb_ads_spaced,video_marketing_fb_ads_spaced,youtube_marketing_fb_ads_spaced,animation_spaced,content_spaced,adtech_spaced,blogging_spaced,content_distri_spaced,conversion_spaced,infographics_spaced,podcasting_spaced,presentation_spaced,side_deck_spaced,social_media_spaced,video_content_spaced,visual_content_spaced,animation_LIX_talk_ads,content_LIX_talk_ads,adtech_LIX_talk_ads,blogging_LIX_talk_ads,content_distri_LIX_talk_ads,conversion_LIX_talk_ads,infographics_LIX_talk_ads,podcasting_LIX_talk_ads,presentation_LIX_talk_ads,side_deck_LIX_talk_ads,social_media_LIX_talk_ads,video_content_LIX_talk_ads,visual_content_LIX_talk_ads,ceo_spaced, cio_spaced, coo_spaced, cto_spaced, doo_spaced, gom_spaced, hom_spaced, hos_spaced, md_spaced,ceo_LIX_talk_ads, cio_LIX_talk_ads,coo_LIX_talk_ads,cto_LIX_talk_ads,doo_LIX_talk_ads,gom_LIX_talk_ads,hom_LIX_talk_ads,hos_LIX_talk_ads,md_LIX_talk_ads,enterpreneurs_fb_talk_ads_spaced,Figma_LIX_talk, figma_LIX_talk_ads, Notion_LIX_talk, notion_LIX_talk_ads, Figma_twi_talk, figma_twi_talk_ads, notion_twi_talk_ads, Notion_twi_talk,Onalytica_twi_talk,onalytica_twi_talk_ads,CB_LIX_talk,CM_LIX_talk,CManag_LIX_talk,DC_LIX_talk,CB_Phantom_talk,CManag_Phantom_talk,CM_Phantom_talk,DC_Phantom_talk,chatbot_twi,cb_twi,cg_twi,cm_twi,twi_marketing,web3_com_twi,web3_marketing_twi,discordbot_twi,CB_LIX_talk_ads,CManag_LIX_talk_ads,CM_LIX_talk_ads,DC_LIX_talk_ads,CB_phantom_talk_ads,CManag_phantom_talk_ads,CM_phantom_talk_ads,DC_phantom_talk_ads,chatbot_twi_talk_ads,CB_twi_talk_ads,CG_twi_talk_ads,CManag_twi_talk_ads,discordbot_twi_talk_ads,twitter_marketing_twi_talk_ads,web3_community_twi_talk_ads,web3_marketing_twi_talk_ads,d3_design_fb,graphics_design_fb,UX_fb,UIUX_insta,d3_design_LIX,d3_design_LIX_talk_ads,uiux_insta_talk_ads,uiux_design_fb_talk_ads,graphic_design_fb_talk_ads,d3_design_fb_talk_ads,Brand_Designers_LIX_talk,brand_designers_LIX_talk_ads,branding_consultant_LIX,branding_consultant_LIX_talk_ads,graphics_design_LIX,graphic_design_LIX_talk_ads,marketing_designer_LIX,marketing_designer_LIX_talk_ads,uiux_LIX_talk_ads,UIUX,visual_design_LIX,visual_design_LIX_talk_ads,d3_design_phantom,d3_design_phantom_talk_ads,Brand_Designers_phantom_talk,brand_designers_phantom_talk_ads,branding_consultant_phantom,branding_consultant_phantom_talk_ads,graphics_design_phantom,graphic_design_phantom_talk_ads,marketing_designer_phantom,marketing_designer_phantom_talk_ads,UIUX_phantom,uiux_design_phantom_talk_ads,visual_design_phantom,visual_design_phantom_talk_ads,d3_design_twi,d3_design_twi_talk_ads,branding_consultant_twi,branding_consultant_twi_talk_ads,graphics_design_twi,graphic_design_twi_talk_ads,marketing_designer_twi,marketing_designer_twi_talk_ads,uxui_twi,uiux_design_twi_talk_ads,visual_design_twi,visual_design_twi_talk_ads,MicroMentor_insta_talk,MentorPass_insta_talk,MicroMentor_twi_talk,MentorPass_twi_talk,micromente_insta_talk_ads,menterpass_insta_talk_ads,micromentor_twi_talk_ads,mentorpass_twi_talk_ads





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



def customer_list(request):
   
    acc = Accelerators_talk_new.objects.count()
    enter_fb=Entrepreneurship_fb.objects.count()
    enterpreneurs_fb_ads= enterpreneurs_fb_talk_ads_spaced.objects.count()
    enter=Entrepreneur1.objects.count()
    enterpreneurs_lix__ads= enterpreneurs_LIX_talk_ads.objects.count()
    fn=Founder1.objects.count()
    founder_lix_ads= founder_LIX_talk_ads.objects.count()
    enter_phantom=Entrepreneur_Phantom.objects.count()
    enterpreneurs_phantom_ads= enterpreneurs_phantom_talk_ads.objects.count()
    fn_phantom=Founder_Phantom.objects.count()
    founders_phantom_ads= founders_phantom_talk_ads.objects.count()

    ceo_lix=ceo_spaced.objects.count()
    cio_lix=cio_spaced.objects.count()
    coo_lix=coo_spaced.objects.count()
    cto_lix=cto_spaced.objects.count()
    doo_lix=doo_spaced.objects.count()
    gom_lix=gom_spaced.objects.count()
    hom_lix=hom_spaced.objects.count()
    hos_lix=hos_spaced.objects.count()
    md_lix=md_spaced.objects.count()

    ceo_lix_ads=ceo_LIX_talk_ads.objects.count()
    cio_lix_ads=cio_LIX_talk_ads.objects.count()
    coo_lix_ads=coo_LIX_talk_ads.objects.count()
    cto_lix_ads=cto_LIX_talk_ads.objects.count()
    doo_lix_ads=doo_LIX_talk_ads.objects.count()
    gom_lix_ads=gom_LIX_talk_ads.objects.count()
    hom_lix_ads=hom_LIX_talk_ads.objects.count()
    hos_lix_ads=hos_LIX_talk_ads.objects.count()
    md_lix_ads=md_LIX_talk_ads.objects.count()


    total_count=acc+enter_fb+enter+fn+enter_phantom+fn_phantom+ceo_lix+cio_lix+coo_lix+cto_lix+doo_lix+gom_lix+hom_lix+hos_lix+md_lix

    total_count_ads=enterpreneurs_fb_ads+enterpreneurs_lix__ads+founder_lix_ads+enterpreneurs_phantom_ads+founders_phantom_ads+ceo_lix_ads+cio_lix_ads+coo_lix_ads+cto_lix_ads+doo_lix_ads+gom_lix_ads,hom_lix_ads,hos_lix_ads+md_lix_ads


    return render(request, 'accounts/customer_display.html',{'acc':acc,'enter_fb':enter_fb,'enterpreneurs_fb_ads':enterpreneurs_fb_ads,'enter':enter,'enterpreneurs_lix__ads':enterpreneurs_lix__ads,'fn':fn,'founder_lix_ads':founder_lix_ads,'enter_phantom':enter_phantom,'enterpreneurs_phantom_ads':enterpreneurs_phantom_ads,'fn_phantom':fn_phantom,'founders_phantom_ads':founders_phantom_ads,'ceo_lix':ceo_lix, 'cio_lix':cio_lix, 'coo_lix':coo_lix, 'cto_lix':cto_lix, 'doo_lix':doo_lix, 'gom_lix':gom_lix, 'hom_lix':hom_lix, 'hos_lix':hos_lix, 'md_lix':md_lix,'ceo_lix_ads':ceo_lix_ads, 'cio_lix_ads':cio_lix_ads, 'coo_lix_ads':coo_lix_ads, 'cto_lix_ads':cto_lix_ads, 'doo_lix_ads':doo_lix_ads, 'gom_lix_ads':gom_lix_ads,'hom_lix_ads':hom_lix_ads,'hos_lix_ads':hos_lix_ads, 'md_lix_ads':md_lix_ads,'total':total_count})



def marketing_list(request):
   
    digi_fb=Digital_marketing_fb.objects.count()
    digital_marketing_fb_ads= digital_marketing_fb_talk_ads_spaced.objects.count()
    digi_insta=Digital_marketing_insta.objects.count()
    digital_marketing_insta_ads= digital_marketing_insta_talk_ads.objects.count()
    dm = Digital_marketing.objects.count()
    digital_marketing_lix_ads= digital_marketing_LIX_talk_ads.objects.count()
    digital_marketing_phantom=Digital_marketing_phantom.objects.count()
    
    digital_marketing_phantom_ads= digital_marketing_phantom_talk_ads.objects.count()
    dmar_twi=Digital_marketing_twi.objects.count()
    digital_marketing_twi_ads= digital_marketing_twi_talk_ads.objects.count()

    d3_animation_fb=d3_animation_talk.objects.count()
    d3_modeling_fb=d3_modeling_talk.objects.count()
    blogging_fb=blogging_talk.objects.count()
    content_marketing_fb=content_marketing_talk.objects.count()
    email_marketing_fb=email_marketing_talk.objects.count()
    figma_design_fb=figma_design_talk.objects.count()
    graphic_design_fb=graphic_design_talk.objects.count()
    infographics_fb=infographics_talk.objects.count()
    marketing_video_fb=marketing_video_talk.objects.count()
    poadcasting_fb=poadcasting_talk.objects.count()
    instagram_marketing_fb=instagram_marketing_talk.objects.count()
    social_media_marketing_fb=social_media_marketing_talk.objects.count()
    tiktok_marketing_fb=tiktok_marketing_talk.objects.count()
    video_marketing_fb=video_marketing_talk.objects.count()
    youtube_marketing_fb=youtube_marketing_talk.objects.count()

    d3_animation_fb_ads=d3_animation_fb_ads_spaced.objects.count()
    d3_modeling_fb_ads=d3_modeling_fb_ads_spaced.objects.count()
    blogging_fb_ads=blogging_fb_ads_spaced.objects.count()
    content_marketing_fb_ads=content_marketing_fb_ads_spaced.objects.count()
    email_marketing_fb_ads=email_marketing_fb_ads_spaced.objects.count()
    figma_design_fb_ads=figma_design_fb_ads_spaced.objects.count()
    graphic_design_fb_ads=graphic_design_fb_ads_spaced.objects.count()
    infographics_fb_ads=infographics_fb_ads_spaced.objects.count()
    marketing_video_fb_ads=marketing_video_fb_ads_spaced.objects.count()
    poadcasting_fb_ads=poadcasting_fb_ads_spaced.objects.count()
    instagram_marketing_fb_ads=instagram_marketing_fb_ads_spaced.objects.count()
    social_media_marketing_fb_ads=social_media_marketing_fb_ads_spaced.objects.count()
    tiktok_marketing_fb_ads=tiktok_marketing_fb_ads_spaced.objects.count()
    video_marketing_fb_ads=video_marketing_fb_ads_spaced.objects.count()
    youtube_marketing_fb_ads=youtube_marketing_fb_ads_spaced.objects.count()


    animation_lix=animation_spaced.objects.count()
    content_lix=content_spaced.objects.count()
    adtech_lix=adtech_spaced.objects.count()
    blogging_lix=blogging_spaced.objects.count()
    content_distri_lix=content_distri_spaced.objects.count()
    conversion_lix=conversion_spaced.objects.count()
    infographics_lix=infographics_spaced.objects.count()
    podcasting_lix=podcasting_spaced.objects.count()
    presentation_lix=presentation_spaced.objects.count()
    side_deck_lix=side_deck_spaced.objects.count()
    social_media_lix=social_media_spaced.objects.count()
    video_content_lix=video_content_spaced.objects.count()
    visual_content_lix=visual_content_spaced.objects.count()

    animation_lix_ads=animation_LIX_talk_ads.objects.count()
    content_lix_ads=content_LIX_talk_ads.objects.count()
    adtech_lix_ads=adtech_LIX_talk_ads.objects.count()
    blogging_lix_ads=blogging_LIX_talk_ads.objects.count()
    content_distri_lix_ads=content_distri_LIX_talk_ads.objects.count()
    conversion_lix_ads=conversion_LIX_talk_ads.objects.count()
    infographics_lix_ads=infographics_LIX_talk_ads.objects.count()
    podcasting_lix_ads=podcasting_LIX_talk_ads.objects.count()
    presentation_lix_ads=presentation_LIX_talk_ads.objects.count()
    side_deck_lix_ads=side_deck_LIX_talk_ads.objects.count()
    social_media_lix_ads=social_media_LIX_talk_ads.objects.count()
    video_content_lix_ads=video_content_LIX_talk_ads.objects.count()
    visual_content_lix_ads=visual_content_LIX_talk_ads.objects.count()

    figma_lix=Figma_LIX_talk.objects.count()
    figma_lix_ads= figma_LIX_talk_ads.objects.count()
    notion_lix=Notion_LIX_talk.objects.count()
    notion_lix_ads= notion_LIX_talk_ads.objects.count()
    figma_twi=Figma_twi_talk.objects.count()
    figma_twi_ads= figma_twi_talk_ads.objects.count()
    notion_twi=Notion_twi_talk.objects.count()
    notion_twi_ads= notion_twi_talk_ads.objects.count()
    onalytica_twi=Onalytica_twi_talk.objects.count()
    onalytica_twi_ads= onalytica_twi_talk_ads.objects.count()

    cb_LIX=CB_LIX_talk.objects.count()
    cm_LIX=CM_LIX_talk.objects.count()
    cman_LIX=CManag_LIX_talk.objects.count()
    dc_LIX=DC_LIX_talk.objects.count()
    cb_phantom=CB_Phantom_talk.objects.count()
    cman_phantom=CManag_Phantom_talk.objects.count()
    cm_phantom=CM_Phantom_talk.objects.count()
    dc_phantom=DC_Phantom_talk.objects.count()
    chatbot_twi_count=chatbot_twi.objects.count()
    cb_twi_count=cb_twi.objects.count()
    cg_twi_count=cg_twi.objects.count()
    cm_twi_count=cm_twi.objects.count()
    twi_marketing_count=twi_marketing.objects.count()
    web3_com_twi_count=web3_com_twi.objects.count()
    web3_marketing_twi_count=web3_marketing_twi.objects.count()
    discordbot_twi_count=discordbot_twi.objects.count()


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

    d3_fb=d3_design_fb.objects.count()
    gd_fb=graphics_design_fb.objects.count()
    ux_ui_fb=UX_fb.objects.count()
    uiux_instagram=UIUX_insta.objects.count()
    d3_lix=d3_design_LIX.objects.count()
    d3_design_lix_ads= d3_design_LIX_talk_ads.objects.count()
    uiux_insta_ads= uiux_insta_talk_ads.objects.count()
    uiux_design_fb_ads= uiux_design_fb_talk_ads.objects.count()
    graphic_design_fb_ads= graphic_design_fb_talk_ads.objects.count()
    d3_design_fb_ads= d3_design_fb_talk_ads.objects.count()
    bd_design_lix=Brand_Designers_LIX_talk.objects.count()
    brand_designers_lix_ads= brand_designers_LIX_talk_ads.objects.count()
    bc_lix=branding_consultant_LIX.objects.count()
    branding_consultant_lix_ads= branding_consultant_LIX_talk_ads.objects.count()
    gd_lix=graphics_design_LIX.objects.count()
    graphic_design_lix_ads= graphic_design_LIX_talk_ads.objects.count()
    md_lix=marketing_designer_LIX.objects.count()
    marketing_designer_lix_ads= marketing_designer_LIX_talk_ads.objects.count()
    uiux_lix_ads= uiux_LIX_talk_ads.objects.count()
    uiux = UIUX.objects.count()
    vd_lix=visual_design_LIX.objects.count()
    visual_design_lix_ads= visual_design_LIX_talk_ads.objects.count()
    d3_phantom=d3_design_phantom.objects.count()
    d3_design_phantom_ads= d3_design_phantom_talk_ads.objects.count()
    bd_design_phantom=Brand_Designers_phantom_talk.objects.count()
    brand_designers_phantom_ads= brand_designers_phantom_talk_ads.objects.count()
    bc_phantom=branding_consultant_phantom.objects.count()
    branding_consultant_phantom_ads= branding_consultant_phantom_talk_ads.objects.count()
    gd_phantom=graphics_design_phantom.objects.count()
    graphic_design_phantom_ads= graphic_design_phantom_talk_ads.objects.count()
    md_phantom=marketing_designer_phantom.objects.count()
    marketing_designer_phantom_ads= marketing_designer_phantom_talk_ads.objects.count()
    uiux_phantom=UIUX_phantom.objects.count()
    uiux_design_phantom_ads= uiux_design_phantom_talk_ads.objects.count()
    vd_phantom=visual_design_phantom.objects.count()
    visual_design_phantom_ads= visual_design_phantom_talk_ads.objects.count()
    d3_twi=d3_design_twi.objects.count()
    d3_design_twi_ads= d3_design_twi_talk_ads.objects.count()
    bc_twi=branding_consultant_twi.objects.count()
    branding_consultant_twi_ads= branding_consultant_twi_talk_ads.objects.count()
    gd_twi=graphics_design_twi.objects.count()
    graphic_design_twi_ads= graphic_design_twi_talk_ads.objects.count()
    md_twi=marketing_designer_twi.objects.count()
    marketing_designer_twi_ads= marketing_designer_twi_talk_ads.objects.count()
    uxuidesign_twi=uxui_twi.objects.count()
    uiux_design_twi_ads= uiux_design_twi_talk_ads.objects.count()
    vd_twi=visual_design_twi.objects.count()
    visual_design_twi_ads= visual_design_twi_talk_ads.objects.count()
    micromenter_insta=MicroMentor_insta_talk.objects.count()
    menterpass_insta=MentorPass_insta_talk.objects.count()
    micromenter_twi=MicroMentor_twi_talk.objects.count()
    menterpass_twi=MentorPass_twi_talk.objects.count()
    micromente_insta_ads= micromente_insta_talk_ads.objects.count()
    menterpass_insta_ads= menterpass_insta_talk_ads.objects.count()
    micromentor_twi_ads= micromentor_twi_talk_ads.objects.count()
    mentorpass_twi_ads= mentorpass_twi_talk_ads.objects.count()


    total_count=digi_fb+digi_insta+dm+dmar_twi+digital_marketing_phantom+d3_animation_fb+d3_modeling_fb+blogging_fb+content_marketing_fb+email_marketing_fb+figma_design_fb+graphic_design_fb+infographics_fb+marketing_video_fb+poadcasting_fb+instagram_marketing_fb+social_media_marketing_fb+tiktok_marketing_fb+video_marketing_fb+youtube_marketing_fb+figma_lix+notion_lix+figma_twi+notion_twi+onalytica_twi+ cb_LIX + cm_LIX + cman_LIX + dc_LIX + cb_phantom + cman_phantom + cm_phantom + dc_phantom + chatbot_twi_count + cb_twi_count + cg_twi_count + cm_twi_count + twi_marketing_count + web3_com_twi_count + web3_marketing_twi_count + discordbot_twi_count++d3_fb+gd_fb+ux_ui_fb+uiux_instagram+d3_lix+bd_design_lix+bc_lix+gd_lix+md_lix+uiux+vd_lix+d3_phantom+bd_design_phantom+bc_phantom+gd_phantom+md_phantom+uiux_phantom+vd_phantom+d3_twi+bc_twi+gd_twi+md_twi+uxuidesign_twi+vd_twi+micromenter_insta+menterpass_insta+micromenter_twi+menterpass_twi



    total_count_ads=digital_marketing_fb_ads+digital_marketing_insta_ads+digital_marketing_lix_ads+digital_marketing_phantom_ads+digital_marketing_twi_ads+d3_animation_fb_ads+ d3_modeling_fb_ads+ blogging_fb_ads+ content_marketing_fb_ads+email_marketing_fb_ads+figma_design_fb_ads+ graphic_design_fb_ads+ infographics_fb_ads+marketing_video_fb_ads+poadcasting_fb_ads+ instagram_marketing_fb_ads+social_media_marketing_fb_ads+tiktok_marketing_fb_ads+video_marketing_fb_ads+youtube_marketing_fb_ads+figma_lix_ads+notion_lix_ads+figma_twi_ads+notion_twi_ads+onalytica_twi_ads++cb_lix_ads+cmanag_lix_ads+cm_lix_ads+dc_lix_ads+cb_phantom_ads+cmanag_phantom_ads+cm_phantom_ads+dc_phantom_ads+chatbot_twi_ads+cb_twi_ads+cg_twi_ads+cm_twi_ads+db_twi_ads+twi_marketing_twi_ads+web3_commu_twi_ads+web3_marketing_twi_ads


    return render(request, 'accounts/market_display.html',{'digi_fb':digi_fb,'digital_marketing_fb_ads':digital_marketing_fb_ads,'digi_insta':digi_insta,'digital_marketing_insta_ads':digital_marketing_insta_ads,'dm':dm,'digital_marketing_lix_ads':digital_marketing_lix_ads,'digital_marketing_phantom':digital_marketing_phantom,'digital_marketing_phantom_ads':digital_marketing_phantom_ads,'dmar_twi':dmar_twi,'digital_marketing_twi_ads':digital_marketing_twi_ads,'d3_animation_fb':d3_animation_fb,'d3_modeling_fb':d3_modeling_fb,'blogging_fb':blogging_fb,'content_marketing_fb':content_marketing_fb,'email_marketing_fb':email_marketing_fb,'figma_design_fb':figma_design_fb,'graphic_design_fb':graphic_design_fb,'infographics_fb':infographics_fb,'marketing_video_fb':marketing_video_fb,'poadcasting_fb':poadcasting_fb,'instagram_marketing_fb':instagram_marketing_fb,'social_media_marketing_fb':social_media_marketing_fb,'tiktok_marketing_fb':tiktok_marketing_fb,'video_marketing_fb':video_marketing_fb,'youtube_marketing_fb':youtube_marketing_fb,'d3_animation_fb_ads':d3_animation_fb_ads,'d3_modeling_fb_ads':d3_modeling_fb_ads, 'blogging_fb_ads':blogging_fb_ads, 'content_marketing_fb_ads':content_marketing_fb_ads,'email_marketing_fb_ads':email_marketing_fb_ads,'figma_design_fb_ads':figma_design_fb_ads, 'graphic_design_fb_ads':graphic_design_fb_ads, 'infographics_fb_ads':infographics_fb_ads,'marketing_video_fb_ads':marketing_video_fb_ads,'poadcasting_fb_ads':poadcasting_fb_ads, 'instagram_marketing_fb_ads':instagram_marketing_fb_ads,'social_media_marketing_fb_ads':social_media_marketing_fb_ads,'tiktok_marketing_fb_ads':tiktok_marketing_fb_ads,'video_marketing_fb_ads':video_marketing_fb_ads,'youtube_marketing_fb_ads':youtube_marketing_fb_ads,'animation_lix':animation_lix,'content_lix':content_lix,'adtech_lix':adtech_lix,'blogging_lix':blogging_lix,'content_distri_lix':content_distri_lix,'conversion_lix':conversion_lix,'infographics_lix':infographics_lix,'podcasting_lix':podcasting_lix,'presentation_lix':presentation_lix,'side_deck_lix':side_deck_lix,'social_media_lix':social_media_lix,'video_content_lix':video_content_lix,'visual_content_lix':visual_content_lix,'animation_lix_ads':animation_lix_ads,'content_lix_ads':content_lix_ads,'adtech_lix_ads':adtech_lix_ads,'blogging_lix_ads':blogging_lix_ads,'content_distri_lix_ads':content_distri_lix_ads,'conversion_lix_ads':conversion_lix_ads,'infographics_lix_ads':infographics_lix_ads,'podcasting_lix_ads':podcasting_lix_ads,'presentation_lix_ads':presentation_lix_ads,'side_deck_lix_ads':side_deck_lix_ads,'social_media_lix_ads':social_media_lix_ads,'video_content_lix_ads':video_content_lix_ads,'visual_content_lix_ads':visual_content_lix_ads,'total_count':total_count,'total':total_count,'figma_lix':figma_lix,'figma_lix_ads':figma_lix_ads,'notion_lix':notion_lix,'notion_lix_ads':notion_lix_ads,'figma_twi':figma_twi,'figma_twi_ads':figma_twi_ads,'notion_twi_ads':notion_twi_ads,'notion_twi':notion_twi,'onalytica_twi':onalytica_twi,'onalytica_twi_ads':onalytica_twi_ads,'cb_LIX':cb_LIX,'cb_LIX':cb_LIX,'cman_LIX':cman_LIX,'dc_LIX':dc_LIX,'cb_phantom':cb_phantom,'cman_phantom':cman_phantom,'cm_phantom':cm_phantom,'dc_phantom':dc_phantom,'chatbot_twi_count':chatbot_twi_count,'cb_twi_count':cb_twi_count,'cg_twi_count':cg_twi_count,'cm_twi_count':cm_twi_count,'twi_marketing_count':twi_marketing_count,'web3_com_twi_count':web3_com_twi_count,'web3_marketing_twi_count':web3_marketing_twi_count,'discordbot_twi_count':discordbot_twi_count,'cb_lix_ads':cb_lix_ads,'cmanag_lix_ads':cmanag_lix_ads,'cm_lix_ads':cm_lix_ads,'dc_lix_ads':dc_lix_ads,'cb_phantom_ads':cb_phantom_ads,'cmanag_phantom_ads':cmanag_phantom_ads,'cm_phantom_ads':cm_phantom_ads,'dc_phantom_ads':dc_phantom_ads,'chatbot_twi_ads':chatbot_twi_ads,'cb_twi_ads':cb_twi_ads,'cg_twi_ads':cg_twi_ads,'cm_twi_ads':cm_twi_ads,'db_twi_ads':db_twi_ads,'twi_marketing_twi_ads':twi_marketing_twi_ads,'web3_commu_twi_ads':web3_commu_twi_ads,'web3_marketing_twi_ads':web3_marketing_twi_ads,'d3_fb':d3_fb,'d3_design_fb_ads':d3_design_fb_ads,'gd_fb':gd_fb,'graphic_design_fb_ads':graphic_design_fb_ads,'ux_ui_fb':ux_ui_fb,'uiux_design_fb_ads':uiux_design_fb_ads,'uiux_instagram':uiux_instagram,'uiux_insta_ads':uiux_insta_ads,'d3_lix':d3_lix,'d3_design_lix_ads':d3_design_lix_ads,'bd_design_lix':bd_design_lix,'brand_designers_lix_ads':brand_designers_lix_ads,'bc_lix':bc_lix,'branding_consultant_lix_ads':branding_consultant_lix_ads,'gd_lix':gd_lix,'graphic_design_lix_ads':graphic_design_lix_ads,'md_lix':md_lix,'marketing_designer_lix_ads':marketing_designer_lix_ads,'uiux':uiux,'uiux_lix_ads':uiux_lix_ads,'vd_lix':vd_lix,'visual_design_lix_ads':visual_design_lix_ads,'d3_phantom':d3_phantom,'d3_design_phantom_ads':d3_design_phantom_ads,'bd_design_phantom':bd_design_phantom,'brand_designers_phantom_ads':brand_designers_phantom_ads,'bc_phantom':bc_phantom,'branding_consultant_phantom_ads':branding_consultant_phantom_ads,'gd_phantom':gd_phantom,'graphic_design_phantom_ads':graphic_design_phantom_ads,'md_phantom':md_phantom,'marketing_designer_phantom_ads':marketing_designer_phantom_ads,'uiux_phantom':uiux_phantom,'uiux_design_phantom_ads':uiux_design_phantom_ads,'vd_phantom':vd_phantom,'visual_design_phantom_ads':visual_design_phantom_ads,'d3_twi':d3_twi,'d3_design_twi_ads':d3_design_twi_ads,'bc_twi':bc_twi,'branding_consultant_twi_ads':branding_consultant_twi_ads,'gd_twi':gd_twi,'graphic_design_twi_ads':graphic_design_twi_ads,'md_twi':md_twi,'marketing_designer_twi_ads':marketing_designer_twi_ads,'uxuidesign_twi':uxuidesign_twi,'uiux_design_twi_ads':uiux_design_twi_ads,'vd_twi':vd_twi,'visual_design_twi_ads':visual_design_twi_ads,'micromenter_insta':micromenter_insta,'micromente_insta_ads':micromente_insta_ads,'menterpass_insta':menterpass_insta,'menterpass_insta_ads':menterpass_insta_ads,'micromenter_twi':micromenter_twi,'micromentor_twi_ads':micromentor_twi_ads,'menterpass_twi':menterpass_twi,'mentorpass_twi_ads':mentorpass_twi_ads})
