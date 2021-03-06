# Generated by Django 2.2.2 on 2021-11-04 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ObjABCModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productOil', models.BooleanField()),
                ('productGas', models.BooleanField()),
                ('scf_bo', models.IntegerField()),
                ('bc_mmscfg', models.IntegerField()),
                ('oilPrice', models.IntegerField()),
                ('oilSD', models.IntegerField()),
                ('gasPrice', models.IntegerField()),
                ('gasSD', models.IntegerField()),
                ('oilPerc', models.IntegerField()),
                ('gasPerc', models.IntegerField()),
                ('royalty', models.IntegerField()),
                ('priceUC1', models.BooleanField()),
                ('priceUC2', models.BooleanField()),
                ('fixedCost', models.IntegerField()),
                ('indProdCost', models.IntegerField()),
                ('oilProdCost', models.IntegerField()),
                ('gasProdCost', models.IntegerField()),
                ('excelFile', models.CharField(max_length=200)),
            ],
        ),
    ]
