from django.shortcuts import render
from script.getStatus import run
from django.conf import settings
from django.core.mail import send_mail
from script.models import Emails, SiteInfo
from django.db.models import Q
# Create your views here.

# 定时任务
from apscheduler.scheduler import Scheduler
sched = Scheduler()

#每十分钟检测一次
@sched.interval_schedule(seconds=10*60)
def timer():
    run()
    data = SiteInfo.objects.filter(Q(alive=True) | Q(death=True))
    if data.exists():
        send()

sched.start()


# 当网站状态变化时，发送邮件提醒
def send():
    subject = '站点监测'	#主题
    message = '测试'
    sender = settings.EMAIL_FROM		#发送邮箱，已经在settings.py设置，直接导入
    emalis = Emails.objects.filter(is_send=True)
    emali_list = []
    for i in emalis:
        emali_list.append(i.emali.strip())
   # print(emali_list)
    content = ""
    sites_alive = SiteInfo.objects.filter(alive=True)
    for i in sites_alive:
        content += "<a href= '" + i.url + "'>" + i.url + "</a>  ------  已可访问</br>"
   # print(emali_list)

    sites_death = SiteInfo.objects.filter(death=True)
    for i in sites_death:
        content += "<a href= '" + i.url + "'>" + i.url + "</a>  ------  失联了！</br>"
    send_mail(subject, message, sender, emali_list, html_message=content)


