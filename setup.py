from setuptools import setup, find_packages

setup(
    name='ArtificialVision',
    version='0.0.1',
    description='Artificial Vision Library',
    long_description=open('README.md').read(),
    license='MIT',
    author='hwk06023',
    author_email='hwk06023gmail.com',
    url='https://github.com/hwk06023/ArtificialVision',
    install_requires=['pytorch', 'opencv-python', 'scikit-learn',],
    packages=find_packages(exclude=[]),
    keywords=['hwk060023', 'Vision', 'AI', 'ML', 'DL', 'CV', 'ArtificialVision', 'ArtificialIntelligence', 'MachineLearning', 'DeepLearning', 'ComputerVision', 'Python', 'PyPI', 'Package', 'Tutorial', 'hwk06023'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)