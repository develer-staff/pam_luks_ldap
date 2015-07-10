# pam_luks_ldap

_PAM module that obtains a LUKS decryption key from LDAP_

[![License](https://img.shields.io/badge/license-GPLv3-blue.svg)](http://choosealicense.com/licenses/gpl-3.0/)
[![PPA](http://img.shields.io/badge/PPA-available-brightgreen.svg)](https://launchpad.net/~lvillani/+archive/ubuntu/pam-luks-ldap)

---

pam_luks_ldap is a PAM module that fetches a LUKS decryption key from an LDAP directory server and
forwards it to *pam_mount(8)*, that will then proceed to mount the user's home directory.

The typical use case is to decouple the LUKS encryption key from the user's password so that their
home directory is still transparently mounted at login time but they are free to change their
password without the need to sync the change with the local LUKS setup.


## Installation

Ubuntu 14.04 users can install the package available from the PPA:

    sudo add-apt-repository ppa:lvillani/pam-luks-ldap
    sudo apt-get update
    sudo apt-get install libpam-luks-ldap

Users building from sources can the following command from the top level directory:

    sudo make install

This module depends on the following libraries being installed:

* [pam_mount](http://pam-mount.sourceforge.net)
* [pam-python](http://pam-python.sourceforge.net)
* [python-ldap](http://www.python-ldap.org)


## Usage

### On Ubuntu, with PPA

Congratulations, you don't have to do anything. We plug into Ubuntu's `pam-auth-update`
infrastructure and the package will usually do the right thing when it's installed or removed.


### Building from sources

On Debian-based system you might have to add this line to `/etc/pam.d/common-auth`, right before
pam_mount's configuration entry:

    auth    optional    pam_python.so   pam_luks_ldap.py

The final part of the file should look like this:

    # and here are more per-package modules (the "Additional" block)
    auth    optional        pam_python.so     pam_luks_ldap.py
    auth    optional        pam_mount.so
    auth    optional        pam_cap.so
    # end of pam-auth-update config

Other distribution might have to be configured in a different way, check their documentation for
more details.


## Caveats

This first release doesn't ship with a configuration file and the defaults will be certainly wrong
for your use case. You'll have to edit the constants at the beginning of the
`/lib/security/pam_luks_ldap.py` file.
