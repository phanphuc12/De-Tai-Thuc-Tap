{
    'name': 'Assignment System',
    'version': '1.0',
    'summary': 'He Thog Giao Viec',
    'sequence': -10,
    'description': """He Thong Giao Viec""",
    'category': 'Human Resources',
    'license': 'LGPL-3',
    'depends': [
        'hr'
    ],
    'data': [
        'Security/ir.model.access.csv',
        'Data/sequence.xml',
        'Views/employees.xml',
        'Views/department.xml',
        'Views/assignment.xml',
        'Menu/Menu.xml'
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}