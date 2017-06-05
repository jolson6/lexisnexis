import os
import logging.config

from django.shortcuts import render
from django.middleware.csrf import get_token
from lxml import etree
from django.urls import reverse_lazy
from django.views.generic import FormView
from zeep import Client
from zeep.exceptions import Fault

from file_browser.forms import SearchForm
from lexisnexis.settings.base import BASE_DIR


class FileBrowseView(FormView):
    template_name = 'file_browser/file_browse.html'
    success_url = reverse_lazy('file_browse')
    form_class = SearchForm

    def form_valid(self, form):
        # This bit of code prints out some debugging messages

        # logging.config.dictConfig({
        #     'version': 1,
        #     'formatters': {
        #         'verbose': {
        #             'format': '%(name)s: %(message)s'
        #         }
        #     },
        #     'handlers': {
        #         'console': {
        #             'level': 'DEBUG',
        #             'class': 'logging.StreamHandler',
        #             'formatter': 'verbose',
        #         },
        #     },
        #     'loggers': {
        #         'zeep.transports': {
        #             'level': 'DEBUG',
        #             'propagate': True,
        #             'handlers': ['console'],
        #         },
        #     }
        # })

        # Get the context so it can be returned in the render()
        context = super(FileBrowseView, self).get_context_data()

        path = os.path.join(BASE_DIR, 'static/WSK1.41-General-Cert/WSAPI-1_0.wsdl')

        # Use the Authentication Client to authenticate the user, then retrieve auth_token for use in other requests
        auth_client = Client(path, port_name='Authentication')
        result = auth_client.service.Authenticate(authId='STEVEHAYES@WSK', password='testing77')
        auth_token = result['binarySecurityToken']

        # Use the Search Client to search the database using the parameters from the SearchFrom
        search_client = Client(path, port_name='Search')
        try:
            search_results = search_client.service.Search(
                binarySecurityToken=auth_token,
                query=form.cleaned_data['query'],
                sourceInformation={
                    'sourceIdList': {
                        'sourceId': form.cleaned_data['source_id'],
                    },
                },
                searchOptions={
                    'sortOrder': form.cleaned_data['sort_order'],
                    'searchMethod': form.cleaned_data['search_method'],
                },
                retrievalOptions={
                    'documentView': form.cleaned_data['document_view'],
                    'documentMarkup': form.cleaned_data['document_markup'],
                    'documentRange': {
                        'begin': form.cleaned_data['range_begin'],
                        'end': form.cleaned_data['range_end'],
                    }
                },
            )

            print(search_results)
            context['documents_found'] = search_results.documentsFound

            documents_list = search_results.documentContainerList.documentContainer
            documents = {}

            for i, result in enumerate(documents_list):
                file_path = os.path.join(BASE_DIR, 'media/test-' + str(i + 1) + '.html')
                documents[i + 1] = result['document']
                file = open(file_path, 'wb')
                file.write(result['document'])
                file.close()
            context['documents'] = documents

        except Fault as fault:
            print('fault! ', etree.tostring(fault.detail, pretty_print=True))

        context['form'] = form

        # Since we are re-rendering the page, put the csrf_token in the context manually.
        token = get_token(self.request)
        context['csrf_token'] = token

        # Code for retrieving a particular document by ID. This isn't needed at the moment because the Search Client
        # can also return full text.

        # retrieval_client = Client(path, port_name='Retrieval')
        # try:
        #     print('\nretrieve my documents!\n')
        #     retrieval_result = retrieval_client.service.GetDocumentsByDocumentId(
        #         binarySecurityToken=auth_token,
        #         documentIdList={
        #             'documentId': '02A6A252C52394AB97B14672E56C2F2F0468938A0B5C1E76554DD51C793D8635D6113131EB4D7F4E778B150857AF0000E874A742678F6C1BC2AF35783B5AFF206562C447ED915BBFE8AF3835CCA91D1F6A11A562BED01830ED4E0FBC78575EEA488FAE7847C89631C7EAB25FDC14FAA6',
        #         },
        #         retrievalOptions={
        #             'documentView': 'FullTextWithTerms',
        #             'documentMarkup': 'Semantic',
        #         }
        #     )
        #     print('retrieval result: ', retrieval_result, '\n')
        #     thing = retrieval_result.documentContainerList.documentContainer[0]['document']
        #     print(thing, '\n', type(thing))
        #     xml_thing = etree.fromstring(thing)
        #     thing_again = etree.tostring(xml_thing, pretty_print=True)
        #     print(thing_again, '\n', type(thing_again))
        #
        #     file = open(os.path.join(BASE_DIR, 'solo-test.xml'), 'wb')
        #     file.write(thing)
        #     file.close()
        # except Exception as e:
        #     print(type(e), e)
        #
        # return super(FileBrowseView, self).form_valid(form)

        return render(request=self.request, template_name=self.template_name, context=context)
