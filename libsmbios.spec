%define major 2
%define libname %mklibname smbios %{major}
%define libsmbios_c %mklibname smbios_c %{major}
%define devname %mklibname smbios -d

%define _disable_rebuild_configure 1

Summary:	Open BIOS parsing libs

Name:		libsmbios
Version:	2.4.2
Release:	1
License:	GPLv2+ or OSL
Group:		System/Libraries
Url:		https://github.com/dell/libsmbios
Source0:	https://github.com/dell/libsmbios/archive/v%{version}.tar.gz
Patch0:		https://src.fedoraproject.org/rpms/libsmbios/raw/master/f/0001-libsmbios-fix-more-places-with-loop-iterators-with-b.patch
# libsmbios only ever makes sense on intel compatible arches
# no DMI tables on ppc, s390, etc.
ExclusiveArch:	%{x86_64} ia64 %{ix86}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	pkgconfig(cppunit)
BuildRequires:	pkgconfig(libxml-2.0)

%description
Libsmbios is a library and utilities that can be used by client programs 
to get information from standard BIOS tables, such as the SMBIOS table.

%package -n %{libsmbios_c}
Summary:	Libsmbios shared libraries
Group:		System/Libraries
Conflicts:	%{_lib}smbios2 < 2.2.28-2
Obsoletes:	%{libname}

%description -n %{libsmbios_c}
Libsmbios is a library and utilities that can be used by client programs 
to get information from standard BIOS tables, such as the SMBIOS table.

%package utils
Summary:	The "supported" sample binaries that use libsmbios
Group:		System/Configuration/Hardware
Provides:	%{name}-bin = %{version}-%{release}
BuildRequires:	pkgconfig(python)

%description utils
Libsmbios is a library and utilities that can be used by client programs 
to get information from standard BIOS tables, such as the SMBIOS table.

This package contains some sample binaries that use libsmbios.

%package -n %{devname}
Summary:	Development headers and archives
Group:		Development/C++
Requires:	%{libsmbios_c} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains the development files necessary to compile new 
client programs against libsmbios.

%prep
%autosetup -p1
sed -i -e 's,lzma,xz,g' configure.ac
[ -e autogen.sh ] && ./autogen.sh

#fix tests
find src/ -name *.py -exec sed -i -e 's|python2|python|g' {} \;

sed -i -e 's#-Werror ##' Makefile.*

%build
%configure
%make_build

#check
#make check

%install
%make_install
%find_lang %{name}

%files -n %{libsmbios_c}
%{_libdir}/libsmbios_c.so.%{major}*

%files -n %{devname}
%{_includedir}/smbios*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libsmbios*.pc

%files utils -f %{name}.lang
%doc doc/*
%config(noreplace) %{_sysconfdir}/%{name}/*.conf
%{_sbindir}/*
%{_datadir}/smbios-utils
%{py3_platsitedir}/%{name}_c
%{_mandir}/man1/*
