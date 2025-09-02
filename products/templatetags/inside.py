from django.template import Library
register = Library()


@register.filter()


def inside(array, params):
    
    if array and params:

        l = []

        for i in array:
            l.append(i.id)

        return array_match(l, params)
    
    else:
          
        return ''


def array_match(array1, array2):


    set1 = set(array1)
    set2 = set(array2)

    common_elements = set1.intersection(set2)
    amount_of_matches = len(common_elements)

    return amount_of_matches