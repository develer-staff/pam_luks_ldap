# Paths
DESTDIR ?= /
PREFIX  ?= $(DESTDIR)/usr

# Utilities
INSTALL = install
RM = rm


all: pam_luks_ldap.8.gz


install: all
	$(INSTALL) -D -m0644 libpam-luks-ldap $(PREFIX)/share/pam-configs/libpam-luks-ldap
	$(INSTALL) -D -m0644 pam_luks_ldap.8.gz $(PREFIX)/share/man/man8/pam_luks_ldap.8.gz
	$(INSTALL) -D -m0755 pam_luks_ldap.py $(DESTDIR)/lib/security/pam_luks_ldap.py


uninstall:
	$(RM) -f $(PREFIX)/lib/security/pam_luks_ldap.py
	$(RM) -f $(PREFIX)/share/man/man8/pam_luks_ldap.8.gz
	$(RM) -f $(PREFIX)/share/pam-configs/libpam-luks-ldap


pam_luks_ldap.8.gz: pam_luks_ldap.8
	gzip -f -9 $<


pam_luks_ldap.8: pam_luks_ldap.8.md
	pandoc -s -t man $< -o $@


.PHONY: all install uninstall
