%define major 2
%define libname %mklibname smbios %{major}
%define libsmbios_c %mklibname smbios_c %{major}
%define devname %mklibname smbios -d

Summary:	Open BIOS parsing libs

Name:		libsmbios
Version:	2.2.28
Release:	5
License:	GPLv2+ or OSL
Group:		System/Libraries
Url:		http://linux.dell.com/libsmbios/main
Source0:	http://linux.dell.com/libsmbios/download/%{name}/%{name}-%{version}/%{name}-%{version}.tar.bz2
# libsmbios only ever makes sense on intel compatible arches
# no DMI tables on ppc, s390, etc.
ExclusiveArch:	x86_64 ia64 %{ix86}
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	pkgconfig(cppunit)
BuildRequires:	pkgconfig(libxml-2.0)

%description
Libsmbios is a library and utilities that can be used by client programs 
to get information from standard BIOS tables, such as the SMBIOS table.

%package -n %{libname}
Summary:	Libsmbios shared libraries

Group:		System/Libraries

%description -n %{libname}
Libsmbios is a library and utilities that can be used by client programs 
to get information from standard BIOS tables, such as the SMBIOS table.

%package -n %{libsmbios_c}
Summary:	Libsmbios shared libraries

Group:		System/Libraries
Conflicts:	%{_lib}smbios2 < 2.2.28-2

%description -n %{libsmbios_c}
Libsmbios is a library and utilities that can be used by client programs 
to get information from standard BIOS tables, such as the SMBIOS table.

%package utils
Summary:	The "supported" sample binaries that use libsmbios

Group:		System/Configuration/Hardware
Provides:	%{name}-bin = %{version}-%{release}
BuildRequires:  python-devel

%description utils
Libsmbios is a library and utilities that can be used by client programs 
to get information from standard BIOS tables, such as the SMBIOS table.

This package contains some sample binaries that use libsmbios.

%package -n %{devname}
Summary:	Development headers and archives

Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libsmbios_c} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains the development files necessary to compile new 
client programs against libsmbios.

%prep
%setup -q

#fix tests
find src/ -name *.py -exec sed -i -e 's|python2|python|g' {} \;

sed -i -e 's#-Werror ##' Makefile.*

%build
%configure2_5x \
#	--disable-static
%make

%check
%make check

%install
%makeinstall_std

mkdir -p %{buildroot}/%{_includedir}
cp -a src/include/smbios %{buildroot}/%{_includedir}
cp -a src/include/smbios_c %{buildroot}/%{_includedir}

# (tpg) looks like hal need this
ln -s %{_sbindir}/dellWirelessCtl %{buildroot}%{_bindir}/dellWirelessCtl

# (tpg) wtf is yum ? ;)
rm -rf %{buildroot}%{_prefix}/lib/yum-plugins
rm -rf %{buildroot}%{_sysconfdir}/yum
rm -rf %{buildroot}%{_libdir}/*.a

%find_lang %{name}

%files -n %{libname}
%{_libdir}/libsmbios.so.%{major}*

%files -n %{libsmbios_c}
%{_libdir}/libsmbios_c.so.%{major}*

%files -n %{devname}
%{_includedir}/smbios*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libsmbios*.pc

%files utils -f %{name}.lang
%doc AUTHORS README TODO ChangeLog doc/*
%config(noreplace) %{_sysconfdir}/%{name}/*.conf
%{_sbindir}/*
%{_bindir}/*
%{_datadir}/smbios-utils
%{py_puresitedir}/%{name}_c

