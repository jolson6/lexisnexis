from django.urls import reverse_lazy
from django.views.generic import FormView

from file_browser.forms import SearchForm


class FileBrowseView(FormView):
    template_name = 'file_browser/file_browse.html'
    success_url = reverse_lazy('file_browse')
    form_class = SearchForm

    def form_valid(self, form):
        # Process the form here
        
        return super(FileBrowseView, self).form_valid(form)
