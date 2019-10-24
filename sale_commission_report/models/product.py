##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##########################################################################
from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    commission = fields.Float('Commission', default=0.0)
    not_commission = fields.Boolean('No incluir en comisión')
    
    
class ProductProduct(models.Model):
    _inherit = 'product.product'

    commission = fields.Float(
        related='product_tmpl_id.commission')
   
    not_commission = fields.Boolean(
        related='product_tmpl_id.not_commission')


class ProductCategory(models.Model):

    _inherit = 'product.category'

    commission = fields.Float('Commission', default=0.0)
