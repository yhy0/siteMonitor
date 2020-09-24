from django.contrib import admin
from django.utils.html import format_html

from script.models import SiteInfo, Sites, Emails
from script import getStatus as gs

from concurrent.futures import ThreadPoolExecutor

# Register your models here.
admin.site.site_header = '监测'
admin.site.site_title = '站点监测'
admin.site.index_title = '站点监测'


@admin.register(SiteInfo)
class SiteInfoAdmin(admin.ModelAdmin):
    # 单个增加时显示
    fields = ('url',)

    # list_display设置要显示在列表中的字段，(id字段是Django模型的默认主键）
    list_display = ('id', 'url', 'title', 'colored_status', 'updateTime')
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 20
    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('status',)
    # 设置详细页面中的只读字段，此时不能在详细页面进行更改。
    readonly_fields = ('id', 'updateTime')
    # 筛选器
    list_filter = ('status', )  # 过滤器
    search_fields = ('url', 'title', 'status')  # 搜索字段
    date_hierarchy = 'updateTime'  # 详细时间分层筛选　

    def save_model(self, request, obj, form, change):
        gs.get_status(obj.url)
       # super().save_model(request, obj, form, change)

@admin.register(Sites)
class SitesAdmin(admin.ModelAdmin):

    # list_display设置要显示在列表中的字段，(id字段是Django模型的默认主键）
    list_display = ('id', 'file_upload', )
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 20
    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('id',)
    # 设置详细页面中的只读字段，此时不能在详细页面进行更改。
    readonly_fields = ('id', )
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        gs.get_single_file(obj.file_upload)


@admin.register(Emails)
class EmailsAdmin(admin.ModelAdmin):
    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50
    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('id',)
    # 设置详细页面中的只读字段，此时不能在详细页面进行更改。
    readonly_fields = ('id', )
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        #gs.get_single_file(obj.file_upload)

    # 添加功能，按钮或者超链接之类的
    def buttons(self, obj):
        button_html = '<a href="/email_test?id=%s"><input type="button" value="邮箱测试" /></a>'%(obj.id)
        return format_html(button_html)
    buttons.short_description = "操作"
    # list_display设置要显示在列表中的字段，(id字段是Django模型的默认主键）
    list_display = ('emali', 'is_send', 'buttons')

@admin.register(admin.models.LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    """
    该类用于显示 admin 内置的 django_admin_log 表。
    其中，content_type 是指用户修改的 Model 名
    """
    list_display = ['action_time', 'user', 'content_type', '__str__']
    list_display_links = ['action_time']
    list_filter = ['action_time', 'content_type', 'user']
    list_per_page = 15
    readonly_fields = ['action_time', 'user', 'content_type',
                       'object_id', 'object_repr', 'action_flag', 'change_message']