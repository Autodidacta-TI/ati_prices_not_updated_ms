# -*- coding: utf-8 -*-
import logging 
from datetime import timedelta
from datetime import datetime
from odoo import models, fields, api, exceptions, _
 
_logger = logging.getLogger(__name__)

class POReportPricesWizard(models.TransientModel):
    _name = 'report.prices.not.updated.wizard'  
    
    from_date = fields.Date(string="Fecha ")
    
    def print_report_prices_not_updated_excel(self):        
        return {
            'type': 'ir.actions.act_url',
            'url': '/purchase/report_prices_not_updated/%s' % (self.id),
            'target': 'new',
        }