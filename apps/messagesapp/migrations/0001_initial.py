# Generated by Django 4.0.3 on 2024-04-20 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.CharField(max_length=500)),
                ('image', models.ImageField(blank=True, null=True, upload_to='message_pics')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
