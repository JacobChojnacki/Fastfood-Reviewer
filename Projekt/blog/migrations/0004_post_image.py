# Generated by Django 4.0.3 on 2022-04-25 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(default=0, upload_to='images/'),
            preserve_default=False,
        ),
    ]
