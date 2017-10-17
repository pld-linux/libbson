Summary:	Building, parsing, and iterating BSON documents
Name:		libbson
Version:	1.8.0
Release:	1
License:	ASL 2.0 and ISC and MIT and zlib
Group:		Libraries
Source0:	https://github.com/mongodb/libbson/releases/download/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	8b3c64570eec721f951831958e707a5a
# Do not install COPYING, install ChangeLog, distribution specific
Patch0:		%{name}-1.5.0-rc3-Install-documentation-according-to-guidelines.patch
URL:		https://github.com/mongodb/libbson
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	coreutils
BuildRequires:	libtool
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

%package devel
Summary:	Development files for %{name}
License:	Apache v2.0
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains libraries and header files needed for developing
applications that use %{name}.

%prep
%setup -q
%patch0 -p1

# Remove pregenerated documentation
rm -r doc/html/_static doc/html/*.{html,inv,js} doc/man/*.3

%build
%{__aclocal} -I build/autotools/m4
%{__libtoolize}
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
	--enable-tests

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

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libbson-1.0.la

# Install examples here because it's forbidden to use relative %%doc with
# installing into %%_pkgdocdir
install -d $RPM_BUILD_ROOT%{_docdir}/%{name}-devel/examples
install -t $RPM_BUILD_ROOT%{_docdir}/%{name}-devel/examples examples/*.c

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING THIRD_PARTY_NOTICES
# AUTHORS is empty, README etc. are installed by "make install"
%{_docdir}/%{name}
%attr(755,root,root) %{_libdir}/libbson-1.0.so.*.*.*
%ghost %{_libdir}/libbson-1.0.so.0

%files devel
%defattr(644,root,root,755)
%{_docdir}/%{name}-devel
%{_includedir}/libbson-1.0
%{_libdir}/libbson-1.0.so
%{_libdir}/cmake
%{_pkgconfigdir}/libbson-1.0.pc
%{_mandir}/man3/bson_*.3*
