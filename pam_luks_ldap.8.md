% pam_luks_ldap(8)
% Lorenzo Villani
% June 8, 2015

# NAME

pam_luks_ldap - A PAM module that obtains a LUKS decryption key from LDAP

# SYNOPSIS

auth    required    pam_python.so    pam_luks_ldap.py
auth    optional    pam_mount.so

# DESCRIPTION

pam_luks_ldap is a PAM module that fetches a LUKS decryption key from an LDAP directory server and
forwards it to *pam_mount(8)*, that will then proceed to mount the user's home directory.

The typical use case is to decouple the LUKS encryption key from the user's password so that their
home directory is still transparently mounted at login time but they are free to change their
password without the need to sync the change with the local LUKS setup.


# DIAGNOSTICS

The module logs failures over *syslog(1)*.
