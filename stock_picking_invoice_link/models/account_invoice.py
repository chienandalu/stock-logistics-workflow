# Copyright 2013-15 Agile Business Group sagl (<http://www.agilebg.com>)
# Copyright 2015-2016 AvanzOSC
# Copyright 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# Copyright 2017 Jacques-Etienne Baudoux <je@bcim.be>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.depends('invoice_line_ids.move_line_ids')
    def _compute_picking_ids(self):
        for inv in self:
            inv.picking_ids = inv.invoice_line_ids.mapped(
                'move_line_ids.picking_id')

    picking_ids = fields.Many2many(
        comodel_name='stock.picking',
        compute='_compute_picking_ids',
        string='Related Pickings',
        readonly=True,
        help="Related pickings (only when the invoice has been generated "
             "from a sale order).",
    )

    @api.multi
    def action_view_picking(self):
        action = self.env.ref('stock.action_picking_tree_all').read()[0]
        if len(self.picking_ids) > 1:
            action['domain'] = [('id', 'in', self.picking_ids.ids)]
        elif self.picking_ids:
            action['views'] = [
                (self.env.ref('stock.view_picking_form').id, 'form')]
            action['res_id'] = self.picking_ids.id
        return action


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    move_line_ids = fields.One2many(
        comodel_name='stock.move',
        inverse_name='invoice_line_id',
        string='Related Stock Moves',
        readonly=True,
        copy=False,
        help="Related stock moves "
             "(only when the invoice has been generated from a sale order).",
    )
