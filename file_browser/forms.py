import datetime
from django import forms


class SearchForm (forms.Form):
    query = forms.CharField(label='Query')
    source_id = forms.IntegerField(label='Source ID', initial='161887')
    project_id = forms.IntegerField(label='Project ID', required=False, initial='8412')
    date_restriction_start = forms.DateField(
        label='From',
        required=False,
        widget=forms.SelectDateWidget(years=range(1980, datetime.datetime.now().year + 1)),
        initial=datetime.datetime.now()
    )
    date_restriction_end = forms.DateField(
        label='To',
        required=False,
        widget=forms.SelectDateWidget(years=range(1980, datetime.datetime.now().year + 1)),
        initial=datetime.datetime.now()
    )
    search_method = forms.ChoiceField(
        label='Search Method',
        choices=(
            ('Boolean', 'Boolean'),
            ('MatchOnAllWords', 'Match On All Words'),
            ('MatchOnAnyWord', 'Match On Any Word'),
            ('MatchOnPhrase', 'Match On Phrase'),
        )
    )
    sort_order = forms.ChoiceField(
        label='Sort Order',
        choices=(
            ('Date', 'Date'),
            ('Implied', 'Implied'),
            ('Relevance', 'Relevance')
        )
    )
    document_markup = forms.ChoiceField(
        label='Document Markup',
        choices=(
            ('Display', 'Display'),
            ('Semantic', 'Semantic'),
        ),
        initial='Semantic',
    )
    document_view = forms.ChoiceField(
        label='Document View',
        choices=(
            ('Cite', 'Cite'),
            ('ExpandedCite', 'Expanded Cite'),
            ('FullText', 'Full Text'),
            ('FullTextWithTerms', 'Full Text With Terms')
        ),
        initial='FullTextWithTerms',
    )
    range_begin = forms.IntegerField(label='Begin', initial='1')
    range_end = forms.IntegerField(label='End', initial='10')
