# -*- coding: utf-8 -*-
import logging
from odoo import http, _
from odoo.http import content_disposition, request
from datetime import datetime, timedelta
import io
import xlsxwriter
import xlsxwriter.utility as xl_utility


_logger = logging.getLogger(__name__)
class POPricesController(http.Controller):
    @http.route([                                                   
        '/purchase/po_report_prices_not_updated/<model("po.report.prices.not.updated.wizard"):wizard>',
    ], type='http', auth="user", csrf=False)
    def get_purchase_order_prices_excel_report(self,wizard=None,**args):
        from_date_datetime = datetime.strptime(wizard.from_date, "%Y-%m-%d")
        response = request.make_response(
            None,
            headers=[
                ('Content-Type', 'application/vnd.ms-excel'),
                ('Content-Disposition', content_disposition('Reporte de Precios no actualizados al ' + from_date_datetime.strftime("%d-%m-%Y") + '.xlsx')) #.strftime("%d-%m-%Y")
            ]
        )

        # Crea workbook
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})

        title_style = workbook.add_format({'font_name': 'Calibri',
                                            'font_size': 16, 
                                            'bold': True, 
                                            'align': 'center',  
                                            'left': 0, 
                                            'bottom':0, 
                                            'right':0, 
                                            'top':0
                                            })

        # Buscar todos los productos que cumplen con el criterio de referencia y código de barras distintos de "Falso"
        products = request.env['product.product'].search([
            ('default_code', '!=', 'False'),
            ('barcode', '!=', 'False')
        ])

        _logger.warning('***products: {0}'.format(products))
        _logger.warning('***products: {0}'.format(len(products)))

        fecha = datetime.strptime(wizard.from_date, "%Y-%m-%d")
        nueva_fecha = fecha 
        nueva_fecha_string = nueva_fecha.strftime("%Y-%m-%d %H:%M:%S")

        result_list = []
      
        for product in products:
            # Buscar las líneas de órdenes de compra para el producto y ordenarlas por fecha de creación (ascendente)
            purchase_order_lines = request.env['purchase.order.line'].search([
                ('product_id', '=', product.id),
                ('date_planned', '<=', nueva_fecha_string)
            ], order='create_date')

            _logger.warning('***purchase_order_lines: {0}'.format(purchase_order_lines))

            if purchase_order_lines:
                # Tomar la primera línea de compra (la más antigua) last
                last_purchase_order_line = purchase_order_lines[-1]

                # Compara el precio de costo del producto con el precio de la purchase.order.line
                if product.standard_price == last_purchase_order_line.price_unit:
                    result_list.append({'product': product, 'price_unit': last_purchase_order_line.price_unit})
                    

        #_logger.warning('***result_list: {0}'.format(result_list))

        header_style = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': '#D7E4BC'
        })

        worksheet = workbook.add_worksheet("Reporte")
        worksheet.merge_range('A1:D1', 'Reporte Precios sin Actualizar al ' + from_date_datetime.strftime("%d-%m-%Y"), title_style) 
        
        # Escribir encabezados y aplicar el estilo
        headers = ['Código Producto', 'Nombre del Producto', 'Precio de Costo','Precio de Ultima Compra' ] 
       
        for col, header in enumerate(headers):
            worksheet.write(1, col, header, header_style)
            
        # Crear un formato para los números en formato de moneda (dólares)
        currency_format = workbook.add_format({'num_format': '"$"#,##0.00'})

        # Establecer el ancho de las columnas
        worksheet.set_column('A:A', 20)  # Ancho de la columna para el código del producto
        worksheet.set_column('B:B', 50)  # Ancho de la columna para el nombre del producto
        worksheet.set_column('C:C', 15)  # Ancho de la columna para el precio estándar
        worksheet.set_column('D:D', 25)  # Ancho de la columna para la fecha de compra
        
        # Escribir datos de result_list en el archivo Excel
        row = 2
        for item in result_list:
            product = item['product']
            price_unit = item['price_unit']
            worksheet.write(row, 0, product.default_code)
            worksheet.write(row, 1, product.name)
            worksheet.write_number(row, 2, product.standard_price, currency_format)
            worksheet.write_number(row, 3, price_unit, currency_format)
            row += 1
        ## Cierre del excel
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

        return response
