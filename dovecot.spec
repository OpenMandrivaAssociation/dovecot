%define name		dovecot
%define version     1.0.1
%define rel 1


%global	with_ldap	0
%global	with_sasl	0
%global	with_mysql	1
%global	with_pgsql	0
%{?_without_ldap: %{expand: %%global with_ldap 0}}
%{?_with_sasl: %{expand: %%global with_sasl 1}}
%{?_with_mysql: %{expand: %%global with_mysql 1}}
%{?_with_pgsql: %{expand: %%global with_pgsql 1}}
# TODO
# add configurable ssl support, unfortunatelly --without-ssl doesn't work if
# openssl-devel package is installed

Summary:	Secure IMAP and POP3 server
Name: 		%{name}
Version:	%{version}
Release:	%mkrel %rel
License:	GPL
Group:		System/Servers
URL:		http://dovecot.org
Source0:	http://dovecot.org/releases/%{name}-%{version}.tar.bz2
Source1:	%{name}-pamd
Source2:	%{name}-init
Source4:    http://dovecot.org/tools/migration_wuimp_to_dovecot.pl
Source5:    http://dovecot.org/tools/mboxcrypt.pl
BuildRoot: 	%{_tmppath}/root-%{name}-%{version}
Provides:       imap-server pop3-server
Provides:		imaps-server pop3s-server
Prereq:         rpm-helper
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

%description 
Dovecot is an IMAP and POP3 server for Linux/UNIX-like systems,
written with security primarily in mind. Although it's written with C,
it uses several coding techniques to avoid most of the common
pitfalls.

Dovecot can work with standard mbox and maildir formats and it's fully
compatible with UW-IMAP and Courier IMAP servers as well as mail
clients accessing the mailboxes directly.

This package have some configurable build options:
--without ldap	- build without LDAP support which is by default enabled
--with sasl	- build with Cyrus SASL 2 library support
--with mysql	- build with MySQL support
--with pgsql	- build with PostgreSQL support

%package devel
Summary:	Devel files for Dovecot IMAP and POP3 server
Group: 		System/Servers
Prereq:		rpm-helper

%description devel
Dovecot is an IMAP and POP3 server for Linux/UNIX-like systems,
written with security primarily in mind. Although it's written with C,
it uses several coding techniques to avoid most of the common
pitfalls.

Dovecot can work with standard mbox and maildir formats and it's fully
compatible with UW-IMAP and Courier IMAP servers as well as mail
clients accessing the mailboxes directly.

This package have some configurable build options:
--without ldap	- build without LDAP support which is by default enabled
--with sasl	- build with Cyrus SASL 2 library support
--with mysql	- build with MySQL support
--with pgsql	- build with PostgreSQL support

%prep
%setup -q

%build
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
mkdir -p %{buildroot}%{_sysconfdir}/pki/dovecot
cp doc/dovecot-openssl.cnf %{buildroot}%{_sysconfdir}/pki/dovecot/dovecot-openssl.cnf
cp %{SOURCE4} .
cp %{SOURCE5} . 
# placed in doc
rm -f %{buildroot}%{_sysconfdir}/dovecot*-example.conf

# generate ghost .pem file
mkdir -p %{buildroot}%{_sysconfdir}/ssl/dovecot/{certs,private}
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
if [ ! -f %{_sysconfdir}/ssl/dovecot/certs/dovecot.pem ]; then
pushd %{_sysconfdir}/ssl/dovecot &>/dev/null
umask 077
cat << EOF | openssl req -new -x509 -days 365 -nodes -out certs/dovecot.pem -keyout private/dovecot.pem &>/dev/null
--
SomeState
SomeCity
SomeOrganization
SomeOrganizationalUnit
localhost.localdomain
root@localhost.localdomain
EOF
%__chown root.root private/dovecot.pem certs/dovecot.pem
%__chmod 600 private/dovecot.pem certs/dovecot.pem
popd &>/dev/null
fi
exit 0

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
%dir %{_sysconfdir}/ssl/%{name}
%dir %{_sysconfdir}/ssl/%{name}/certs
%attr(0600,root,root) %dir %{_sysconfdir}/ssl/%{name}/private
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
%dir %{_sysconfdir}/pki/dovecot
%config(noreplace) %{_sysconfdir}/pki/dovecot/dovecot-openssl.cnf
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



