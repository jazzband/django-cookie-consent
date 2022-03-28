from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cookie_consent', '0002_auto__add_logitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='CookieType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'verbose_name': 'Cookie Type',
                'verbose_name_plural': 'Cookie Types',
                'ordering': ('name',),
            },
        ),
        migrations.AddField(
            model_name='cookie',
            name='duration',
            field=models.CharField(blank=True, max_length=256, verbose_name='Duration'),
        ),
        migrations.AddField(
            model_name='cookiegroup',
            name='updated',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Updated'),
        ),
        migrations.AddField(
            model_name='cookie',
            name='cookietype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cookie_consent.CookieType', verbose_name='Cookie Type'),
        ),
    ]
