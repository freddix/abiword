%define		mver		3.0
%define		abipluginsdir	%{_libdir}/abiword-%{mver}/plugins
%define		plugins		gimp mathview goffice latex openwriter openxml

Summary:	Multi-platform word processor
Name:		abiword
Version:	3.0.0
Release:	0.1
Epoch:		1
License:	GPL
Group:		X11/Applications
Source0:	http://www.abisource.com/downloads/abiword/%{version}/source/%{name}-%{version}.tar.gz
# Source0-md5:	8d9c41cff3a8fbef8d0c835c65600e65
Patch0:		%{name}-desktop.patch
URL:		http://www.abisource.com/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	enchant-devel
BuildRequires:	fribidi-devel
BuildRequires:	gtk+-devel
BuildRequires:	gtkmathview-devel
BuildRequires:	gucharmap-devel
BuildRequires:	libglade-devel
BuildRequires:	libgoffice-devel
BuildRequires:	libgsf-gnome-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	librsvg-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
BuildRequires:	wv-devel
Requires(post,postun):	desktop-file-utils
Requires:	fonts-TTF-droid
Requires:	enchant-hunspell
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
AbiWord is a multi-platform word processor with a GTK+ interface on
the UNIX platform.

%package devel
Summary:	Abiword development files
Group:		Development/Libraries

%description devel
Abiword development files.

%prep
%setup -q
#%patch0 -p1

# use generic icon name
#sed -i -e 's|abiword_48.png|abiword.png|' Makefile.am
#sed -i -e 's|abiword_48.png|abiword.png|' src/af/xap/gtk/xap_UnixDlg_About.cpp
#sed -i -e 's|abiword_48|abiword|' src/wp/ap/gtk/ap_UnixFrameImpl.cpp
#mv abiword_48.png abiword.png

# set default font
sed -i -e 's|Times New Roman|Droid Serif|g' user/wp/templates/normal.*

%build
%{__libtoolize}
%{__aclocal} -I .
%{__automake}
%{__autoconf}
%configure \
	--disable-static		\
	--without-gnomevfs
	#--enable-plugins="%{plugins}"	\
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT		\
	desktopdir=%{_desktopdir}	\
	icondir=%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database_post

%postun
/sbin/ldconfig
%update_desktop_database_postun

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libabiword-*.so

%{_datadir}/abiword-%{mver}
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png

%dir %{_libdir}/abiword-%{mver}
%dir %{abipluginsdir}
%if 0
%attr(755,root,root) %{abipluginsdir}/gimp.so
%attr(755,root,root) %{abipluginsdir}/goffice.so
%attr(755,root,root) %{abipluginsdir}/latex.so
%attr(755,root,root) %{abipluginsdir}/mathview.so
%attr(755,root,root) %{abipluginsdir}/openwriter.so
%attr(755,root,root) %{abipluginsdir}/openxml.so
%endif
%attr(755,root,root) %{abipluginsdir}/opendocument.so
%{_mandir}/man1/abiword.1*

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}-%{mver}
%{_pkgconfigdir}/*.pc

