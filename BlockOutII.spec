# Copyright (c) 2007 oc2pus <toni@links2linux.de>
# Copyright (c) 2007 Hans de Goede <j.w.r.degoede@hhs.nl>
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

Name:		BlockOutII
Version:	2.4
Release:	%mkrel 2
Summary:	A free adaptation of the original BlockOut DOS game
Group:		Games/Arcade
License:	GPLv2+
URL:		http://www.blockout.net/blockout2
Source0:	http://downloads.sourceforge.net/project/blockout/blockout/BlockOut%202.4/bl24-src-linux-i586.tar.gz
Source1:	%{name}.desktop
Source2:	%{name}.png
Source3:	music.ogg
Source4:	%{name}-readme.txt
Patch0:		BlockOutII-2.3-syslibs.patch
Patch1:		BlockOutII-2.3-bl2Home.patch
Patch2:		BlockOutII-2.3-music.patch
Patch3:		BlockOutII-jpegdecoder.patch
Patch4:		BlockOutII-strings.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}
BuildRequires:	SDL_mixer-devel
BuildRequires:	libpng-devel 
BuildRequires:	desktop-file-utils

%description
BlockOut II is a free adaptation of the original BlockOut
DOS game edited by California Dreams in 1989. BlockOut II
has the same features than the original game with few graphic
improvements. The score calculation is also nearly similar to
the original game. BlockOut II has been designed by an addicted
player for addicted players. BlockOut II is an open source
project available for both Windows and Linux.

Blockout is a registered trademark of Kadon Enterprises, Inc.,
used by permission for the BlockOut II application by Jean-Luc
Pons.

%prep
%setup -q -n bl24_lin_src
%patch0 -p2
%patch3 -p2
pushd BlockOut
%patch1 -p2
%patch2 -p2
%patch4 -p2
popd
chmod -x `find -type f`
# readme file sourced from bl23-src-win-1.zip, converted using the following.
# iconv -f ISO8859-1 -t UTF8 BlockOut/README.txt > t; mv t BlockOut/README.txt

install -m 644 %{SOURCE3} BlockOut/sounds
install -m 644 %{SOURCE4} README.txt

%build
pushd ImageLib/src
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS -Dlinux -c" \
    CXXFLAGS="$RPM_OPT_FLAGS -Dlinux -c"
popd

pushd BlockOut
make %{?_smp_mflags} \
    CXXFLAGS="$RPM_OPT_FLAGS -Dlinux `sdl-config --cflags` -I../ImageLib/src -c" \
    SDL_ROOT=%{_prefix} LIBS="-L../ImageLib/src -lpng -lz" \
    IMGLIB_ROOT=../ImageLib/src
popd

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/games/%{name}/images
mkdir -p %{buildroot}%{_datadir}/games/%{name}/sounds

install -m 755 BlockOut/blockout %{buildroot}%{_bindir}/%{name}
install -p -m 644 BlockOut/images/* %{buildroot}%{_datadir}/games/%{name}/images
install -p -m 644 BlockOut/sounds/* %{buildroot}%{_datadir}/games/%{name}/sounds

# below is the desktop file and icon stuff.
mkdir -p %{buildroot}%{_datadir}/applications
install -p -m644 %{SOURCE1} \
  %{buildroot}%{_datadir}/applications/%{name}.desktop
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
install -p -m 644 %{SOURCE2} \
  %{buildroot}%{_datadir}/icons/hicolor/32x32/apps

rm %{buildroot}%{_datadir}/games/%{name}/sounds/music.mp3


%clean
rm -rf %{buildroot}

%post
# touch --no-create %{_datadir}/icons/hicolor || :
# if [ -x %{_bindir}/gtk-update-icon-cache ]; then
#    %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
# fi

%postun
# touch --no-create %{_datadir}/icons/hicolor || :
# if [ -x %{_bindir}/gtk-update-icon-cache ]; then
#    %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
# fi


%files
%defattr(-,root,root,-)
%doc README.txt
%{_bindir}/%{name}
%{_datadir}/games/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png


