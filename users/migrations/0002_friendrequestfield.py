# Generated by Django 4.0 on 2022-02-07 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendRequestField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to='auth.user')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to='auth.user')),
            ],
        ),
    ]
