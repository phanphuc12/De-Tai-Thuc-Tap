{
    'name': 'Assignment System',
    'version': '1.0',
    'summary': 'He Thong Giao Viec',
    'sequence': -10,
    'description': """He Thong Giao Viec""",
    'category': 'Human Resources',
    'license': 'LGPL-3',
    'depends': [
        'hr',
        'mail',
        'base',

    ],
    'data': [
        # Security
        'security/security.xml',
        'security/ir.model.access.csv',
        # Data
        'Data/sequence.xml',
        # # Wizards
        # 'Wizards/send_assignment.xml',
        # Views
        'Views/employees.xml',
        'Views/department.xml',
        'Views/assignment.xml',
        'Views/my_assignment.xml',
        'Views/users.xml',
        'Views/projects.xml',
        'Views/topic_categories.xml',
        'Views/templates.xml',
        # Menu
        'Menu/Menu.xml'
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
