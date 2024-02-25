from setuptools import setup, find_packages

setup(
    name='ArtificialVision',
    version='0.1.0',
    description='Artificial Vision Library',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    license='MIT',
    author='hwk06023',
    author_email='hwk06023@gmail.com',
    url='https://github.com/hwk06023/ArtificialVision',
    install_requires=['torch', 'torchvision', 'tensorflow', 'opencv-python', 'scikit-learn', 'numpy', 'scipy', 'matplotlib', 'tqdm', 'pillow'],
    packages=find_packages(exclude=[]),
    keywords=['hwk060023', 'Vision', 'AI', 'ML', 'DL', 'CV', 'ArtificialVision', 'ArtificialIntelligence', 'MachineLearning', 'DeepLearning', 'ComputerVision', 'Python', 'PyPI', 'Package', 'Tutorial'],
    python_requires='>=3.9',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)