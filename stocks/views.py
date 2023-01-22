from django.shortcuts import render

def stocks_view(request):
    context = {}
    return render(request, 'stocks/stocks.html',context)
