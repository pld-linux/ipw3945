#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_with	verbose		# verbose build (V=1)
#
%define		_rel		23
%define		_fwver		1.14.2
%define		_mod_suffix	current
%define		pname	ipw3945
Summary:	Intel(R) PRO/Wireless 3945 Driver for Linux
Summary(de.UTF-8):	Intel(R) PRO/Wireless 3945 Treiber für Linux
Summary(pl.UTF-8):	Sterownik dla Linuksa do kart Intel(R) PRO/Wireless 3945
Name:		%{pname}%{_alt_kernel}
Version:	1.2.2
Release:	%{_rel}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/ipw3945/%{pname}-%{version}.tgz
# Source0-md5:	9e5ca2f3ffbb84270ede45d5572df4c9
Source1:	%{pname}-modprobe.conf
Patch0:		%{pname}-bashizm.patch
Patch1:		%{pname}-config.patch
Patch2:		%{pname}-build.patch
Patch3:		%{pname}-kernel-2.6.24.patch
URL:		http://ipw3945.sourceforge.net/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.22}
BuildRequires:	rpmbuild(macros) >= 1.379
BuildRequires:	sed >= 4.0
Requires:	ipw3945-firmware = %{_fwver}
Requires:	ipw3945d
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This project was created by Intel to enable support for the Intel
PRO/Wireless 3945 Network Connection mini PCI adapter.

Warning: this driver is obsolete - try using iwl3945 instead.

%description -l de.UTF-8
Dieses Projekt wurde von Intel gestartet um die Wartung von mini PCI
Intel PRO/Wireless 3945 Netzwerkkarten zu ermöglichen.

%description -l pl.UTF-8
Ten projekt został stworzony przez Intela, aby umożliwić obsługę kart
mini PCI Intel PRO/Wireless 3945 Network Connection.

Uwaga: ten sterownik jest przestarzały, lepiej używać iwl3945.

%package -n kernel%{_alt_kernel}-net-%{name}
Summary:	Linux kernel module for the Intel(R) PRO/Wireless 3945
Summary(de.UTF-8):	Linux Kernel Modul für Intel(R) PRo/Wireless 3945 Netzwerkkarten
Summary(pl.UTF-8):	Moduł jądra Linuksa dla kart Intel(R) PRO/Wireless 3945
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel}
Requires(post,postun):	/sbin/depmod
Requires:	module-init-tools >= 3.2.2-2
Provides:	%{name}

%description -n kernel%{_alt_kernel}-net-%{name}
This package contains Linux kernel drivers for the Intel(R)
PRO/Wireless 3945.

Warning: this driver is obsolete - try using iwl3945 instead.

%description -n kernel%{_alt_kernel}-net-%{name} -l de.UTF-8
Dieses Paket enthält Linux Kernel Treiber für Intel(R) PRO/Wireless
3945 Netzwerkkarten.

%description -n kernel%{_alt_kernel}-net-%{name} -l pl.UTF-8
Ten pakiet zawiera sterowniki jądra Linuksa dla kart Intel(R)
PRO/Wireless 3945.

Uwaga: ten sterownik jest przestarzały, lepiej używać iwl3945.

%prep
%setup -q -n %{pname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
export IEEE80211_INC="%{_kernelsrcdir}"
%build_kernel_modules -m ipw3945

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -s %{_mod_suffix} -n %{name} -m ipw3945 -d misc

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-net-%{name}
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-net-%{name}
%depmod %{_kernel_ver}

%if %{with dist_kernel}
%files -n kernel%{_alt_kernel}-net-%{name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/ipw3945-%{_mod_suffix}.ko*
%{_sysconfdir}/modprobe.d/%{_kernel_ver}/ipw3945%{_alt_kernel}.conf
%endif
