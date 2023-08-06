from setuptools import setup
from pathlib import Path


kwargs = {
    'name': 'manuscriptify',
    'version': '1.1.1',
    'description': 'Compile google docs into a manuscript',
    'long_description': Path('README.md').read_text(),
    'long_description_content_type': 'text/markdown',
    'author': 'Jonas McCallum',
    'author_email': 'jonasmccallum@gmail.com',
    'url': 'https://manuscriptify.com',
    'packages': [
        'manuscriptify',
        'manuscriptify.google_api',
    ],
    'package_data': {
          '': ['launch_button/*']
    },
    'license_files': ('LICENSE.txt'),
    'install_requires': [
        'google-api-python-client',
        'google_auth_oauthlib',
        'pyyaml',
    ],
    'extras_require': {'testing': ['pytest']},
    'entry_points': {
        'console_scripts': [
            'manuscriptify = manuscriptify.bin:manuscriptify',
            'mify = manuscriptify.bin:manuscriptify',
            'msfy = manuscriptify.bin:manuscriptify'
        ]
    },
    'project_urls': {
        'Source': 'https://bitbucket.org/msfy/manuscriptify',
        'Tracker': 'https://bitbucket.org/msfy/manuscriptify/issues'
    },
    'zip_safe': False
}

setup(**kwargs)
