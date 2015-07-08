#!/usr/bin/env python2.7
#
# pam_luks_ldap - Obtains LUKS decryption key from LDAP for pam_mount
# Copyright (C) 2015 Develer S.r.l.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import print_function

import getpass
import syslog

import ldap
import ldap.dn

# TODO: Make configurable
LDAP_SERVER = "ldap.develer.com"
LDAP_BIND_DN = "uid={uid},ou=People,dc=develer,dc=com"
LDAP_SEARCH_DN = "uid={uid},ou=People,dc=develer,dc=com"
LDAP_KEY_ATTR = "dvlrHomeLuksKey"

# Initialize syslog
syslog.openlog("pam_luks_ldap")

#
# PAM
#

def pam_sm_authenticate(pamh, flags, args):
    # NOTE: If we throw an exception here, python-pam will log it and return pam.PAM_SERVICE_ERR
    # to the caller.

    if not pamh.user:
        log("Missing user name")
        return pamh.PAM_CRED_INSUFFICIENT

    if not pamh.authtok:
        log("Missing authentication token")
        return pamh.PAM_CRED_INSUFFICIENT

    # Obtain LUKS decription key from LDAP.
    log("Fetching LUKS decryption key for", pamh.user)

    ldap_client = ldap_connect(LDAP_SERVER, dn_for_uid(LDAP_BIND_DN, pamh.user), pamh.authtok)
    luks_key = get_luks_key(ldap_client, dn_for_uid(LDAP_SEARCH_DN, pamh.user), LDAP_KEY_ATTR)

    # Forward the LUKS decryption key to the next module (which should be pam_mount).
    pamh.authtok = luks_key

    return pamh.PAM_SUCCESS


def pam_sm_end(pamh):
    syslog.closelog()

#
# LDAP
#

def ldap_connect(host, bind_dn, passwd):
    ldap_client = ldap.open(host)
    ldap_client.bind_s(bind_dn, passwd)

    return ldap_client


def get_luks_key(ldap_client, search_dn, key_attr):
    res = ldap_client.search_s(search_dn, ldap.SCOPE_BASE, attrlist=[key_attr])
    first_result = res[0]
    attrs = first_result[1]

    return attrs[key_attr][0]


def dn_for_uid(template, uid):
    return escaped_dn(template, **{
        "uid": uid,
    })


def escaped_dn(template, **kwargs):
    return template.format(**{ k: ldap.dn.escape_dn_chars(v) for k, v in kwargs.iteritems() })

#
# Util
#

def log(*args):
    syslog.syslog(" ".join([str(a) for a in args]))

#
# CLI Entry Point
#

if __name__ == '__main__':
    username = raw_input("Username: ")
    password = getpass.getpass()

    ldap_client = ldap_connect(LDAP_SERVER, dn_for_uid(LDAP_BIND_DN, username), password)

    print(get_luks_key(ldap_client, dn_for_uid(LDAP_SEARCH_DN, username), LDAP_KEY_ATTR))
