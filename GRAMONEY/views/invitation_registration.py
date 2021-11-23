import random
import string

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404

from ..forms import *
from ..models import *


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def referral_registration(request, invite):
    get_code = get_object_or_404(Account, code=invite)

    if request.POST:
        form = RegisterForm(request.POST)

        if form.is_valid():
            get_user = form.save()

            login(request, get_user)
            Account.objects.create(user=get_user, invite=get_code.code, code=id_generator())

            return redirect('GRAMONEY:user_home')

    else:
        form = RegisterForm()

    context = {

        'form': form,

    }
    return render(request, 'GRAMONEY/registration_referral.html', context)
