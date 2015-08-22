Invoicing
*********

Django application for invoicing.

Install
=======

Virtual Environment
-------------------

::

  pyvenv-3.4 --without-pip venv-invoice
  source venv-invoice/bin/activate
  wget https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py
  python get-pip.py

  pip install -r requirements/local.txt

Testing
=======

::

  find . -name '*.pyc' -delete
  py.test -x

Usage
=====

::

  ./init_dev.sh

Release
=======

https://pkimber.net/open/
