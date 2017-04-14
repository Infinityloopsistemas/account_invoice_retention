import datetime
from openerp.osv import fields, osv, expression
from openerp import models, fields, api
from openerp import exceptions, tools
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp



class account_invoice_retention(models.Model):
    _name="account.invoice.retention"
    _description = "Retenciones a cuenta por garantia de obra"

    name       = fields.Char(string="Retencion")
    porcentaje = fields.Float(string="Porcentaje Retencion",required=True,digits=dp.get_precision('Account'), help="Introducir en %")
    account_id = fields.Many2one('account.account', string='Account',required=True,help="Cuenta contable de retencion por garantia")
    type       = fields.Selection([('A',"After Tax"),('B',"Before Tax")])
    taxes_id   = fields.Many2one('account.tax', string='Taxes Retention', domain=[('parent_id', '=', False), ('type_tax_use', 'in', ['sale', 'all'])])



class account_invoice(models.Model):
    _inherit = ['account.invoice']

    @api.multi
    def invoice_print(self):
        """ Print the invoice and mark it as sent, so that we can see more
            easily the next step of the workflow
        """
        assert len(self) == 1, 'This option should only be used for a single id at a time.'
        self.sent = True
        return self.env['report'].get_action(self, 'account_invoice_retention.report_invoice_retention')

    @api.one
    @api.depends('invoice_line.price_subtotal', 'tax_line.amount')
    def _compute_amount(self):
        if self.retention_id:
            self.amount_untaxed   = sum(line.price_subtotal for line in self.invoice_line)
            self.amount_retention = -1 * self.amount_untaxed * self.retention_id.porcentaje / 100
            if self.retention_id.type == 'A':
                self.amount_tax             = sum(line.amount for line in self.tax_line)
                self.amount_total_retention = self.amount_untaxed   + self.amount_retention
            if self.retention_id.type =='B' :
                self.amount_tax             = sum(line.amount for line in self.tax_line) + (self.amount_retention*self.retention_id.taxes_id.amount)
                self.amount_total_retention = self.amount_untaxed  + self.amount_retention

            self.amount_total = self.amount_total_retention + self.amount_tax
        else:
            super(account_invoice,self)._compute_amount()

        return True

    move_retention_id      = fields.Many2one('account.move', string='Aistento de Retencion',
                              readonly=True, index=True, ondelete='restrict', copy=False,
                              help="Link to the automatically generated Journal Items.")

    retention_id            = fields.Many2one("account.invoice.retention", string="Retencion")

    amount_total_retention  = fields.Float(string='Total con Retencion', digits=dp.get_precision('Account'),
                                  store=True, readonly=True, compute='_compute_amount', track_visibility='always')
    amount_retention        = fields.Float(string='Retencion', digits=dp.get_precision('Account'),
                              store=True, readonly=True, compute='_compute_amount')



    @api.multi
    def TaxRetention(self,id):
        """Creamos funcion auxiliar para colcular el impuesto de la rentencion, se utliza en el report"""
        invoice = self.env['account.invoice'].browse([id])
        tax=0
        if invoice:
            tax =  invoice.amount_retention*invoice.retention_id.taxes_id.amount
        return tax

    @api.multi
    def action_cancel(self):
        super(account_invoice,self).action_cancel()
        account_move      = self.env['account.move']
        idmove_retention  = self.move_retention_id.id
        if idmove_retention:
            moves             = account_move.browse([idmove_retention])
            for objmove in moves:
                if objmove['state'] != 'draft':
                    raise osv.except_osv(_('User Error!'),
                                         _('You cannot delete a posted journal entry "%s".') % \
                                         objmove['name'])

                for objmoveline in moves.line_id:
                    objmoveline.unlink()
                    #line_ids = map(lambda x: x.id, moves.line_id)
                self.write({'move_retention_id': None})
                objmove.unlink()

    @api.multi
    def action_move_create(self):
        super(account_invoice, self).action_move_create()
        account_move      = self.env['account.move']
        account_move_line = self.env['account.move.line']
        account_partner   = self.partner_id.property_account_receivable
        retention         = self.retention_id.account_id
        for inv in self:
            if inv.retention_id:

                 move_vals = {
                    'ref': inv.move_id.name,
                    'journal_id': inv.journal_id.id,
                    'date': inv.date_invoice,
                    'narration': inv.comment,
                    'company_id': inv.company_id.id,
                    'partner_id': inv.partner_id.id
                }
                 idmove = account_move.create(move_vals)

                 vals_line =[]
                 amount_retention = -1*inv.amount_retention
                 vals_line.append( {
                    'credit': amount_retention,
                    'debit':  0.0,
                    'account_id' : account_partner.id,
                    'partner_id' : inv.partner_id.id,
                    'move_id' : idmove.id,
                     'name' : inv.retention_id.name,
                     'invoice' : inv.id,
                     'ref': inv.move_id.ref
                 })
                 vals_line.append({
                     'credit': 0.0,
                     'debit': amount_retention,
                     'account_id': retention.id,
                     'partner_id': inv.partner_id.id,
                      'move_id'  : idmove.id,
                     'name': inv.retention_id.name,
                     'invoice': inv.id,
                     'ref': inv.move_id.ref
                 })
                 for move_line in vals_line:
                     account_move_line.create(move_line)

                 inv.write({'move_retention_id': idmove.id})
                 idmove.button_validate()


        return True
