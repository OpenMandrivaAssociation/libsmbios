%define major 1
%define libname %mklibname smbios %{major}
%define develname %mklibname smbios -d

Name:       libsmbios
Version:    0.13.10
Release:    %mkrel 3
Summary:    Open BIOS parsing libs
License:    GPL/Open Software License
Group:      System/Libraries
URL:        http://linux.dell.com/libsmbios/main
Source:     http://linux.dell.com/libsmbios/download/%{name}/%{name}-%{version}/%{name}-%{version}.tar.gz
# libsmbios only ever makes sense on intel compatible arches
# no DMI tables on ppc, s390, etc.
ExclusiveArch: x86_64 ia64 %{ix86}
BuildRequires: libxml2-devel
BuildRequires: cppunit-devel
Buildroot:      %{_tmppath}/%{name}-%{version}

%description
Libsmbios is a library and utilities that can be used by client programs 
to get information from standard BIOS tables, such as the SMBIOS table.

%package -n %{libname}
Summary: Libsmbios shared libraries
Group: System/Libraries

%description -n %{libname}
Libsmbios is a library and utilities that can be used by client programs 
to get information from standard BIOS tables, such as the SMBIOS table.


%package bin
Summary: The "supported" sample binaries that use libsmbios
Group: System/Configuration/Hardware

%description bin
Libsmbios is a library and utilities that can be used by client programs 
to get information from standard BIOS tables, such as the SMBIOS table.

This package contains some sample binaries that use libsmbios.


%package -n %{develname}
Summary: Development headers and archives
Group: Development/C++
Requires: %{libname} = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}
Obsoletes: %{libname}-devel

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

%install
rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}/%{_includedir}
cp -a include/smbios %{buildroot}/%{_includedir}
rm -f %{buildroot}/%{_libdir}/lib*.la

#remove unpackaged stuff 
rm -f %{buildroot}/%{_bindir}/{activateCmosToken,ascii2enUS_scancode,createUnitTestFiles,disable_console_redir,dumpCmos,getPasswordFormat,isCmosTokenActive,probes,smitest,stateByteCtl,upBootCtl,dumpSmbios}

%clean
rm -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root)
%doc COPYING-GPL COPYING-OSL README
%{_libdir}/libsmbios.so.%{major}*
%{_libdir}/libsmbiosxml.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%doc COPYING-GPL COPYING-OSL README
/usr/include/smbios
%{_libdir}/*.a
%{_libdir}/*.so

%files bin 
%defattr(-,root,root)
%doc COPYING-GPL COPYING-OSL README bin-unsupported/getopts_LICENSE.txt
%{_bindir}/assetTag
%{_bindir}/dellBiosUpdate
%{_bindir}/getSystemId
%{_bindir}/propertyTag
%{_bindir}/serviceTag
%{_bindir}/tokenCtl
%{_bindir}/verifySmiPassword
%{_bindir}/wakeupCtl
%{_bindir}/dellLcdBrightness
%{_bindir}/dellLEDCtl
%{_bindir}/dellWirelessCtl
