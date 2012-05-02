%define _disable_ld_no_undefined 1

%define modname optimizer
%define soname %{modname}.so
%define inifile 99_%{modname}.ini

Summary:	PHP optimizer extension for APC
Name:		php-%{modname}
Version:	0.1
Release:	%mkrel 0.alpha2.18
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

