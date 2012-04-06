# -*- coding: utf-8 -*-
# <Lettuce - Behaviour Driven Development for python>
# Copyright (C) <2010-2011>  Gabriel Falcão <gabriel@nacaolivre.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

LANGUAGES = {
    'en': {
        'examples': u'Examples|Scenarios',
        'feature': u'Feature',
        'name': u'English',
        'native': u'English',
        'scenario': u'Scenario',
        'scenario_outline': u'Scenario Outline',
        'scenario_separator': u'(Scenario Outline|Scenario)',
    },
    'pt-br': {
        'examples': u'Exemplos|Cenários',
        'feature': u'Funcionalidade',
        'name': u'Portuguese',
        'native': u'Português',
        'scenario': u'Cenário|Cenario',
        'scenario_outline': u'Esquema do Cenário|Esquema do Cenario',
        'scenario_separator': u'(Esquema do Cenário|Esquema do Cenario|Cenario|Cenário)',
    },
    'pl': {
        'examples': u'Przykład',
        'feature': u'Właściwość',
        'name': u'Polish',
        'native': u'Polski',
        'scenario': u'Scenariusz',
        'scenario_outline': u'Zarys Scenariusza',
        'scenario_separator': u'(Zarys Scenariusza|Scenariusz)',
    },
    'ca': {
        'examples': u'Exemples',
        'feature': u'Funcionalitat',
        'name': u'Catalan',
        'native': u'Català',
        'scenario': u'Escenari',
        'scenario_outline': u"Esquema d'Escenari",
        'scenario_separator': u"(Esquema d'Escenari|Escenari)",
    },
    'es': {
        'examples': u'Ejemplos',
        'feature': u'Funcionalidad',
        'name': u'Spanish',
        'native': u'Español',
        'scenario': u'Escenario',
        'scenario_outline': u'Esquema de Escenario',
        'scenario_separator': u'(Esquema de Escenario|Escenario)',
    },
    'hu': {
        'examples': u'Példák',
        'feature': u'Jellemző',
        'name': u'Hungarian',
        'native': u'Magyar',
        'scenario': u'Forgatókönyv',
        'scenario_outline': u'Forgatókönyv vázlat',
        'scenario_separator': u'(Forgatókönyv|Forgatókönyv vázlat)',
    },
    'fr': {
        'examples': u'Exemples|Scénarios',
        'feature': u'Fonctionnalité|Fonction',
        'name': u'French',
        'native': u'Français',
        'scenario': u'Scénario',
        'scenario_outline': u'Plan de Scénario|Plan du Scénario',
        'scenario_separator': u'(Plan de Scénario|Plan du Scénario|Scénario)',
   },
    'de': {
        'examples': u'Beispiele|Szenarios',
        'feature': u'Funktionalität|Funktion',
        'name': u'German',
        'native': u'Deutsch',
        'scenario': u'Szenario',
        'scenario_outline': u'Szenario-Zusammenfassung|Zusammenfassung',
        'scenario_separator': u'(Szenario-Zusammenfassung|Zusammenfassung)',
   },
    'ja': {
        'examples': u'例',
        'feature': u'フィーチャ',
        'name': u'Japanese',
        'native': u'日本語',
        'scenario': u'シナリオ',
        'scenario_outline': u'シナリオアウトライン|シナリオテンプレート|テンプレ|シナリオテンプレ',
        'scenario_separator': u'(シナリオ|シナリオアウトライン|シナリオテンプレート|テンプレ|シナリオテンプレ)',
    },
    'tr': {
        'examples': u'Örnekler',
        'feature': u'Özellik',
        'name': u'Turkish',
        'native': u'Türkçe',
        'scenario': u'Senaryo',
        'scenario_outline': u'Senaryo taslağı|Senaryo Taslağı',
        'scenario_separator': u'(Senaryo taslağı|Senaryo Taslağı|Senaryo)',
     },
     'zh-CN': {
        'examples': u'例如|场景集',
        'feature': u'特性',
        'name': u'Simplified Chinese',
        'native': u'简体中文',
        'scenario': u'场景',
        'scenario_outline': u'场景模板',
        'scenario_separator': u'(场景模板|场景)',
    },
     'zh-TW': {
        'examples': u'例如|場景集',
        'feature': u'特性',
        'name': u'Traditional Chinese',
        'native': u'繁體中文',
        'scenario': u'場景',
        'scenario_outline': u'場景模板',
        'scenario_separator': u'(場景模板|場景)',
    },
    'ru': {
        'examples': u'Примеры|Сценарии',
        'feature': u'Функционал',
        'name': u'Russian',
        'native': u'Русский',
        'scenario': u'Сценарий',
        'scenario_outline': u'Структура сценария',
        'scenario_separator': u'(Структура сценария|Сценарий)',
    },
    'uk': {
        'examples': u'Приклади|Сценарії',
        'feature': u'Функціонал',
        'name': u'Ukrainian',
        'native': u'Українська',
        'scenario': u'Сценарій',
        'scenario_outline': u'Структура сценарію',
        'scenario_separator': u'(Структура сценарію|Сценарій)',
    },
    'it': {
        'examples': u'Esempi|Scenari|Scenarii',
        'feature': u'Funzionalità|Funzione',
        'name': u'Italian',
        'native': u'Italiano',
        'scenario': u'Scenario',
        'scenario_outline': u'Schema di Scenario|Piano di Scenario',
        'scenario_separator': u'(Schema di Scenario|Piano di Scenario|Scenario)',
    },
    'no': {
        'examples': u'Eksempler',
        'feature': u'Egenskaper',
        'name': u'Norwegian',
        'native': u'Norsk',
        'scenario': u'Situasjon',
        'scenario_outline': u'Situasjon Oversikt',
        'scenario_separator': u'(Situasjon Oversikt|Situasjon)',
    }
}
