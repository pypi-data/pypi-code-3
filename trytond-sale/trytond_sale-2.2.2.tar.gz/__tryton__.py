#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
{
    'name': 'Sale',
    'name_bg_BG': 'Продажби',
    'name_de_DE': 'Verkauf',
    'name_es_CO': 'Ventas',
    'name_es_ES': 'Venta',
    'name_fr_FR': 'Vente',
    'name_nl_NL': 'Verkoop',
    'version': '2.2.2',
    'author': 'B2CK',
    'email': 'info@b2ck.com',
    'website': 'http://www.tryton.org/',
    'description': '''Define sale order.
Add to product sale informations.
Define the sale price as the list price.

With the possibilities:
    - to follow invoice and shipment states from the sale order.
    - to define invoice method:
        - Manual
        - On Order Confirmed
        - On shipment Sent
    - to define shipment method:
        - Manual
        - On Order Confirmed
        - On Invoice Paid
''',
    'description_bg_BG': ''' Задаване на поръчка за продажба.
 - Добавяне на информация за продажба на продукт.
 - Задаване на продажна цена като ценова листа.

Със следните възможности:
    - проследяване на състоянията на фактура и доставка от поръчката за продажба
    - задаване на начини на фактуриране:
        - Ръчно
        - При потвърждаване на поръчката
        - При изпращане
    - задаване на начина на доставка:
        - Ръчно
        - При потвърждаване на поръчката
        - При плащане на фактурата
''',
    'description_de_DE': ''' - Dient der Erstellung von Verkaufsvorgängen (Entwurf, Angebot, Auftrag).
 - Fügt den Artikeln Einkaufsinformationen hinzu.
 - Erlaubt die Definition des Einkaufspreises als Listenpreis.

Ermöglicht:
    - die Verfolgung des Status von Rechnungsstellung und Versand für Verkäufe
    - die Festlegung der Methode für die Rechnungsstellung:
        - Manuell
        - Nach Auftragsbestätigung
        - Nach Versand
    - die Festlegung der Methode für den Versand:
        - Manuell
        - Nach Auftragsbestätigung
        - Nach Bezahlung
''',
    'description_es_CO': ''' - Define la orden de Ventas.
 - Se añade al producto la información de ventas.
 - Definición del precio de venta y el precio de lista.

 - Con las posibilidades de:
    - seguir los estados de facturación y empaque desde la orden de venta.
    - definir el método de facturación:
        - Manual
        - Al Confirmar la Orden
        - Al Envío del Paquete
    - definir el método de empaque:
        - Manual
        - Al Confirmar la Orden
        - Contra el Pago de la Factura
''',
    'description_es_ES': '''Define orden de venta.
 - Añade a los productos información de ventas.
 - Define el precio de venta como el precio de lista.

 - Con la posibilidad de:
    - seguir los estados de facturación y envio desde la orden de venta.
    - definir el método de facturación:
        - Manual
        - A la confirmación de la orden
        - Al enviarlo
    - definir el método de envio:
        - Manual
        - Al confirmar la orden
        - Al pagar la factura
''',
    'description_fr_FR': '''Défini l'ordre de vente.
Ajoute au produit les informations de vente.

Avec la possibilité:
    - de suivre l'état de la facture et du colisage depuis l'ordre de vente
    - de choisir entre plusieurs méthodes de facturation:
        - Manuelle
        - Sur confirmation de la commande
        - À la livraison
    - de choisir entre plusieurs méthodes de colisage:
        - Manuelle
        - Sur confirmation de la commande
        - Au paiement de la facture
''',
	'description_nl_NL': '''Verkoopmodule.
Voegt verkoopinformatie toe aan producten.
Zet de catalogusprijs als verkoopprijs.

Biedt mogelijkheden tot:
    - het volgen van de factuur en de aflevering vanuit de offerte.
    - het instellen van de factuurafhandeling:
        - Handmatig
        - Bij opdrachtbevestiging
        - Bij aflevering
    - het instellen van de aflevering:
        - Handmatig
        - Bij opdrachtbevestiging
        - Na betaling
''',
    'depends': [
        'company',
        'party',
        'stock',
        'account',
        'product',
        'account_invoice',
        'workflow',
        'res',
        'ir',
        'currency',
        'account_product',
    ],
    'xml': [
        'sale.xml',
        'configuration.xml',
        'party.xml',
    ],
    'translation': [
        'locale/bg_BG.po',
        'locale/cs_CZ.po',
        'locale/de_DE.po',
        'locale/es_CO.po',
        'locale/es_ES.po',
        'locale/fr_FR.po',
        'locale/nl_NL.po',
        'locale/fr_FR.po',
        'locale/ru_RU.po',
    ],
}
