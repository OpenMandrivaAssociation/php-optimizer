%define _disable_ld_no_undefined 1

%define modname optimizer
%define soname %{modname}.so
%define inifile 99_%{modname}.ini

Summary:	PHP optimizer extension for APC
Name:		php-%{modname}
Version:	0.1
Release:	%mkrel 0.alpha2.16
Group:		Development/PHP
License:	BSD-Style
URL:		http://pecl.php.net/package/%{modname}
#Source0:	http://pecl.php.net/get/%{modname}-%{version}alpha1.tgz
# cvs -d :pserver:cvsread@cvs.php.net:/repository checkout pecl/optimizer optimizer
Source0:	%{modname}.tar.gz
Source1:	optimizer.ini
Patch0:		optimizer-no_egg.diff
BuildRequires:  php-devel >= 3:5.2.0
Requires:	php-vld
Requires:	php-apc
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
An opcode optimizer for PHP to be used with the APC opcode cache.

%prep

%setup -q -n %{modname}
#[ "../package*.xml" != "/" ] && mv ../package*.xml .

find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

%patch0 -p1

cp %{SOURCE1} %{inifile}

%build
%serverbuild

phpize

mkdir -p build-optimizer
pushd build-optimizer
ln -s ../configure .
%configure2_5x \
    --enable-%{modname}=shared,%{_prefix}

%make
popd

mkdir -p build-optimizer-debug
pushd build-optimizer-debug
ln -s ../configure .
export OPTIMIZER_DEBUG_COMPILE="1"
export OPTIMIZER_STATS_COMPILE="1"

%configure2_5x \
    --enable-%{modname}=shared,%{_prefix}

%make
popd

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/%{inifile}

install -m0755 build-optimizer/modules/optimizer.so %{buildroot}%{_libdir}/php/extensions/optimizer.so
install -m0755 build-optimizer-debug/modules/optimizer.so %{buildroot}%{_libdir}/php/extensions/optimizer-debug.so

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README package*.xml
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/optimizer.so
%attr(0755,root,root) %{_libdir}/php/extensions/optimizer-debug.so



%changelog
* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1-0.alpha2.16mdv2011.0
+ Revision: 696371
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1-0.alpha2.15
+ Revision: 695315
- rebuilt for php-5.3.7

* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1-0.alpha2.14
+ Revision: 667482
- mass rebuild

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1-0.alpha2.13
+ Revision: 646555
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1-0.alpha2.12mdv2011.0
+ Revision: 629741
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0.1-0.alpha2.11mdv2011.0
+ Revision: 628047
- ensure it's built without automake1.7

* Tue Nov 23 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1-0.alpha2.10mdv2011.0
+ Revision: 600179
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1-0.alpha2.9mdv2011.0
+ Revision: 588716
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1-0.alpha2.8mdv2010.1
+ Revision: 514588
- rebuilt for php-5.3.2

* Mon Feb 22 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1-0.alpha2.7mdv2010.1
+ Revision: 509469
- rebuild
- rebuild

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 0.1-0.alpha2.5mdv2010.1
+ Revision: 485262
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1-0.alpha2.4mdv2010.1
+ Revision: 468089
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1-0.alpha2.3mdv2010.0
+ Revision: 451219
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 0.1-0.alpha2.2mdv2010.0
+ Revision: 397306
- Rebuild

* Wed May 13 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1-0.alpha2.1mdv2010.0
+ Revision: 375444
- use a recent cvs snapshot, but call it "alpha2" for now
- rediffed P0
- rebuilt against php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1-0.alpha1.5mdv2009.1
+ Revision: 346524
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 0.1-0.alpha1.4mdv2009.1
+ Revision: 341512
- rebuilt against php-5.2.9RC2

* Wed Dec 31 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1-0.alpha1.3mdv2009.1
+ Revision: 321794
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1-0.alpha1.2mdv2009.1
+ Revision: 310221
- rebuilt against php-5.2.7

* Thu Aug 07 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1-0.alpha1.1mdv2009.0
+ Revision: 266242
- import php-optimizer


* Thu Aug 07 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1-0.alpha1.1mdv2009.0
- initial Mandriva package
