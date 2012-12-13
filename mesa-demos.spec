%define gitdate 20101028
%define tarball mesa-demos
%define xdriinfo xdriinfo-1.0.3

%define demodir %{_libdir}/mesa

Summary: Mesa demos
Name: mesa-demos
Version: 7.10
Release: 9.%{gitdate}%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.mesa3d.org

Source0: %{tarball}-%{gitdate}.tar.bz2
Source1: http://www.x.org/pub/individual/app/%{xdriinfo}.tar.bz2
Source2: mesad-git-snapshot.sh

BuildRequires: pkgconfig autoconf automake libtool
BuildRequires: freeglut-devel
BuildRequires: libGL-devel
BuildRequires: libGLU-devel
BuildRequires: glew-devel

Group: Development/Libraries

%description
This package provides some demo applications for testing Mesa.

%package -n glx-utils
Summary: GLX utilities
Group: Development/Libraries

%description -n glx-utils
The glx-utils package provides the glxinfo and glxgears utilities.

%prep
%setup -q -n %{tarball}-%{gitdate} -b1

# Hack the demos to use installed data files

sed -i 's,../images,%{_libdir}/mesa,' src/demos/*.c
sed -i 's,geartrain.dat,%{_libdir}/mesa/&,' src/demos/geartrain.c
sed -i 's,isosurf.dat,%{_libdir}/mesa/&,' src/demos/isosurf.c
sed -i 's,terrain.dat,%{_libdir}/mesa/&,' src/demos/terrain.c

%build
autoreconf -i
%configure --bindir=%{demodir}
make %{?_smp_mflags}

pushd ../%{xdriinfo}
%configure
make %{?_smp_mflags}
popd

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
install -m 0644 src/images/*.rgb $RPM_BUILD_ROOT/%{demodir}
install -m 0644 src/images/*.rgba $RPM_BUILD_ROOT/%{demodir}
install -m 0644 src/demos/*.dat $RPM_BUILD_ROOT/%{demodir}

pushd ../%{xdriinfo}
make %{?_smp_mflags} install DESTDIR=$RPM_BUILD_ROOT
popd

install -m 0755 src/xdemos/glxgears $RPM_BUILD_ROOT%{_bindir}
install -m 0755 src/xdemos/glxinfo $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%check

%files
%defattr(-,root,root,-)
%{demodir}

%files -n glx-utils
%defattr(-,root,root,-)
%{_bindir}/glxinfo
%{_bindir}/glxgears
%{_bindir}/xdriinfo
%{_datadir}/man/man1/xdriinfo.1*

%changelog
* Thu Dec 13 2012 Adam Jackson <ajax@redhat.com> - 7.10-9.20101028
- Rebuild for glew 1.9.0

* Fri Jul 27 2012 Kalev Lember <kalevlember@gmail.com> - 7.10-8.20101028
- Rebuilt for GLEW soname bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.10-7.20101028
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.10-6.20101028
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 ajax@redhat.com - 7.10-5.20101028
- Rebuild for new glew soname

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.10-4.20101028
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 01 2010 Adam Jackson <ajax@redhat.com> 7.10-3.20101028
- Install rgba images too (#640688)

* Sat Oct 30 2010 Dave Airlie <airlied@redhat.com> 7.10-2.20101028
- fix install of gears/info (#647947)

* Thu Oct 28 2010 Adam Jackson <ajax@redhat.com> 7.10-1.20101028
- Today's git snapshot
- Arbitrary EVR bump to be newer than when the mesa source package dropped
  the demos subpackage.

* Tue Jun 15 2010 Jerome Glisse <jglisse@redhat.com> 7.7
- Initial build.
