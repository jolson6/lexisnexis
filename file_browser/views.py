from django.views.generic import TemplateView


class FileBrowseView(TemplateView):
    template_name = 'file_browser/file_browse.html'
