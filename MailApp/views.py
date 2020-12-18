from django.shortcuts import redirect


def main(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('report')
        else:
            return redirect('requests')
    else:
        return redirect('login')
