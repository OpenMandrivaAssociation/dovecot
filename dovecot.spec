%global	with_ldap	1
%global	with_mysql	1
%global	with_gssapi	1
%global	with_sasl	0
%global	with_pgsql	0
%{?_without_ldap: %{expand: %%global with_ldap 0}}
%{?_without_mysql: %{expand: %%global with_mysql 0}}
%{?_without_gssapi: %{expand: %%global with_gssapi 0}}
%{?_with_sasl: %{expand: %%global with_sasl 1}}
%{?_with_pgsql: %{expand: %%global with_pgsql 1}}
# TODO
# add configurable ssl support, unfortunately --without-ssl doesn't work if
# openssl-devel package is installed

Summary:	Secure IMAP and POP3 server
Name: 		dovecot
Version:	1.0.8
Release:	%mkrel 1
License:	MIT and LGPLv2 and BSD-like and Public Domain 
Group:		System/Servers
URL:		http://dovecot.org
Source0:	http://dovecot.org/releases/%{name}-%{version}.tar.gz
Source1:	http://dovecot.org/releases/%{name}-%{version}.tar.gz.sig
Source2:	%{name}-pamd
Source3:	%{name}-init
Source4:	http://dovecot.org/tools/migration_wuimp_to_dovecot.pl
Source5:	http://dovecot.org/tools/mboxcrypt.pl
Patch:		dovecot-conf-ssl.patch
Provides:	imap-server pop3-server
Provides:	imaps-server pop3s-server
Requires(pre):	rpm-helper >= 0.19
Requires(post):	rpm-helper >= 0.19
Requires(preun):	rpm-helper >= 0.19
Requires(postun):	rpm-helper >= 0.19
BuildRequires:	pam-devel
BuildRequires:	openssl-devel
%if %{with_ldap}
BuildRequires:	openldap-devel
%endif
%if %{with_sasl}
BuildRequires:	libsasl-devel
%endif
%if %{with_mysql}
BuildRequires:	mysql-devel
%endif
%if %{with_pgsql}
BuildRequires:	postgresql-devel
%endif
%if %{with_gssapi}
BuildRequires:	gssglue-devel
BuildRequires:	krb5-devel
%endif
BuildRequires:  rpm-helper >= 0.19
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description 
Dovecot is an IMAP and POP3 server for Linux/UNIX-like systems, written with
security primarily in mind. Although it's written with C, it uses several
coding techniques to avoid most of the common pitfalls.

Dovecot can work with standard mbox and maildir formats and it's fully
compatible with UW-IMAP and Courier IMAP servers as well as mail clients
accessing the mailboxes directly.

This package has some configurable build options:

 --without ldap		- build without LDAP (default enabled)
 --without mysql	- build without MySQL support (default enabled)
 --without gssapi	- build without GSSAPI support (default enabled)
 --with sasl		- build with Cyrus SASL 2 library support
 --with pgsql		- build with PostgreSQL support

%package	devel
Summary:	Devel files for Dovecot IMAP and POP3 server
Group:		Development/C

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
%patch -p1 -b .sslfix

%build
%serverbuild
%configure \
    --with-ssl=openssl \
    --with-ssldir="%{_sysconfdir}/ssl/%{name}" \
    --with-moduledir="%{_datadir}/%{name}/" \
%if %{with_ldap}
    --with-ldap \
%endif
%if %{with_pgsql}
    --with-sql \
    --with-pgsql \
%endif
%if %{with_mysql}
    --with-sql \
    --with-mysql \
%endif
%if %{with_sasl}
    --with-cyrus-sasl2 \
%endif
%if %{with_gssapi}
    --with-gssapi
%endif
%make

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_datadir}/%{name}

%makeinstall_std
mkdir -p %{buildroot}%{_sysconfdir}/pam.d \
	%{buildroot}%{_initrddir} \
	%{buildroot}%{_var}/%{_lib}/%{name}
cat %{SOURCE2} > %{buildroot}%{_sysconfdir}/pam.d/%{name}
cat %{SOURCE3} > %{buildroot}%{_initrddir}/%{name}
cp dovecot-example.conf %{buildroot}%{_sysconfdir}/dovecot.conf
cp %{SOURCE4} .
cp %{SOURCE5} . 
# placed in doc
rm -f %{buildroot}%{_sysconfdir}/dovecot*-example.conf

# Clean up buildroot
rm -rf %{buildroot}%{_datadir}/doc/dovecot/

%pre
%_pre_useradd dovecot %{_var}/%{_lib}/%{name} /bin/false
%_pre_groupadd dovecot dovecot

%post
%_post_service dovecot
%create_ssl_certificate dovecot false

%preun
%_preun_service dovecot

%postun
%_postun_userdel dovecot
%_postun_groupdel dovecot

%clean
rm -rf %{buildroot}

%files
%defattr(0755, root, root, 0755)
%{_initrddir}/%{name}
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*
%{_sbindir}/*
%attr(0700,root,root) %dir %{_var}/%{_lib}/%{name}
%defattr(0644,root,root,0755)
%doc AUTHORS ChangeLog COPYING* NEWS README TODO
%doc doc/*.conf doc/*.sh doc/*.txt doc/*.cnf
%doc mboxcrypt.pl migration_wuimp_to_dovecot.pl
%config(noreplace) %{_sysconfdir}/dovecot.conf
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.la
%{_datadir}/%{name}/*.so
%{_datadir}/%{name}/pop3/*.so
%{_datadir}/%{name}/lda/*.so
%{_datadir}/%{name}/imap/*.so
%{_datadir}/%{name}/imap/*.la

%files devel
%defattr(0755, root, root, 0755)
%{_datadir}/%{name}/*.a
%{_datadir}/%{name}/imap/*.a
