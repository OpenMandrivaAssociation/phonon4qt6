%define major 4
#define git 20230616

Summary:	Plasma Multimedia Framework
Name:		phonon4qt6
Version:	4.12.0
Release:	%{?git:0.%{git}.}5
License:	LGPLv2+
Group:		Graphical desktop/KDE
Url:		https://invent.kde.org/libraries/phonon
%if 0%{?git:1}
Source0:	https://invent.kde.org/libraries/phonon/-/archive/master/phonon-master.tar.bz2#/phonon-%{git}.tar.bz2
%else
Source0:	http://download.kde.org/stable/phonon/%{version}/phonon-%{version}.tar.xz
%endif
Patch0:		phonon-4.11.1-clang16-gcc13.patch
BuildRequires:	imagemagick
BuildRequires:	cmake(Qt6)
BuildRequires:	pkgconfig(Qt6Core)
BuildRequires:	pkgconfig(Qt6OpenGL)
BuildRequires:	pkgconfig(Qt6Gui)
BuildRequires:	pkgconfig(Qt6DBus)
BuildRequires:	pkgconfig(Qt6Widgets)
BuildRequires:	pkgconfig(Qt6Quick)
BuildRequires:	pkgconfig(Qt6UiTools)
BuildRequires:	pkgconfig(Qt6Quick)
BuildRequires:  cmake(Qt6Designer)
BuildRequires:  cmake(Qt6LinguistTools)
BuildRequires:  cmake(Qt6Core5Compat)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	cmake(ECM)

%description
Phonon is the Plasma Multimedia Framework.

%files 
# -f %{name}.lang
%{_bindir}/phononsettings6

#--------------------------------------------------------------------

%define libphonon4qt6experimental %mklibname phonon4qt6experimental %{major}

%package -n %{libphonon4qt6experimental}
Summary:	Phonon Library
Group:		System/Libraries

%description -n %{libphonon4qt6experimental}
Library for Phonon.

%files -n %{libphonon4qt6experimental}
%{_libdir}/libphonon4qt6experimental.so.%{major}*

#--------------------------------------------------------------------

%define libphonon4qt6 %mklibname phonon4qt6 %{major}

%package -n %{libphonon4qt6}
Summary:	Phonon Library
Group:		System/Libraries
# The %{name} package contains only translations and the phononsettings tool
Requires:	%{name} = %{EVRD}

%description -n %{libphonon4qt6}
Library for Phonon.

%files -n %{libphonon4qt6}
%{_libdir}/libphonon4qt6.so.%{major}*


#--------------------------------------------------------------------

%package -n phonon4qt6-devel
Group:		Development/KDE and Qt
Summary:	Phonon Development Files
Requires:	%{libphonon4qt6experimental} = %{EVRD}
Requires:	%{libphonon4qt6} = %{EVRD}

%description -n phonon4qt6-devel
Header files needed to compile applications for KDE.

%files -n phonon4qt6-devel
%{_includedir}/phonon4qt6/
%{_libdir}/libphonon4qt6.so
%{_libdir}/libphonon4qt6experimental.so
%{_libdir}/pkgconfig/phonon4qt6.pc
%{_libdir}/cmake/phonon4qt6

#--------------------------------------------------------------------

%package -n phonon4qt6-designer-plugin
Summary:        Phonon Designer Plugin
Group:          System/Libraries

%description -n phonon4qt6-designer-plugin
Designer plugin for phonon for Qt 6.

%files -n phonon4qt6-designer-plugin
%{_libdir}/qt6/plugins/designer/phonon4qt6widgets.so
#--------------------------------------------------------------------


%prep
%autosetup -p1 -n phonon-%{?git:master}%{!?git:%{version}}

%build
%cmake \
	-DPHONON_BUILD_QT5=OFF \
	-DPHONON_BUILD_QT6=ON \
	-DCMAKE_BUILD_TYPE:STRING="Release" \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-DWITH_PulseAudio=ON \
	-DPHONON_INSTALL_QT_COMPAT_HEADERS:BOOL=ON \
	-DPHONON_INSTALL_QT_EXTENSIONS_INTO_SYSTEM_QT:BOOL=ON \
	-G Ninja

%ninja_build

%install
%ninja_install -C build

# FIXME: phononsettings conflicts with qt5 phonon
mv %{buildroot}%{_bindir}/phononsettings %{buildroot}%{_bindir}/phononsettings6

# FIXME: Translations conflict with qt5 phonon...
rm -rf %{buildroot}%{_datadir}/locale
#find %{buildroot}%{_datadir}/locale -name "*.qm" |while read r; do
#    L=$(echo $r |rev |cut -d/ -f3 |rev)
#    echo "%%lang($L) %%{_datadir}/locale/$L/LC_MESSAGES/$(basename $r)" >>%{name}.lang
#done
