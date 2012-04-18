def str_to_unicode(text, encoding=None, errors='strict'):
    if encoding is None:
        encoding = 'utf-8'
    if isinstance(text, str):
        return text.decode(encoding, errors)
    return text

def unicode_to_str(text, encoding=None, errors='strict'):
    if encoding is None:
        encoding = 'utf-8'
    if isinstance(text, unicode):
        return text.encode(encoding, errors)
    return text
