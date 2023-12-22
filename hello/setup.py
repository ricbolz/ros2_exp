from setuptools import find_packages, setup
import os
from glob import glob 

package_name = 'hello'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*_launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ubuntu',
    maintainer_email='ubuntu@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'hello_node = hello.hello_node:main',
            'hello_publisher = hello.hello_publisher:main',
            'hello_subscriber = hello.hello_subscriber:main',
            'joypad_mouse_controller = hello.JoypadMouseController:main',
            'lightsensor_monitor = hello.lightsensor_monitor:main',
        ],
    },
)
