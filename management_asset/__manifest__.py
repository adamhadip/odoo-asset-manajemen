{
    'name' : 'Asset Management PT PAL',
    'author' : 'Adam Hadi Pratama',
    'summary':'Asset Management for PT PAL',
    'category': 'Productivity',
    'depends': ['mail'],
    'data' : [
        'security/ir.model.access.csv',
        'views/asset_form.xml',
        'views/asset_status.xml',
        'views/asset_perbaikan.xml',
        'views/dashboard.xml',
        'views/template.xml',
        'reports/asset_loan_report.xml',
        'reports/asset_status_report.xml',
        'reports/report.xml'
    ],
    'qweb': [
        'static/xml/*.xml',
    ]
}