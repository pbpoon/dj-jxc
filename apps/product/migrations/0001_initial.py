# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-22 15:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=20, unique=True, verbose_name='批次编号')),
                ('buy_price', models.PositiveIntegerField(blank=True, null=True, verbose_name='采购价格')),
                ('buy_date', models.DateField(blank=True, null=True, verbose_name='采购日期')),
                ('ps', models.CharField(blank=True, max_length=200, null=True, verbose_name='备注信息')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='添加日期')),
            ],
            options={
                'verbose_name': '批次信息',
                'verbose_name_plural': '批次信息',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=20, unique=True, verbose_name='品种名称')),
                ('created', models.DateField(auto_now_add=True, verbose_name='添加日期')),
            ],
            options={
                'verbose_name': '品种信息',
                'verbose_name_plural': '品种信息',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('block_num', models.CharField(db_index=True, max_length=20, unique=True, verbose_name='编号')),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='重量')),
                ('long', models.IntegerField(null=True, verbose_name='长')),
                ('width', models.IntegerField(null=True, verbose_name='宽')),
                ('high', models.IntegerField(null=True, verbose_name='高')),
                ('m3', models.DecimalField(decimal_places=2, max_digits=5, null=True, verbose_name='立方')),
                ('type', models.CharField(choices=[('block', '荒料'), ('coarse', '毛板'), ('slab', '板材')], max_length=6, verbose_name='形态')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新日期')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='添加日期')),
                ('ccl_state', models.BooleanField(default=True, verbose_name='出材率计算方式')),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Batch', verbose_name='批次')),
            ],
            options={
                'verbose_name': '产品信息',
                'verbose_name_plural': '产品信息',
            },
        ),
        migrations.CreateModel(
            name='Quarry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='矿口名称')),
                ('desc', models.CharField(max_length=200, verbose_name='描述信息')),
                ('created', models.DateField(auto_now_add=True, verbose_name='添加日期')),
                ('updated', models.DateField(auto_now=True, verbose_name='更新日期')),
            ],
            options={
                'verbose_name': '矿口信息',
                'verbose_name_plural': '矿口信息',
            },
        ),
        migrations.CreateModel(
            name='SlabList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=20, verbose_name='录入人员')),
                ('ps', models.CharField(blank=True, max_length=200, null=True, verbose_name='备注信息')),
                ('thick', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='厚度')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='添加日期')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新日期')),
                ('block_num', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slablist', to='product.Product', verbose_name='荒料编号')),
            ],
            options={
                'verbose_name': '码单信息',
                'verbose_name_plural': '码单信息',
            },
        ),
        migrations.CreateModel(
            name='SlabListItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_num', models.CharField(max_length=8, verbose_name='夹号')),
                ('part_index', models.PositiveSmallIntegerField(verbose_name='序号')),
                ('long', models.PositiveSmallIntegerField(verbose_name='长')),
                ('high', models.PositiveSmallIntegerField(verbose_name='高')),
                ('kl1', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='长1')),
                ('kl2', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='长2')),
                ('kh1', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='高1')),
                ('kh2', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='高2')),
                ('m2', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='平方')),
                ('is_sell', models.BooleanField(default=False, verbose_name='是否已售')),
                ('is_booking', models.BooleanField(default=False, verbose_name='是否已定')),
                ('is_pickup', models.BooleanField(default=False, verbose_name='是否已提货')),
                ('slablistitem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='product.SlabList', verbose_name='码单')),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='batch',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Category', verbose_name='品种名称'),
        ),
        migrations.AddField(
            model_name='batch',
            name='quarry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Quarry', verbose_name='矿口'),
        ),
    ]
