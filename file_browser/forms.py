from django import forms


class SearchForm (forms.Form):
    query = forms.CharField(label='Query')
    project_id = forms.IntegerField(label='Source ID')
    source_id = forms.IntegerField(label='Source ID')
    date_restriction_start = forms.DateField(label='From', required=False)
    date_restriction_end = forms.DateField(label='To', required=False)
    search_method = forms.ChoiceField(
        label='Search Method',
        choices=(
            ('boolean', 'Boolean'),
            ('match_on_all_words', 'Match On All Words'),
            ('match_on_any_word', 'Match On Any Word'),
            ('match_on_phrase', 'Match On Phrase'),
        )
    )
    sort_order = forms.ChoiceField(
        label='Sort Order',
        choices=(
            ('date', 'Date'),
            ('implied', 'Implied'),
            ('relevance', 'Relevance')
        )
    )
    document_markup = forms.ChoiceField(
        label='Document Markup',
        choices=(
            ('display', 'Display'),
            ('semantic', 'Semantic'),
        )
    )
    document_view = forms.ChoiceField(
        label='Sort Order',
        choices=(
            ('cite', 'Cite'),
            ('expanded_cite', 'Expanded Cite'),
            ('full_text', 'Full Text'),
            ('full_text_with_terms', 'Full Text With Terms')
        )
    )
    range_begin = forms.IntegerField(label='Begin', required=False)
    range_end = forms.IntegerField(label='End', required=False)
