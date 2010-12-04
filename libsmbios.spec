%define major 2
%define libname %mklibname smbios %{major}
%define develname %mklibname smbios -d

Summary:	Open BIOS parsing libs
Name:		libsmbios
Version:	2.2.26
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

%find_lang %{name} %{name}-2.2

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
