# Generated by Django 3.1.7 on 2023-01-18 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_angle_investor_fb_talk_ads_spaced_artificial_intelligence_fb_ads_spaced_blockchain_fb_talk_ads_space'),
    ]

    operations = [
        migrations.CreateModel(
            name='adtech_LIX_talk_ads',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('Description', models.TextField()),
                ('Profile_Link', models.TextField()),
                ('Email_id', models.TextField()),
                ('Location', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='adtech_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('Profile_Link', models.TextField()),
                ('Category', models.TextField()),
                ('Description', models.TextField()),
                ('Experience_Title', models.TextField()),
                ('LinkedIn_Name', models.TextField()),
                ('Location', models.TextField(default='')),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='animation_LIX_talk_ads',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('Description', models.TextField()),
                ('Profile_Link', models.TextField()),
                ('Email_id', models.TextField()),
                ('Location', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='animation_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('Profile_Link', models.TextField()),
                ('Category', models.TextField()),
                ('Description', models.TextField()),
                ('Experience_Title', models.TextField()),
                ('LinkedIn_Name', models.TextField()),
                ('Location', models.TextField(default='')),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='blogging_LIX_talk_ads',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('Description', models.TextField()),
                ('Profile_Link', models.TextField()),
                ('Email_id', models.TextField()),
                ('Location', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='blogging_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('Profile_Link', models.TextField()),
                ('Category', models.TextField()),
                ('Description', models.TextField()),
                ('Experience_Title', models.TextField()),
                ('LinkedIn_Name', models.TextField()),
                ('Location', models.TextField(default='')),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ceo_LIX_talk_ads',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('Description', models.TextField()),
                ('Profile_Link', models.TextField()),
                ('Email_id', models.TextField()),
                ('Location', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ceo_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('Profile_Link', models.TextField()),
                ('Category', models.TextField()),
                ('Description', models.TextField()),
                ('Experience_Title', models.TextField()),
                ('LinkedIn_Name', models.TextField()),
                ('Location', models.TextField(default='')),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='cio_LIX_talk_ads',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('Description', models.TextField()),
                ('Profile_Link', models.TextField()),
                ('Email_id', models.TextField()),
                ('Location', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='cio_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('Profile_Link', models.TextField()),
                ('Category', models.TextField()),
                ('Description', models.TextField()),
                ('Experience_Title', models.TextField()),
                ('LinkedIn_Name', models.TextField()),
                ('Location', models.TextField(default='')),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='content_distri_LIX_talk_ads',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('Description', models.TextField()),
                ('Profile_Link', models.TextField()),
                ('Email_id', models.TextField()),
                ('Location', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='content_distri_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('Profile_Link', models.TextField()),
                ('Category', models.TextField()),
                ('Description', models.TextField()),
                ('Experience_Title', models.TextField()),
                ('LinkedIn_Name', models.TextField()),
                ('Location', models.TextField(default='')),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='content_LIX_talk_ads',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('Description', models.TextField()),
                ('Profile_Link', models.TextField()),
                ('Email_id', models.TextField()),
                ('Location', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='content_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('Profile_Link', models.TextField()),
                ('Category', models.TextField()),
                ('Description', models.TextField()),
                ('Experience_Title', models.TextField()),
                ('LinkedIn_Name', models.TextField()),
                ('Location', models.TextField(default='')),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='conversion_LIX_talk_ads',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('Description', models.TextField()),
                ('Profile_Link', models.TextField()),
                ('Email_id', models.TextField()),
                ('Location', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='conversion_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('Profile_Link', models.TextField()),
                ('Category', models.TextField()),
                ('Description', models.TextField()),
                ('Experience_Title', models.TextField()),
                ('LinkedIn_Name', models.TextField()),
                ('Location', models.TextField(default='')),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='coo_LIX_talk_ads',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('Description', models.TextField()),
                ('Profile_Link', models.TextField()),
                ('Email_id', models.TextField()),
                ('Location', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='coo_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('Profile_Link', models.TextField()),
                ('Category', models.TextField()),
                ('Description', models.TextField()),
                ('Experience_Title', models.TextField()),
                ('LinkedIn_Name', models.TextField()),
                ('Location', models.TextField(default='')),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='cto_LIX_talk_ads',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('Description', models.TextField()),
                ('Profile_Link', models.TextField()),
                ('Email_id', models.TextField()),
                ('Location', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='cto_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('Profile_Link', models.TextField()),
                ('Category', models.TextField()),
                ('Description', models.TextField()),
                ('Experience_Title', models.TextField()),
                ('LinkedIn_Name', models.TextField()),
                ('Location', models.TextField(default='')),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='doo_LIX_talk_ads',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('Description', models.TextField()),
                ('Profile_Link', models.TextField()),
                ('Email_id', models.TextField()),
                ('Location', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='doo_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('Profile_Link', models.TextField()),
                ('Category', models.TextField()),
                ('Description', models.TextField()),
                ('Experience_Title', models.TextField()),
                ('LinkedIn_Name', models.TextField()),
                ('Location', models.TextField(default='')),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='gom_LIX_talk_ads',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('Description', models.TextField()),
                ('Profile_Link', models.TextField()),
                ('Email_id', models.TextField()),
                ('Location', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='gom_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('Profile_Link', models.TextField()),
                ('Category', models.TextField()),
                ('Description', models.TextField()),
                ('Experience_Title', models.TextField()),
                ('LinkedIn_Name', models.TextField()),
                ('Location', models.TextField(default='')),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='hom_LIX_talk_ads',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('Description', models.TextField()),
                ('Profile_Link', models.TextField()),
                ('Email_id', models.TextField()),
                ('Location', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='hom_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('Profile_Link', models.TextField()),
                ('Category', models.TextField()),
                ('Description', models.TextField()),
                ('Experience_Title', models.TextField()),
                ('LinkedIn_Name', models.TextField()),
                ('Location', models.TextField(default='')),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='hos_LIX_talk_ads',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('Description', models.TextField()),
                ('Profile_Link', models.TextField()),
                ('Email_id', models.TextField()),
                ('Location', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='hos_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('Profile_Link', models.TextField()),
                ('Category', models.TextField()),
                ('Description', models.TextField()),
                ('Experience_Title', models.TextField()),
                ('LinkedIn_Name', models.TextField()),
                ('Location', models.TextField(default='')),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='infographics_LIX_talk_ads',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('Description', models.TextField()),
                ('Profile_Link', models.TextField()),
                ('Email_id', models.TextField()),
                ('Location', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='infographics_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('Profile_Link', models.TextField()),
                ('Category', models.TextField()),
                ('Description', models.TextField()),
                ('Experience_Title', models.TextField()),
                ('LinkedIn_Name', models.TextField()),
                ('Location', models.TextField(default='')),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='md_LIX_talk_ads',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('Description', models.TextField()),
                ('Profile_Link', models.TextField()),
                ('Email_id', models.TextField()),
                ('Location', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='md_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('Profile_Link', models.TextField()),
                ('Category', models.TextField()),
                ('Description', models.TextField()),
                ('Experience_Title', models.TextField()),
                ('LinkedIn_Name', models.TextField()),
                ('Location', models.TextField(default='')),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='podcasting_LIX_talk_ads',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('Description', models.TextField()),
                ('Profile_Link', models.TextField()),
                ('Email_id', models.TextField()),
                ('Location', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='podcasting_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('Profile_Link', models.TextField()),
                ('Category', models.TextField()),
                ('Description', models.TextField()),
                ('Experience_Title', models.TextField()),
                ('LinkedIn_Name', models.TextField()),
                ('Location', models.TextField(default='')),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='presentation_LIX_talk_ads',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('Description', models.TextField()),
                ('Profile_Link', models.TextField()),
                ('Email_id', models.TextField()),
                ('Location', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='presentation_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('Profile_Link', models.TextField()),
                ('Category', models.TextField()),
                ('Description', models.TextField()),
                ('Experience_Title', models.TextField()),
                ('LinkedIn_Name', models.TextField()),
                ('Location', models.TextField(default='')),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='side_deck_LIX_talk_ads',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('Description', models.TextField()),
                ('Profile_Link', models.TextField()),
                ('Email_id', models.TextField()),
                ('Location', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='side_deck_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('Profile_Link', models.TextField()),
                ('Category', models.TextField()),
                ('Description', models.TextField()),
                ('Experience_Title', models.TextField()),
                ('LinkedIn_Name', models.TextField()),
                ('Location', models.TextField(default='')),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='social_media_LIX_talk_ads',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('Description', models.TextField()),
                ('Profile_Link', models.TextField()),
                ('Email_id', models.TextField()),
                ('Location', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='social_media_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('Profile_Link', models.TextField()),
                ('Category', models.TextField()),
                ('Description', models.TextField()),
                ('Experience_Title', models.TextField()),
                ('LinkedIn_Name', models.TextField()),
                ('Location', models.TextField(default='')),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='video_content_LIX_talk_ads',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('Description', models.TextField()),
                ('Profile_Link', models.TextField()),
                ('Email_id', models.TextField()),
                ('Location', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='video_content_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('Profile_Link', models.TextField()),
                ('Category', models.TextField()),
                ('Description', models.TextField()),
                ('Experience_Title', models.TextField()),
                ('LinkedIn_Name', models.TextField()),
                ('Location', models.TextField(default='')),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='visual_content_LIX_talk_ads',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('Description', models.TextField()),
                ('Profile_Link', models.TextField()),
                ('Email_id', models.TextField()),
                ('Location', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='visual_content_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('Profile_Link', models.TextField()),
                ('Category', models.TextField()),
                ('Description', models.TextField()),
                ('Experience_Title', models.TextField()),
                ('LinkedIn_Name', models.TextField()),
                ('Location', models.TextField(default='')),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
    ]
