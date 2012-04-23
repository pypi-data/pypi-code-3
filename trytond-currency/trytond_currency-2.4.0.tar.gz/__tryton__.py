#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
{
    'name': 'Currency',
    'name_bg_BG': 'Валута',
    'name_ca_ES': 'Divisa',
    'name_de_DE': 'Währung',
    'name_es_AR': 'Divisa',
    'name_es_CO': 'Moneda',
    'name_es_ES': 'Divisa',
    'name_fr_FR': 'Devise',
    'version': '2.4.0',
    'author': 'B2CK',
    'email': 'info@b2ck.com',
    'website': 'http://www.tryton.org/',
    'description': '''Define currencies and exchange rate.
Allow to customize the formatting of the currency amount.
''',
    'description_bg_BG': '''Задаване на валути и обменни курсове.
 Позволява настройване на форматиране на сумата на валута.
''',
    'description_ca_ES': '''Defineix les monedes i la taxa de conversió.
Permet personalitzar el format de visualització de la divisa.
''',
    'description_de_DE': ''' - Ermöglicht die Eingabe von Währungen und Wechselkursen.
 - Erlaubt die beliebige Formatierung von Währungsbeträgen.
''',
    'description_es_AR': '''Define las divisas y la tasa de cambio.
 - Permite personalizar el formato de visualización de la divisa.
''',
    'description_es_CO': '''Define las monedas y la tasa de cambio.
Permite personalizar el formato de visualización de la moneda.
''',
    'description_es_ES': '''Define las divisas y la tasa de cambio.
 - Permite personalizar el formato de visualización de la divisa.
''',
    'description_fr_FR': '''Défini les devises et leurs taux de change.
Permet de formater les montants en fonction de la devise.
''',
    'depends': [
        'ir',
        'res',
    ],
    'xml': [
        'currency.xml',
    ],
    'translation': [
        'locale/bg_BG.po',
        'locale/cs_CZ.po',
        'locale/ca_ES.po',
        'locale/de_DE.po',
        'locale/es_AR.po',
        'locale/es_CO.po',
        'locale/es_ES.po',
        'locale/fr_FR.po',
        'locale/nl_NL.po',
        'locale/ru_RU.po',
    ]
}
