#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
{
    'name': 'Workflow',
    'name_de_DE': 'Workflow',
    'name_es_ES': 'Flujo de trabajo',
    'name_fr_FR': 'Workflow',
    'name_ru_RU': 'Бизнес процессы',
    'description': '''Basic module providing concept and administration of workflows.
''',
    'description_de_DE': '''Basismodul für Konzept und Administration von Workflows
''',
    'description_es_ES': '''Módulo básico que provee el concepto y administración de flujos de trabajo.
''',
    'description_fr_FR': '''Module de base fournissant les concepts et l'administration de workflows.
''',
    'description_ru_RU': '''Базовый модуль концепция обеспечения и администрирования рабочих процессов.
''',
    'active': True,
    'depends': ['ir', 'res'],
    'xml': [
        'workflow.xml',
        ],
    'translation': [
        'fr_FR.csv',
        'de_DE.csv',
        'es_ES.csv',
        'es_CO.csv',
        'ru_RU.csv',
    ],
}
