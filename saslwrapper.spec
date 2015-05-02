#
# Conditional build:
%bcond_without	tests		# build without tests
%bcond_without	ruby		# Ruby binding
%bcond_without	python		# Python binding

Summary:	Ruby and Python wrappers for the Cyrus SASL library
Name:		saslwrapper
Version:	0.16
Release:	2
License:	Apache v2.0
Group:		Libraries
# svn export -r 1346225 https://svn.apache.org/repos/asf/qpid/tags/0.16/qpid/extras/sasl saslwrapper-0.16
# tar -cJf saslwrapper-0.16.tar.xz saslwrapper-0.16
Source0:	http://pkgs.fedoraproject.org/repo/pkgs/saslwrapper/%{name}-%{version}.tar.xz/e801d697a196647938eb1521be414090/saslwrapper-%{version}.tar.xz
# Source0-md5:	e801d697a196647938eb1521be414090
URL:		http://qpid.apache.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cyrus-sasl-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.665
BuildRequires:	swig
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%if %{with python}
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	swig-python
# ./configure checks for these, even though it probably needn't
BuildRequires:	/usr/bin/python
%endif
%if %{with ruby}
BuildRequires:	rpm-rubyprov
BuildRequires:	ruby-devel
BuildRequires:	swig-ruby
# ./configure checks for these, even though it probably needn't
BuildRequires:	/usr/bin/ruby
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# Unresolved symbols found: sasl_*
%define		skip_post_check_so	libsaslwrapper.so.1.0.0

%description
A simple wrapper for Cyrus SASL that permits easy binding into
scripting languages.

%package devel
Summary:	Header files for developing with saslwrapper
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The header files for developing with saslwrapper.

%package -n python-saslwrapper
Summary:	Python bindings for saslwrapper
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description -n python-saslwrapper
Python bindings for the saslwrapper library.

%package -n ruby-saslwrapper
Summary:	Ruby bindings for saslwrapper
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description -n ruby-saslwrapper
Ruby bindings for the saslwrapper library.

%prep
%setup -q

%build
%{__aclocal} -I m4
%{__autoheader}
%{__libtoolize} --automake
%{__automake}
%{__autoconf}

export RUBY_LIB_ARCH="%{ruby_vendorarchdir}"
%configure
%{__make} SUBDIRS="src %{?with_python:python} %{?with_ruby:ruby}"

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libsaslwrapper.la
%{?with_python:%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/_saslwrapper.la}
%{?with_ruby:%{__rm} $RPM_BUILD_ROOT%{ruby_vendorarchdir}/saslwrapper.la}

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE
%attr(755,root,root) %{_libdir}/libsaslwrapper.so.*.*.*
%ghost %{_libdir}/libsaslwrapper.so.1

%files devel
%defattr(644,root,root,755)
%{_libdir}/libsaslwrapper.so
%{_includedir}/saslwrapper.h

%if %{with python}
%files -n python-saslwrapper
%defattr(644,root,root,755)
%{py_sitedir}/saslwrapper.py[co]
%attr(755,root,root) %{py_sitedir}/_saslwrapper.so
%endif

%if %{with ruby}
%files -n ruby-saslwrapper
%defattr(644,root,root,755)
%attr(755,root,root) %{ruby_vendorarchdir}/saslwrapper.so
%endif
