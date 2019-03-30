Summary:	Building, parsing, and iterating BSON documents
Summary(pl.UTF-8):	Tworzenie, analiza i przechodzenie dokumentów BSON
Name:		libbson
Version:	1.9.5
Release:	2
License:	Apache v2.0 and ISC and MIT and zlib
Group:		Libraries
#Source0Download: https://github.com/mongodb/libbson/releases/
Source0:	https://github.com/mongodb/libbson/releases/download/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	716127054644aec0cf751a2c0c7693b1
Patch0:		%{name}-1.5.0-rc3-Install-documentation-according-to-guidelines.patch
Patch1:		sphinx-no-fatal-warn.patch
URL:		https://github.com/mongodb/libbson
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
BuildRequires:	gcc >= 6:4.1
BuildRequires:	libtool >= 2:2.2
BuildRequires:	pkgconfig
BuildRequires:	sphinx-pdg
# Modified (with bson allocator and some warning fixes and huge indentation
# refactoring) jsonsl is bundled <https://github.com/mnunberg/jsonsl>.
# jsonsl upstream likes copylib approach and does not plan a release
# <https://github.com/mnunberg/jsonsl/issues/14>.
Provides:	bundled(jsonsl)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a library providing useful routines related to building,
parsing, and iterating BSON documents <http://bsonspec.org/>.

%description -l pl.UTF-8
Ta biblioteka udostępnia przydatne funkcje związane z budowaniem,
analizą i przechodzeniem dokumentów BSON (<http://bsonspec.org/>).

%package devel
Summary:	Development files for libbson
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libbson
License:	Apache v2.0
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files needed for developing
applications that use libbson.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących bibliotekę libbson.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

# Remove pregenerated documentation
%{__rm} -r doc/html/_static doc/html/*.{html,inv,js} doc/man/*.3

%build
%{__libtoolize}
%{__aclocal} -I build/autotools/m4
%{__autoconf}
%{__automake}
# Switching experimental-features support changes ABI (bson_visitor_t type)
%configure \
	--disable-coverage \
	--disable-debug \
	--disable-debug-symbols \
	--enable-examples \
	--enable-extra-align \
	--disable-html-docs \
	--enable-libtool-lock \
	--disable-lto \
	--disable-maintainer-flags \
	--enable-man-pages \
	--disable-optimizations \
	--enable-shared \
	--disable-silent-rules \
	--disable-static \
	%{?with_tests:--enable-tests}

# Explicit man target is needed for generating manual pages.
# If you produced HTML pages be ware doc/conf.py injects tracking JavaScript
# code (search for add_ga_javascript function).
%{__make} all doc/man

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libbson-1.0.la
# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_docdir}/libbson/{ChangeLog,NEWS,README}

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -p examples/*.c $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog NEWS README THIRD_PARTY_NOTICES
%attr(755,root,root) %{_libdir}/libbson-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbson-1.0.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbson-1.0.so
%{_includedir}/libbson-1.0
%{_pkgconfigdir}/libbson-1.0.pc
%{_libdir}/cmake/libbson-1.0
%{_mandir}/man3/bson_*.3*
%{_examplesdir}/%{name}-%{version}
