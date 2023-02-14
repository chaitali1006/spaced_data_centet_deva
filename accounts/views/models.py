from django.db import models
from django.contrib.auth.models import User
from django.db import IntegrityError

class Activation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)


class Instagram_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    profileUrl= models.TextField()
    fullName = models.TextField()  
    query = models.TextField()
    username = models.CharField(max_length=50, default="", editable=False)
    contact= models.PositiveSmallIntegerField(default=0)

    
class Linkedin_lix_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class Digital_marketing(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class Blockchain_LIX(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class Data_analysis(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class Venture_funding(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class UIUX(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class Software_dev(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class Product_fit(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)


class Digital_marketing_phantom(models.Model):
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class Blockchain_LIX_phantom(models.Model):
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class Data_analysis_phantom(models.Model):
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class Venture_funding_phantom(models.Model):
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class UIUX_phantom(models.Model):
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class Software_dev_phantom(models.Model):
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class Product_fit_phantom(models.Model):
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class Linkedin_group_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    headline=models.TextField()
    fullName=models.TextField()
    query=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class Linkedin_search_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

#Data scintist, NFT, DAO, Dapp, DeFi, Yield Farming LIX
class LIX_search_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)


#Community Moderator
class CM_LIX_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

#Community Building
class CB_LIX_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

#Community Management
class CManag_LIX_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

#Discord Community
class DC_LIX_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

# #Venture Capital
# class venture_capital_LIX(models.Model):
#     Row_id = models.AutoField(primary_key=True)
#     Profile_Link=models.TextField()
#     Category=models.TextField()
#     Description=models.TextField()
#     Experience_Title=models.TextField()
#     LinkedIn_Name=models.TextField()
#     Location=models.TextField()
#     contact= models.PositiveSmallIntegerField(default=0)


#Venture Capital
class Venture_capital_LIX(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

#Venture capital phantom
class Venture_capital_phantom(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


#Angle investor
class Angle_investor_LIX(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

#Angle investor phanotm
class Angle_investor_phantom(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

#Seed Capital
class Seed_capital_LIX(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

#Seed Capital Phantom
class Seed_capital_phantom(models.Model):
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


#Fundraising
class Fundraising_LIX(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

#Fundraisingm phantom
class Fundraising_phantom(models.Model):
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

#Private Investor
class Private_investor_LIX(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

#Private Investor phantom
class Private_investor_phantom(models.Model):
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

#Data scintist, NFT, DAO, Dapp, DeFi, Yield Farming Phantombuster

class Phantom_search_talk(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

#Community Moderator
class CM_Phantom_talk(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

#Community Building
class CB_Phantom_talk(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

#Community Management
class CManag_Phantom_talk(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

#Discord Community

class DC_Phantom_talk(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class Web_dev_phantom(models.Model):
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class Mobile_dev_phantom(models.Model):
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class Entrepreneur1(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class Entrepreneur_Phantom(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class Founder_Phantom(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)



class Founder1(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class Scaleup1(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class Web_dev_lix(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class Mobile_dev_lix(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)



class Facebook_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_URL=models.TextField()
    Full_Name=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Education=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class venture_capital_fb(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_URL=models.TextField()
    Full_Name=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Education=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class angle_investor_fb(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_URL=models.TextField()
    Full_Name=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Education=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class pitchdesk_fb(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_URL=models.TextField()
    Full_Name=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Education=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class private_investor_fb(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_URL=models.TextField()
    Full_Name=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Education=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class business_angle_fb(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_URL=models.TextField()
    Full_Name=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Education=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class Twitter_talk_web2(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class Twitter_talk_web3(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class cb_twi(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class cg_twi(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class cm_twi(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class twi_marketing(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class web3_com_twi(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class web3_marketing_twi(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class chatbot_twi(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class discordbot_twi(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class blank(models.Model):
    Row_id=models.AutoField(primary_key=True)
    DiscordID=models.TextField()
    Author=models.TextField()
    Date1=models.TextField()
    Twitter=models.TextField()
    Question1=models.TextField()
    Question3=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class Wonderverse(models.Model):
    Row_id=models.AutoField(primary_key=True)
    AuthorID=models.TextField()
    Author=models.TextField()
    Date1=models.TextField()
    Content=models.TextField()
    Attachments=models.TextField()
    Reactions=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class Accelerators_talk_new(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Accelerators=models.TextField()
    ID=models.TextField()
    LinkedIn_Name=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Email_Top_Guess=models.TextField()
    Email_Other_Guesses=models.TextField()
    Description=models.TextField()
    Organisation=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class venture_capital_twi(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class angle_investor_twi(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class seed_capital_twi(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class web3_fund_twi(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class web3_grants_twi(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class fundraising_twi(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class whitepaper_twi(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class pitchdesk_twi(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class private_investor_twi(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class business_angle_twi(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class web3_investor_twi(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)



class d3_design_twi(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class graphics_design_twi(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class visual_design_twi(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class marketing_designer_twi(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class branding_consultant_twi(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class d3_design_fb(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_URL=models.TextField()
    Full_Name=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Education=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class graphics_design_fb(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_URL=models.TextField()
    Full_Name=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Education=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class d3_design_LIX(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)


class graphics_design_LIX(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)


class visual_design_LIX(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)


class marketing_designer_LIX(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class branding_consultant_LIX(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)


class artificial_intelligence_LIX(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class machine_learning_LIX(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class algorithm_LIX(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default=' ')
    contact= models.PositiveSmallIntegerField(default=0)

class data_mining_LIX(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class neural_network_LIX(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class data_prediction_LIX(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class d3_design_phantom(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class graphics_design_phantom(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class visual_design_phantom(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class marketing_designer_phantom(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class branding_consultant_phantom(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class artificial_intelligence_phantom(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class machine_learning_phantom(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class algorithm_phantom(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default=' ')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class data_mining_phantom(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class neural_network_phantom(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class data_prediction_phantom(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class artificial_intelligence_fb(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_URL=models.TextField()
    Full_Name=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Education=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class machine_learning_fb(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_URL=models.TextField()
    Full_Name=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Education=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class algorithm_fb(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_URL=models.TextField()
    Full_Name=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Education=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class data_mining_fb(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_URL=models.TextField()
    Full_Name=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Education=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class neural_network_fb(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_URL=models.TextField()
    Full_Name=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Education=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)



class artificial_intelligence_twi(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class machine_learning_twi(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class algorithm_twi(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class data_mining_twi(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class neural_network_twi(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class data_prediction_twi(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)



class Digital_marketing_fb(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_URL=models.TextField()
    Full_Name=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Education=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class Blockchain_fb(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_URL=models.TextField()
    Full_Name=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Education=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class software_development_fb(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_URL=models.TextField()
    Full_Name=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Education=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class data_analysis_fb(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_URL=models.TextField()
    Full_Name=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Education=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class UX_fb(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_URL=models.TextField()
    Full_Name=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Education=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class Entrepreneurship_fb(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_URL=models.TextField()
    Full_Name=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Education=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class UIUX_insta(models.Model):
    Row_id = models.AutoField(primary_key=True)
    profileUrl= models.TextField()
    fullName = models.TextField()  
    query = models.TextField()
    username = models.CharField(max_length=50, default="", editable=False)
    contact= models.PositiveSmallIntegerField(default=0)

class Entrepreneurship_insta(models.Model):
    Row_id = models.AutoField(primary_key=True)
    profileUrl= models.TextField()
    fullName = models.TextField()  
    query = models.TextField()
    username = models.CharField(max_length=50, default="", editable=False)
    contact= models.PositiveSmallIntegerField(default=0)

class Digital_marketing_insta(models.Model):
    Row_id = models.AutoField(primary_key=True)
    profileUrl= models.TextField()
    fullName = models.TextField()  
    query = models.TextField()
    username = models.CharField(max_length=50, default="", editable=False)
    contact= models.PositiveSmallIntegerField(default=0)



class Entrepreneurship_twi(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class Digital_marketing_twi(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)



class uxui_twi(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)







class Figma_LIX_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)


class Notion_LIX_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class Slack_LIX_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class Trello_LIX_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)


class Miro_LIX_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)




class Figma_twi_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class Onalytica_twi_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class Slack_twi_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class Trello_twi_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class Miro_twi_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class Notion_twi_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)



class MicroMentor_insta_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    profileUrl= models.TextField()
    fullName = models.TextField()  
    query = models.TextField()
    username = models.CharField(max_length=50, default="", editable=False)
    contact= models.PositiveSmallIntegerField(default=0)

class MentorPass_insta_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    profileUrl= models.TextField()
    fullName = models.TextField()  
    query = models.TextField()
    username = models.CharField(max_length=50, default="", editable=False)
    contact= models.PositiveSmallIntegerField(default=0)

class MicroMentor_twi_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class MentorPass_twi_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class Figma_phantom_talk(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class Notion_phantom_talk(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class Slack_phantom_talk(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class Trello_phantom_talk(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class Brand_Designers_phantom_talk(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    profileUrl=models.TextField()
    currentJob=models.TextField()
    job=models.TextField()
    Keyword=models.TextField()
    location=models.TextField(default='')
    fullName=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class Brand_Designers_LIX_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)


class algorithm_fb_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class algorithm_fb_ads_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    email=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class artificial_intelligence_fb_ads_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    email=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class data_analysis_fb_ads_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    email=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class data_mining_fb_ads_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    email=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class machine_learning_fb_ads_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    email=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class neural_network_fb_ads_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    email=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)



class artificial_intelligence_fb_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class data_analysis_fb_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class data_mining_fb_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)
 
class machine_learning_fb_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class neural_network_fb_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class algorithm_LIX_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class artificial_intelligence_LIX_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class data_analysis_LIX_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class data_mining_LIX_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class data_prediction_LIX_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class data_scientist_LIX_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class machine_learning_LIX_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class neural_network_LIX_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class algorithm_phantom_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class artificial_intelligence_phantom_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class data_analysis_phantom_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class data_mining_phantom_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class data_prediction_phantom_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class data_scientist_phantom_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class machine_learning_phantom_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class neural_network_phantom_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class algorithm_twi_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class artificial_intelligence_twi_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class data_mining_twi_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class data_prediction_twi_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class machine_learning_twi_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class neural_networks_twi_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class figma_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class miro_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class notion_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class slack_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class trello_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class figma_phantom_talk_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class notion_phantom_talk_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class slack_phantom_talk_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class trello_phantom_talk_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class figma_twi_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class miro_twi_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class notion_twi_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class onalytica_twi_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class slack_twi_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class trello_twi_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class CB_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class CManag_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class CM_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class DC_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class CB_phantom_talk_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class CManag_phantom_talk_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class CM_phantom_talk_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class DC_phantom_talk_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class chatbot_twi_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class CB_twi_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class CG_twi_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class CManag_twi_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class discordbot_twi_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class twitter_marketing_twi_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class web3_community_twi_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class web3_marketing_twi_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class enterpreneurs_fb_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class enterpreneurs_fb_talk_ads_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    email=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class d3_design_fb_talk_ads_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    email=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class graphic_design_fb_talk_ads_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    email=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class uiux_design_fb_talk_ads_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    email=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class digital_marketing_fb_talk_ads_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    email=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class software_development_fb_talk_ads_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    email=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class angle_investor_fb_talk_ads_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    email=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class business_angle_fb_talk_ads_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    email=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class pitchdesk_fb_talk_ads_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    email=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)
    
class private_investor_fb_talk_ads_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    email=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class venture_capital_fb_talk_ads_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    email=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class blockchain_fb_talk_ads_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    email=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)
    

class enterpreneurs_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class founder_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class enterpreneurs_phantom_talk_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class founders_phantom_talk_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class enterpreneurs_twi_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class d3_design_fb_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class graphic_design_fb_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class uiux_design_fb_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class d3_design_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class brand_designers_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class branding_consultant_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class graphic_design_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class marketing_designer_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class uiux_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class visual_design_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class d3_design_phantom_talk_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class brand_designers_phantom_talk_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class branding_consultant_phantom_talk_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class graphic_design_phantom_talk_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class marketing_designer_phantom_talk_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class uiux_design_phantom_talk_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class visual_design_phantom_talk_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class d3_design_twi_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)
class branding_consultant_twi_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)
class graphic_design_twi_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)
class marketing_designer_twi_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)
class uiux_design_twi_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)
class visual_design_twi_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class micromentor_twi_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)
class mentorpass_twi_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class digital_marketing_fb_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class digital_marketing_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class digital_marketing_phantom_talk_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class digital_marketing_twi_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class pm_fit_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class pm_fit_phantom_talk_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class software_development_fb_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class mobile_development_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class software_development_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class web_development_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class mobile_development_phantom_talk_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class software_development_phantom_talk_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class web_development_phantom_talk_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class angle_investor_fb_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class business_angle_fb_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class pitchdesk_fb_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class private_investor_fb_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class venture_capital_fb_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class angle_investor_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField(default='')
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class fundraising_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class private_investor_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class seed_capital_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class venture_capital_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class angle_investor_phantom_talk_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class fundraising_phantom_talk_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class private_investor_phantom_talk_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class seed_capital_phantom_talk_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class venture_capital_phantom_talk_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class angle_investor_twi_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)
class business_angle_twi_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)
class fundraising_twi_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)
class pitchdesk_twi_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)
class private_investor_twi_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)
class seed_capital_twi_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)
class venture_capital_twi_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)
class web3_fund_twi_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)
class web3_grants_twi_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)
class web3_investor_twi_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)
class whitepaper_twi_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class blockchain_fb_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class blockchain_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class blockchain_LIX_talk_ads_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class dao_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)
class dapp_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)
class defi_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)
class nft_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)
class yield_farming_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class blockchain_phantom_talk_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class dao_phantom_talk_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class dapp_phantom_talk_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class defi_phantom_talk_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class nft_phantom_talk_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class yield_farming_phantom_talk_ads(models.Model): 
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    currentJob=models.TextField()
    profileUrl=models.TextField() 
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class entrepreneurs_insta_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class digital_marketing_insta_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class uiux_insta_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class micromente_insta_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class menterpass_insta_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class defi_talk_twi(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Url=models.TextField()
    Screen_Name=models.TextField()
    User_Id=models.TextField()
    Name=models.TextField()
    Img_Url=models.TextField()
    Background_Img=models.TextField()
    Bio=models.TextField()
    Website=models.TextField()
    Location=models.TextField(default='')
    Created_At=models.TextField()
    Followers_Count=models.IntegerField()
    Friends_Count=models.IntegerField()
    Tweets_Count=models.IntegerField()
    Certified=models.TextField()
    Following=models.TextField()
    Followed_By=models.TextField()
    Query=models.TextField()
    Timestamp1=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class defi_talk_twi_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    User_Id=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class ceo_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class cio_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class coo_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class cto_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)


class doo_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class gom_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class hom_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class hos_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class md_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class ceo_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class cio_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class coo_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class cto_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class doo_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class gom_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class hom_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class hos_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class md_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class animation_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class content_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class adtech_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class blogging_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class content_distri_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class conversion_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class infographics_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class podcasting_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class presentation_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class side_deck_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class social_media_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class video_content_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class visual_content_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_Link=models.TextField()
    Category=models.TextField()
    Description=models.TextField()
    Experience_Title=models.TextField()
    LinkedIn_Name=models.TextField()
    Location=models.TextField(default='')
    contact= models.PositiveSmallIntegerField(default=0)

class animation_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class content_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class adtech_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class blogging_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class content_distri_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class conversion_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class infographics_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class podcasting_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class presentation_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class side_deck_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class social_media_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class video_content_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class visual_content_LIX_talk_ads(models.Model):
    Row_id = models.AutoField(primary_key=True)
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Description=models.TextField()
    Profile_Link=models.TextField()
    Email_id=models.TextField()
    Location=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class d3_animation_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_URL=models.TextField()
    Full_Name=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Education=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class d3_modeling_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_URL=models.TextField()
    Full_Name=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Education=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class blogging_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_URL=models.TextField()
    Full_Name=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Education=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class content_marketing_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_URL=models.TextField()
    Full_Name=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Education=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class email_marketing_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_URL=models.TextField()
    Full_Name=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Education=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class instagram_marketing_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_URL=models.TextField()
    Full_Name=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Education=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class social_media_marketing_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_URL=models.TextField()
    Full_Name=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Education=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class figma_design_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_URL=models.TextField()
    Full_Name=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Education=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class graphic_design_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_URL=models.TextField()
    Full_Name=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Education=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class infographics_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_URL=models.TextField()
    Full_Name=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Education=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class marketing_video_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_URL=models.TextField()
    Full_Name=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Education=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class poadcasting_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_URL=models.TextField()
    Full_Name=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Education=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

       
class tiktok_marketing_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_URL=models.TextField()
    Full_Name=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Education=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class video_marketing_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_URL=models.TextField()
    Full_Name=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Education=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class youtube_marketing_talk(models.Model):
    Row_id = models.AutoField(primary_key=True)
    Profile_URL=models.TextField()
    Full_Name=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    Education=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class d3_animation_fb_ads_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    email=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class d3_modeling_fb_ads_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    email=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class blogging_fb_ads_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    email=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class content_marketing_fb_ads_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    email=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class email_marketing_fb_ads_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    email=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class figma_design_fb_ads_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    email=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class graphic_design_fb_ads_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    email=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class infographics_fb_ads_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    email=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class marketing_video_fb_ads_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    email=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class poadcasting_fb_ads_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    email=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class instagram_marketing_fb_ads_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    email=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)


class social_media_marketing_fb_ads_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    email=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class tiktok_marketing_fb_ads_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    email=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class video_marketing_fb_ads_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    email=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)

class youtube_marketing_fb_ads_spaced(models.Model):
    Row_id = models.AutoField(primary_key=True)
    email=models.TextField()
    First_Name=models.TextField()
    Last_Name=models.TextField()
    uid=models.TextField()
    Category=models.TextField()
    contact= models.PositiveSmallIntegerField(default=0)
    