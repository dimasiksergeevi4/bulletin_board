from django import template


register = template.Library()

CENSORS = ['редиска', 'сосиска', 'петух гамбургский', 'корм', 'матч']


@register.filter(name='censor')
def censor(value):
    for word in CENSORS:
        if word in value:
            value = value.replace(word, f'{word[0]}{(len(word)-1)*"*"}')
    return value
