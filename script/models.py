from django.db import models
from django.utils.html import format_html

# Create your models here.
class SiteInfo(models.Model):
    url = models.CharField(max_length= 100)
    title = models.CharField(max_length= 100, blank = True)
    status = models.CharField(max_length=10, blank = True)
    updateTime = models.DateTimeField('updateTime', auto_now=True)
    is_send = models.BooleanField(default = True)
    alive = models.BooleanField(default = True)
    death = models.BooleanField(default = True)

    class Meta:
        verbose_name = u"目标状况"
        verbose_name_plural = u"1.目标状况"
    #设置响应码颜色
    def colored_status(self):
        color_code = 'green'
        if self.status != '200':
            color_code = "red"
        return format_html(
            '<span style="color: {};">{}</span>',
            color_code,
            self.status,
        )
    # 让有颜色的字段在排序时遵循原来的字段和别名
    colored_status.admin_order_field = 'status'
    colored_status.short_description = u'status'

    def shortcut_title(self):
        if len(str(self.title)) > 10:
            return self.title[:10] + "..."
        else:
            return self.title
    # 设置截断的intro在排序时遵循原来的字段
    shortcut_title.admin_order_field = 'title'



class Sites(models.Model):
    # 文件上传
    file_upload = models.FileField(verbose_name='文件',)

    class Meta:
        verbose_name = u"文件上传"
        verbose_name_plural = u"2.文件上传"

class Emails(models.Model):
    # 文件上传
    emali = models.CharField(max_length = 100)
    is_send = models.BooleanField("是否发送", default=True)

    # 设置响应码颜色
    def colored_status(self):
        color_code = 'green'
        if not self.is_send :
            color_code = "red"
        return format_html(
            '<span style="color: {};">{}</span>',
            color_code,
            self.is_send,
        )

    # 让有颜色的字段在排序时遵循原来的字段和别名
    colored_status.admin_order_field = 'status'
    colored_status.short_description = u'status'

    class Meta:
        verbose_name = u"邮箱管理"
        verbose_name_plural = u"3.邮箱管理"
