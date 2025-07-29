from django import template

register = template.Library()


@register.inclusion_tag("TourSite/partials/header.html", takes_context=True)
def header(context):
    return context


@register.inclusion_tag("TourSite/partials/footer.html", takes_context=True)
def footer(context):
    return context
