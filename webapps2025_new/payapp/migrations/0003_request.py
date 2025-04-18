# Generated by Django 5.1.7 on 2025-04-07 09:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payapp', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('requester_currency', models.CharField(choices=[('gbp', 'GBP'), ('eur', 'EUR'), ('usd', 'USD')], default='GBP', max_length=3)),
                ('recipient_currency', models.CharField(choices=[('gbp', 'GBP'), ('eur', 'EUR'), ('usd', 'USD')], default='GBP', max_length=3)),
                ('status', models.CharField(choices=[('accepted', 'accepted'), ('rejected', 'rejected'), ('pending', 'pending')], default='pending', max_length=8)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='req_recipients', to=settings.AUTH_USER_MODEL)),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='req_requesters', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['datetime'],
            },
        ),
    ]
