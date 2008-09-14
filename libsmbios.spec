%define major 2
%define libname %mklibname smbios %{major}
%define develname %mklibname smbios -d

Summary:	Open BIOS parsing libs
Name:		libsmbios
Version:	2.0.3
Release:	%mkrel 1
License:	GPLv2+ or OSL
Group:		System/Libraries
URL:		http://linux.dell.com/libsmbios/main
Source:		http://linux.dell.com/libsmbios/download/%{name}/%{name}-%{version}/%{name}-%{version}.tar.gz
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

%build
%configure2_5x
%make

%check
make check

%install
rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}/%{_includedir}
cp -a include/smbios %{buildroot}/%{_includedir}
rm -f %{buildroot}/%{_libdir}/lib*.la

# (tpg) looks like hal need this
ln -s %{_sbindir}/dellWirelessCtl %{buildroot}%{_bindir}/dellWirelessCtl

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
%doc COPYING-GPL COPYING-OSL README
%{_libdir}/*.so.%{major}*
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/smbios
%{_libdir}/*.a
%{_libdir}/*.so

%files utils
%defattr(-,root,root)
%doc bin-unsupported/getopts_LICENSE.txt
%{_sbindir}/activateCmosToken
%{_sbindir}/ascii2enUS_scancode
%{_sbindir}/assetTag
%{_sbindir}/createUnitTestFiles
%{_sbindir}/dellBiosUpdate
%{_sbindir}/dellLEDCtl
%{_sbindir}/dellLcdBrightness
%{_sbindir}/dellWirelessCtl
%{_sbindir}/disable_console_redir
%{_sbindir}/dumpCmos
%{_sbindir}/dumpSmbios
%{_sbindir}/getPasswordFormat
%{_sbindir}/getSystemId
%{_sbindir}/isCmosTokenActive
%{_sbindir}/mkbiospkg.sh
%{_sbindir}/probes
%{_sbindir}/propertyTag
%{_sbindir}/serviceTag
%{_sbindir}/smitest
%{_sbindir}/stateByteCtl
%{_sbindir}/upBootCtl
%{_sbindir}/verifySmiPassword
%{_sbindir}/wakeupCtl
%{_bindir}/dellWirelessCtl
