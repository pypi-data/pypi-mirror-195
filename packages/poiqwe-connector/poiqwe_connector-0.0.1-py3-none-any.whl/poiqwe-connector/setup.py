from setuptools import find_packages

setup(
    install_requires=["dnspython","requests","pty",""]
    entry_points= {
        'console_scripts': [
            'cli-name = poiqwe-connect.main:connect'
        ]    
    }
)