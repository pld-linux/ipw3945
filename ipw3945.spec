#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)
#
%define		_rel		2	
%define		_ieeever	1.1.14
%define		_fwver		1.13

Summary:	Intel(R) PRO/Wireless 3945 Driver for Linux
Summary(de):	Intel(R) PRO/Wireless 3945 Treiber für Linux
Summary(pl):	Sterownik dla Linuksa do kart Intel(R) PRO/Wireless 3945
Name:		ipw3945
Version:	1.1.0
Release:	%{_rel}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tgz
# Source0-md5:	1f393d7a080879dba1a824dec251d71e
Patch0:		%{name}-bashizm.patch
Patch1:		%{name}-fix_undefined_symbols.patch
URL:		http://ipw3945.sourceforge.net/
BuildRequires:	ieee80211-devel >= %{_ieeever}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.308
BuildRequires:	sed >= 4.0
Requires:	ipw3945-firmware = %{_fwver}
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This project was created by Intel to enable support for the Intel
PRO/Wireless 3945 Network Connection mini PCI adapter.

%description -l de
Dieses Projekt wurde von Intel gestartet um die Wartung von mini PCI
Intel PRO/Wireless 3945 Netzwerk Karten zu ermöglichen.

%description -l pl
Ten projekt zosta³ stworzony przez Intela, aby umo¿liwiæ obs³ugê kart
mini PCI Intel PRO/Wireless 3945 Network Connection.

%package -n kernel%{_alt_kernel}-net-%{name}
Summary:	Linux kernel module for the Intel(R) PRO/Wireless 3945
Summary(de):	Linux Kernel Modul für Intel(R) PRo/Wireless 3945 Netzwerk Karten
Summary(pl):	Modu³ j±dra Linuksa dla kart Intel(R) PRO/Wireless 3945
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
Dieses Paket enthält Linux Kernel Treiber für Intel(R) PRO/Wireless
3945 Netzwerk Karten.

%description -n kernel%{_alt_kernel}-net-%{name} -l pl
Ten pakiet zawiera sterowniki j±dra Linuksa dla kart Intel(R)
PRO/Wireless 3945.

%package -n kernel%{_alt_kernel}-smp-net-%{name}
Summary:	Linux SMP kernel module for the Intel(R) PRO/Wireless 3945
Summary(de):	Linux SMP Kernel Modul für Intel(R) PRO/Wireless 3945 Netzwerk Karten
Summary(pl):	Modu³ j±dra Linuksa SMP dla kart Intel(R) PRO/Wireless 3945
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
Dieses Paket enthält Linux SMP Kernel Treiber für Intel(R)
PRO/Wireless 3945 Netzwerk Karten.

%description -n kernel%{_alt_kernel}-smp-net-%{name} -l pl
Ten pakiet zawiera sterowniki j±dra Linuksa SMP dla kart Intel(R)
PRO/Wireless 3945.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
# kernel module(s)
rm -rf built
mkdir -p built/{nondist,smp,up}
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	install -d o/include/linux
	ln -sf %{_kernelsrcdir}/config-$cfg o/.config
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h o/include/linux/autoconf.h
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg o/Module.symvers
%if %{with dist_kernel}
	%{__make} -C %{_kernelsrcdir} O=$PWD/o prepare scripts 
%else
	install -d o/include/config
	touch o/include/config/MARKER
	ln -sf %{_kernelsrcdir}/scripts o/scripts
%endif
	export IEEE80211_INC=%{_kernelsrcdir}/include
	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		SYSSRC=%{_kernelsrcdir} \
		SYSOUT=$PWD/o \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1} 
	%{__make} -C %{_kernelsrcdir} modules \
		CC="%{__cc}" CPP="%{__cpp}" \
		SYSSRC=%{_kernelsrcdir} \
		SYSOUT=$PWD/o \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}
	mv *.ko built/$cfg
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc \
	 $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/%{_kernel_ver}{,smp}

cd built
install %{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}/ipw3945.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/ipw3945_current.ko
echo "alias ipw3945 ipw3945_current
	install ipw3945 /sbin/modprobe --ignore-install ipw3945 ; sleep 0.5 ; \
        	/sbin/ipw3945d-$(uname -r) --quiet
	remove  ipw3945 /sbin/ipw3945d-$(uname -r) --kill ; \
        	/sbin/modprobe -r --ignore-remove ipw3945" \
	>> $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/%{_kernel_ver}/ipw3945.conf

%if %{with smp} && %{with dist_kernel}
install smp/ipw3945.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/ipw3945_current.ko
echo "alias ipw3945 ipw3945_current
	install ipw3945 /sbin/modprobe --ignore-install ipw3945 ; sleep 0.5 ; \
        	/sbin/ipw3945d --quiet
	remove  ipw3945 /sbin/ipw3945d --kill ; \
        	/sbin/modprobe -r --ignore-remove ipw3945
" \
	>> $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/%{_kernel_ver}smp/ipw3945.conf
%endif

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
/lib/modules/%{_kernel_ver}/misc/ipw3945*.ko*
%{_sysconfdir}/modprobe.d/%{_kernel_ver}/ipw3945.conf

%if %{with smp} && %{with dist_kernel}
%files -n kernel%{_alt_kernel}-smp-net-%{name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/ipw3945*.ko*
%{_sysconfdir}/modprobe.d/%{_kernel_ver}smp/ipw3945.conf
%endif
