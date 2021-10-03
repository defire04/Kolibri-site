from django.shortcuts import render

from django.shortcuts import render

def test_view(request):
    return render(request, 'base.html', {})

