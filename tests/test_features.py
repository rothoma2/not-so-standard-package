import pytest
import sys

# import features

sys.path.append('/home/arlindo/not-so-standard-package')
from features.features import SnippetStats



def test_stats():

    # snippet = "fFewrgwjr\nfghfghfedbetneytl356903598y24R#%^#%^Y5e\ndfkjdgfjbwrtijlh356h"
    # snippet='fA\ndsfergkopGF#%^34534tgjklwrtb\ngk'
    snippet = '''from django.contrib import admin\n
    from django.urls import path\n
    dfjhsdfhdsf$56456745$%#^fdDFGBNDFgbDFGHND\n
    from . import views\n

    '''
    snippet_stats=SnippetStats()
    snippet_stats.set_snippet(snippet)
    snippet_stats.line_entropy()
    # print(snippet_stats.entropy_list)

    entropy = snippet_stats.shannon_entropy__file()
    # assert entropy !=0

    # value = snippet_stats.shannon_entropy__max()
    # # print(snippet_stats.entropy_list)
    # assert value !=0 

    # value = snippet_stats.shannon_entropy__mean()
    # # print(snippet_stats.entropy_list)
    # assert value ==0 

    # value = snippet_stats.shannon_entropy__median()
    # # print(snippet_stats.entropy_list)
    # assert value!=0 

    # value = snippet_stats.shannon_entropy__1Q()
    # # print(snippet_stats.entropy_list)
    # assert value !=0 

    # value = snippet_stats.shannon_entropy__3Q()
    # # print(snippet_stats.entropy_list)
    # assert value ==0 

    value = snippet_stats.shannon_entropy__outliers()
    print(value)
    # print(snippet_stats.entropy_list)
    assert 1==0