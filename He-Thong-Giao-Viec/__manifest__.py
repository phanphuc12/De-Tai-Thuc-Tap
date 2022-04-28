{
    'name': 'Assignment System',
    'version': '1.0',
    'summary': 'Assignment, Task.',
    'sequence': -9,
    'description': """This module made by Phan Bao Phuc.'
               'Contact: baophuc12k@gmail.com""",
    'category': 'Human Resources',
    'license': 'LGPL-3',
    'depends': [
        'hr',
        'mail',
        'base',
        'board',

    ],
    'data': [
        # Security
        'security/security.xml',
        'security/ir.model.access.csv',
        # Data
        'Data/sequence.xml',
        # Wizards
        'Wizards/deny.xml',
        # Views
        'Views/employees.xml',
        'Views/department.xml',
        'Views/assignment.xml',
        'Views/my_assignment.xml',
        'Views/users.xml',
        'Views/projects.xml',
        'Views/topic_categories.xml',
        'Views/templates.xml',
        'Views/assistance.xml',
        'Views/my_task.xml',
        'Views/sprint.xml',
        'Views/employee_rating.xml',
        'Views/dashboard.xml',
        # reports
        'Reports/assignment_report.xml',
        'Reports/report.xml',
        # Menu
        'Menu/Menu.xml'
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
