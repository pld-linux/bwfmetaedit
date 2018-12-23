# TODO: system tinyxml2 and libzen
Summary:	Embed, validate and export BWF files metadata
Summary(pl.UTF-8):	Osadzanie, sprawdzanie i eksport metadanych z plików BWF
Name:		bwfmetaedit
Version:	1.3.6
Release:	1
License:	Public Domain (bwfmetaedit), BSD (embedded libraries)
Group:		Applications/Multimedia
Source0:	https://mediaarea.net/download/source/bwfmetaedit/%{version}/%{name}_%{version}.tar.xz
# Source0-md5:	95f60d6488e9be608aa7e683a70afe90
URL:		https://mediaarea.net/BWFMetaEdit
BuildRequires:	Qt5Gui-devel >= 5
BuildRequires:	Qt5Widgets-devel >= 5
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	pkgconfig
BuildRequires:	qt5-build >= 5
BuildRequires:	rpmbuild(macros) >= 1.566
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
BWF MetaEdit is a tool that supports embedding, validating, and
exporting of metadata in Broadcast WAVE Format (BWF) files. It
supports the FADGI Broadcast WAVE Metadata Embedding Guidelines.

%description -l pl.UTF-8
BWF MetaEdit to narzędzie obsługujące osadzanie, sprawdzanie
poprawności i eksportowanie metadanych w plikach Broadcast WAVE (BWF).
Obsługuje wytyczne osadzania metadanych w Broadcast WAVE wg FADGI.

%package gui
Summary:	GUI to embed, validate and export BWF files metadata
Summary(pl.UTF-8):	Graficzny interfejs użytkownika do osadzania, sprawdzania i eksportu metadanych z plików BWF
Group:		X11/Applications/Multimedia

%description gui
BWF MetaEdit is a tool that supports embedding, validating, and
exporting of metadata in Broadcast WAVE Format (BWF) files. It
supports the FADGI Broadcast WAVE Metadata Embedding Guidelines.

%description gui -l pl.UTF-8
BWF MetaEdit to narzędzie obsługujące osadzanie, sprawdzanie
poprawności i eksportowanie metadanych w plikach Broadcast WAVE (BWF).
Obsługuje wytyczne osadzania metadanych w Broadcast WAVE wg FADGI.

%prep
%setup -q -n bwfmetaedit
%undos *.html *.txt Release/*.txt
chmod 644 *.html *.txt Release/*.txt

%build
# build CLI
cd Project/GNU/CLI
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}
# now build GUI
cd ../../../Project/GNU/GUI
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
# Qt5Core with -reduce-relocations requires PIC code
%configure \
	CXXFLAGS="%{rpmcxxflags} -fPIC"
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C Project/GNU/CLI install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C Project/GNU/GUI install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_datadir}/metainfo,%{_desktopdir},%{_iconsdir}/hicolor/128x128/apps}
cp -p Project/GNU/GUI/bwfmetaedit-gui.desktop $RPM_BUILD_ROOT%{_desktopdir}
cp -p Project/GNU/GUI/bwfmetaedit-gui.metainfo.xml $RPM_BUILD_ROOT%{_datadir}/metainfo
cp -p Source/Resource/Image/FADGI/Logo128.png $RPM_BUILD_ROOT%{_iconsdir}/hicolor/128x128/apps/bwfmetaedit.png

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc License.html History_CLI.txt Release/ReadMe_CLI_Linux.txt
%attr(755,root,root) %{_bindir}/bwfmetaedit

%files gui
%defattr(644,root,root,755)
%doc License.html History_GUI.txt Release/ReadMe_GUI_Linux.txt
%attr(755,root,root) %{_bindir}/bwfmetaedit-gui
%{_datadir}/metainfo/bwfmetaedit-gui.metainfo.xml
%{_desktopdir}/bwfmetaedit-gui.desktop
%{_iconsdir}/hicolor/128x128/apps/bwfmetaedit.png
