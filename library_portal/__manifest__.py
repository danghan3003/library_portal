{
    'name': 'Library Portal',
    'version': '1.0',
    'category': 'Custom',
    'summary': 'Library_Portal',
    'author': 'Dang Han',
    'depends': ['base', 'website'], 
    'data': [
        'security/ir.model.access.csv',
        'views/library_view.xml',
        'views/library_menu.xml',
        'views/library_templates.xml',
    ],
    'installable': True,
    'application': True,
}