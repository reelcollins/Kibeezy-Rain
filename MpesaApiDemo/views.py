from django.shortcuts import render

from .genrateAcesstoken import get_access_token
from .stkPush import initiate_stk_push
from .query import query_stk_status



def stkpush_form(request):
    return render(request, 'stkpush_form.html')