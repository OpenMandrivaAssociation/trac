# rationale behind the splitting
# every database backend is here to pull the proper database module
# every vcs backend is here for the same reason
# frontend are here to place specific configuration files, except
#   wsgi, here to not pull anything ( ie, not pull apache ) or change the configuration

# TODO people who want to use fcgi with lighttpd ?
%define rel 1

Name:		trac
Version: 0.11
Release: %mkrel %rel
License:	BSD
Group:		Networking/WWW
Summary:	Integrated SCM & Project manager
Source0:    http://ftp.edgewall.com/pub/trac/Trac-%{version}.tar.gz
Source1:    tracd.init
Source2:    tracd.sysconfig
Source3:    Trac.pm

Url:		http://projects.edgewall.com/trac/wiki/TracDownload
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: python-devel
Requires:   python-clearsilver
Requires:   python-genshi
Requires:   python-pygments
Requires:   python-silvercity
Requires:   python-simplejson
Requires:   python-textile
Requires:   %{name}-frontend %{name}-db_backend %{name}-vcs_backend
BuildArch:  noarch
%description
Trac is a minimalistic web-based software project management
and bug/issue tracking system. It provides an interface to
revision control systems (Subversion), an integrated
Wiki and convenient report facilities.


%package cgi
Group:		Networking/WWW
Summary:	Trac Integrated SCM & Project manager - cgi frontend
Group:		Networking/WWW
Requires:       %{name}
# it can work with any cgi webserver, but only apache is covered by the package
Requires:       webserver
Provides:       %{name}-frontend

%description cgi
Trac is a minimalistic web-based software project management
and bug/issue tracking system. It provides an interface to
revision control systems (Subversion), an integrated
Wiki and convenient report facilities.

This package contains various files needed to integrate it
with apache.

%package fcgi
Group:		Networking/WWW
Summary:	Trac Integrated SCM & Project manager - cgi frontend
Group:		Networking/WWW
Requires:       %{name}
# it can work with any fcgi webserver, but only apache is covered by the package
Requires:       apache-mod_fcgid
Provides:       %{name}-frontend

%description fcgi
Trac is a minimalistic web-based software project management
and bug/issue tracking system. It provides an interface to
revision control systems (Subversion), an integrated
Wiki and convenient report facilities.

This package contains various files needed to integrate it
with apache and fcgi.

%package wsgi
Group:		Networking/WWW
Summary:	Trac Integrated SCM & Project manager - wsgi frontend
Group:		Networking/WWW
Requires:       %{name}
Provides:       %{name}-frontend

%description wsgi
Trac is a minimalistic web-based software project management
and bug/issue tracking system. It provides an interface to
revision control systems (Subversion), an integrated
Wiki and convenient report facilities.

This package contains various files needed to integrate it
with a wsgi (Web Server Gateway Interface) compliant server,
such as Twisted or Paste.

%package mod_python
Group:		Networking/WWW
Summary:	Trac Integrated SCM & Project manager - mod_python frontend
Group:		Networking/WWW
Requires:       %{name}
Requires:       apache-mod_python
Provides:       %{name}-frontend

%description mod_python
Trac is a minimalistic web-based software project management
and bug/issue tracking system. It provides an interface to
revision control systems (Subversion), an integrated
Wiki and convenient report facilities.

This package contains various files needed to integrate it
with apache and mod_python by default.

# TODO fast cgi


%package -n drakwizard-%{name}
Group:		System/Configuration/Other
Summary:	Trac Integrated SCM & Project manager - project creation wizard


%description -n drakwizard-%{name}
Trac is a minimalistic web-based software project management
and bug/issue tracking system. It provides an interface to
revision control systems (Subversion), an integrated
Wiki and convenient report facilities.

This package provides a wizard to create trac multiple project
repository using tracd.

You can access it with drakwizard or with Mandriva control center.


%package standalone
Group:		Networking/WWW
Summary:	Trac Integrated SCM & Project manager - standalone frontend
Requires:       %{name}
Provides:       %{name}-frontend
Requires(pre):  rpm-helper

%description standalone
Trac is a minimalistic web-based software project management
and bug/issue tracking system. It provides an interface to
revision control systems (Subversion), an integrated
Wiki and convenient report facilities.

This package contains various files needed to run as standalone
http server.


%package sqlite
Group:		Networking/WWW
Summary:	Trac Integrated SCM & Project manager - sqlite database support
Requires:       %{name}
Requires:       python-sqlite2
Provides:       %{name}-db_backend

%description sqlite
Trac is a minimalistic web-based software project management
and bug/issue tracking system. It provides an interface to
revision control systems (Subversion), an integrated
Wiki and convenient report facilities.

This package contains the needed modules to use sqlite as trac
database backend.


%package postgresql
Group:		Networking/WWW
Summary:	Trac Integrated SCM & Project manager - postgresql database support
Requires:       %{name}
Requires:       python-psycopg
Requires:       pyPgSQL
Provides:       %{name}-db_backend

%description postgresql
Trac is a minimalistic web-based software project management
and bug/issue tracking system. It provides an interface to
revision control systems (Subversion), an integrated
Wiki and convenient report facilities.

This package contains the needed modules to use postgresql as trac
database backend.


%package mysql
Group:		Networking/WWW
Summary:	Trac Integrated SCM & Project manager - mysql database support
Requires:       %{name}
Requires:       python-mysql
Provides:       %{name}-db_backend

%description mysql
Trac is a minimalistic web-based software project management
and bug/issue tracking system. It provides an interface to
revision control systems (Subversion), an integrated
Wiki and convenient report facilities.

This package contains the needed modules to use mysql as trac
database backend.
Beware, the module is still experimental for the moment.

%package svn
Group:		Networking/WWW
Summary:	Trac Integrated SCM & Project manager - subversion support
Requires:       %{name}
Requires:       python-svn subversion
Provides:       %{name}-vcs_backend

%description svn
Trac is a minimalistic web-based software project management
and bug/issue tracking system. It provides an interface to
revision control systems (Subversion), an integrated
Wiki and convenient report facilities.

This package contains the needed modules to use subversion as trac
version control system backend.


%prep
%setup -q -n Trac-%{version}

%build
cat > README.upgrade.urpmi << EOF
Trac changed the format of the database in the 0.10 release.
If you are upgrading from a pre-0.10 version, please see the
file UPGRADE, in %_defaultdocdir/%{name}-%{version}/.

Remember you will need to run:
  trac-admin <env-path> upgrade
and
  trac-admin <env-path> wiki upgrade
to ensure your installation is up to date (remember to backup first!)

In order to ease the installation, and provides more modularity,
trac package have been split in four frontends. You can choose
%{name}-standalone for a version with tracd, or %{name}-cgi,
%{name}-fcgi or %{name}-mod_python for integration with
a webserver (e.g. apache).

EOF

cat > %{name}.conf << EOF
Alias /trac/ "/usr/share/trac/htdocs/"

# fix mdk bug #16298
PassEnv LC_ALL
PassEnv LANG

# fix mdk bug #16298
<Directory "/usr/share/trac/htdocs">
        Allow from All
</Directory>

# Trac need to know where the database is located
#<Location "/cgi-bin/trac.cgi">
#        SetEnv TRAC_ENV "/somewhere/myproject.env/"
#</Location>

# You need this to allow users to authenticate
#<Location "/cgi-bin/trac.cgi/login">
#        AuthType Basic
#        AuthName "trac"
#        AuthUserFile /somewhere/trac.htpasswd
#        Require valid-user
#</location>
EOF

cat > %{name}_mod_python.conf << EOF
# fix mdk bug #16298
PassEnv LC_ALL
PassEnv LANG

# in order to have the project in /projects/myproject
# see http://projects.edgewall.com/trac/wiki/TracModPython
# for the complete doc

#<Location /projects/myproject>
#   SetHandler mod_python
#   PythonHandler trac.web.modpython_frontend
#   PythonOption TracEnv /var/trac/myproject
#   PythonOption TracUriRoot /projects/myproject
#</Location>
#
#<Location "/projects/myproject/login">
#  AuthType Basic
#  AuthName "myproject"
#  AuthUserFile /var/trac/myproject/.htaccess
#  Require valid-user
#</Location>
EOF

cat > %{name}_fcgi.conf << EOF
# fix mdk bug #16298
PassEnv LC_ALL
PassEnv LANG

# see http://projects.edgewall.com/trac/wiki/TracFastCgi
# for the complete doc

#DefaultInitEnv TRAC_ENV "/var/trac/myproject/"

# You need this to allow users to authenticate
#<Location "/cgi-bin/trac.fcgi/login">
#        AuthType Basic
#        AuthName "trac"
#        AuthUserFile /somewhere/trac.htpasswd
#        Require valid-user
#</location>
EOF


cat > wizard.trac.conf << EOF
NAME="Trac"
DESCRIPTION="Trac wizard ( project management software )"
LONG_DESCRIPTION="A wizard to setup a bugtracking system"
EOF

cat > README.wizard << EOF
Since many people complain that wizards do not help to understand their
system, here is a quick summary of this wizard actions, and how to do the
same by hand :

1) subversion repository creation ( if it do not exist )
$ svnadmin create --fs-type fsfs \$DIRECTORY

fsfs was chosen over bdbd because it is more robust, according to trac
developers.

2) trac repository creation
$ trac-admin \$TRAC_REPOSITORY_PATH initenv \$PROJECT_NAME

3) integration with tracd
in order to use your new trac project, you need to add it to tracd config
file, in /etc/sysconfig/tracd. All you need is to add it to PROJECT,
and reload tracd, with service tracd restart.

EOF
%install

rm -rf %{buildroot}
python ./setup.py install --root=%{buildroot} --prefix=%_prefix

#change default config
perl -pi -e "s#%{buildroot}##" %{buildroot}/%{_libdir}/python%{pyver}/site-packages/%{name}/siteconfig.py
rm -f %{buildroot}/%{_libdir}/python%{pyver}/site-packages/%{name}/siteconfig.pyc

mkdir -p %{buildroot}/%{_sysconfdir}/httpd/conf/webapps.d
cp %{name}.conf  %{buildroot}/%{_sysconfdir}/httpd/conf/webapps.d/
cp %{name}_mod_python.conf %{buildroot}/%{_sysconfdir}/httpd/conf/webapps.d/
cp %{name}_fcgi.conf %{buildroot}/%{_sysconfdir}/httpd/conf/webapps.d/

mkdir -p %{buildroot}/var/www
cp -ar cgi-bin %{buildroot}/var/www

mkdir -p %{buildroot}/%{_initrddir}
cat %{SOURCE1} >  %{buildroot}/%{_initrddir}/%{name}d
chmod 0755 %{buildroot}/%{_initrddir}/%{name}d

mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig/
cat %{SOURCE2} >  %{buildroot}/%{_sysconfdir}/sysconfig/%{name}d

mkdir -p %{buildroot}/%{_sysconfdir}/wizard.d/
cp wizard.trac.conf %{buildroot}/%{_sysconfdir}/wizard.d/%{name}.conf

mkdir -p %{buildroot}/%{perl_vendorlib}/MDK/Wizard/
cat %{SOURCE3} >  %{buildroot}/%{perl_vendorlib}/MDK/Wizard/Trac.pm

%clean
rm -rf %{buildroot}

%post cgi
%{_initrddir}/httpd reload

%postun cgi
%{_initrddir}/httpd reload

%post fcgi
%{_initrddir}/httpd reload

%postun fcgi
%{_initrddir}/httpd reload


%post standalone
%_post_service tracd

%preun standalone
%_preun_service tracd

%files
%defattr(-,root,root)
%doc AUTHORS  ChangeLog README COPYING
%doc INSTALL   RELEASE UPGRADE doc THANKS contrib
%doc README.upgrade.urpmi

%{_bindir}/%{name}-admin
%{py_puresitedir}/%{name}/
%if %{mdkversion} > 200700
%{py_puresitedir}/*.egg-info
%endif
%exclude %{py_puresitedir}/%{name}/web/modpython_frontend.py*
%exclude %{py_puresitedir}/%{name}/web/fcgi_frontend.py*
%exclude %{py_puresitedir}/%{name}/web/_fcgi.py*

%files standalone
%defattr(-,root,root)
%config(noreplace) %{_initrddir}/%{name}d
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}d
%{_bindir}/%{name}d

%files cgi
%defattr(-,root,root)
/var/www/cgi-bin/%{name}.cgi
%config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf


%files fcgi
%defattr(-,root,root)
/var/www/cgi-bin/%{name}.fcgi
%config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}_fcgi.conf
%{py_puresitedir}/%{name}/web/fcgi_frontend.py*
%{py_puresitedir}/%{name}/web/_fcgi.py*


%files mod_python
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}_mod_python.conf
%{py_puresitedir}/%{name}/web/modpython_frontend.py*


# empty subpackages, to pull deps.
# trac already does autodetection, and the default list of component
# will try to load the default backend, and trigger a error if it cannot
%files sqlite
%defattr(-,root,root)
%doc COPYING

%files postgresql
%defattr(-,root,root)
%doc COPYING

%files mysql
%defattr(-,root,root)
%doc COPYING

%files svn
%defattr(-,root,root)
%doc COPYING

%files wsgi
%defattr(-,root,root)
%doc COPYING

%files -n drakwizard-%{name}
%defattr(-,root,root)
%doc README.wizard
%{perl_vendorlib}/MDK/Wizard/*
%config(noreplace) %{_sysconfdir}/wizard.d/%{name}.conf


