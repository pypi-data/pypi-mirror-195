![PyPI - Python Version](https://img.shields.io/pypi/pyversions/xoa-utils) [![PyPI](https://img.shields.io/pypi/v/xoa-utils)](https://pypi.python.org/pypi/xoa-utils) ![GitHub](https://img.shields.io/github/license/xenanetworks/open-automation-utilities) [![Documentation Status](https://readthedocs.org/projects/xena-openautomation-utilities/badge/?version=stable)](https://xena-openautomation-utilities.readthedocs.io/en/stable/?badge=stable)

# Xena OpenAutomation Utilities

Xena OpenAutomation Utilities provides a shell-like command-line interface for users to do explorative tests interactively, such as ANLT test.

## Installing XOA Utilities

### Installing From PyPI Using ``pip``

    pip install xoa-utils

### Generate SSH Key

    ssh-keygen -t rsa

> The key pair will be stored in C:\Users\YOU\\.ssh (Windows) or /Users/YOU/.ssh (macOS/Linux)

### Start XOA Utils

After installing the package and ensuring the SSH key in place, you can start XOA Utils simply by typing ``xoa-utils``

    > xoa-utils

    Xena SSH running on 0.0.0.0:22622

> If you want to run xoa-utils SSH service on a different port, do ``xoa-utils 12345``

Then you can SSH to your localhost:

    > ssh yourname@localhost -p 22622

    Welcome to Xena SSH server, yourname!

    xoa_util >

## Step-by-Step Guide

This section provides a step-by-step guide on how to use XOA Utility to do interactive ANLT test.

> ⚡️ You can use **tab key** to auto-complete a command to speed up your input speed.

### Connect

First, you need to connect to your tester using the command ``connect``.

If you don't know which ports you will use at the time of connecting to the port, just leave the option ``--ports`` empty as the example shows below. You can reserve ports later.

    xoa-utils > connect 10.10.10.10 yourname

### Reserve Port

Then, reserve a port on the tester using the command ``port``, as shown in the example below.

> You can only work on one port at a time in one console window. If you want to simultaneously work on multiple ports, you can open multiple console windows.

    xoa-utils[123456] > port 0/0

### Disable Link Recovery

Before doing ANLT testing, remember to disable link recovery on the port using command ``anlt_recovery``.

This is because the port always tries to re-do ANLT command sequence every five seconds if it detects no sync on the port.

This will disturb your manual link training procedure if you don't disable it prior to your interactive test.

    xoa-utils[123456][port0/0] > anlt recovery --off

### Configure AN & LT

After disabling link recovery on the port, you can start configuring AN and LT using ``an_config``, ``lt_config``, and ``lt_im`` as the example shown below.

    xoa-utils[123456][port0/0] > an config --off --no-loopback

    xoa-utils[123456][port0/0] > lt config --on --preset0=standard --mode=interactive

    xoa-utils[123456][port0/0] > lt im 0 nrz

> The initial modulation of each lane on a port is by default PAM2 (NRZ). If you want to change them, you can use ``lt_im``, otherwise do nothing.

> ``an_config``, ``lt_config``, and ``lt_im`` only change the local ANLT configuration state. To execute the configuration, you need to run ``anlt_do``, otherwise your changes will not take effect on the tester.

### Start ANLT

After configuring the ANLT scenario on the port, you should execute ``anlt_do`` to let XOA Utilities application send low-level commands to the tester to start the ANLT procedure, either AN-only, or AN + LT, or LT (auto), or LT (interactive).

    xoa-utils[123456][port0/0] > anlt do

### Control LT Interactive

If you run LT (interactive), you will need to manually control the LT parameters using the LT Control Commands, for example:

    xoa-utils[123456][port0/0] > lt preset 0 2

    xoa-utils[123456][port0/0] > lt inc 0 pre3

    xoa-utils[123456][port0/0] > lt inc 0 main

    xoa-utils[123456][port0/0] > lt dec 0 post

    xoa-utils[123456][port0/0] > lt status 0

    xoa-utils[123456][port0/0] > lt trained 0

    xoa-utils[123456][port0/0] > lt txtagget 0

    xoa-utils[123456][port0/0] > lt txtagset 0 0 0 1 56 0

### Check AN Status

Check AN statistics by ``an_status``.

### Check LT Status

Check LT statistics by ``lt_status``.

### Check ANLT Log

Check ANLT logging by ``anlt_log``.

    xoa-utils[123456][port0/0] > anlt log -f mylog.log

> This commands **continuously displays** the log messages on the screen so you can keep track of your ANLT actions. To **quit** the continuous display mode, press `CTRL-Z`.

### Start Over

If you want to start over on the port, you can reset the port by ``port <PORT> --reset`` as shown below.

This will bring the port back to its default state.

    xoa-utils[123456][port0/0] > port 0/0 --reset
