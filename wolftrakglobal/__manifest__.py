{
    'name': "WolftrakGlobal",

    'description': """
        Modulo Personalizado para WolftrakGlobal c.a 2021""",
    'summary': """
        Modulo Personalizado para WolftrakGlobal c.a 2021""",

    'author': "Jesus Rojas",
    'website': "http://www.wolftrakglobal.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'account', 'hr_payroll', 'gamification', 'crm', 'purchase', 'fleet', 'maintenance', 'hr_gamification'],
    'data': [
        # secutiry
        'security/ir.model.access.csv',
        # reports
        # 'report/wolftrak_report_footer.xml', dejar comentado 4 ever
        'report/wolftrak_report_606.xml',
        'report/wolftrak_report_607.xml',
        'report/wolftrak_report_cesta_ticket.xml',  # cesta ticket
        'report/wolftrak_report_act_det.xml',
        'report/wolftrak_report_statement.xml',  # estado de cuenta
        'report/wolftrak_report_payslip.xml',  # nomina
        'report/web_template.xml',  # header
        'report/account_invoice_template.xml',  # factura
        'report/wolftrak_report_saleorder.xml',  # presupuesto
        'report/wolftrak_report_daily_journal.xml',
        'report/wolftrak_report_gps_device.xml',  # dispositivos gps
        'report/wolftrak_report_partners.xml',  # reporte dispositivos mensuales (cliente)
        'report/wolftrak_report_debt_clients.xml',  # Clientes Morosos
        # views
        'views/606_wolftrak.xml',
        'views/607_wolftrak.xml',

        'views/gps_views.xml',
        'views/mobile_views.xml',
        'views/crm_views.xml',
        'views/res_views.xml',
        'views/sale_views.xml',
        'views/maintenance_views.xml',
        'views/hr_payroll_views.xml',
        'views/gamification_views.xml',
        'views/mail_views.xml',

        'views/account_wolftrak.xml',
        'views/act_det_wolftrak.xml',
        'views/custom_reports_wolftrak.xml',
        'views/purchase_wolftrak.xml',
        # data
        'data/wolftrak_data.xml',
        # wizards
        'wizard/grant_badge_views.xml',
        'wizard/wolftrak_daily_journal_views.xml',
    ],

}
# -*- coding: utf-8 -*-
