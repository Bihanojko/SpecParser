{"beginning": "", "block_list": [{"block_type": 0, "content": "A program that ejects removable media using software control", "key": "Summary", "metastring": "%0            %2\n"}, {"block_type": 0, "content": "eject", "key": "Name", "metastring": "%0               %2\n"}, {"block_type": 0, "content": "2.1.5", "key": "Version", "metastring": "%0            %2\n"}, {"block_type": 0, "content": "21%{?dist}", "key": "Release", "metastring": "%0            %2\n"}, {"block_type": 0, "content": "GPLv2+", "key": "License", "metastring": "%0            %2\n"}, {"block_type": 0, "content": "%{name}-%{version}.tar.gz", "key": "Source", "metastring": "%0             %2\n"}, {"block_type": 0, "content": "eject-2.1.1-verbose.patch", "key": "Patch1", "metastring": "%0             %2\n"}, {"block_type": 0, "content": "eject-timeout.patch", "key": "Patch2", "metastring": "%0             %2\n"}, {"block_type": 0, "content": "eject-2.1.5-opendevice.patch", "key": "Patch3", "metastring": "%0             %2\n"}, {"block_type": 0, "content": "eject-2.1.5-spaces.patch", "key": "Patch4", "metastring": "%0             %2\n"}, {"block_type": 0, "content": "eject-2.1.5-lock.patch", "key": "Patch5", "metastring": "%0             %2\n"}, {"block_type": 0, "content": "eject-2.1.5-umount.patch", "key": "Patch6", "metastring": "%0             %2\n"}, {"block_type": 0, "content": "http://www.pobox.com/~tranter", "key": "URL", "metastring": "%0                %2\n"}, {"block_type": 0, "content": "s390 s390x", "key": "ExcludeArch", "metastring": "%0        %2\n"}, {"block_type": 0, "content": "gettext", "key": "BuildRequires", "metastring": "%0      %2\n"}, {"block_type": 0, "content": "libtool", "key": "BuildRequires", "metastring": "%0      %2\n\n"}, {"block_type": 1, "content": "The eject program allows the user to eject removable media (typically\nCD-ROMs, floppy disks or Iomega Jaz or Zip disks) using software\ncontrol. Eject can also control some multi-disk CD changers and even\nsome devices' auto-eject features.\n\nInstall eject if you'd like to eject removable media using software\ncontrol.", "keyword": "description", "metastring": "%0\n%4\n\n"}, {"block_type": 1, "content": "%autosetup -n %{name}", "keyword": "prep", "metastring": "%0\n%4\n\n"}, {"block_type": 1, "content": "%configure\n%make_build", "keyword": "build", "metastring": "%0\n%4\n\n"}, {"block_type": 1, "content": "%make_install\n\ninstall -m 755 -d %{buildroot}/%{_sbindir}\nln -s ../bin/eject %{buildroot}/%{_sbindir}\n\n%find_lang %{name}", "keyword": "install", "metastring": "%0\n%4\n\n"}, {"block_type": 1, "content": "%license COPYING\n%doc README TODO ChangeLog\n%{_bindir}/*\n%{_sbindir}/*\n%{_mandir}/man1/*", "keyword": "files", "metastring": "%0 %2 %3\n%4\n\n", "parameters": "f", "subname": "%{name}.lang"}, {"block_type": 1, "content": ["* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.5-21\n- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild", "* Fri Jul 02 2010 Kamil Dudka <kdudka@redhat.com> 2.1.5-20\n- handle multi-partition devices with spaces in mount points properly (#608502)"], "keyword": "changelog", "metastring": "%0\n%4\n\n%4"}], "end": "\n"}
