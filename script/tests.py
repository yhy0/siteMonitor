from django.test import TestCase
import django.utils.timezone as timezone
# Create your tests here.
url = "https://jd.com"

if (not url.startswith('http://')) and (not url.startswith('https://')):
    url = 'http://' + url

print(url)