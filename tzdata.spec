%define		tzdata_ver	2012f
%define		tzcode_ver	2012f

Summary:	Timezone data
Name:		tzdata
Version:	%{tzdata_ver}
Release:	1
License:	Public Domain (database), BSD/LGPL v2.1+ (code/test suite)
Group:		Base
Source0:	http://www.iana.org/time-zones/repository/releases/%{name}%{tzdata_ver}.tar.gz
# Source0-md5:	944ad681a8623336230dcdb306d5c9f6
Source1:	http://www.iana.org/time-zones/repository/releases/tzcode%{tzcode_ver}.tar.gz
# Source1-md5:	edc0b55c4afbad7249ccacb3503e7f10
URL:		http://www.iana.org/time-zones
BuildRequires:	grep
BuildRequires:	glibc-misc
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains data files with rules for various timezones
around the world.

%prep
%setup -qc -a1

grep -v tz-art.htm tz-link.htm > tz-link.html

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/sysconfig,%{systemdunitdir},/usr/lib/systemd}

for tzone in \
    	africa antarctica asia australasia europe northamerica \
    	southamerica pacificnew etcetera backward systemv factory \
	solar87 solar88 solar89; do
	/usr/sbin/zic -y ./yearistype -d $RPM_BUILD_ROOT%{_datadir}/zoneinfo $tzone
done
/usr/sbin/zic -y ./yearistype -d $RPM_BUILD_ROOT%{_datadir}/zoneinfo -p America/New_York

install iso3166.tab zone.tab $RPM_BUILD_ROOT%{_datadir}/zoneinfo

# glibc.spec compat
ln -sf %{_sysconfdir}/localtime	$RPM_BUILD_ROOT%{_datadir}/zoneinfo/localtime
ln -sf localtime $RPM_BUILD_ROOT%{_datadir}/zoneinfo/posixtime
ln -sf localtime $RPM_BUILD_ROOT%{_datadir}/zoneinfo/posixrules

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README Theory tz-link.html
%{_datadir}/zoneinfo

