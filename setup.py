import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()


setuptools.setup(
    name='clover',
    author='Anonymous',
    description='CLOVER: Compositional Loop Invariant Inference for Multiphase Programs via Tree-Structured Neurosymbolic Reasoning',
    keywords='loop-invariant, program-verification, smt, neurosymbolic, llm',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/clover-icse/clover',
    project_urls={
        'Homepage': 'https://github.com/clover-icse/clover',
    },
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    python_requires='>=3.9',
    install_requires=[
        'setuptools',
    ],
    include_package_data=True,
)
