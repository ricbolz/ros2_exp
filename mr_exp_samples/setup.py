from setuptools import find_packages, setup

package_name = 'mr_exp_samples'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
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
            'joy_teleop = mr_exp_samples.joy_teleop:main',
            'hello_sub_and_pub = mr_exp_samples.hello_sub_and_pub:main',
            'watermark_node = mr_exp_samples.watermark_node:main',
        ],
    },
)
