%bcond_without gssapi
%bcond_without ldap
%bcond_without lucene
%bcond_without mysql
%bcond_without pgsql
%bcond_without sqlite
%bcond_without sieve
%bcond_without systemd

# The Sieve plugin needs to reference internal symbols
%define _disable_ld_no_undefined 1
%define _disable_rebuild_configure 1

%define major %(echo %version |cut -d. -f1-2)
%define sieve_version 0.5.21

Summary:	Secure IMAP and POP3 server
Name: 		dovecot
Version:	2.3.21.1
Release:	1
License:	MIT and LGPLv2 and BSD-like and Public Domain
Group:		System/Servers
Url:		https://dovecot.org
Source0:	http://dovecot.org/releases/%{major}/dovecot-%{version}.tar.gz
Source1:	http://dovecot.org/releases/%{major}/dovecot-%{version}.tar.gz.sig
Source2:	%{name}-pamd
Source3:	%{name}-init
Source4:	http://dovecot.org/tools/migration_wuimp_to_dovecot.pl
Source5:	http://dovecot.org/tools/mboxcrypt.pl
Source6:	http://pigeonhole.dovecot.org/releases/%{major}/dovecot-%{major}-pigeonhole-%{sieve_version}.tar.gz
Source7:	http://www.earth.ox.ac.uk/~steve/sieve/procmail2sieve.pl
Source20:	dovecot.sysusers
Source100:	%{name}.rpmlintrc
Patch0:		dovecot-conf-ssl.patch
Patch1:		dovecot-2.2.2-quota-tirpc.patch
Patch2:		dovecot-2.2.26.0-find-libstemmer.patch

BuildRequires:	cap-devel
BuildRequires:	gettext-devel
BuildRequires:	pam-devel
BuildRequires:	sasl-devel
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(libtirpc)
BuildRequires:	pkgconfig(libsodium)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(liblz4)
BuildRequires:	pkgconfig(libzstd)
BuildRequires:	pkgconfig(libsystemd)
%if %{with ldap}
BuildRequires:	pkgconfig(ldap)
%endif
%if %{with lucene}
BuildRequires:	pkgconfig(libclucene-core)
%endif
%if %{with mysql}
BuildRequires:	mysql-devel
%endif
%if %{with pgsql}
BuildRequires:	postgresql-devel
%endif
%if %{with gssapi}
BuildRequires:	pkgconfig(libgssglue)
BuildRequires:	krb5-devel
%endif
%if %{with sqlite}
BuildRequires:	pkgconfig(sqlite3)
%endif
BuildRequires:	rpm-helper >= 0.21
BuildRequires:	bzip2-devel
BuildRequires:	libstemmer-devel
Provides:	imap-server
Provides:	pop3-server
Provides:	imaps-server
Provides:	pop3s-server
Requires(pre,post,preun,postun):	rpm-helper >= 0.21
Requires:	%{name}-config >= 2.1

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

%if %{with sieve}
%package	plugins-sieve
Summary:	CMU Sieve plugin for dovecot LDA
Group:		System/Servers
Requires:	%{name} >= %{version}

%description	plugins-sieve
This package provides the CMU Sieve plugin version %{sieve_version} for dovecot LDA.
%endif

%if %{with pgsql}
%package	plugins-pgsql
Summary:	Postgres SQL backend for dovecot
Group:		System/Servers
Requires:	%{name} >= %{version}

%description	plugins-pgsql
This package provides the Postgres SQL backend for dovecot-auth etc.
%endif

%if %{with mysql}
%package	plugins-mysql
Summary:	MySQL backend for dovecot
Group:		System/Servers
Requires:	%{name} >= %{version}

%description	plugins-mysql
This package provides the MySQL backend for dovecot-auth etc.
%endif

%if %{with ldap}
%package	plugins-ldap
Summary:	LDAP support for dovecot
Group:		System/Servers
Requires:	%{name} >= %{version}

%description	plugins-ldap
This package provides LDAP capabilities to dovecot in a modular form.
%endif

%if %{with gssapi}
%package	plugins-gssapi
Summary:	GSSAPI support for dovecot
Group:		System/Servers
Requires:	%{name} >= %{version}

%description	plugins-gssapi
This package provides GSSAPI capabilities to dovecot in a modular form.
%endif

%if %{with sqlite}
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
Provides:	%{name}-config = %version-%release

%description	config-standalone
Config files for running the Dovecot IMAP and POP3 server by itself.

This is the basic configuration for running a Dovecot server - you may
want to install the postfix-dovecot-config package instead if you wish
to run a combination of the Postfix SMTP server and the Dovecot IMAP/POP3
server.

%prep

%setup -qn %{name}-%{version}
%if %{with sieve}
%setup -qn %{name}-%{version} -D -T -a 6
%endif
%autopatch -p1

# Remove patch backups so they don't get packaged into the
# config subpackages
find . -name "*~" |xargs rm -rf

libtoolize --force
aclocal -I m4
automake -a
autoconf
cd *pigeonhole*
libtoolize --force
aclocal -I m4
automake -a
autoconf

%build
%serverbuild

%configure \
    --enable-header-install \
    --disable-static \
    --with-sql=plugin \
    --with-sql-drivers \
    --with-ssl=openssl \
    --with-ssldir=%{_sysconfdir}/pki/%{name} \
    --with-moduledir=%{_libdir}/%{name}/modules \
%if %{with systemd}
    --with-systemdsystemunitdir=%{_unitdir} \
%endif
    --with-nss \
%if %{with ldap}
    --with-ldap=plugin \
%endif
%if %{with pgsql}
    --with-pgsql \
%endif
%if %{with mysql}
    --with-mysql \
%endif
%if %{with sqlite}
    --with-sqlite \
%endif
%if %{with gssapi}
    --with-gssapi=plugin \
%endif
%if %{with lucene}
    --with-lucene \
%endif
    --with-libcap

%make

%if %{with sieve}
pushd dovecot-*-pigeonhole-%{sieve_version}
rm -f configure
autoreconf -fi
touch doc/man/sieve-filter.1
%configure \
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

%if %{with sieve}
pushd dovecot-*-pigeonhole-%{sieve_version}
%makeinstall_std
# temporary borkiness i guess...
f=%{buildroot}%{_mandir}/man1/sieve-filter.1
if ! [ -s $f ]; then rm -f $f; fi
popd
%endif

cat %{SOURCE2} > %{buildroot}%{_sysconfdir}/pam.d/%{name}
%if %{without systemd}
cat %{SOURCE3} > %{buildroot}%{_initrddir}/%{name}
chmod 0755 %{buildroot}%{_initrddir}/%{name}
%else
mkdir -p %{buildroot}%{_sysusersdir}
cp %{S:20} %{buildroot}%{_sysusersdir}/dovecot.conf
%endif
pwd
cp doc/example-config/dovecot.conf %{buildroot}%{_sysconfdir}/%{name}/dovecot.conf
cp -a doc/example-config/conf.d %buildroot%{_sysconfdir}/%{name}/
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
%sysusers_create_package dovecot %{S:20}

%post
%_post_service dovecot
%_create_ssl_certificate dovecot

%preun
%_preun_service dovecot

%if %{with sieve}
%post plugins-sieve
/sbin/service %{name} condrestart > /dev/null 2>&1 || :

%postun plugins-sieve
if [ "$1" = "0" ]; then
    /sbin/service %{name} condrestart > /dev/null 2>&1 || :
fi
%endif

%if %{with mysql}
%post plugins-mysql
/sbin/service %{name} condrestart > /dev/null 2>&1 || :

%postun plugins-mysql
if [ "$1" = "0" ]; then
    /sbin/service %{name} condrestart > /dev/null 2>&1 || :
fi
%endif

%if %{with pgsql}
%post plugins-pgsql
/sbin/service %{name} condrestart > /dev/null 2>&1 || :

%postun plugins-pgsql
if [ "$1" = "0" ]; then
    /sbin/service %{name} condrestart > /dev/null 2>&1 || :
fi
%endif

%if %{with sqlite}
%post plugins-sqlite
/sbin/service %{name} condrestart > /dev/null 2>&1 || :

%postun plugins-sqlite
if [ "$1" = "0" ]; then
    /sbin/service %{name} condrestart > /dev/null 2>&1 || :
fi
%endif

%if %{with ldap}
%post plugins-ldap
/sbin/service %{name} condrestart > /dev/null 2>&1 || :

%postun plugins-ldap
if [ "$1" = "0" ]; then
    /sbin/service %{name} condrestart > /dev/null 2>&1 || :
fi
%endif

%if %{with gssapi}
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
%doc AUTHORS ChangeLog COPYING* NEWS README TODO
%doc doc/*.sh doc/*.txt doc/*.cnf
%attr(0750,root,mail) %dir %{_sysconfdir}/%{name}
%attr(0750,root,mail) %dir %{_sysconfdir}/%{name}/conf.d
%doc %{_sysconfdir}/dovecot/README
%if %{with systemd}
%{_unitdir}/dovecot.service
%{_unitdir}/dovecot.socket
%{_sysusersdir}/dovecot.conf
%else
%attr(0755,root,root) %{_initrddir}/%{name}
%endif
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%{_bindir}/doveadm
%{_bindir}/doveconf
%{_bindir}/dovecot
%{_bindir}/dovecot-sysreport
%{_bindir}/dsync
%{_bindir}/procmail2sieve.pl
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/checkpassword-reply
%{_libexecdir}/%{name}/deliver
%{_libexecdir}/%{name}/aggregator
%{_libexecdir}/%{name}/anvil
%{_libexecdir}/%{name}/auth
%{_libexecdir}/%{name}/config
%{_libexecdir}/%{name}/decode2text.sh
%{_libexecdir}/%{name}/dict
%{_libexecdir}/%{name}/director
%{_libexecdir}/%{name}/dns-client
%{_libexecdir}/%{name}/doveadm-server
%attr(2755,root,mail) %{_libexecdir}/%{name}/dovecot-lda
%{_libexecdir}/%{name}/health-check.sh
%{_libexecdir}/%{name}/imap-urlauth
%{_libexecdir}/%{name}/imap-urlauth-login
%{_libexecdir}/%{name}/imap-urlauth-worker
%{_libexecdir}/%{name}/indexer
%{_libexecdir}/%{name}/indexer-worker
%{_libexecdir}/%{name}/ipc
%{_libexecdir}/%{name}/gdbhelper
%{_libexecdir}/%{name}/imap
%{_libexecdir}/%{name}/imap-hibernate
%{_libexecdir}/%{name}/imap-login
%{_libexecdir}/%{name}/lmtp
%{_libexecdir}/%{name}/log
%{_libexecdir}/%{name}/maildirlock
%{_libexecdir}/%{name}/old-stats
%{_libexecdir}/%{name}/pop3
%{_libexecdir}/%{name}/pop3-login
%{_libexecdir}/%{name}/quota-status
%{_libexecdir}/%{name}/rawlog
%{_libexecdir}/%{name}/replicator
%{_libexecdir}/%{name}/script
%{_libexecdir}/%{name}/script-login
%{_libexecdir}/%{name}/stats
%{_libexecdir}/%{name}/submission
%{_libexecdir}/%{name}/submission-login
%{_libexecdir}/%{name}/xml2text
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/libdcrypt_openssl.so
%{_libdir}/%{name}/libdovecot-compression.so*
%{_libdir}/%{name}/libdovecot-dsync.so*
%{_libdir}/%{name}/libdovecot-fts.so*
%{_libdir}/%{name}/libdovecot-lda.so*
%{_libdir}/%{name}/libdovecot-ldap.so*
%{_libdir}/%{name}/libdovecot-login.so*
%{_libdir}/%{name}/libdovecot-sql.so*
#{_libdir}/%{name}/libdovecot-ssl.so*
%{_libdir}/%{name}/libdovecot-storage.so*
%{_libdir}/%{name}/libdovecot.so*
%dir %{_libdir}/%{name}/modules
%{_libdir}/%{name}/modules/*.so
%dir %{_libdir}/%{name}/modules/auth
%{_libdir}/%{name}/modules/auth/*.so
%exclude %{_libdir}/%{name}/modules/auth/libauthdb_ldap.so
%exclude %{_libdir}/%{name}/modules/auth/libmech_gssapi.so
%if %{with pgsql}
%exclude %{_libdir}/%{name}/modules/auth/libdriver_pgsql.so
%exclude %{_libdir}/%{name}/modules/dict/libdriver_pgsql.so
%exclude %{_libdir}/%{name}/modules/libdriver_pgsql.so
%endif
%if %{with mysql}
%exclude %{_libdir}/%{name}/modules/auth/libdriver_mysql.so
%exclude %{_libdir}/%{name}/modules/dict/libdriver_mysql.so
%exclude %{_libdir}/%{name}/modules/libdriver_mysql.so
%endif
%if %{with sqlite}
%exclude %{_libdir}/%{name}/modules/auth/libdriver_sqlite.so
%exclude %{_libdir}/%{name}/modules/dict/libdriver_sqlite.so
%exclude %{_libdir}/%{name}/modules/libdriver_sqlite.so
%endif
%dir %{_libdir}/%{name}/modules/dict
%{_libdir}/%{name}/modules/dict/libdict_ldap.so
%dir %{_libdir}/%{name}/modules/doveadm
%{_libdir}/%{name}/modules/doveadm/*.so
%dir %{_libdir}/%{name}/modules/settings
%{_libdir}/%{name}/modules/settings/*.so
%dir %{_libdir}/%{name}/modules/old-stats
%{_libdir}/%{name}/modules/old-stats/*.so
%{_datadir}/%{name}
%attr(0700,root,root) %dir /var/lib/%{name}
%{_mandir}/man1/deliver.1*
%{_mandir}/man1/doveadm*.1*
%{_mandir}/man1/doveconf.1*
%{_mandir}/man1/dovecot-sysreport.1*
%{_mandir}/man1/dovecot-lda.1*
%{_mandir}/man1/dovecot.1*
%{_mandir}/man1/dsync.1*
%{_mandir}/man1/sieve-dump.1*
%{_mandir}/man1/sieved.1*
%{_mandir}/man7/doveadm-search-query.7*
%{_mandir}/man7/pigeonhole.7*

%files config-standalone
%attr(0644,root,mail) %config(noreplace) %{_sysconfdir}/%{name}/dovecot.conf
%attr(0644,root,mail) %{_sysconfdir}/%{name}/conf.d/*

%if %{with sieve}
%files plugins-sieve
%{_bindir}/sieve-filter
%{_bindir}/sieve-test
%{_bindir}/sievec
%{_bindir}/sieve-dump
%{_libdir}/%name/libdovecot-sieve.so*
%{_libdir}/dovecot/modules/sieve/lib90_sieve_extprograms_plugin.so
%{_libdir}/dovecot/modules/sieve/lib90_sieve_imapsieve_plugin.so
%{_libexecdir}/%name/managesieve
%{_libexecdir}/%name/managesieve-login
%{_mandir}/man1/sievec.1*
%{_mandir}/man1/sieve-test.1*
%endif

%if %{with ldap}
%files plugins-ldap
%{_libdir}/%{name}/modules/auth/libauthdb_ldap.so
%endif

%if %{with gssapi}
%files plugins-gssapi
%{_libdir}/%{name}/modules/auth/libmech_gssapi.so
%endif

%if %{with sqlite}
%files plugins-sqlite
%{_libdir}/%{name}/modules/auth/libdriver_sqlite.so
%{_libdir}/%{name}/modules/dict/libdriver_sqlite.so
%{_libdir}/%{name}/modules/libdriver_sqlite.so
%endif

%if %{with mysql}
%files plugins-mysql
%{_libdir}/%{name}/modules/auth/libdriver_mysql.so
%{_libdir}/%{name}/modules/dict/libdriver_mysql.so
%{_libdir}/%{name}/modules/libdriver_mysql.so
%endif

%if %{with pgsql}
%files plugins-pgsql
%{_libdir}/%{name}/modules/auth/libdriver_pgsql.so
%{_libdir}/%{name}/modules/dict/libdriver_pgsql.so
%{_libdir}/%{name}/modules/libdriver_pgsql.so
%endif

%files devel
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_libdir}/%{name}/dovecot-config
#{_libdir}/%{name}/modules/*.*a
#{_libdir}/%{name}/modules/auth/*.*a
%{_datadir}/aclocal/*.m4
