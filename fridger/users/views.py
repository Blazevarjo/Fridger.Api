from django.shortcuts import render


def activate_account(request, uid, token):
    return render(request, "activate_account.html", {"uid": uid, "token": token})
