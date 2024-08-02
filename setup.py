from setuptools import setup, find_packages

setup(
    name='corsair-rgb-screen-mirror',
    version='1.0.0',
    description='Mirror your screen on your Corsair RGB keyboard.',
    author='Henry Sands-Grant',
    author_email='henrysandsgrant@gmail.com',
    packages=find_packages(),
    install_requires=[
        'cuesdk',
        'pyautogui',
    ],
    entry_points={
        'console_scripts': [
            'corsair-rgb=corsair_rgb.main:main',
        ],
    },
)
