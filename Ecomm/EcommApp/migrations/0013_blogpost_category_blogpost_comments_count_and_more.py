# Generated by Django 5.1.4 on 2025-01-10 11:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EcommApp', '0012_blogpost'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='category',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='comments_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='tags',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('likes', models.IntegerField(default=0)),
                ('shares', models.IntegerField(default=0)),
                ('blog_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='EcommApp.blogpost')),
            ],
        ),
    ]
