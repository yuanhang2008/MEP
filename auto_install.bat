python setup.py develop
del /s /q dist\*.*
python setup.py bdist_wheel
pip uninstall MEP -y
python install.py