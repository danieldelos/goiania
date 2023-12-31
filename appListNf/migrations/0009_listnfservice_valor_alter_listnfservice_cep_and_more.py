# Generated by Django 4.2.1 on 2023-10-05 20:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("appListNf", "0008_listnfservice_numero_nf"),
    ]

    operations = [
        migrations.AddField(
            model_name="listnfservice",
            name="valor",
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name="listnfservice",
            name="cep",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="listnfservice",
            name="cod_mun_prestador",
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name="listnfservice",
            name="cod_mun_tomador",
            field=models.CharField(max_length=120, null=True),
        ),
    ]
