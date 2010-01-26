%define build_gssapi 1
%define build_ldap 1
%define build_lucene 1
%define build_mysql 1
%define build_pgsql 1
%define build_sqlite 1
%define build_sieve 1
%define build_managesieve 1

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
%{?_with_managesieve: %{expand: %%global build_managesieve 1}}
%{?_without_managesieve: %{expand: %%global build_managesieve 0}}

%if %{build_managesieve}
%define build_sieve 1
%endif

%define sieve_version 0.1.15
%define managesieve_version 0.11.11

Summary:	Secure IMAP and POP3 server
Name: 		dovecot
Version:	1.2.10
Release:	%mkrel 1
License:	MIT and LGPLv2 and BSD-like and Public Domain
Group:		System/Servers
URL:		http://dovecot.org
Source0:	http://dovecot.org/releases/1.2/%{name}-%{version}.tar.gz
Source1:	http://dovecot.org/releases/1.2/%{name}-%{version}.tar.gz.sig
Source2:	%{name}-pamd
Source3:	%{name}-init
Source4:	http://dovecot.org/tools/migration_wuimp_to_dovecot.pl
Source5:	http://dovecot.org/tools/mboxcrypt.pl
Source6:	http://www.rename-it.nl/dovecot/1.2/dovecot-1.2-sieve-%{sieve_version}.tar.gz
Source7:	http://www.earth.ox.ac.uk/~steve/sieve/procmail2sieve.pl
Source8:	http://www.rename-it.nl/dovecot/1.2/dovecot-1.2-managesieve-%{managesieve_version}.tar.gz
Patch8:		http://www.rename-it.nl/dovecot/1.2/dovecot-1.2.10-managesieve-%{managesieve_version}.diff.gz
Patch0:		dovecot-conf-ssl.patch
Provides:	imap-server pop3-server
Provides:	imaps-server pop3s-server
Requires(pre):	rpm-helper >= 0.21
Requires(post):	rpm-helper >= 0.21
Requires(preun): rpm-helper >= 0.21
Requires(postun): rpm-helper >= 0.21
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
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
    --with[out] managesieve	MmanageSieve support (enabled)

%if %{build_sieve}
%package	plugins-sieve
Summary:	CMU Sieve plugin for dovecot LDA
Group:		System/Servers
Requires:	%{name} >= %{version}

%description	plugins-sieve
This package provides the CMU Sieve plugin version %{sieve_version} for dovecot LDA.
%endif

%if %{build_managesieve}
%package	plugins-managesieve
Summary:	Manage Sieve daemon for dovecot
Group:		System/Servers
Requires:	%{name} >= %{version}
Requires:	%{name}-plugins-sieve >= %{version}

%description	plugins-managesieve
This package provides the Manage Sieve daemon version %{managesieve_version} for dovecot.
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

%prep

%setup -q
# Bug #27491
%patch0 -p0 -b .sslfix

%if %{build_sieve}
%setup -q -D -T -a 6
%endif

%if %{build_managesieve}
%setup -q -D -T -a 8
%patch8 -p1
%endif

%build
%serverbuild
rm -f configure
autoreconf -fi

%configure2_5x \
    --enable-header-install \
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
pushd dovecot-*-sieve-%{sieve_version}
rm -f configure
autoreconf -fis
touch doc/man/sieve-filter.1
%configure2_5x \
    --disable-static \
    --with-dovecot=../ \
    --with-unfinished-features
%make
popd
%endif

%if %{build_managesieve}
pushd dovecot-*-managesieve-%{managesieve_version}
rm -f configure
autoreconf -fis
%configure2_5x \
    --disable-static \
    --with-dovecot=../ \
    --with-dovecot-sieve=../dovecot-*-sieve-%{sieve_version}/
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
pushd dovecot-*-sieve-%{sieve_version}
%makeinstall_std
# temporary borkiness i guess...
f=%{buildroot}%{_mandir}/man1/sieve-filter.1
if ! [ -s $f ]; then rm -f $f; fi
popd
%endif

%if %{build_managesieve}
pushd dovecot-*-managesieve-%{managesieve_version}
%makeinstall_std
popd
%endif

cat %{SOURCE2} > %{buildroot}%{_sysconfdir}/pam.d/%{name}
cat %{SOURCE3} > %{buildroot}%{_initrddir}/%{name}
chmod 0755 %{buildroot}%{_initrddir}/%{name}
cp dovecot-example.conf %{buildroot}%{_sysconfdir}/dovecot.conf
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
rm -rf %{buildroot}%{_datadir}/doc/dovecot/

%pre
%_pre_useradd dovecot /var/lib/%{name} /bin/false
%_pre_groupadd dovecot dovecot

%post
%_post_service dovecot
%_create_ssl_certificate dovecot

%preun
%_preun_service dovecot

%postun
%_postun_userdel dovecot
%_postun_groupdel dovecot

%if %{build_sieve}
%post plugins-sieve
%{_initrddir}/%{name} condrestart > /dev/null 2>&1 || :

%postun plugins-sieve
if [ "$1" = "0" ]; then
    %{_initrddir}/%{name} condrestart > /dev/null 2>&1 || :
fi
%endif

%if %{build_managesieve}
%post plugins-managesieve
%{_initrddir}/%{name} condrestart > /dev/null 2>&1 || :

%postun plugins-managesieve
if [ "$1" = "0" ]; then
    %{_initrddir}/%{name} condrestart > /dev/null 2>&1 || :
fi
%endif

%if %{build_mysql}
%post plugins-mysql
%{_initrddir}/%{name} condrestart > /dev/null 2>&1 || :

%postun plugins-mysql
if [ "$1" = "0" ]; then
    %{_initrddir}/%{name} condrestart > /dev/null 2>&1 || :
fi
%endif

%if %{build_pgsql}
%post plugins-pgsql
%{_initrddir}/%{name} condrestart > /dev/null 2>&1 || :

%postun plugins-pgsql
if [ "$1" = "0" ]; then
    %{_initrddir}/%{name} condrestart > /dev/null 2>&1 || :
fi
%endif

%if %{build_sqlite}
%post plugins-sqlite
%{_initrddir}/%{name} condrestart > /dev/null 2>&1 || :

%postun plugins-sqlite
if [ "$1" = "0" ]; then
    %{_initrddir}/%{name} condrestart > /dev/null 2>&1 || :
fi
%endif

%if %{build_ldap}
%post plugins-ldap
%{_initrddir}/%{name} condrestart > /dev/null 2>&1 || :

%postun plugins-ldap
if [ "$1" = "0" ]; then
    %{_initrddir}/%{name} condrestart > /dev/null 2>&1 || :
fi
%endif

%if %{build_gssapi}
%post plugins-gssapi
%{_initrddir}/%{name} condrestart > /dev/null 2>&1 || :

%postun plugins-gssapi
if [ "$1" = "0" ]; then
    %{_initrddir}/%{name} condrestart > /dev/null 2>&1 || :
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
%doc doc/*.conf doc/*.sh doc/*.txt doc/*.cnf
%doc mboxcrypt.pl migration_wuimp_to_dovecot.pl
%attr(0755,root,root) %{_initrddir}/%{name}
%attr(0640,root,mail) %config(noreplace) %{_sysconfdir}/dovecot.conf
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%{_sbindir}/*
%{_bindir}/procmail2sieve.pl
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/checkpassword-reply
%{_libdir}/%{name}/convert-tool
%attr(2755,root,mail) %{_libdir}/%{name}/deliver
%{_libdir}/%{name}/authtest
%{_libdir}/%{name}/dict
%{_libdir}/%{name}/dovecot-auth
%{_libdir}/%{name}/expire-tool
%{_libdir}/%{name}/gdbhelper
%{_libdir}/%{name}/idxview
%{_libdir}/%{name}/imap
%{_libdir}/%{name}/imap-login
%{_libdir}/%{name}/listview
%{_libdir}/%{name}/logview
%{_libdir}/%{name}/maildirlock
%{_libdir}/%{name}/pop3
%{_libdir}/%{name}/pop3-login
%{_libdir}/%{name}/rawlog
%{_libdir}/%{name}/ssl-build-param
%{_libdir}/%{name}/imap-utf7
%{_libdir}/%{name}/threadview
%dir %{_libdir}/%{name}/modules
%{_libdir}/%{name}/modules/*.so
%{_libdir}/%{name}/modules/pop3/*.so
%{_libdir}/%{name}/modules/lda/*.so
%{_libdir}/%{name}/modules/imap/*.so
%if %{build_sieve}
%exclude %{_libdir}/%{name}/modules/lda/lib90_sieve_plugin.so
%endif
%attr(0700,root,root) %dir /var/lib/%{name}

%if %{build_sieve}
%files plugins-sieve
%defattr(-,root,root,-)
%{_libdir}/%{name}/modules/lda/lib90_sieve_plugin.so
%{_bindir}/sieve-filter
%{_bindir}/sieve-test
%{_bindir}/sievec
%{_bindir}/sieved
%{_mandir}/man1/sievec.1*
%{_mandir}/man1/sieved.1*
%{_mandir}/man1/sieve-filter.1*
%{_mandir}/man1/sieve-test.1*
%endif

%if %{build_managesieve}
%files plugins-managesieve
%defattr(-,root,root,-)
%{_libexecdir}/%{name}/managesieve
%{_libexecdir}/%{name}/managesieve-login
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
%{_libdir}/%{name}/modules/*.*a
%{_libdir}/%{name}/modules/imap/*.*a
%{_libdir}/%{name}/modules/auth/*.*a
%{_libdir}/%{name}/modules/lda/*.*a
%{_libdir}/%{name}/modules/sql/*.*a
