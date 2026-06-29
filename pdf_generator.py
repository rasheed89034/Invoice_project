import os
from jinja2 import Template
from xhtml2pdf import pisa

def generate_invoice_pdf(invoice_data: dict, output_filename: str = "Solar_Invoice.pdf") -> str:
    try:

        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: Helvetica, Arial, sans-serif; color: #333; }
                .header { text-align: center; padding: 20px; background-color: #2c3e50; color: white; }
                .invoice-details { margin-top: 20px; margin-bottom: 20px; }
                .invoice-details p { margin: 5px 0; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
                th { background-color: #f4f4f4; color: #333; }
                .total-row td { font-weight: bold; background-color: #e8f4f8; }
                .footer { margin-top: 50px; text-align: center; font-size: 12px; color: #777; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>SOLAR SYSTEM INVOICE</h1>
                <p>Powering your future with clean energy</p>
            </div>
            
            <div class="invoice-details">
                <h3>Client Information:</h3>
                <p><strong>Name:</strong> {{ client_name }}</p>
                <p><strong>CNIC:</strong> {{ cnic_number }}</p>
                <p><strong>Address:</strong> {{ address }}</p>
            </div>

            <table>
                <tr>
                    <th>Description</th>
                    <th>Details</th>
                </tr>
                <tr>
                    <td>Total Solar Panels</td>
                    <td>{{ total_panels }} Panels</td>
                </tr>
                <tr>
                    <td>Price Per Panel</td>
                    <td>Rs. {{ per_panel_price }}</td>
                </tr>
                <tr>
                    <td>Gross Amount</td>
                    <td>Rs. {{ total_amount }}</td>
                </tr>
                <tr>
                    <td>Discount Applied</td>
                    <td>Rs. {{ discount }}</td>
                </tr>
                <tr>
                    <td>Payment Received</td>
                    <td>Rs. {{ receive_payment }}</td>
                </tr>
                <tr class="total-row">
                    <td>Remaining Balance</td>
                    <td>Rs. {{ remaining_amount }}</td>
                </tr>
            </table>

            <div class="footer">
                <p>Thank you for choosing our Solar Services!</p>
                <p>This is an AI-generated official invoice.</p>
            </div>
        </body>
        </html>
        """

        template = Template(html_template)
        rendered_html = template.render(**invoice_data)


        with open(output_filename, "w+b") as pdf_file:
            pisa_status = pisa.CreatePDF(rendered_html, dest=pdf_file)

        
        if pisa_status.err:
            return f"Error: PDF doesn't generate ."
        
        return output_filename

    except Exception as e:
        return f"System Error PDF generation: {str(e)}"