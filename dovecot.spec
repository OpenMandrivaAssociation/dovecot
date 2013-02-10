%define build_gssapi 1
%define build_ldap 1
%define build_lucene 1
%define build_mysql 0
%define build_pgsql 0
%define build_sqlite 0
%define build_sieve 1

%{?_with_gssapi: %{expand: %%global build_gssapi 1}}
%{?_without_gssapi: %{expand: %%global build_gssapi 0}}
%{?_with_ldap: %{expand: %%global build_ldap 1}}
%{?_without_ldap: %{expand: %%global build_ldap 0}}
%{?_with_lucene: %{expand: %%global build_lucene 1}}
%{?_without_lucene: %{expand: %%global build_lucene 0}}
%{?_with_mysql: %{expand: %%global build_mysql 1}}
%{?_without_mysql: %{expand: %%global build_mysql 0}}
%{?_with_pgsql: %{expand: %%global build_pgsql 1}}
%{?_without_pgsql: %{expand: %%global build_pgsql 0}}
%{?_with_sqlite: %{expand: %%global build_sqlite 1}}
%{?_without_sqlite: %{expand: %%global build_sqlite 0}}
%{?_with_sieve: %{expand: %%global build_sieve 1}}
%{?_without_sieve: %{expand: %%global build_sieve 0}}

# The Sieve plugin needs to reference internal symbols
%define _disable_ld_no_undefined 1

%define sieve_version 0.3.3

Summary:	Secure IMAP and POP3 server
Name: 		dovecot
Version:	2.1.15
Release:	1
License:	MIT and LGPLv2 and BSD-like and Public Domain
Group:		System/Servers
URL:		http://dovecot.org
Source0:	http://syksy.dovecot.org/releases/2.1/%{name}-%{version}.tar.gz
Source1:	http://syksy.dovecot.org/releases/2.1/%{name}-%{version}.tar.gz.sig
Source2:	%{name}-pamd
Source3:	%{name}-init
Source4:	http://dovecot.org/tools/migration_wuimp_to_dovecot.pl
Source5:	http://dovecot.org/tools/mboxcrypt.pl
Source6:	http://www.rename-it.nl/dovecot/2.1/dovecot-2.1-pigeonhole-%{sieve_version}.tar.gz
Source7:	http://www.earth.ox.ac.uk/~steve/sieve/procmail2sieve.pl
Patch0:		dovecot-conf-ssl.patch
Patch1:		dovecot.pkglib.patch
Provides:	imap-server pop3-server
Provides:	imaps-server pop3s-server
Requires(pre):	rpm-helper >= 0.21
Requires(post):	rpm-helper >= 0.21
Requires(preun): rpm-helper >= 0.21
Requires(postun): rpm-helper >= 0.21
Requires:	%name-config >= 2.1
BuildRequires:	pam-devel
BuildRequires:	openssl-devel
BuildRequires:	libsasl-devel
BuildRequires:	libcap-devel
BuildRequires:	gettext-devel
%if %{build_ldap}
BuildRequires:	openldap-devel
%endif
%if %{build_lucene}
BuildRequires:	clucene-devel
%endif
%if %{build_mysql}
BuildRequires:	mysql-devel
%endif
%if %{build_pgsql}
BuildRequires:	postgresql-devel
%endif
%if %{build_gssapi}
BuildRequires:	gssglue-devel
BuildRequires:	krb5-devel
%endif
%if %{build_sqlite}
BuildRequires: sqlite3-devel
%endif
BuildRequires:	rpm-helper >= 0.21
BuildRequires:	bzip2-devel

%description
Dovecot is an IMAP and POP3 server for Linux/UNIX-like systems, written with
security primarily in mind. Although it's written with C, it uses several
coding techniques to avoid most of the common pitfalls.

Dovecot can work with standard mbox and maildir formats and it's fully
compatible with UW-IMAP and Courier IMAP servers as well as mail clients
accessing the mailboxes directly.

You can build %{name} with some conditional build swithes;

(ie. use with rpm --rebuild):

    --with[out] gssapi		GSSAPI support (enabled)
    --with[out] ldap		LDAP support (enabled)
    --with[out] lucene		Lucene support (enabled)
    --with[out] mysql		MySQL support (enabled)
    --with[out] pgsql		PostgreSQL support (enabled)
    --with[out] sqlite		SQLite support (enabled)
    --with[out] sieve		CMU Sieve support (enabled)

%if %{build_sieve}
%package	plugins-sieve
Summary:	CMU Sieve plugin for dovecot LDA
Group:		System/Servers
Requires:	%{name} >= %{version}

%description	plugins-sieve
This package provides the CMU Sieve plugin version %{sieve_version} for dovecot LDA.
%endif

%if %{build_pgsql}
%package	plugins-pgsql
Summary:	Postgres SQL backend for dovecot
Group:		System/Servers
Requires:	%{name} >= %{version}

%description	plugins-pgsql
This package provides the Postgres SQL backend for dovecot-auth etc.
%endif

%if %{build_mysql}
%package	plugins-mysql
Summary:	MySQL backend for dovecot
Group:		System/Servers
Requires:	%{name} >= %{version}

%description	plugins-mysql
This package provides the MySQL backend for dovecot-auth etc.
%endif

%if %{build_ldap}
%package	plugins-ldap
Summary:	LDAP support for dovecot
Group:		System/Servers
Requires:	%{name} >= %{version}

%description	plugins-ldap
This package provides LDAP capabilities to dovecot in a modular form.
%endif

%if %{build_gssapi}
%package	plugins-gssapi
Summary:	GSSAPI support for dovecot
Group:		System/Servers
Requires:	%{name} >= %{version}

%description	plugins-gssapi
This package provides GSSAPI capabilities to dovecot in a modular form.
%endif

%if %{build_sqlite}
%package	plugins-sqlite
Summary:	SQLite backend for dovecot
Group:		System/Servers
Requires:	%{name} >= %{version}

%description	plugins-sqlite
This package provides the SQLite backend for dovecot-auth etc.
%endif

%package	devel
Summary:	Devel files for Dovecot IMAP and POP3 server
Group:		Development/C
Requires:	%{name} >= %{version}

%description	devel
Dovecot is an IMAP and POP3 server for Linux/UNIX-like systems, written with
security primarily in mind. Although it's written with C, it uses several
coding techniques to avoid most of the common pitfalls.

Dovecot can work with standard mbox and maildir formats and it's fully
compatible with UW-IMAP and Courier IMAP servers as well as mail clients
accessing the mailboxes directly.

This package contains development files for dovecot.

%package	config-standalone
Summary:	Config files for running dovecot standalone
Group:		System/Servers
Provides:	%name-config = %version-%release

%description	config-standalone
Config files for running the Dovecot IMAP and POP3 server by itself.

This is the basic configuration for running a Dovecot server - you may
want to install the postfix-dovecot-config package instead if you wish
to run a combination of the Postfix SMTP server and the Dovecot IMAP/POP3
server.

%prep

%setup -q
# Bug #27491
%patch0 -p1 -b .sslfix

%if %{build_sieve}
%setup -q -D -T -a 6
%endif

%build
%serverbuild

%configure2_5x \
    --enable-header-install \
    --disable-static \
    --with-sql=plugin \
    --with-sql-drivers \
    --with-ssl=openssl \
    --with-ssldir=%{_sysconfdir}/ssl/%{name} \
    --with-moduledir=%{_libdir}/%{name}/modules \
    --with-nss \
%if %{build_ldap}
    --with-ldap=plugin \
%endif
%if %{build_pgsql}
    --with-pgsql \
%endif
%if %{build_mysql}
    --with-mysql \
%endif
%if %{build_sqlite}
    --with-sqlite \
%endif
%if %{build_gssapi}
    --with-gssapi=plugin \
%endif
%if %{build_lucene}
    --with-lucene \
%endif
    --with-libcap

%make

%if %{build_sieve}
pushd dovecot-*-pigeonhole-%{sieve_version}
rm -f configure
autoreconf -fi
touch doc/man/sieve-filter.1
%configure2_5x \
    --disable-static \
    --with-dovecot=../ \
    --with-unfinished-features
%make
popd
%endif

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/pam.d
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_libdir}/%{name}/modules
install -d %{buildroot}/var/lib/%{name}

%makeinstall_std

%if %{build_sieve}
pushd dovecot-*-pigeonhole-%{sieve_version}
%makeinstall_std
# temporary borkiness i guess...
f=%{buildroot}%{_mandir}/man1/sieve-filter.1
if ! [ -s $f ]; then rm -f $f; fi
popd
%endif

cat %{SOURCE2} > %{buildroot}%{_sysconfdir}/pam.d/%{name}
cat %{SOURCE3} > %{buildroot}%_initrddir/%{name}
chmod 0755 %{buildroot}%_initrddir/%{name}
pwd
cp doc/example-config/dovecot.conf %{buildroot}%{_sysconfdir}/%name/dovecot.conf
cp -a doc/example-config/conf.d %buildroot%_sysconfdir/%name/
cp %{SOURCE4} .
cp %{SOURCE5} .
# procmail2sieve converter
install -d -m 755 %{buildroot}%{_bindir}
install %{SOURCE7} -m 755 %{buildroot}%{_bindir}
perl -pi -e 's|#!/usr/local/bin/perl|#!%{_bindir}/perl|' \
    %{buildroot}%{_bindir}/procmail2sieve.pl

# placed in doc
rm -f %{buildroot}%{_sysconfdir}/dovecot*-example.conf

# Clean up buildroot
rm -rf %{buildroot}%{_datadir}/doc/dovecot*

%pre
%_pre_useradd dovecot /var/lib/%{name} /bin/false
%_pre_groupadd dovecot dovecot
%_pre_useradd dovenull /var/lib/%{name} /bin/false
%_pre_groupadd dovenull dovenull

%post
%_post_service dovecot
%_create_ssl_certificate dovecot

%preun
%_preun_service dovecot

%postun
%_postun_userdel dovecot
%_postun_groupdel dovecot
%_postun_userdel dovenull
%_postun_groupdel dovenull

%if %{build_sieve}
%post plugins-sieve
/sbin/service %{name} condrestart > /dev/null 2>&1 || :

%postun plugins-sieve
if [ "$1" = "0" ]; then
    /sbin/service %{name} condrestart > /dev/null 2>&1 || :
fi
%endif

%if %{build_mysql}
%post plugins-mysql
/sbin/service %{name} condrestart > /dev/null 2>&1 || :

%postun plugins-mysql
if [ "$1" = "0" ]; then
    /sbin/service %{name} condrestart > /dev/null 2>&1 || :
fi
%endif

%if %{build_pgsql}
%post plugins-pgsql
/sbin/service %{name} condrestart > /dev/null 2>&1 || :

%postun plugins-pgsql
if [ "$1" = "0" ]; then
    /sbin/service %{name} condrestart > /dev/null 2>&1 || :
fi
%endif

%if %{build_sqlite}
%post plugins-sqlite
/sbin/service %{name} condrestart > /dev/null 2>&1 || :

%postun plugins-sqlite
if [ "$1" = "0" ]; then
    /sbin/service %{name} condrestart > /dev/null 2>&1 || :
fi
%endif

%if %{build_ldap}
%post plugins-ldap
/sbin/service %{name} condrestart > /dev/null 2>&1 || :

%postun plugins-ldap
if [ "$1" = "0" ]; then
    /sbin/service %{name} condrestart > /dev/null 2>&1 || :
fi
%endif

%if %{build_gssapi}
%post plugins-gssapi
/sbin/service %{name} condrestart > /dev/null 2>&1 || :

%postun plugins-gssapi
if [ "$1" = "0" ]; then
    /sbin/service %{name} condrestart > /dev/null 2>&1 || :
fi
%endif

%clean
rm -rf %{buildroot}

%files
# to preserve security of the ssl password which may be in the config
# file but also allow the use of the 'deliver' command as any user,
# we set the 'deliver' command sgid mail and have the config file owned
# by root.mail. See bug #44926. idea from Josh Bressers at Red Hat.
# - AdamW 2008/10
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING* NEWS README TODO
%doc doc/*.sh doc/*.txt doc/*.cnf
%attr(0750,root,mail) %dir %_sysconfdir/%name
%attr(0750,root,mail) %dir %_sysconfdir/%name/conf.d
%doc %_sysconfdir/dovecot/README
%attr(0755,root,root) %_initrddir/%{name}
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%{_sbindir}/*
%_bindir/doveadm
%_bindir/doveconf
%_bindir/dsync
%{_bindir}/procmail2sieve.pl
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/checkpassword-reply
%attr(2755,root,mail) %{_libdir}/%{name}/deliver
%_libdir/%name/aggregator
%_libdir/%name/anvil
%_libdir/%name/auth
%_libdir/%name/config
%_libdir/%name/decode2text.sh
%{_libdir}/%{name}/dict
%_libdir/%name/director
%_libdir/%name/dns-client
%_libdir/%name/doveadm-server
%_libdir/%name/dovecot-lda
%_libdir/%name/indexer
%_libdir/%name/indexer-worker
%_libdir/%name/ipc
%{_libdir}/%{name}/gdbhelper
%{_libdir}/%{name}/imap
%{_libdir}/%{name}/imap-login
%{_libdir}/%{name}/maildirlock
%{_libdir}/%{name}/pop3
%{_libdir}/%{name}/pop3-login
%{_libdir}/%{name}/rawlog
%_libdir/%name/replicator
%_libdir/%name/script
%_libdir/%name/script-login
%_libdir/%name/ssl-params
%_libdir/%name/stats
%_libdir/%name/xml2text
%_libdir/%name/libdovecot-lda.so*
%_libdir/%name/libdovecot-login.so*
%_libdir/%name/libdovecot-sql.so*
%_libdir/%name/libdovecot-ssl.so*
%_libdir/%name/libdovecot-storage.so*
%_libdir/%name/libdovecot.so*
%_libdir/dovecot/lmtp
%_libdir/dovecot/log
%dir %{_libdir}/%{name}/modules
%{_libdir}/%{name}/modules/*.so
%dir %_libdir/%name/modules/auth
%{_libdir}/%{name}/modules/auth/*.so
%exclude %_libdir/%name/modules/auth/libauthdb_ldap.so
%exclude %_libdir/%name/modules/auth/libmech_gssapi.so
%dir %_libdir/%name/modules/doveadm
%{_libdir}/%{name}/modules/doveadm/*.so
%dir %_libdir/%name/modules/settings
%{_libdir}/%{name}/modules/settings/*.so
%attr(0700,root,root) %dir /var/lib/%{name}
%_mandir/man1/deliver.1*
%_mandir/man1/doveadm*.1*
%_mandir/man1/doveconf.1*
%_mandir/man1/dovecot-lda.1*
%_mandir/man1/dovecot.1*
%_mandir/man1/dsync.1*
%_mandir/man1/sieve-dump.1*
%_mandir/man1/sieved.1*
%_mandir/man7/doveadm-search-query.7*
%_mandir/man7/pigeonhole.7*

%files config-standalone
%defattr(-,root,root,-)
%attr(0640,root,mail) %config(noreplace) %{_sysconfdir}/%name/dovecot.conf
%attr(0640,root,mail) %_sysconfdir/%name/conf.d/*

%if %{build_sieve}
%files plugins-sieve
%defattr(-,root,root,-)
%{_bindir}/sieve-filter
%{_bindir}/sieve-test
%{_bindir}/sievec
%_bindir/sieve-dump
%_libdir/%name/libdovecot-sieve.so*
%_libdir/%name/managesieve
%_libdir/%name/managesieve-login
%{_mandir}/man1/sievec.1*
%{_mandir}/man1/sieve-filter.1*
%{_mandir}/man1/sieve-test.1*
%endif

%if %{build_ldap}
%files plugins-ldap
%defattr(-,root,root)
%{_libdir}/%{name}/modules/auth/libauthdb_ldap.so
%endif

%if %{build_gssapi}
%files plugins-gssapi
%defattr(-,root,root)
%{_libdir}/%{name}/modules/auth/libmech_gssapi.so
%endif

%if %{build_sqlite}
%files plugins-sqlite
%defattr(-,root,root,-)
%{_libdir}/%{name}/modules/auth/libdriver_sqlite.so
%{_libdir}/%{name}/modules/dict/libdriver_sqlite.so
%{_libdir}/%{name}/modules/sql/libdriver_sqlite.so
%endif

%if %{build_mysql}
%files plugins-mysql
%defattr(-,root,root,-)
%{_libdir}/%{name}/modules/auth/libdriver_mysql.so
%{_libdir}/%{name}/modules/dict/libdriver_mysql.so
%{_libdir}/%{name}/modules/sql/libdriver_mysql.so
%endif

%if %{build_pgsql}
%files plugins-pgsql
%defattr(-,root,root,-)
%{_libdir}/%{name}/modules/auth/libdriver_pgsql.so
%{_libdir}/%{name}/modules/dict/libdriver_pgsql.so
%{_libdir}/%{name}/modules/sql/libdriver_pgsql.so
%endif

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/%{name}/dovecot-config
#{_libdir}/%{name}/modules/*.*a
#{_libdir}/%{name}/modules/auth/*.*a
%_datadir/aclocal/*.m4


%changelog
* Sat Aug 18 2012 Bernhard Rosenkraenzer <bero@bero.eu> 2.1.9-2mdv2012.0
+ Revision: 815335
- Split config files into a separate package to make room for postfix-dovecot-config
- Update to 2.1.9

* Tue Jul 03 2012 Bernhard Rosenkraenzer <bero@bero.eu> 2.1.8-1
+ Revision: 807945
- Update to 2.1.8

* Fri Jun 01 2012 Bernhard Rosenkraenzer <bero@bero.eu> 2.1.7-1
+ Revision: 801701
- Update to 2.1.7, Pigeonhole 0.3.1

* Thu May 10 2012 Bernhard Rosenkraenzer <bero@bero.eu> 2.1.6-1
+ Revision: 798129
- Update to 2.1.6, pigeonhole 0.3.0

  + Paulo Andrade <pcpa@mandriva.com.br>
    - Add patch to rebuild with autoconf 2.68 or newer.

* Thu May 12 2011 Funda Wang <fwang@mandriva.org> 1.2.17-1
+ Revision: 673945
- update to new version 1.2.17

* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.2.16-5
+ Revision: 663847
- mass rebuild

* Thu Mar 17 2011 Oden Eriksson <oeriksson@mandriva.com> 1.2.16-4
+ Revision: 645744
- relink against libmysqlclient.so.18

* Sat Jan 01 2011 Oden Eriksson <oeriksson@mandriva.com> 1.2.16-3mdv2011.0
+ Revision: 626996
- rebuilt against mysql-5.5.8 libs, again

* Mon Dec 27 2010 Oden Eriksson <oeriksson@mandriva.com> 1.2.16-2mdv2011.0
+ Revision: 625417
- rebuilt against mysql-5.5.8 libs

* Tue Nov 30 2010 Oden Eriksson <oeriksson@mandriva.com> 1.2.16-1mdv2011.0
+ Revision: 603523
- 1.2.16
- update the 3rd party addons

* Mon Oct 04 2010 Oden Eriksson <oeriksson@mandriva.com> 1.2.15-1mdv2011.0
+ Revision: 582946
- 1.2.15

* Sat Sep 18 2010 Funda Wang <fwang@mandriva.org> 1.2.14-2mdv2011.0
+ Revision: 579485
- update file list
- sieve 0.1.17

* Sat Sep 18 2010 Funda Wang <fwang@mandriva.org> 1.2.14-1mdv2011.0
+ Revision: 579455
- new version 1.2.14

* Sun Jul 25 2010 Funda Wang <fwang@mandriva.org> 1.2.13-1mdv2011.0
+ Revision: 558262
- New version 1.2.13

* Sun Jul 11 2010 Funda Wang <fwang@mandriva.org> 1.2.12-1mdv2011.0
+ Revision: 550587
- update to new version 1.2.12

* Thu Apr 08 2010 Eugeni Dodonov <eugeni@mandriva.com> 1.2.11-2mdv2010.1
+ Revision: 533057
- Rebuild for new openssl

* Tue Mar 09 2010 Funda Wang <fwang@mandriva.org> 1.2.11-1mdv2010.1
+ Revision: 516829
- new version 1.2.11

* Fri Feb 26 2010 Oden Eriksson <oeriksson@mandriva.com> 1.2.10-3mdv2010.1
+ Revision: 511561
- rebuilt against openssl-0.9.8m

* Wed Feb 17 2010 Oden Eriksson <oeriksson@mandriva.com> 1.2.10-2mdv2010.1
+ Revision: 507027
- rebuild

* Tue Jan 26 2010 Oden Eriksson <oeriksson@mandriva.com> 1.2.10-1mdv2010.1
+ Revision: 496739
- 1.2.10
- updated the addons to the latest versions

* Thu Dec 17 2009 Funda Wang <fwang@mandriva.org> 1.2.9-1mdv2010.1
+ Revision: 479643
- new version 1.2.9

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1.2.8-1mdv2010.1
+ Revision: 468250
- 1.2.8
- 1.2.7-managesieve-0.11.9
- sieve-0.1.13

* Wed Oct 14 2009 Oden Eriksson <oeriksson@mandriva.com> 1.2.6-1mdv2010.0
+ Revision: 457352
- 1.2.6
- update P8

* Tue Sep 22 2009 Oden Eriksson <oeriksson@mandriva.com> 1.2.5-1mdv2010.0
+ Revision: 447364
- 1.2.5
- sieve-0.1.12
- managesieve-0.11.9

* Mon Aug 10 2009 Funda Wang <fwang@mandriva.org> 1.2.3-2mdv2010.0
+ Revision: 414137
- fix build

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 1.2.3-1mdv2010.0
+ Revision: 412951
- fix deps
- 1.2.3
- sync changes with dovecot-1.2.2-1.20090728snap.fc12.src.rpm but with a twist

* Mon Jun 01 2009 Frederik Himpe <fhimpe@mandriva.org> 1.1.16-1mdv2010.0
+ Revision: 381971
- update to new version 1.1.16

* Mon May 18 2009 Frederik Himpe <fhimpe@mandriva.org> 1.1.15-1mdv2010.0
+ Revision: 377278
- update to new version 1.1.15

* Sun May 03 2009 Funda Wang <fwang@mandriva.org> 1.1.14-1mdv2010.0
+ Revision: 370983
- New versin 1.1.14

* Thu Mar 19 2009 Frederik Himpe <fhimpe@mandriva.org> 1.1.13-1mdv2009.1
+ Revision: 357723
- update to new version 1.1.13

* Tue Mar 17 2009 Frederik Himpe <fhimpe@mandriva.org> 1.1.12-1mdv2009.1
+ Revision: 356874
- update to new version 1.1.12

* Thu Feb 05 2009 Michael Scherer <misc@mandriva.org> 1.1.11-1mdv2009.1
+ Revision: 337739
- update to 1.1.11
- fix dovecot-sieve compilation

* Mon Feb 02 2009 Jérôme Soyer <saispo@mandriva.org> 1.1.10-1mdv2009.1
+ Revision: 336528
- New upstream release

* Wed Jan 14 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.1.8-2mdv2009.1
+ Revision: 329402
- add procmail to sieve conversion tool

* Fri Jan 09 2009 Oden Eriksson <oeriksson@mandriva.com> 1.1.8-1mdv2009.1
+ Revision: 327528
- dovecot-1.1.8
- dovecot-sieve-1.1.6

* Wed Dec 17 2008 Oden Eriksson <oeriksson@mandriva.com> 1.1.7-2mdv2009.1
+ Revision: 315214
- rediffed one fuzzy patch

* Mon Dec 08 2008 Oden Eriksson <oeriksson@mandriva.com> 1.1.7-1mdv2009.1
+ Revision: 311826
- 1.1.7

* Sat Dec 06 2008 Oden Eriksson <oeriksson@mandriva.com> 1.1.6-3mdv2009.1
+ Revision: 311198
- rebuilt against mysql-5.1.30 libs

* Wed Nov 05 2008 Adam Williamson <awilliamson@mandriva.org> 1.1.6-2mdv2009.1
+ Revision: 300121
- fix the permission stuff again (numeric mode in filelist was overriding the
  earlier chmod command)

* Wed Nov 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1.1.6-1mdv2009.1
+ Revision: 300041
- 1.1.6

* Wed Nov 05 2008 Adam Williamson <awilliamson@mandriva.org> 1.1.4-5mdv2009.1
+ Revision: 299971
- set deliver to be group mail (forgot in last commit)

* Tue Nov 04 2008 Adam Williamson <awilliamson@mandriva.org> 1.1.4-4mdv2009.1
+ Revision: 299933
- implement nifty dodge for permissions issues relating to #44926 (see comment)

* Fri Oct 24 2008 Adam Williamson <awilliamson@mandriva.org> 1.1.4-3mdv2009.1
+ Revision: 296857
- fix non-parallel init for the ntpd issue too

* Fri Oct 24 2008 Adam Williamson <awilliamson@mandriva.org> 1.1.4-2mdv2009.1
+ Revision: 296853
- add should-start ntpd to initscript (fabrice facorat, #45035)
- dovecot.conf needs to be 644 not 640 (#44926)

* Wed Oct 15 2008 Oden Eriksson <oeriksson@mandriva.com> 1.1.4-1mdv2009.1
+ Revision: 293893
- 1.1.4

* Sun Sep 07 2008 Adam Williamson <awilliamson@mandriva.org> 1.1.3-3mdv2009.0
+ Revision: 282240
- 0755 for initscript not 0700

* Sun Sep 07 2008 Adam Williamson <awilliamson@mandriva.org> 1.1.3-2mdv2009.0
+ Revision: 282065
- ensure initscript has 0700 permissions (twice, belt and braces!) #41788

* Thu Sep 04 2008 Jérôme Soyer <saispo@mandriva.org> 1.1.3-1mdv2009.0
+ Revision: 280492
- New release

* Fri Aug 15 2008 Michael Scherer <misc@mandriva.org> 1.1.2-1mdv2009.0
+ Revision: 272216
- new version
- fix source url

* Thu Jun 26 2008 Oden Eriksson <oeriksson@mandriva.com> 1.1.1-0.2mdv2009.0
+ Revision: 229256
- nss had nothing to do with nss-devel :-)
- enable everything per default
- fix conditionals
- reload dovecot if needed for the plugins sub packages
- added lsm headers

* Wed Jun 25 2008 Oden Eriksson <oeriksson@mandriva.com> 1.1.1-0.1mdv2009.0
+ Revision: 229123
- 1.1.1
- reworked the conditional magic
- the ldap and gssapi functionalities has been broken
  out to subpackages, dovecot-plugins-ldap and dovecot-plugins-gssapi
- the modulesdir should not be %%{_datadir}/%%{name} but in fact
  %%{_libdir}/%%{name}/modules

* Fri Jun 13 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.14-1mdv2009.0
+ Revision: 218841
- 1.0.14

* Mon Mar 10 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.13-1mdv2008.1
+ Revision: 183490
- 1.0.13 (Minor security fixes)

* Thu Mar 06 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.12-2mdv2008.1
+ Revision: 180930
- fix #38615

* Thu Mar 06 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.12-1mdv2008.1
+ Revision: 180856
- 1.0.12

* Fri Feb 15 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.0.10-4mdv2008.1
+ Revision: 168821
- versionned build dependency on rpm-helper

* Tue Jan 29 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.0.10-3mdv2008.1
+ Revision: 159934
- use new create ssl certificate helper macro interface

* Mon Jan 28 2008 Adam Williamson <awilliamson@mandriva.org> 1.0.10-2mdv2008.1
+ Revision: 159425
- add sieve plugin (#32581)

* Tue Jan 15 2008 Oden Eriksson <oeriksson@mandriva.com> 1.0.10-1mdv2008.1
+ Revision: 153290
- 1.0.10

* Mon Dec 24 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.9-2mdv2008.1
+ Revision: 137504
- rebuilt against openldap-2.4.7 libs

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Dec 14 2007 Jérôme Soyer <saispo@mandriva.org> 1.0.9-1mdv2008.1
+ Revision: 119730
- New release 1.0.9

* Tue Dec 04 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.8-1mdv2008.1
+ Revision: 115393
- 1.0.8

* Tue Nov 06 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.7-1mdv2008.1
+ Revision: 106384
- 1.0.7

* Mon Sep 17 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.5-1mdv2008.0
+ Revision: 89292
- 1.0.5

* Fri Aug 17 2007 Guillaume Rousse <guillomovitch@mandriva.org> 1.0.3-4mdv2008.0
+ Revision: 64673
- use ssl certs creation helpers

  + Tibor Pittich <tibor@mandriva.com>
    - fixed Bug #27491 and #27561

* Thu Aug 16 2007 Tibor Pittich <tibor@mandriva.com> 1.0.3-2mdv2008.0
+ Revision: 64136
- increase release number
- really enable ldap support
- fix with/without rpm build options, fix dexcription

* Wed Aug 15 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.3-1mdv2008.0
+ Revision: 63642
- 1.0.3

* Thu Aug 02 2007 Adam Williamson <awilliamson@mandriva.org> 1.0.2-4mdv2008.0
+ Revision: 58315
- BuildRequires krb5-devel for gssapi build
- use Fedora licensing policy (licensing on this app is insane, this is a good way to handle it)

* Fri Jul 27 2007 Adam Williamson <awilliamson@mandriva.org> 1.0.2-3mdv2008.0
+ Revision: 56127
- build with support for GSSAPI authentication (bug #32112)

* Tue Jul 17 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-2mdv2008.0
+ Revision: 52872
- fix rpm-helper Requires(post,preun) and such
- fix deps
- 1.0.2

* Wed Jun 27 2007 Andreas Hasenack <andreas@mandriva.com> 1.0.1-2mdv2008.0
+ Revision: 45127
- using serverbuild macro (-fstack-protector-all)

  + Adam Williamson <awilliamson@mandriva.org>
    - adjust ssl stuff as advised by guillaume (#27561)

* Fri Jun 15 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-1mdv2008.0
+ Revision: 40141
- 1.0.1

* Tue Jun 12 2007 Adam Williamson <awilliamson@mandriva.org> 1.0.0-2mdv2008.0
+ Revision: 38341
- install /etc/pki/dovecot/dovecot-openssl.cnf (bug #27561)
- argh, wrong branch! revert
- import 2007 package to updates

* Tue May 01 2007 Michael Scherer <misc@mandriva.org> 1.0.0-1mdv2008.0
+ Revision: 19904
- upgrade to 1.0.0 ( at last )

* Sat Apr 21 2007 Anssi Hannula <anssi@mandriva.org> 1.0.rc26-2mdv2008.0
+ Revision: 16707
- migrate away from deprecated pam_stack.so

