from django.shortcuts import render


def activate_account(request, uid, token):
    return render(request, "activate_account.html", {"uid": uid, "token": token})


def password_reset(request, uid, token):
    return render(request, "password_reset.html", {"uid": uid, "token": token})
