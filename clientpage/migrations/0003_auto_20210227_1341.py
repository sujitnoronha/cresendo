# Generated by Django 3.1.7 on 2021-02-27 08:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clientpage', '0002_donationdrives_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donationdrives',
            name='image',
            field=models.ImageField(null=True, upload_to='donationprofiles'),
        ),
        migrations.CreateModel(
            name='Appointments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('phonenumber', models.CharField(blank=True, max_length=20, null=True)),
                ('datetime', models.DateField()),
                ('message', models.CharField(blank=True, max_length=100, null=True)),
                ('drive', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='drives', to='clientpage.donationdrives')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
