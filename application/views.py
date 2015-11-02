from django.shortcuts import render
# from django.contrib.auth import authenticate, login
# from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie


# @csrf_protect
# @ensure_csrf_cookie
# def app(request):
#     user = authenticate(username='bob', password='bob')
#     if user is not None:
#         login(request, user)
#         return render(request, 'app')

def app(request):
    return render(request, 'app.html')
