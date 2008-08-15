%define build_gssapi 1
%define build_ldap 1
%define build_lucene 1
%define build_mysql 1
%define build_pgsql 1
%define build_sasl 1

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
%{?_with_sasl: %{expand: %%global build_sasl 1}}
%{?_without_sasl: %{expand: %%global build_sasl 0}}

# TODO
# add configurable ssl support, unfortunately --without-ssl doesn't work if
# openssl-devel package is installed

Summary:	Secure IMAP and POP3 server
Name: 		dovecot
Version:	1.1.2
Release:	%mkrel 1
License:	MIT and LGPLv2 and BSD-like and Public Domain
Group:		System/Servers
URL:		http://dovecot.org
Source0:	http://dovecot.org/releases/1.1/%{name}-%{version}.tar.gz
Source1:	http://dovecot.org/releases/1.1/%{name}-%{version}.tar.gz.sig
Source2:	%{name}-pamd
Source3:	%{name}-init
Source4:	http://dovecot.org/tools/migration_wuimp_to_dovecot.pl
Source5:	http://dovecot.org/tools/mboxcrypt.pl
# sieve plugin. Must be updated when minor version increases.
Source6:	http://www.dovecot.org/releases/sieve/dovecot-sieve-1.1.5.tar.gz
Patch:		dovecot-conf-ssl.patch
Provides:	imap-server pop3-server
Provides:	imaps-server pop3s-server
Requires(pre):	rpm-helper >= 0.21
Requires(post):	rpm-helper >= 0.19
Requires(preun): rpm-helper >= 0.19
Requires(postun): rpm-helper >= 0.19
BuildRequires:	pam-devel
BuildRequires:	openssl-devel
%if %{build_ldap}
BuildRequires:	openldap-devel
%endif
%if %{build_lucene}
BuildRequires:	clucene-devel
%endif
%if %{build_sasl}
BuildRequires:	libsasl-devel
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
BuildRequires:  rpm-helper >= 0.21
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

    --with[out] gssapi	GSSAPI support (enabled)
    --with[out] ldap	LDAP support (enabled)
    --with[out] lucene	Lucene support (enabled)
    --with[out] mysql	MySQL support (enabled)
    --with[out] pgsql	PostgreSQL support (enabled)
    --with[out] sasl	Cyrus SASL 2 library support (enabled)

%if %{build_ldap}
%package	plugins-ldap
Summary:	LDAP support for dovecot
Group:		System/Servers
Requires:	%{name} = %{version}

%description	plugins-ldap
This package provides LDAP capabilities to dovecot in a modular form.
%endif

%if %{build_gssapi}
%package	plugins-gssapi
Summary:	GSSAPI support for dovecot
Group:		System/Servers
Requires:	%{name} = %{version}

%description	plugins-gssapi
This package provides GSSAPI capabilities to dovecot in a modular form.
%endif

%package	devel
Summary:	Devel files for Dovecot IMAP and POP3 server
Group:		Development/C
Requires:	%{name} = %{version}

%description	devel
Dovecot is an IMAP and POP3 server for Linux/UNIX-like systems, written with
security primarily in mind. Although it's written with C, it uses several
coding techniques to avoid most of the common pitfalls.

Dovecot can work with standard mbox and maildir formats and it's fully
compatible with UW-IMAP and Courier IMAP servers as well as mail clients
accessing the mailboxes directly.

This package contains development files for dovecot.

%prep

%setup -q -a 6
# Bug #27491
%patch -p1 -b .sslfix

%build
%serverbuild

%configure2_5x \
    --with-ssl=openssl \
    --with-ssldir=%{_sysconfdir}/ssl/%{name} \
    --with-moduledir=%{_libdir}/%{name}/modules \
    --with-nss \
%if %{build_ldap}
    --with-ldap=plugin \
%endif
%if %{build_pgsql}
    --with-sql \
    --with-pgsql \
%endif
%if %{build_mysql}
    --with-sql \
    --with-mysql \
%endif
%if %{build_sasl}
    --with-cyrus-sasl2 \
%endif
%if %{build_gssapi}
    --with-gssapi=plugin \
%endif
%if %{build_lucene}
    --with-lucene \
%endif

%make

#build sieve plugin
pushd dovecot-sieve-*
%configure2_5x --with-dovecot=../
%make
popd

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/pam.d
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_libdir}/%{name}/modules
install -d %{buildroot}/var/lib/%{name}

%makeinstall_std

pushd dovecot-sieve-*
%makeinstall_std
popd

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

%post plugins-ldap
%{_initrddir}/%{name} condrestart > /dev/null 2>&1 || :

%postun plugins-ldap
if [ "$1" = "0" ]; then
    %{_initrddir}/%{name} condrestart > /dev/null 2>&1 || :
fi

%post plugins-gssapi
%{_initrddir}/%{name} condrestart > /dev/null 2>&1 || :

%postun plugins-gssapi
if [ "$1" = "0" ]; then
    %{_initrddir}/%{name} condrestart > /dev/null 2>&1 || :
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING* NEWS README TODO
%doc doc/*.conf doc/*.sh doc/*.txt doc/*.cnf
%doc mboxcrypt.pl migration_wuimp_to_dovecot.pl
%{_initrddir}/%{name}
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/dovecot.conf
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%{_sbindir}/*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/checkpassword-reply
%{_libdir}/%{name}/convert-tool
%{_libdir}/%{name}/deliver
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
%{_libdir}/%{name}/sievec
%{_libdir}/%{name}/sieved
%{_libdir}/%{name}/ssl-build-param
%dir %{_libdir}/%{name}/modules
%{_libdir}/%{name}/modules/*.so
%{_libdir}/%{name}/modules/pop3/*.so
%{_libdir}/%{name}/modules/lda/*.so
%{_libdir}/%{name}/modules/imap/*.so
%attr(0700,root,root) %dir /var/lib/%{name}

%files devel
%defattr(0755, root, root, 0755)
%{_libdir}/%{name}/modules/*.*a
%{_libdir}/%{name}/modules/imap/*.*a
%{_libdir}/%{name}/modules/auth/*.*a
%{_libdir}/%{name}/modules/lda/*.*a

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
