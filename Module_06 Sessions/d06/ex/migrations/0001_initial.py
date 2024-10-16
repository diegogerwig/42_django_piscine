# Generated by Django 4.2 on 2024-10-15 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Downvote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voted_user', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Upvote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voted_user', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Tip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('auteur', models.CharField(max_length=150)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('downvote', models.ManyToManyField(to='ex.downvote')),
                ('upvote', models.ManyToManyField(to='ex.upvote')),
            ],
        ),
    ]
