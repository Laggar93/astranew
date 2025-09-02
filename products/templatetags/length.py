from django.template import Library
register = Library()


@register.filter()


def length(array):
    
    if array:
        
        return len(array)
    
    else:
          
        return ''