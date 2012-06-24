#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)
#
%define		_rel		4
%define		_ieeever	1.1.14
%define		_fwver		1.13
%define		_mod_suffix	current
Summary:	Intel(R) PRO/Wireless 3945 Driver for Linux
Summary(de):	Intel(R) PRO/Wireless 3945 Treiber f�r Linux
Summary(pl):	Sterownik dla Linuksa do kart Intel(R) PRO/Wireless 3945
Name:		ipw3945
Version:	1.1.0
Release:	%{_rel}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/ipw3945/%{name}-%{version}.tgz
# Source0-md5:	1f393d7a080879dba1a824dec251d71e
Source1:	%{name}-modprobe.conf
Patch0:		%{name}-bashizm.patch
Patch1:		%{name}-fix_undefined_symbols.patch
Patch2:		%{name}-config.patch
URL:		http://ipw3945.sourceforge.net/
BuildRequires:	ieee80211-devel >= %{_ieeever}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.330
BuildRequires:	sed >= 4.0
Requires:	ipw3945-firmware = %{_fwver}
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This project was created by Intel to enable support for the Intel
PRO/Wireless 3945 Network Connection mini PCI adapter.

%description -l de
Dieses Projekt wurde von Intel gestartet um die Wartung von mini PCI
Intel PRO/Wireless 3945 Netzwerk Karten zu erm�glichen.

%description -l pl
Ten projekt zosta� stworzony przez Intela, aby umo�liwi� obs�ug� kart
mini PCI Intel PRO/Wireless 3945 Network Connection.

%package -n kernel%{_alt_kernel}-net-%{name}
Summary:	Linux kernel module for the Intel(R) PRO/Wireless 3945
Summary(de):	Linux Kernel Modul f�r Intel(R) PRo/Wireless 3945 Netzwerk Karten
Summary(pl):	Modu� j�dra Linuksa dla kart Intel(R) PRO/Wireless 3945
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%(rpm -q --qf 'Requires: kernel%{_alt_kernel}-net-ieee80211 = %%{epoch}:%%{version}-%%{release}\n' ieee80211-devel | sed -e 's/ (none):/ /' | grep -v "is not")
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Requires:	module-init-tools >= 3.2.2-2
Provides:	%{name}

%description -n kernel%{_alt_kernel}-net-%{name}
This package contains Linux kernel drivers for the Intel(R)
PRO/Wireless 3945.

%description -n kernel%{_alt_kernel}-net-%{name} -l de
Dieses Paket enth�lt Linux Kernel Treiber f�r Intel(R) PRO/Wireless
3945 Netzwerk Karten.

%description -n kernel%{_alt_kernel}-net-%{name} -l pl
Ten pakiet zawiera sterowniki j�dra Linuksa dla kart Intel(R)
PRO/Wireless 3945.

%package -n kernel%{_alt_kernel}-smp-net-%{name}
Summary:	Linux SMP kernel module for the Intel(R) PRO/Wireless 3945
Summary(de):	Linux SMP Kernel Modul f�r Intel(R) PRO/Wireless 3945 Netzwerk Karten
Summary(pl):	Modu� j�dra Linuksa SMP dla kart Intel(R) PRO/Wireless 3945
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires:	ipw3945-firmware = %{_fwver}
%(rpm -q --qf 'Requires: kernel%{_alt_kernel}-smp-net-ieee80211 = %%{epoch}:%%{version}-%%{release}\n' ieee80211-devel | sed -e 's/ (none):/ /' | grep -v "is not")
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Requires:	module-init-tools >= 3.2.2-2
Provides:	%{name}

%description -n kernel%{_alt_kernel}-smp-net-%{name}
This package contains Linux SMP kernel drivers for the Intel(R)
PRO/Wireless 3945.

%description -n kernel%{_alt_kernel}-smp-net-%{name} -l de
Dieses Paket enth�lt Linux SMP Kernel Treiber f�r Intel(R)
PRO/Wireless 3945 Netzwerk Karten.

%description -n kernel%{_alt_kernel}-smp-net-%{name} -l pl
Ten pakiet zawiera sterowniki j�dra Linuksa SMP dla kart Intel(R)
PRO/Wireless 3945.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
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

%post	-n kernel%{_alt_kernel}-smp-net-%{name}
%depmod %{_kernel_ver}smp

%postun	-n kernel%{_alt_kernel}-smp-net-%{name}
%depmod %{_kernel_ver}smp

%files -n kernel%{_alt_kernel}-net-%{name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/ipw3945-%{_mod_siffix}.ko*
%{_sysconfdir}/modprobe.d/ipw3945.conf

%if %{with smp} && %{with dist_kernel}
%files -n kernel%{_alt_kernel}-smp-net-%{name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/ipw3945-%{_mod_suffix}.ko*
%{_sysconfdir}/modprobe.d/ipw3945.conf
%endif
