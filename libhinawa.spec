#
# Conditional build:
%bcond_without	apidocs		# API documentation
#
Summary:	GObject introspection library for devices connected to IEEE 1394 bus
Summary(pl.UTF-8):	Biblioteka GObject introspection do urządzeń połączonych do szyny IEEE 1394
Name:		libhinawa
Version:	2.6.0
Release:	1
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://github.com/alsa-project/libhinawa/tags
Source0:	https://www.kernel.org/pub/linux/libs/ieee1394/%{name}-%{version}.tar.xz
# Source0-md5:	3cf6ba40750c7fd3a5640277ca356d7f
URL:		https://github.com/alsa-project/libhinawa
BuildRequires:	glib2-devel >= 1:2.44.0
BuildRequires:	gobject-introspection-devel >= 1.32.1
%{?with_apidocs:BuildRequires:	gi-docgen >= 2021.8}
BuildRequires:	meson >= 0.46.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	python3-pygobject3-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.44.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Hinawa is an GObject introspection library for devices connected to
IEEE 1394 bus. This library supports any types of transactions over
IEEE 1394 bus. This library also supports some functionality which
ALSA Firewire stack produces.

%description -l pl.UTF-8
Hinawa to biblioteka GObject introspection do urządzeń podłączonych do
szyny IEEE 1394. Obsługuje dowolne rodzaje transakcji po szynie IEEE
1394, a także część funkcjonalności zapewnianej przez stos Firewire
ALSA.

%package devel
Summary:	Header files for hinawa library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki hinawa
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.44.0

%description devel
Header files for hinawa library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki hinawa.

%package static
Summary:	Static hinawa library
Summary(pl.UTF-8):	Statyczna biblioteka hinawa
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static hinawa library.

%description static -l pl.UTF-8
Statyczna biblioteka hinawa.

%package apidocs
Summary:	API documentation for hinawa library
Summary(pl.UTF-8):	Dokumentacja API biblioteki hinawa
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for hinawa library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki hinawa.

%prep
%setup -q

%build
%meson build \
	%{?with_apidocs:-Ddoc=true}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%if %{with apidocs}
# FIXME: where to package gi-docgen generated docs?
install -d $RPM_BUILD_ROOT%{_gtkdocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/libhinawa $RPM_BUILD_ROOT%{_gtkdocdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.rst
%attr(755,root,root) %{_libdir}/libhinawa.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhinawa.so.2
%{_libdir}/girepository-1.0/Hinawa-3.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhinawa.so
%{_includedir}/libhinawa
%{_datadir}/gir-1.0/Hinawa-3.0.gir
%{_pkgconfigdir}/hinawa.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libhinawa.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libhinawa
%endif
