# Generated by Django 5.1.4 on 2025-02-05 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_teacher_last_rangoli_batch_completion_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='District',
        ),
        migrations.RemoveField(
            model_name='user',
            name='address',
        ),
        migrations.RemoveField(
            model_name='user',
            name='birthday',
        ),
        migrations.RemoveField(
            model_name='user',
            name='education',
        ),
        migrations.RemoveField(
            model_name='user',
            name='full_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='user',
            name='hobbies',
        ),
        migrations.RemoveField(
            model_name='user',
            name='ira_rangoli_reference',
        ),
        migrations.RemoveField(
            model_name='user',
            name='picture',
        ),
        migrations.RemoveField(
            model_name='user',
            name='pincode',
        ),
        migrations.RemoveField(
            model_name='user',
            name='state',
        ),
        migrations.RemoveField(
            model_name='user',
            name='taluka',
        ),
        migrations.AddField(
            model_name='student',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='education',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='student',
            name='full_address',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='student',
            name='full_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='student',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='hobbies',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='student',
            name='ira_rangoli_reference',
            field=models.CharField(blank=True, choices=[('WhatsApp', 'WhatsApp'), ('YouTube', 'YouTube'), ('Instagram', 'Instagram'), ('Newspaper', 'Newspaper'), ('Friend', 'Friend')], max_length=50),
        ),
        migrations.AddField(
            model_name='student',
            name='jilha',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='student',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='static/profile_images'),
        ),
        migrations.AddField(
            model_name='student',
            name='pincode',
            field=models.CharField(blank=True, max_length=6),
        ),
        migrations.AddField(
            model_name='student',
            name='state',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='student',
            name='taluka',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='teacher',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='education',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='teacher',
            name='full_address',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='full_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='teacher',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='hobbies',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='ira_rangoli_reference',
            field=models.CharField(blank=True, choices=[('WhatsApp', 'WhatsApp'), ('YouTube', 'YouTube'), ('Instagram', 'Instagram'), ('Newspaper', 'Newspaper'), ('Friend', 'Friend')], max_length=50),
        ),
        migrations.AddField(
            model_name='teacher',
            name='jilha',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='teacher',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='static/profile_images'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='pincode',
            field=models.CharField(blank=True, max_length=6),
        ),
        migrations.AddField(
            model_name='teacher',
            name='state',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='teacher',
            name='taluka',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
