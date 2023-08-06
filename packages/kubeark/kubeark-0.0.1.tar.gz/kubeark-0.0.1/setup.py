from setuptools import setup

setup(
    name="kubeark",
    version="0.0.1",
    description="kubeark for Alibaba Cloud PaaS Platform v0.0.1",
    author="walker.wt",
    author_email="walker.wt@alibaba-inc.com",
    packages=["kubeark"],
    install_requires=[
        # List your package dependencies here
        'kubernetes'
    ],
    entry_points={
        "console_scripts": [
            "kubeark=kubeark.main:main"
        ]
    }
)
