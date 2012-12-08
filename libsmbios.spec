%define major 2
%define libname %mklibname smbios %{major}
%define develname %mklibname smbios -d

Summary:	Open BIOS parsing libs
Name:		libsmbios
Version:	2.2.28
Release:	%mkrel 1
License:	GPLv2+ or OSL
Group:		System/Libraries
URL:		http://linux.dell.com/libsmbios/main
Source:		http://linux.dell.com/libsmbios/download/%{name}/%{name}-%{version}/%{name}-%{version}.tar.bz2
# libsmbios only ever makes sense on intel compatible arches
# no DMI tables on ppc, s390, etc.
ExclusiveArch:	x86_64 ia64 %{ix86}
BuildRequires:	libxml2-devel
BuildRequires:	cppunit-devel
BuildRequires:	doxygen
BuildRequires:	graphviz
Buildroot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Libsmbios is a library and utilities that can be used by client programs 
to get information from standard BIOS tables, such as the SMBIOS table.

%package -n %{libname}
Summary:	Libsmbios shared libraries
Group:		System/Libraries

%description -n %{libname}
Libsmbios is a library and utilities that can be used by client programs 
to get information from standard BIOS tables, such as the SMBIOS table.

%package utils
Summary:	The "supported" sample binaries that use libsmbios
Group:		System/Configuration/Hardware
Provides:	%{name}-bin = %{version}-%{release}
Obsoletes:	%{name}-bin < 2.0.2
%py_requires -d

%description utils
Libsmbios is a library and utilities that can be used by client programs 
to get information from standard BIOS tables, such as the SMBIOS table.

This package contains some sample binaries that use libsmbios.

%package -n %{develname}
Summary:	Development headers and archives
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname smbios 1 -d

%description -n %{develname}
Libsmbios is a library and utilities that can be used by client programs 
to get information from standard BIOS tables, such as the SMBIOS table.

This package contains the headers and .a files necessary to compile new 
client programs against libsmbios.

%prep
%setup -q

#fix tests
find src/ -name *.py -exec sed -i -e 's|python2|python|g' {} \;

sed -i -e 's#-Werror ##' Makefile.*

%build
%configure2_5x \
	    --disable-rpath
%make

%check
%make check

%install
rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}/%{_includedir}
cp -a src/include/smbios %{buildroot}/%{_includedir}
cp -a src/include/smbios_c %{buildroot}/%{_includedir}
rm -f %{buildroot}/%{_libdir}/lib*.la

# (tpg) looks like hal need this
ln -s %{_sbindir}/dellWirelessCtl %{buildroot}%{_bindir}/dellWirelessCtl

# (tpg) wtf is yum ? ;)
rm -rf %{buildroot}%{_prefix}/lib/yum-plugins
rm -rf %{buildroot}%{_sysconfdir}/yum

%find_lang %{name}

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/smbios*
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/libsmbios*.pc

%files utils -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS README TODO ChangeLog doc/*
%config(noreplace) %{_sysconfdir}/%{name}/*.conf
%{_sbindir}/*
%{_bindir}/*
%{_datadir}/smbios-utils
%{python_sitelib}/%{name}_c


%changelog
* Mon May 02 2011 Funda Wang <fwang@mandriva.org> 2.2.26-2mdv2011.0
+ Revision: 661760
- disable Werror

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Sat Dec 04 2010 Jani Välimaa <wally@mandriva.org> 2.2.26-1mdv2011.0
+ Revision: 609521
- new version 2.2.26

* Fri Jan 01 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 2.2.19-1mdv2011.0
+ Revision: 484670
- update to new version 2.2.19

* Tue May 26 2009 Christophe Fergeau <cfergeau@mandriva.com> 2.2.16-1mdv2010.0
+ Revision: 379926
- new upstream release

* Tue Feb 10 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 2.2.13-1mdv2009.1
+ Revision: 339287
- update to new version 2.2.13

* Tue Jan 20 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 2.2.9-1mdv2009.1
+ Revision: 331800
- fix file list
- update to new version 2.2.9

* Sat Dec 27 2008 Funda Wang <fwang@mandriva.org> 2.2.5-5mdv2009.1
+ Revision: 319685
- rebuild for new python

* Sun Dec 21 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2.2.5-4mdv2009.1
+ Revision: 317040
- bump tag for hungry bs
- fix last commit
- remove useless stuff also for x86_64
- use right macro
- fix file list
- now lot of utils are python based instead of C++ blobs
- update to new version 2.2.5
- kill rpath

* Sun Sep 14 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2.0.3-1mdv2009.0
+ Revision: 284773
- fix file list
- update to new version 2.0.3

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 2.0.2-2mdv2009.0
+ Revision: 264891
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Thu May 01 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2.0.2-1mdv2009.0
+ Revision: 199830
- update to the lastest upstream release
- add missing buildrequires on doxygen and graphviz
- rename libsmbios-bin to libsmbios-utils, as it looks more appropriate
- bump major
- new license policy
- add symlinks for hal
- enable checks
- spec file clean

* Tue Mar 04 2008 Oden Eriksson <oeriksson@mandriva.com> 0.13.10-3mdv2008.1
+ Revision: 178996
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Sep 03 2007 Guillaume Rousse <guillomovitch@mandriva.org> 0.13.10-1mdv2008.0
+ Revision: 78857
- new version

* Tue Jul 17 2007 Funda Wang <fwang@mandriva.org> 0.13.6-2mdv2008.0
+ Revision: 52938
- fix develpackage requires typo

* Tue Jul 17 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 0.13.6-1mdv2008.0
+ Revision: 52808
- new devel library policy
- spec file clean
- new version
- fix file list


* Thu Mar 08 2007 Frederic Crozat <fcrozat@mandriva.com> 0.13.2-1mdv2007.1
+ Revision: 136302
- Import libsmbios

