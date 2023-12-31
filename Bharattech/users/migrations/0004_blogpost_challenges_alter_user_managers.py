# Generated by Django 4.0.3 on 2023-12-05 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_merge_0002_user_mobile_0002_user_mobile_user_otp'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('writer', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Challenges',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problemstatement', models.TextField()),
                ('sample_input_1', models.TextField()),
                ('sample_input_2', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('sample_output_1', models.TextField()),
                ('sample_output_2', models.TextField()),
                ('explanations', models.TextField()),
                ('language', models.CharField(choices=[('1', 'Python'), ('2', 'Java'), ('3', 'CPP')], default='1', max_length=10)),
                ('stack', models.CharField(choices=[('1', 'Frontend'), ('2', 'Backtend'), ('3', 'FullStack'), ('4', 'AI/ML'), ('5', 'Data Analyst'), ('6', 'Data Science')], max_length=20)),
                ('level', models.CharField(choices=[('Easy', 'Easy'), ('Medium', 'Mediun'), ('Hard', 'Hard')], default='Easy', max_length=10)),
                ('rating', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], default='1', max_length=10)),
            ],
        ),
        migrations.AlterModelManagers(
            name='user',
            managers=[
            ],
        ),
    ]
