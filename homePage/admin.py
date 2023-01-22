from django.contrib import admin

#allow admin to add embeded videos to page

from homePage.models import Video

admin.site.register(Video)