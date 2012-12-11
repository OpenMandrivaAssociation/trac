# rationale behind the splitting
# every database backend is here to pull the proper database module
# every vcs backend is here for the same reason
# frontend are here to place specific configuration files, except
#   wsgi, here to not pull anything ( ie, not pull apache ) or change the configuration

# TODO people who want to use fcgi with lighttpd ?

Summary:	Integrated SCM & Project manager
Name:		trac
Version:	0.12.1
Release:	%mkrel 1
License:	BSD
Group:		Networking/WWW
Url:		http://trac.edgewall.org/
Source0:	ftp://ftp.edgewall.com/pub/trac/Trac-%{version}.tar.gz
Source1:	tracd.init
Source2:	tracd.sysconfig
Source3:	Trac.pm
BuildRequires:	python-devel
BuildRequires:	python-setuptools
Requires:	python-clearsilver
Requires:	python-genshi
Requires:	python-pygments
Requires:	python-silvercity
Requires:	python-simplejson
Requires:	python-textile
%if %mdkversion > 200900
Requires:	python-pkg-resources
%endif
Requires:	python-setuptools
Requires:	%{name}-frontend
Requires:	%{name}-db_backend
Requires:	%{name}-vcs_backend
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Trac is a minimalistic web-based software project management
and bug/issue tracking system. It provides an interface to
revision control systems (Subversion), an integrated
Wiki and convenient report facilities.


%package cgi
Summary:	Trac Integrated SCM & Project manager - cgi frontend
Group:		Networking/WWW
Requires:	%{name} = %{version}-%{release}
# it can work with any cgi webserver, but only apache is covered by the package
Requires:	webserver
Provides:	%{name}-frontend

%description cgi
Trac is a minimalistic web-based software project management
and bug/issue tracking system. It provides an interface to
revision control systems (Subversion), an integrated
Wiki and convenient report facilities.

This package contains various files needed to integrate it
with apache.

%package fcgi
Summary:	Trac Integrated SCM & Project manager - cgi frontend
Group:		Networking/WWW
Requires:	%{name} = %{version}-%{release}
# it can work with any fcgi webserver, but only apache is covered by the package
Requires:	apache-mod_fcgid
Provides:	%{name}-frontend

%description fcgi
Trac is a minimalistic web-based software project management
and bug/issue tracking system. It provides an interface to
revision control systems (Subversion), an integrated
Wiki and convenient report facilities.

This package contains various files needed to integrate it
with apache and fcgi.

%package wsgi
Summary:	Trac Integrated SCM & Project manager - wsgi frontend
Group:		Networking/WWW
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-frontend

%description wsgi
Trac is a minimalistic web-based software project management
and bug/issue tracking system. It provides an interface to
revision control systems (Subversion), an integrated
Wiki and convenient report facilities.

This package contains various files needed to integrate it
with a wsgi (Web Server Gateway Interface) compliant server,
such as Twisted or Paste.

%package mod_python
Summary:	Trac Integrated SCM & Project manager - mod_python frontend
Group:		Networking/WWW
Requires:	%{name} = %{version}-%{release}
Requires:	apache-mod_python
Provides:	%{name}-frontend

%description mod_python
Trac is a minimalistic web-based software project management
and bug/issue tracking system. It provides an interface to
revision control systems (Subversion), an integrated
Wiki and convenient report facilities.

This package contains various files needed to integrate it
with apache and mod_python by default.

# TODO fast cgi


%package -n drakwizard-%{name}
Summary:	Trac Integrated SCM & Project manager - project creation wizard
Group:		System/Configuration/Other

%description -n drakwizard-%{name}
Trac is a minimalistic web-based software project management
and bug/issue tracking system. It provides an interface to
revision control systems (Subversion), an integrated
Wiki and convenient report facilities.

This package provides a wizard to create trac multiple project
repository using tracd.

You can access it with drakwizard or with Mandriva control center.


%package standalone
Summary:	Trac Integrated SCM & Project manager - standalone frontend
Group:		Networking/WWW
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-frontend
Requires(pre):	rpm-helper

%description standalone
Trac is a minimalistic web-based software project management
and bug/issue tracking system. It provides an interface to
revision control systems (Subversion), an integrated
Wiki and convenient report facilities.

This package contains various files needed to run as standalone
http server.


%package sqlite
Summary:	Trac Integrated SCM & Project manager - sqlite database support
Group:		Networking/WWW
Requires:	%{name} = %{version}-%{release}
Requires:	python-sqlite2
Provides:	%{name}-db_backend

%description sqlite
Trac is a minimalistic web-based software project management
and bug/issue tracking system. It provides an interface to
revision control systems (Subversion), an integrated
Wiki and convenient report facilities.

This package contains the needed modules to use sqlite as trac
database backend.


%package postgresql
Summary:	Trac Integrated SCM & Project manager - postgresql database support
Group:		Networking/WWW
Requires:	%{name} = %{version}-%{release}
Requires:	python-psycopg
Requires:	pyPgSQL
Provides:	%{name}-db_backend

%description postgresql
Trac is a minimalistic web-based software project management
and bug/issue tracking system. It provides an interface to
revision control systems (Subversion), an integrated
Wiki and convenient report facilities.

This package contains the needed modules to use postgresql as trac
database backend.


%package mysql
Summary:	Trac Integrated SCM & Project manager - mysql database support
Group:		Networking/WWW
Requires:	%{name} = %{version}-%{release}
Requires:	python-mysql
Provides:	%{name}-db_backend

%description mysql
Trac is a minimalistic web-based software project management
and bug/issue tracking system. It provides an interface to
revision control systems (Subversion), an integrated
Wiki and convenient report facilities.

This package contains the needed modules to use mysql as trac
database backend.
Beware, the module is still experimental for the moment.

%package svn
Summary:	Trac Integrated SCM & Project manager - subversion support
Group:		Networking/WWW
Requires:	%{name}
Requires:	python-svn
Requires:	subversion
Provides:	%{name}-vcs_backend

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
file UPGRADE, in %{_defaultdocdir}/%{name}-%{version}/.

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
python ./setup.py install --root=%{buildroot} --prefix=%{_prefix}

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
%if %mdkversion < 201010
%_post_webapp
%endif

%postun cgi
%if %mdkversion < 201010
%_postun_webapp
%endif

%post fcgi
%if %mdkversion < 201010
%_post_webapp
%endif

%postun fcgi
%if %mdkversion < 201010
%_postun_webapp
%endif

%post mod_python
%if %mdkversion < 201010
%_post_webapp
%endif

%postun mod_python
%if %mdkversion < 201010
%_postun_webapp
%endif

%post standalone
%_post_service tracd

%preun standalone
%_preun_service tracd

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog README
%doc RELEASE UPGRADE doc THANKS contrib
%doc README.upgrade.urpmi

%{_bindir}/%{name}-admin
%{py_puresitedir}/tracopt/
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


%changelog
* Sun Jan 16 2011 Michael Scherer <misc@mandriva.org> 0.12.1-1mdv2011.0
+ Revision: 631155
- update to 0.12.1

* Fri Oct 29 2010 Michael Scherer <misc@mandriva.org> 0.11.7-2mdv2011.0
+ Revision: 590116
- rebuild for python 2.7

* Sat Mar 27 2010 Michael Scherer <misc@mandriva.org> 0.11.7-1mdv2010.1
+ Revision: 528265
- update to new version 0.11.7

* Sun Jan 17 2010 Guillaume Rousse <guillomovitch@mandriva.org> 0.11.6-2mdv2010.1
+ Revision: 492724
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise

* Fri Dec 25 2009 Frederik Himpe <fhimpe@mandriva.org> 0.11.6-1mdv2010.1
+ Revision: 482291
- update to new version 0.11.6

* Tue Sep 15 2009 Frederik Himpe <fhimpe@mandriva.org> 0.11.5-1mdv2010.0
+ Revision: 443149
- update to new version 0.11.5

* Sat Apr 04 2009 Frederik Himpe <fhimpe@mandriva.org> 0.11.4-1mdv2009.1
+ Revision: 364052
- Update to 0.11.4 final

* Sun Mar 22 2009 Frederik Himpe <fhimpe@mandriva.org> 0.11.4-0.1mdv2009.1
+ Revision: 360259
- Update to version 0.11.4rc1 (fixes e-mail notification with
  Python 2.6)

* Mon Feb 16 2009 Michael Scherer <misc@mandriva.org> 0.11.3-1mdv2009.1
+ Revision: 340830
- update to new version 0.11.3

* Tue Feb 10 2009 Michael Scherer <misc@mandriva.org> 0.11.2.1-4mdv2009.1
+ Revision: 339032
- add a requires on python-setuptools, to fix 47649

* Thu Jan 08 2009 Jérôme Soyer <saispo@mandriva.org> 0.11.2.1-3mdv2009.1
+ Revision: 327068
- Rebuild for new python

* Thu Dec 25 2008 Olivier Thauvin <nanardon@mandriva.org> 0.11.2.1-2mdv2009.1
+ Revision: 318807
- rebuild for python

* Sat Nov 29 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 0.11.2.1-1mdv2009.1
+ Revision: 308073
- update to new version 0.11.2.1
- correct urls
- fix mixture of tabs and spaces
- spec file clean
- require python-pkg-resources for mdv version greater than 200900, instead of python-setuptools which requires bunch of useless python stuff and python-devel

* Sun Nov 09 2008 Frederik Himpe <fhimpe@mandriva.org> 0.11.2-1mdv2009.1
+ Revision: 301319
- update to new version 0.11.2

* Fri Aug 08 2008 Olivier Thauvin <nanardon@mandriva.org> 0.11.1-2mdv2009.0
+ Revision: 267459
- requires python-setuptools

* Thu Aug 07 2008 Frederik Himpe <fhimpe@mandriva.org> 0.11.1-1mdv2009.0
+ Revision: 266878
- update to new version 0.11.1

* Wed Aug 06 2008 Michael Scherer <misc@mandriva.org> 0.11-1mdv2009.0
+ Revision: 264211
- missing BuildRequires

  + Colin Guthrie <cguthrie@mandriva.org>
    - s/$RPM_BUILD_ROOT/%%{buildroot}/g
    - New version: 0.11
    - Drop old patch (merged upstream)

* Sat Feb 16 2008 Frederik Himpe <fhimpe@mandriva.org> 0.10.4-2mdv2008.1
+ Revision: 169358
- Add patch0: makes version control browser work when using
  PostgreSQL 8.3

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Thauvin <nanardon@mandriva.org>
    - postgresql module requires pyPgSQL

* Fri May 04 2007 Michael Scherer <misc@mandriva.org> 0.10.4-2mdv2008.0
+ Revision: 22397
- fix #30629
- make trac use sqlite2, close bug #30465

* Sun Apr 22 2007 Michael Scherer <misc@mandriva.org> 0.10.4-1mdv2008.0
+ Revision: 17003
- update to 0.10.4


* Thu Mar 08 2007 Michael Scherer <misc@mandriva.org> 0.10.3.1-1mdv2007.1
+ Revision: 138428
- upgrade to 0.10.3.1, security upgrade

* Wed Feb 14 2007 Michael Scherer <misc@mandriva.org> 0.10.3-3mdv2007.1
+ Revision: 120770
- fix backporting on 2007.0

* Mon Feb 12 2007 Michael Scherer <misc@mandriva.org> 0.10.3-2mdv2007.1
+ Revision: 120020
- fix trac-admin default templates, as reported by saispo on irc

* Mon Dec 18 2006 Michael Scherer <misc@mandriva.org> 0.10.3-1mdv2007.1
+ Revision: 98367
- use the proper release
- upgrade to version 0.10.3

* Tue Dec 12 2006 Michael Scherer <misc@mandriva.org> 0.10.2-2mdv2007.1
+ Revision: 95704
- Rebuild for python 2.5

* Mon Nov 13 2006 Michael Scherer <misc@mandriva.org> 0.10.2-1mdv2007.1
+ Revision: 83945
- 0.10.2 release ( bugfixes )

* Thu Nov 09 2006 Michael Scherer <misc@mandriva.org> 0.10.1-1mdv2007.0
+ Revision: 79194
- upgrade to 0.10.1

* Tue Oct 03 2006 Michael Scherer <misc@mandriva.org> 0.10-1mdv2007.1
+ Revision: 62825
- fix wizard for the new wizard interface and the new trac-admin
- revert changes in packaging, trac ido not work if some parts of it are missing
- fix for bug #23317, wizard interface have changed
- remove mime-types, leftover of previous bzipped patchs
- bunzip additional source files
- clean the comment, and some typo
- split wsgi from the main codebase, to not pull apache as a requires of a
  frontend, or use tracd ( activated by default, by policy ) for someone
  wanting to use wsgi.
- place svn in a separate package, in order to support other vcs in the future
- version 0.10, with splitted database backend
- Import trac

* Sun Jul 09 2006 Michael Scherer <misc@mandriva.org> 0.9.6-1mdv2007.0
- New release 0.9.6

* Wed Apr 19 2006 Michael Scherer <misc@mandriva.org> 0.9.5-1mdk
- New release 0.9.5

* Tue Mar 07 2006 Michael Scherer <misc@mandriva.org> 0.9.4-5mdk
- cgi_frontend.py is needed by standalone, so i place it back in main package

* Fri Mar 03 2006 Michael Scherer <misc@mandriva.org> 0.9.4-4mdk
- do not ship empty package as the upload script reject them

* Fri Mar 03 2006 Michael Scherer <misc@mandriva.org> 0.9.4-3mdk
- add fcgi sub package

* Wed Mar 01 2006 Michael Scherer <misc@mandriva.org> 0.9.4-2mdk
- add mod_python, pgsql and sqlite subpackage

* Thu Feb 16 2006 Michael Scherer <misc@mandriva.org> 0.9.4-1mdk
- New release 0.9.4

* Wed Jan 11 2006 Michael Scherer <misc@mandriva.org> 0.9.3-2mdk
- use new python macro

* Mon Jan 09 2006 Michael Scherer <misc@mandriva.org> 0.9.3-1mdk
- New release 0.9.3

* Mon Dec 05 2005 Michael Scherer <misc@mandriva.org> 0.9.2-1mdk
- New release 0.9.2

* Fri Nov 04 2005 Michael Scherer <misc@mandriva.org> 0.9-3mdk
- fix initscript

* Thu Nov 03 2005 Michael Scherer <misc@mandriva.org> 0.9-2mdk
- whoops, forget to change license

* Wed Nov 02 2005 Michael Scherer <misc@mandriva.org> 0.9-1mdk
- New release 0.9
- remove patch1, integrated upstream
- fix 19386 by supporting multiple $AUTH entries in /etc/sysconfig/trac

* Sun Oct 09 2005 Michael Scherer <misc@mandriva.org> 0.8.4-6mdk
- install subversion-tools instead of libfsfs_1_0 in the wizard, fix #19073

* Sun Sep 25 2005 Michael Scherer <misc@mandriva.org> 0.8.4-5mdk
- fix again ( python-svn => python-subversion )

* Sun Sep 25 2005 Michael Scherer <misc@mandriva.org> 0.8.4-4mdk
- fix deps with new subversion package

* Sat Sep 03 2005 Michael Scherer <misc@mandriva.org> 0.8.4-3mdk
- Fix #16298

* Sun Aug 14 2005 Michael Scherer <misc@mandriva.org> 0.8.4-2mdk
- fix location of the apache config file

* Tue Jun 21 2005 Michael Scherer <misc@mandriva.org> 0.8.4-1mdk
- New release 0.8.4

* Sat Jun 18 2005 Michael Scherer <misc@mandriva.org> 0.8.3-2mdk
- fix #16298

* Fri Jun 17 2005 Lenny Cartier <lenny@mandriva.com> 0.8.3-1mdk
- 0.8.3

* Sat Jun 04 2005 Michael Scherer <misc@mandriva.org> 0.8.2-1mdk
- New release 0.8.2

* Fri Mar 11 2005 Michael Scherer <misc@mandrake.org> 0.8.1-2mdk 
- add wizard
- add %%mkrel

* Fri Mar 04 2005 Lenny Cartier <lenny@mandrakesoft.com> 0.8.1-1mdk
- 0.8.1

* Sun Dec 05 2004 Michael Scherer <misc@mandrake.org> 0.8-2mdk
- Rebuild for new python

* Sun Nov 21 2004 Michael Scherer <misc@mandrake.org> 0.8-1mdk 
- New release 0.8
- split tracd and cgi support
- patch for tracd daemonisation

* Sat Jun 05 2004 Michael Scherer <misc@mandrake.org> 0.7.1-1mdk
- New release 0.7.1

* Thu May 20 2004 Michael Scherer <misc@mandrake.org> 0.7-1mdk
- New release 0.7
- update config files

* Thu Apr 15 2004 Michael Scherer <misc@mandrake.org> 0.6.1-2mdk 
- remove compiled config file, with wrong path inside

* Tue Apr 13 2004 Michael Scherer <misc@mandrake.org> 0.6.1-1mdk
- New release 0.6.1
- add support for rpmbuildupdate

* Sat Apr 03 2004 Michael Scherer <misc@mandrake.org> 0.6-1mdk
- First Mandrakesoft Package

