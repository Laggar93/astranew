from django.template import Library
register = Library()


@register.filter()


def replace_ajax(value):
     
    if value:
        
        return value.replace('_ajax', '')
    
    else:
          
        return ''