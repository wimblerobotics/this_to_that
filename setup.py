from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'this_to_that'

setup(
    name=package_name,
    version='0.0.1', # Adjust version as needed
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Include launch files if any
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
        # Include config files if any
        # (os.path.join('share', package_name, 'config'), glob(os.path.join('config', '*.yaml'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name', # Add your name
    maintainer_email='your.email@example.com', # Add your email
    description='Package to subscribe to a topic field.', # Add description
    license='Apache License 2.0', # Or your chosen license
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'this_to_that_node.py = this_to_that.this_to_that_node:main',
        ],
    },
)
