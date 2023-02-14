# Generated by Django 3.1.7 on 2023-02-08 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_adtech_lix_talk_ads_adtech_spaced_animation_lix_talk_ads_animation_spaced_blogging_lix_talk_ads_blog'),
    ]

    operations = [
        migrations.CreateModel(
            name='blogging_fb_ads_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.TextField()),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('uid', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='blogging_talk',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('Profile_URL', models.TextField()),
                ('Full_Name', models.TextField()),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('Education', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='content_marketing_fb_ads_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.TextField()),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('uid', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='content_marketing_talk',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('Profile_URL', models.TextField()),
                ('Full_Name', models.TextField()),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('Education', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='d3_animation_fb_ads_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.TextField()),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('uid', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='d3_animation_talk',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('Profile_URL', models.TextField()),
                ('Full_Name', models.TextField()),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('Education', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='d3_modeling_fb_ads_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.TextField()),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('uid', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='d3_modeling_talk',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('Profile_URL', models.TextField()),
                ('Full_Name', models.TextField()),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('Education', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='email_marketing_fb_ads_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.TextField()),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('uid', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='email_marketing_talk',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('Profile_URL', models.TextField()),
                ('Full_Name', models.TextField()),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('Education', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='figma_design_fb_ads_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.TextField()),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('uid', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='graphic_design_fb_ads_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.TextField()),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('uid', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='infographics_fb_ads_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.TextField()),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('uid', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='instagram_marketing_fb_ads_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.TextField()),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('uid', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='instagram_marketing_talk',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('Profile_URL', models.TextField()),
                ('Full_Name', models.TextField()),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('Education', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='marketing_video_fb_ads_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.TextField()),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('uid', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='poadcasting_fb_ads_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.TextField()),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('uid', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='social_media_marketing_fb_ads_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.TextField()),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('uid', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='social_media_marketing_talk',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('Profile_URL', models.TextField()),
                ('Full_Name', models.TextField()),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('Education', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='tiktok_marketing_fb_ads_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.TextField()),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('uid', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='tiktok_marketing_talk',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('Profile_URL', models.TextField()),
                ('Full_Name', models.TextField()),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('Education', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='video_marketing_fb_ads_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.TextField()),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('uid', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='video_marketing_talk',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('Profile_URL', models.TextField()),
                ('Full_Name', models.TextField()),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('Education', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='youtube_marketing_fb_ads_spaced',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.TextField()),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('uid', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='youtube_marketing_talk',
            fields=[
                ('Row_id', models.AutoField(primary_key=True, serialize=False)),
                ('Profile_URL', models.TextField()),
                ('Full_Name', models.TextField()),
                ('First_Name', models.TextField()),
                ('Last_Name', models.TextField()),
                ('Education', models.TextField()),
                ('Category', models.TextField()),
                ('contact', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
    ]