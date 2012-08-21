%define		tzdata_ver	2012e
%define		tzcode_ver	2012e

Summary:	Timezone data
Name:		tzdata
Version:	%{tzdata_ver}
Release:	1
License:	Public Domain (database), BSD/LGPL v2.1+ (code/test suite)
Group:		Base
Source0:	http://www.iana.org/time-zones/repository/releases/%{name}%{tzdata_ver}.tar.gz
# Source0-md5:	cb74e1f7bcc9a968a891a471e72e47b8
Source1:	http://www.iana.org/time-zones/repository/releases/tzcode%{tzcode_ver}.tar.gz
# Source1-md5:	cc56398842289807a80791f1f654181f
Source2:	timezone.service
Source3:	timezone.sysconfig
URL:		http://www.iana.org/time-zones
BuildRequires:	grep
BuildRequires:	glibc-misc
BuildArch:	noarch
Requires(post,preun,postun):	systemd-units
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains data files with rules for various timezones
around the world.

%prep
%setup -qc -a1

grep -v tz-art.htm tz-link.htm > tz-link.html

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/sysconfig,%{systemdunitdir}}

for tzone in \
    	africa antarctica asia australasia europe northamerica \
    	southamerica pacificnew etcetera backward systemv factory \
	solar87 solar88 solar89; do
	/usr/sbin/zic -y ./yearistype -d $RPM_BUILD_ROOT%{_datadir}/zoneinfo $tzone
done
/usr/sbin/zic -y ./yearistype -d $RPM_BUILD_ROOT%{_datadir}/zoneinfo -p America/New_York

install iso3166.tab zone.tab $RPM_BUILD_ROOT%{_datadir}/zoneinfo

install %{SOURCE2} $RPM_BUILD_ROOT%{systemdunitdir}/timezone.service
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/timezone

# behave more like glibc.spec
ln -sf %{_sysconfdir}/localtime	$RPM_BUILD_ROOT%{_datadir}/zoneinfo/localtime
ln -sf localtime $RPM_BUILD_ROOT%{_datadir}/zoneinfo/posixtime
ln -sf localtime $RPM_BUILD_ROOT%{_datadir}/zoneinfo/posixrules

> $RPM_BUILD_ROOT/etc/localtime

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post timezone.service

%preun
%systemd_preun timezone.service

%postun
%systemd_reload

%files
%defattr(644,root,root,755)
%doc README Theory tz-link.html
%ghost /etc/localtime
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/timezone
%{systemdunitdir}/timezone.service
%{_datadir}/zoneinfo

