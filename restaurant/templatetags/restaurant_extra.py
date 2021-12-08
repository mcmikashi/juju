from django import template
register = template.Library()

@register.simple_tag
def caculeTotale(quantite,prix_unitaire):
    return quantite*prix_unitaire