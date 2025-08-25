from django.template import Library
register = Library()


@register.filter()


def float(price):
     
    if price:
        
        return '{:,}'.format(price).replace(',', ' ').replace('.0', '').replace('.', ',')
    
    else:
          
        return ''