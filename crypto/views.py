from django.shortcuts import render

def crypto_view(request):
    context = {}
    return render(request, 'crypto/crypto.html',context)
