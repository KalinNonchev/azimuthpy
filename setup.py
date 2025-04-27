from setuptools import setup, find_packages

setup(
    name='azimuthpy',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='Python wrapper for Azimuth (Seurat-based single-cell mapping) using rpy2',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/KalinNonchev/azimuthpy',  # your repo if you have one
    packages=find_packages(),
    install_requires=[
        'anndata',
        'numpy',
        'pandas',
        'rpy2',
    ],
    python_requires='>=3.8',
)