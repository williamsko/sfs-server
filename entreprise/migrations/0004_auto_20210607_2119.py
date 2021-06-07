# Generated by Django 3.1.5 on 2021-06-07 21:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entreprise', '0003_auto_20210526_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='matricule',
            field=models.CharField(default='1488239987', max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='entreprise',
            name='code',
            field=models.CharField(default='4148786645', max_length=10, unique=True),
        ),
        migrations.CreateModel(
            name='Key',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(default='8529725917', max_length=32, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=False)),
                ('entreprise', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='entreprise.entreprise')),
            ],
            options={
                'verbose_name': 'Clé',
                'verbose_name_plural': 'Clés',
            },
        ),
    ]