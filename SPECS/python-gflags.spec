%global srcname gflags

%if 0%{?fedora} || 0%{?rhel} > 7
%global with_python3 1
%endif

%if 0%{?rhel} > 7
# Disable python2 build by default
%bcond_with python2
%else
%bcond_without python2
%endif

Name:           python-%{srcname}
Version:        2.0
Release:        13%{?dist}
Summary:        Commandline flags module for Python

Group:          Development/Languages
License:        BSD
URL:            https://github.com/gflags/python-gflags
Source0:        https://github.com/gflags/python-gflags/archive/python-gflags-%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch

%description
This project is the python equivalent of google-gflags, a Google commandline
flag implementation for C++. It is intended to be used in situations where a
project wants to mimic the command-line flag handling of a C++ app that uses
google-gflags, or for a Python app that, via swig or some other means, is
linked with a C++ app that uses google-gflags.

The gflags package contains a library that implements commandline flags
processing. As such it's a replacement for getopt(). It has increased
flexibility, including built-in support for Python types, and the ability to
define flags in the source file in which they're used. (This last is its major
difference from OptParse.)

%if %{with python2}
%package -n python2-%{srcname}
Summary:        Commandline flags module for Python 2
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
This project is the python equivalent of google-gflags, a Google commandline
flag implementation for C++. It is intended to be used in situations where a
project wants to mimic the command-line flag handling of a C++ app that uses
google-gflags, or for a Python app that, via swig or some other means, is
linked with a C++ app that uses google-gflags.

The gflags package contains a library that implements commandline flags
processing. As such it's a replacement for getopt(). It has increased
flexibility, including built-in support for Python types, and the ability to
define flags in the source file in which they're used. (This last is its major
difference from OptParse.)
%endif # with python2

%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:        Commandline flags module for Python 3
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-tools
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
This project is the python equivalent of google-gflags, a Google commandline
flag implementation for C++. It is intended to be used in situations where a
project wants to mimic the command-line flag handling of a C++ app that uses
google-gflags, or for a Python app that, via swig or some other means, is
linked with a C++ app that uses google-gflags.

The gflags package contains a library that implements commandline flags
processing. As such it's a replacement for getopt(). It has increased
flexibility, including built-in support for Python types, and the ability to
define flags in the source file in which they're used. (This last is its major
difference from OptParse.)
%endif


%prep
%setup -qc
%if %{with python2}
cp -a %{name}-%{version} python2
sed -i '1s|^#!/usr/bin/env python$|#!%{__python2}|' python2/gflags2man.py
sed -i '/^#!\/usr\/bin\/env python$/,+1 d' python2/gflags*.py
%endif # with python2
%if 0%{?with_python3}
cp -a %{name}-%{version} python3
pathfix.py -i %{__python3} -pn python3/*.py \
python3/tests/*py
2to3 --write --nobackup python3
%endif


%build
%if %{with python2}
pushd python2
%py2_build
popd
%endif # with python2
%if 0%{?with_python3}
pushd python3
%py3_build
popd
%endif


%install
%if 0%{?with_python3}
pushd python3
%py3_install
%if %{without python2}
mv %{buildroot}%{_bindir}/gflags2man.py  %{buildroot}%{_bindir}/gflags2man
chmod +x %{buildroot}%{_bindir}/gflags2man
%else
mv %{buildroot}%{_bindir}/gflags2man.py  %{buildroot}%{_bindir}/gflags2man-3
chmod +x %{buildroot}%{_bindir}/gflags2man-3
%endif
popd
%endif

%if %{with python2}
pushd python2
%py2_install
mv %{buildroot}%{_bindir}/gflags2man.py  %{buildroot}%{_bindir}/gflags2man
chmod +x %{buildroot}%{_bindir}/gflags2man
popd
%endif # with python2


%check
%if %{with python2}
pushd python2
%{__python2} setup.py test
popd
%endif # with python2

%if 0%{?with_python3}
pushd python3
%{__python3} setup.py test
popd
%endif

%if %{with python2}
%files -n python2-%{srcname}
%license python2/COPYING
%doc python2/AUTHORS python2/ChangeLog python2/COPYING python2/README
%{python2_sitelib}/%{srcname}.py*
%{python2_sitelib}/%{srcname}_validators.py*
%{python2_sitelib}/python_gflags-%{version}-*egg-info
%{_bindir}/gflags2man
%endif # with python2

%if 0%{?with_python3}
%files -n python3-%{srcname}
%license python3/COPYING
%doc python3/AUTHORS python3/ChangeLog python3/COPYING python3/README
%{python3_sitelib}/%{srcname}.py*
%{python3_sitelib}/%{srcname}_validators.py*
%{python3_sitelib}/python_gflags-%{version}-*egg-info
%{python3_sitelib}/__pycache__/*
%if %{without python2}
%{_bindir}/gflags2man
%else
%{_bindir}/gflags2man-3
%endif
%endif


%changelog
* Thu Jun 14 2018 Charalampos Stratakis <cstratak@redhat.com> - 2.0-13
- Conditionalize the python2 subpackage

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 2.0-11
- Cleanup spec file conditionals

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.0-8
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-7
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 18 2015 Orion Poplawski <orion@cora.nwra.com> - 2.0-5
- Update spec, make python3 package optional for EPEL7

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr 6 2015 Orion Poplawski <orion@cora.nwra.com> - 2.0-2
- Create python3 package (bug #1209201)

* Mon Apr 6 2015 Orion Poplawski <orion@cora.nwra.com> - 2.0-1
- Update to 2.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jul 24 2011 Silas Sewell <silas@sewell.org> - 1.5.1-1
- Update to 1.5.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 26 2010 Silas Sewell <silas@sewell.ch> - 1.4-2
- Fix non-executable-script error

* Wed Oct 13 2010 Silas Sewell <silas@sewell.ch> - 1.4-1
- Initial package
