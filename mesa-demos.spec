%define gitdate 20100615
%define tarball mesa-demos
%define xdriinfo xdriinfo-1.0.3

%define demodir %{_libdir}/mesa

Summary: Mesa demos
Name: mesa-demos
Version: 1.0
Release: 1%{gitdate}
License: MIT
Group: System Environment/Libraries
URL: http://www.mesa3d.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0: %{tarball}-%{gitdate}.tar.bz2
Source1: http://www.x.org/pub/individual/app/%{xdriinfo}.tar.bz2
Source2: mesad-git-snapshot.sh

BuildRequires: pkgconfig autoconf automake
BuildRequires: freeglut-devel
BuildRequires: elfutils
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
install -m 0644 src/demos/*.dat $RPM_BUILD_ROOT/%{demodir}

pushd ../%{xdriinfo}
make %{?_smp_mflags} install DESTDIR=$RPM_BUILD_ROOT
popd

%clean
rm -rf $RPM_BUILD_ROOT

%check

%files
%defattr(-,root,root,-)
%{demodir}

%files -n glx-utils
%defattr(-,root,root,-)
%{demodir}/glxgears
%{demodir}/glxinfo
%{_bindir}/xdriinfo
%{_datadir}/man/man1/xdriinfo.1*

%changelog
* Tue Jun 15 2010 Jerome Glisse <jglisse@redhat.com> 7.7
- Initial build.
