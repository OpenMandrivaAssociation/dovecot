%define name		dovecot
%define version     1.0.rc7

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
Release:	%mkrel 1
License:	GPL
Group:		System/Servers
URL:		http://dovecot.org
Source0:	http://dovecot.org/releases/%{name}-%{version}.tar.bz2
Source1:	%{name}-pamd.bz2
Source2:	%{name}-init.bz2
Source3:	%{name}.conf.bz2
Source4:    http://dovecot.org/tools/migration_wuimp_to_dovecot.pl
Source5:    http://dovecot.org/tools/mboxcrypt.pl
# (misc) patch to change the default order of autodiscovery ( ~/Mail before ~/mail )
Patch2:		%{name}-0.99.10-mbox.patch.bz2
# (saispo) patch for CVE-2006-2414
Patch3:		%{name}-CVE-2006-2414.patch.bz2
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
#%patch2 -p1 -b .mbox
#%patch3 -p1 -b .CVE-2006-2414

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
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/pam.d/%{name}
bzcat %{SOURCE2} > %{buildroot}%{_initrddir}/%{name}
bzcat %{SOURCE3} > %{buildroot}%{_sysconfdir}/dovecot.conf
cp %{SOURCE4} .
cp %{SOURCE5} . 
rm -f %{buildroot}%{_sysconfdir}/dovecot-example.conf

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

%changelog
* Mon Sep 04 2006 Jerome Soyer <saispo@mandriva.org> 1.0.rc7.1mdv2007.0
- new version

* Wed Jul 12 2006 Nicolas Chipaux <chipaux@mandriva.com> 1.0.rc2.1mdv2007.0
- new version
- split in devel rpm

* Sun Jun 25 2006 Nicolas Chipaux <chipaux@mandriva.com> 1.09.beta9.1mdv2007.0
- new version

* Mon May 29 2006 Jerome Soyer <saispo@mandriva.org> 0.99.14-4mdv2007.0
- CVE-2006-2414 
- use mkrel

* Wed Nov 30 2005 Oden Eriksson <oeriksson@mandriva.com> 0.99.14-3mdk
- rebuilt against openssl-0.9.8a

* Tue Aug 30 2005 Oden Eriksson <oeriksson@mandriva.com> 0.99.14-2mdk
- rebuilt against new openldap-2.3.6 libs

* Fri Mar 18 2005 Michael Scherer <misc@mandrake.org> 0.99.14-1mdk
- New release 0.99.14
- better summary
- add some tools in %%doc

* Fri Feb 04 2005 Michael Scherer <misc@mandrake.org> 0.99.12-2mdk
- Rebuild new ldap

* Sun Dec 05 2004 Michael Scherer <misc@mandrake.org> 0.99.12-1mdk
- New release 0.99.12

* Mon Aug 10 2004 Tibor Pittich <Tibor.Pittich@mandrake.org> 0.99.10.9-2mdk
- fix init script to make rpmlint happy
- create switches to allow/deny some features and and describe it in
  description
- update url
- by default disable pgsql support, added configurable support for mysql
- change provides to pop3-server and add imaps and pop3s-server provides
- minimalize number of nonstandard permission in files
- some other spec changes, macroszification

* Mon Aug 9 2004 Tibor Pittich <Tibor.Pittich@mandrake.org> 0.99.10.9-1mdk
- 0.99.10.9

* Wed Jul 14 2004 Michael Scherer <misc@mandrake.org> 0.99.10.7-1mdk 
- 0.99.10.7
- rpmbuildupdate aware

* Tue Jul 13 2004 Michael Scherer <misc@mandrake.org> 0.99.10.6-1mdk
- New release 0.99.10.6
- replaced the patch on conf by a source file
- fix BuildRequires, and init script ( from Michael Reinsch <mr@uue.org> )
- remove implicit requires, added new provides scheme
- remove service restart on upgrade, as it is already done by spec-helper

* Sun Oct 12 2003 Brook Humphrey <bah@linux-mandrake.com> 0.99.10-4mdk
- fixed syntax error

* Sun Oct 12 2003 Brook Humphrey <bah@linux-mandrake.com> 0.99.10-3mdk
- fix to properly generate ssl and add directories

* Sun Oct 12 2003 Brook Humphrey <bah@linux-mandrake.com> 0.99.10-2mdk
- added scripts for generating ssl certificates

* Sun Jul 26 2003 Giuseppe Ghibò <ghibo@mandrakesoft.com> 0.99.10-1mdk
- initial release based on Diag Wieers <dag@wieers.com> SPEC file.
- Patch for searching /Mail before /mail.
- Patch for providing a working default config file (still need
  to add SSL certificates or script to generate them).
