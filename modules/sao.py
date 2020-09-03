attributes = {
    ('ROUTINE', 'READ', 'DATA'): {
        'DATA': {
            'type': 'plaintext'
        },
        'READ': {
            'from': {
                'file': {
                    'path': 'current',
                    'filename': 'input',
                    'format': 'plaintext'
                },
                # 'console': {},
                # 'database': {},
                # 'api': {}
            }
        }
    },
    ('ROUTINE', 'PRINT', 'DATA'): {
        'PRINT': {
            'to': {
                'file': {
                    'path': 'current',
                    'filename': 'input',
                    'format': "plaintext",
                },
                'console': {},
                # 'database': {},
                # 'api': {},
            }
        }
    }
}

SAOList = list(attributes.keys())