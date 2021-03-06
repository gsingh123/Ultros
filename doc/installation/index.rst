.. highlight:: bash
   :linenothreshold: 1

.. _installation:

Installation
============

Ultros requires the following for its basic functions:

* Python 2.6 or 2.7 32-bit (NOT 64-bit as some libraries don't support it yet)
    * **NOTE: Do not install Python from the website if you're on a Mac! See the Mac instructions below!**
    * Twisted
    * Zope.Interface
    * Kitchen
    * Yapsy 1.10.2 (Specifically, as they keep changing their API)
    * PyYAML
* Optionally, the following are required for some core features
    * To support SSL in protocols:
        * PyOpenSSL
    * For the Mumble protocol:
        * Google Protobuf
    * For the URLs plugin:
        * BeautifulSoup 4
        * Netaddr
* On linux, you'll need the following
    * libffi
    * libffi-dev
    * build-essential

.. _downloading:

Downloading Ultros
------------------

We highly recommend you use Git to download Ultros, as it allows you to easily keep it up to date,
without worrying about patching or moving files around.

* For Windows, you can install MSysGit here (Allow it to install to System32): https://code.google.com/p/msysgit/downloads/detail?name=Git-1.9.0-preview20140217.exe
    * Where I mention a terminal below, you can use "Git Bash" from your start menu.
* On Linux, install Git from your package manager.

Next, open a terminal and run the following commands::

    cd <path>  # Replace <path> with the directory you want to store Ultros in
    git clone https://github.com/UltrosBot/Ultros.git
    cd Ultros

You will now have a full copy of Ultros, just waiting to be set up!

To update Ultros in future, simply do the following::

    cd <path>/Ultros  # Replace <path> with the directory from above
    git pull

If you're thick-skulled, paranoid about wasting space or just don't like Git, you can download a zipball from the site_, but you will have to keep it up-to-date manually.

Please see below for OS-specific installation instructions. For configuration, please see the :ref:`configuration` page.

.. _installation-all:

Quick-start
-----------

If you're going to use one of the start scripts, you'll need to install both **pip** and **virtualenv**. Install python, and then run the following commands to set both of those up::

    cd <path>/Ultros  # Replace <path> with the directory you stored Ultros in
    python packages.py setup
    pip install virtualenv

On linux, you'll also want to run the following::

    chmod a+x start.sh

To start Ultros, run **start.bat** on Windows, and **start.sh** on everything else. Always use CTRL+C to kill Ultros gracefully.

On linux, you may need to install libffi-dev for the installer to work. On Debian-based systems (such as Ubuntu), you can do something like this::

    apt-get install libffi-dev

.. _install-no-virtualenv:

Without virtualenv
------------------

If you don't want to use a virtualenv (which you really should), you can set up and run Ultros in the following way.

On all systems, you should simply be able to open a terminal, **cd** to your copy of Ultros and run the package manager to install dependencies. ::

    cd <path>/Ultros  # Replace <path> with the directory you stored Ultros in
    python packages.py setup

The packages in this installer only support Python 2.7.

On linux, you may need to install **libffi-dev** for the installer to work. On Debian-based systems (such as Ubuntu), you can do something like this::

    apt-get install libffi-dev

Presuming all is well, the following will start Ultros::

    python run.py

If this doesn't work for you, then you can try the OS-specific methods below.

.. _installation-windows:

Windows
-------

.. highlight:: bat
   :linenothreshold: 1

* Download and install Python 2.7.6: https://www.python.org/ftp/python/2.7.6/python-2.7.6.msi
* Add Python to your PATH: http://www.anthonydebarros.com/2011/10/15/setting-up-python-in-windows-7/
* Install pip by downloading and running this script (Just copy it into a file ending in .py and run it): https://raw.github.com/pypa/pip/master/contrib/get-pip.py
* Download and install Twisted: http://twistedmatrix.com/Releases/Twisted/13.2/Twisted-13.2.0.win32-py2.7.msi
* If you require SSL support:
    * Download and install OpenSSL for Windows: http://slproweb.com/download/Win32OpenSSL-1_0_1g.exe
    * Download and install PyOpenSSL: https://pypi.python.org/packages/2.7/p/pyOpenSSL/pyOpenSSL-0.13.1.win32-py2.7.exe
    * You'll see some errors in the next step if you don't do this, but Ultros should still work just fine for things that don't need SSL.

Now, open a command prompt, and run the following (replacing **<path>** with the *path to wherever you downloaded Ultros*)::

    cd <path>
    pip install -r requirements.txt

Once this is done, you can start Ultros. On Windows, you should never do this by double-clicking run.py, it's always much safer
to run it in a command prompt, so that you'll be able to shut Ultros down properly.

You may create a batch script using either of the below methods for starting Ultros.

To start Ultros normally::

    @ECHO off
    echo Starting Ultros..
    python run.py
    PAUSE

To start Ultros in debug mode::

    @ECHO off
    echo Starting Ultros in debug mode..
    python run.py --debug
    PAUSE

When you want to stop Ultros, instead of closing the window, **click on it and press CTRL+C to stop it gracefully**, and *then* close the window.
Due to some annoying quirks in Windows, if you don't do this, then Ultros may not have time to save all its data. If you do this and lose some
data, then it's not a bug, and we would appreciate if you would use the above method for stopping Ultros, instead of reporting it as one.

.. _installation-linux:

Linux
-----

.. highlight:: bash
   :linenothreshold: 1

As the superior operating system for hosting practically anything, we highly recommend you use Linux to host your bot
if you plan to keep it online for long periods of time. Linux also has a much easier setup, as follows.

* Install Python from your package manager.
    * Most package managers will install the latest version of Python 2, but some versions of Linux will install Python 3.
      Remember to check which version it installs!
* Install libffi and libffi-dev from your package manager.
* If you need SSL, remember to install the standard OpenSSL package from your package manger, as well as a compiler (such as gcc) and the Python development package.
    * You'll see some errors in the next step if you don't do this, but Ultros should still work just fine for things that don't need SSL.
* Use pip to install all of the required modules.
    * On some distros, you may also need to install python-pip

If you're on a recent version of Ubuntu or Debian, you should be able to do all of this in a method similar to the following, replacing <path> with the path
to your copy of Ultros. ::

    sudo apt-get install python python-dev openssl build-essential libffi libffi-dev
    cd <path>
    pip install -r requirements.txt

Naturally, you should replace the call to apt-get above with a call to your distro's package manager if you're not using Ubuntu or Debian.

Once you've done this, you can start Ultros using one of the following methods.

To start Ultros normally::

    cd <path>
    python run.py

To start Ultros in debug mode::

    cd <path>
    python run.py --debug

.. _installation-mac:

Mac OSX
-------

These instructions are for Mavericks (10.9) and may need to be modified accordingly.

* First of all, you should install Homebrew, if you haven't already: http://brew.sh/
* Set up your environment as described here: http://hackercodex.com/guide/mac-osx-mavericks-10.9-configuration/
* Open Terminal.app and run the following::

    brew install python
    cd <path>  # Replace <path> with the directory you downloaded Ultros to
    pip install -r requirements.txt

This could take a little while to complete - The first part may require you to update xcode as well.

To start Ultros normally::

    cd <path>
    python run.py

To start Ultros in debug mode::

    cd <path>
    python run.py --debug

.. Footnote links, etc

.. _site: http://ultros.io
