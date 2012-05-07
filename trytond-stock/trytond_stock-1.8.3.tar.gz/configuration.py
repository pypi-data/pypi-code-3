#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, ModelSingleton, fields
from trytond.pyson import Eval


class Configuration(ModelSingleton, ModelSQL, ModelView):
    'Stock Configuration'
    _name = 'stock.configuration'
    _description = __doc__

    shipment_in_sequence = fields.Property(fields.Many2One('ir.sequence',
        'Supplier Shipment Sequence', domain=[
            ('company', 'in', [Eval('company'), False]),
            ('code', '=', 'stock.shipment.in'),
        ], required=True))
    shipment_in_return_sequence = fields.Property(fields.Many2One(
        'ir.sequence', 'Supplier Return Shipment Sequence', domain=[
            ('company', 'in', [Eval('company'), False]),
            ('code', '=', 'stock.shipment.in.return'),
        ], required=True))
    shipment_out_sequence = fields.Property(fields.Many2One( 'ir.sequence',
        'Customer Shipment Sequence', domain=[
            ('company', 'in', [Eval('company'), False]),
            ('code', '=', 'stock.shipment.out'),
        ], required=True))
    shipment_out_return_sequence = fields.Property(fields.Many2One(
        'ir.sequence', 'Customer Return Shipment Sequence', domain=[
            ('company', 'in', [Eval('company'), False]),
            ('code', '=', 'stock.shipment.out.return'),
        ], required=True))
    shipment_internal_sequence = fields.Property(fields.Many2One(
        'ir.sequence', 'Internal Shipment Sequence', domain=[
            ('company', 'in', [Eval('company'), False]),
            ('code', '=', 'stock.shipment.internal'),
        ], required=True))

Configuration()
