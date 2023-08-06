import setuptools
from setuptools import find_packages
setuptools.setup(
    name="joonmyung",
    version="1.3.5",
    author="JoonMyung Choi",
    author_email="pizard@korea.ac.kr",
    description="JoonMyung's Library",
    url="https://github.com/pizard/JoonMyung.git",
    license="MIT",
    packages=find_packages(exclude=["playground.*",
                                    "99_backup.*"]),
    zip_safe=False,
    install_requires=[
    ]
)

# git add .
# git commit
# git push
#
# python setup.py sdist
# python -m twine upload dist/*     # Remove All File
# ID:JoonmyungChoi
