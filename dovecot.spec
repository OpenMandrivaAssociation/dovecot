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
Version:	1.0.3
Release:	%mkrel 2
License:	MIT and LGPLv2 and BSD-like and Public Domain 
Group:		System/Servers
URL:		http://dovecot.org
Source0:	http://dovecot.org/releases/%{name}-%{version}.tar.bz2
Source1:	%{name}-pamd
Source2:	%{name}-init
Source4:	http://dovecot.org/tools/migration_wuimp_to_dovecot.pl
Source5:	http://dovecot.org/tools/mboxcrypt.pl
Provides:	imap-server pop3-server
Provides:	imaps-server pop3s-server
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
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
BuildRequires:	gssapi-devel
BuildRequires:	krb5-devel
%endif
BuildRoot:	%{_tmppath}/root-%{name}-%{version}

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
cat %{SOURCE1} > %{buildroot}%{_sysconfdir}/pam.d/%{name}
cat %{SOURCE2} > %{buildroot}%{_initrddir}/%{name}
cp dovecot-example.conf %{buildroot}%{_sysconfdir}/dovecot.conf
# Bug #27561 - AdamW 2007/06
mkdir -p %{buildroot}%{_sysconfdir}/pki/tls
cp doc/dovecot-openssl.cnf %{buildroot}%{_sysconfdir}/pki/tls/dovecot.cnf
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

# TODO
# move this somewhere else, because these commands is "dangerous" as rpmlint say
#
# create a ssl cert
# generate SSL cert if needed
if [ $1 = 1 ]; then
    openssl req -new -x509 -days 365 \
        -config %{_sysconfdir}/pki/tls/dovecot.cnf \
        -keyout %{_sysconfdir}/pki/tls/private/dovecot.pem \
        -out %{_sysconfdir}/pki/tls/certs/dovecot.pem
    # enforce strict perms
    chmod 600 %{_sysconfdir}/pki/tls/private/dovecot.pem
fi

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
%config(noreplace) %{_sysconfdir}/pki/tls/dovecot.cnf
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
