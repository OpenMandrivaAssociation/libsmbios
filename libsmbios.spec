%define lib_major 1
%define lib_name %mklibname smbios %{lib_major}

Name: libsmbios
Version: 0.13.6
Release: %mkrel 1
License: GPL/Open Software License
Group: System/Libraries
Source: http://linux.dell.com/libsmbios/download/%{name}/%{name}-%{version}/%{name}-%{version}.tar.bz2
URL: http://linux.dell.com/libsmbios/main
Summary: Open BIOS parsing libs
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root

# libsmbios only ever makes sense on intel compatible arches
# no DMI tables on ppc, s390, etc.
ExclusiveArch: x86_64 ia64 %{ix86}

BuildRequires: libxml2-devel
BuildRequires: cppunit-devel

%description
Libsmbios is a library and utilities that can be used by client programs 
to get information from standard BIOS tables, such as the SMBIOS table.

%package -n %{lib_name}
Summary: Libsmbios shared libraries
Group: System/Libraries

%description -n %{lib_name}
Libsmbios is a library and utilities that can be used by client programs 
to get information from standard BIOS tables, such as the SMBIOS table.


%package bin
Summary: The "supported" sample binaries that use libsmbios
Group: System/Configuration/Hardware

%description bin
Libsmbios is a library and utilities that can be used by client programs 
to get information from standard BIOS tables, such as the SMBIOS table.

This package contains some sample binaries that use libsmbios.


%package -n %{lib_name}-devel
Summary: Development headers and archives
Group: Development/C++
Requires: %{lib_name} = %{version}
Provides: %{name}-devel = %{version}-%{release}

%description -n %{lib_name}-devel
Libsmbios is a library and utilities that can be used by client programs 
to get information from standard BIOS tables, such as the SMBIOS table.

This package contains the headers and .a files necessary to compile new 
client programs against libsmbios


%prep
%setup -q

%build
%configure2_5x
%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std

mkdir -p %{buildroot}/%{_includedir}
cp -a include/smbios %{buildroot}/%{_includedir}
rm -f %{buildroot}/%{_libdir}/lib*.la

#remove unpackaged stuff 
rm -f %{buildroot}/%{_bindir}/{activateCmosToken,ascii2enUS_scancode,createUnitTestFiles,disable_console_redir,dumpCmos,getPasswordFormat,isCmosTokenActive,probes,smitest,stateByteCtl,upBootCtl,dumpSmbios}

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%post -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig

%files -n %{lib_name}
%defattr(-,root,root)
%doc COPYING-GPL COPYING-OSL README
%{_libdir}/libsmbios.so.%{lib_major}*
%{_libdir}/libsmbiosxml.so.%{lib_major}*

%files -n %{lib_name}-devel
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
