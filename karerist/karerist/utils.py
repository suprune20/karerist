# -*- coding: utf-8 -*-

import re, string

def capitalize(s):
    """
    Капитализация строки имени, фамилии, отчества

    Учесть двойные фамилии (Петров-Водкин) и много слов, например, Эрих Мария
    """
    if s is None:
        return ''
    dash_char = lambda m: u"-%s" % m.group(1).upper()
    return s and re.sub(r'\-(\S)', dash_char, string.capwords(s)) or ''
