from django.shortcuts import redirect

from karaage.common.decorators import login_required


@login_required
def shib_receiver(request, next_path):
    if next_path:
        return redirect(next_path)
    return redirect('index')
