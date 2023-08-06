# # To publish into PyPi
# # On a virtual environment:
# # pip install -U wheel setuptools
# # python -m setup sdist bdist_wheel
# # check-manifest -c
# # twine upload dist/*
# #   username: __token__
# #   password: <your_token_here>

# from setuptools import setup

# python3 -m build
# python3 -m twine upload --repository testpypi dist/*