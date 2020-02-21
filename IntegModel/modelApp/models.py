# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.conf import settings
from django.db import models

from django.contrib.auth.models import User

from django.db import models

# Create your models here.

import datetime


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


# 1.数据库类型
class DatabaseType(models.Model):
    db_type_name = models.CharField(max_length=64, unique=True, db_column='db_name', verbose_name='数据库类型')

    remark = models.TextField(blank=True, default="", verbose_name="备注")

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        verbose_name='创建者',
        default='1',
    )

    # 创建时间auto_now_add为添加时的时间，更新对象时不会有变动
    create_date = models.DateTimeField(auto_now_add=True)

    # 修改时间 auto_now无论是你添加还是修改对象
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "integ_db_type"
        verbose_name = '数据库类型'

    def __str__(self):
        return "{}".format(self.db_type_name)


# 2.主题域
class Theme(models.Model):
    table_theme_name = models.CharField(max_length=64, unique=True, db_column='table_theme_name', verbose_name='主题名称')
    table_theme_cn_name = models.CharField(max_length=64, unique=True, db_column='table_theme_cn_name',
                                           verbose_name='主题中文名称')

    table_theme_describe = models.TextField(blank=True, default="", verbose_name="说明")

    remark = models.TextField(blank=True, default="", verbose_name="备注")

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        verbose_name='创建者',
        default='1',
    )

    # 创建时间auto_now_add为添加时的时间，更新对象时不会有变动
    create_date = models.DateTimeField(auto_now_add=True)

    # 修改时间 auto_now无论是你添加还是修改对象
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "integ_tbtheme"
        verbose_name = '表主题'

    def __str__(self):
        return "{}({})".format(self.table_theme_name, self.table_theme_cn_name)


# 3.字段类型
class FieldType(models.Model):
    # 数据库类型
    db_type = models.ForeignKey(DatabaseType, on_delete=models.PROTECT, verbose_name='数据库类型', default='1')

    # 字段类型
    fields_type = models.CharField(max_length=64, verbose_name='字段类型')

    remark = models.TextField(blank=True, default="", verbose_name="备注")

    # 创建者
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        verbose_name='创建者',
        default='1',
    )
    # 创建时间auto_now_add为添加时的时间，更新对象时不会有变动
    create_date = models.DateTimeField(auto_now_add=True)
    # 修改时间 auto_now无论是你添加还是修改对象
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "integ_fieldtype"
        unique_together = ("db_type", "fields_type")
        verbose_name = '字段类型'

    def __str__(self):
        return "{}".format(self.fields_type)


# 4.表层次结构
class TableLevel(models.Model):
    table_level_name = models.CharField(max_length=64, unique=True, db_column='table_level_name', verbose_name='表层次名称')
    table_level_cn_name = models.CharField(max_length=64, unique=True, db_column='table_level_cn_name',
                                           verbose_name='表层次中文名称')
    table_level_describe = models.TextField(blank=True, default="", verbose_name="说明")
    table_level_example = models.TextField(blank=True, default="", verbose_name="举例")
    # 创建时间auto_now_add为添加时的时间，更新对象时不会有变动
    create_date = models.DateTimeField(auto_now_add=True)
    # 修改时间 auto_now无论是你添加还是修改对象
    # 时间为你添加或者修改的时间
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "integ_tblevel"
        verbose_name = '层次结构'

    def __str__(self):
        return "{}({})".format(self.table_level_name, self.table_level_cn_name)


# 5.数据库实体
class Database(models.Model):
    # 数据库类型
    db_type = models.ForeignKey(DatabaseType, on_delete=models.PROTECT, verbose_name='数据库类型', default='1')

    # 数据库名称
    db_name = models.CharField(max_length=64, db_column='db_name', verbose_name='数据库名称')

    # 数据库中文名称
    db_cn_name = models.CharField(max_length=64, verbose_name='数据库中文名称')

    # 所属租户
    # lessee_name = models.ForeignKey(Lessee,on_delete=models.PROTECT,verbose_name='所属租户',default='1')

    # 集群默认路径
    warehouse_dir = models.TextField(blank=True, default="hdfs://NameNodeHACluster/apps/hive/warehouse",
                                     verbose_name="集群默认路径")

    # 数据库默认路径
    database_hdfs = models.CharField(max_length=128, default='db', verbose_name='数据库hdfs配置路径')

    # 是否生效
    EFF_CHOICES = (
        ('0', '失效'),
        ('1', '生效'),
    )

    eff_flag = models.CharField(max_length=16, choices=EFF_CHOICES, verbose_name='是否生效', default='1')

    remark = models.TextField(blank=True, default="", verbose_name="数据库备注")

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        verbose_name='创建者',
        default='1',
    )

    # 创建时间auto_now_add为添加时的时间，更新对象时不会有变动
    create_date = models.DateTimeField(auto_now_add=True)

    # 修改时间 auto_now无论是你添加还是修改对象
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "integ_db"
        unique_together = ("db_type", "db_name")  # 唯一:数据库类型 + 数据库名称
        verbose_name = '数据库'

    def __str__(self):
        return "{}--{}".format(self.db_type, self.db_name)


# 6.表
class Table(models.Model):
    # 所属数据库
    db_name_id = models.ForeignKey(Database, on_delete=models.PROTECT, verbose_name='数据库名称', default='1')

    # 表名称
    tb_name = models.CharField(max_length=64, verbose_name='表名称')

    # 表中文解释
    tb_cn_name = models.CharField(max_length=64, verbose_name='表中文名称')

    # 表作业名称
    tb_job = models.CharField(max_length=64, blank=True, verbose_name='表作业名称')

    # 表业务线
    # table_businessline = models.ManyToManyField(to="BusinessLine",name="Table",verbose_name="来源业务")

    # 表层次结构
    table_level = models.ForeignKey(TableLevel, on_delete=models.PROTECT, verbose_name='层次结构', default='1')

    # 表主题
    table_theme = models.ForeignKey(Theme, on_delete=models.PROTECT, verbose_name='表主题', default='1')

    # 表状态
    MANAGE_ETERNAL_CHOICES = (
        ('-1', '其他'),
        ('0', '管理表'),
        ('1', '外部表'),
    )

    manage_external_flag = models.CharField(max_length=16, choices=MANAGE_ETERNAL_CHOICES, verbose_name='管理外部表标志',
                                            default='1')

    # 是否表分区
    PARTITION_CHOICES = (
        ('-1', '其他'),
        ('0', '非分区表'),
        ('1', '是分区表')
    )
    partition_flag = models.CharField(max_length=16, choices=PARTITION_CHOICES, verbose_name='是否分区', default='1')

    # 全量/增量
    SD_CHOICES = (
        ('-1', '其他'),
        ('0', '增量'),
        ('1', '全量'),
    )
    sd_flag = models.CharField(max_length=16, choices=SD_CHOICES, verbose_name='全量/增量', default='1')

    # 是否静态维表
    STATIC_CHOICES = (
        ('0', '否'),
        ('1', '是'),
    )

    static_flag = models.CharField(max_length=16, choices=STATIC_CHOICES, verbose_name='是否静态维表', default='0')

    # 机密程度

    SECRET_LEVEL_CHOICES = (
        ('0', 'S0'),
        ('1', 'S1'),
        ('2', 'S2'),
        ('3', 'S3'),
    )

    secret_level = models.CharField(max_length=16, choices=SECRET_LEVEL_CHOICES, verbose_name='机密程度', default='1')

    # 重要程度
    IMPORT_LEVEL_CHOICES = (
        ('0', 'P0'),
        ('1', 'P1'),
        ('2', 'P2'),
        ('3', 'P3'),
        ('4', 'P4'),
    )
    import_level = models.CharField(max_length=16, choices=IMPORT_LEVEL_CHOICES, verbose_name='重要程度', default='2')

    # 时间粒度
    TIME_GRANULARITY_CHOICES = (
        ('0', '无'),
        ('1', '秒'),
        ('2', '分钟'),
        ('3', '小时'),
        ('4', '天'),
        ('5', '月'),
        ('6', '年'),
    )
    time_granularity = models.CharField(max_length=16, choices=TIME_GRANULARITY_CHOICES, verbose_name='时间粒度',
                                        default='4')

    # 生命周期
    LIFE_CYCLE_CHOICES = (
        ('0', '未定'),
        ('1', '一天'),
        ('2', '一周'),
        ('3', '一月'),
        ('4', '三月'),
        ('5', '半年'),
        ('6', '一年'),
        ('7', '三年'),
        ('8', '五年'),
        ('9', '永久'),
    )
    life_cycle = models.CharField(max_length=16, choices=LIFE_CYCLE_CHOICES, verbose_name='生命周期', default='7')

    # 表hdfs路径
    hdfsfile = models.CharField(max_length=128, blank=True, verbose_name='HDFS路径')

    # 负责人
    table_author = models.CharField(max_length=128, blank=True, verbose_name='负责人')

    # 表状态
    STATE_CHOICES = (
        ('1', '开发中'),
        ('2', '测试中'),
        ('3', '已上线'),
        ('4', '已下线'),
        ('5', '其他'),
    )
    state_flag = models.CharField(max_length=16, choices=STATE_CHOICES, verbose_name='表状态', default='1')

    # 是否有效
    EFF_CHOICES = (
        ('0', '无效'),
        ('1', '有效'),
    )

    eff_flag = models.CharField(max_length=16, choices=EFF_CHOICES, verbose_name='是否有效', default='1')

    # 对应数据源()
    source_key = models.CharField(max_length=128, blank=True, verbose_name='对应数据源Key')

    # 对应源数据库
    source_db = models.CharField(max_length=128, blank=True, verbose_name='对应源数据库')

    # 对应源数据表
    source_table = models.CharField(max_length=128, blank=True, verbose_name='对应源数据表')

    # 数据源对接人
    source_author = models.CharField(max_length=128, blank=True, verbose_name='数据源对接人')

    # 作业存放路径名称
    job_source_dir = models.CharField(max_length=128, blank=True, verbose_name='作业存放路径名称')

    table_detail = models.TextField(blank=True, default="", verbose_name="表注释(计算逻辑&业务说明)")

    tb_job_script = models.TextField(blank=True, default="", verbose_name="脚本代码")

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        verbose_name='创建者',
        default='1',
    )

    # 创建时间auto_now_add为添加时的时间，更新对象时不会有变动
    create_date = models.DateTimeField(auto_now_add=True)

    # 修改时间 auto_now无论是你添加还是修改对象
    # 时间为你添加或者修改的时间
    update_date = models.DateTimeField(auto_now=True)

    # update_date = models.DateTimeField(auto_now=True,verbose_name='更新时间')

    def __str__(self):
        return "{}--{}".format(self.db_name_id, self.tb_name)

    class Meta:
        db_table = "integ_table"
        unique_together = ("db_name_id", "tb_name")
        verbose_name = '表'


# 字段
class Fields(models.Model):
    # 表id
    tb_name_id = models.ForeignKey(Table, on_delete=models.CASCADE, verbose_name='所属表')
    # 字段序号
    fields_rank = models.IntegerField(verbose_name='字段序号', editable=True)
    # 字段名称
    fields_name = models.CharField(max_length=128, verbose_name='字段名称')
    # 字段中文名称
    fields_cn_name = models.CharField(max_length=128, verbose_name='字段解释')
    # 字段类型
    fields_type = models.ForeignKey(FieldType, on_delete=models.PROTECT, verbose_name='字段类型')

    # 是否分区字段
    PARTITION_CHOICES = (
        ('1', '是'),
        ('0', '否'),
    )

    partition_flag = models.CharField(max_length=16, choices=PARTITION_CHOICES, verbose_name='是否分区字段', default='0')

    # 是否有效
    # EFF_CHOICES = (
    #     ('0', '无效'),
    #     ('1', '有效'),
    # )

    # eff_flag = models.CharField(max_length=16,choices=EFF_CHOICES,verbose_name='是否有效',default='1')

    fields_detail = models.TextField(blank=True, default="来源表和字段:", verbose_name="字段规则")

    create_date = models.DateTimeField(auto_now_add=True)

    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "integ_fields"
        unique_together = ("tb_name_id", "fields_name")
        unique_together = ("tb_name_id", "fields_rank")
        verbose_name = '字段'

    def __str__(self):
        # return "{}.{}  {}--{}".format(self.db_name,self.tb_name,self.fields_name,self.fields_cn_name)
        return "{}".format(self.fields_name)
