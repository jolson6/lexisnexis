from django.conf.urls import url

from file_browser.views import FileBrowseView

urlpatterns = [
    url(r'^$', FileBrowseView.as_view(), name='file_browse'),
]
