# Generated by Django 4.2.1 on 2023-10-05 19:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("appListNf", "0007_remove_listnfservice_numero_nf_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="listnfservice",
            name="Numero_NF",
            field=models.IntegerField(null=True),
        ),
    ]
