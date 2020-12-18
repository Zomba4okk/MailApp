from django.http import JsonResponse

from print_edition.models import PrintEdition


def get_price(request, print_edition_id):
    print_edition = PrintEdition.objects.get(id=print_edition_id)

    return JsonResponse({'price': print_edition.price if print_edition else None})
