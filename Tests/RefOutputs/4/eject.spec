{"HeaderTags": [{"block_type": 0, "content": "eject", "key": "Name", "option": null}, {"block_type": 0, "content": "1.2.5", "key": "Version", "option": null}, {"block_type": 0, "content": "1%{?dist}", "key": "Release", "option": null}, {"block_type": 0, "content": "Short sumary", "key": "Summary", "option": null}, {"block_type": 0, "content": "GPLv2+", "key": "License", "option": null}, {"block_type": 0, "content": "http://www.pobox.com/~tranter", "key": "URL", "option": null}, {"block_type": 0, "content": "http://www.ibiblio.org/pub/Linux/utils/disk-management/%name}-%{version}%license}.tar.gz", "key": "Source0", "option": null}, {"block_type": 0, "content": "requires description", "key": "BuildRequires", "option": null}, {"block_type": 0, "content": "reqs", "key": "Requires", "option": null}], "SectionTags": [{"block_type": 1, "content": "", "keyword": "description", "name": null, "parameters": null, "subname": null}, {"block_type": 1, "content": "%autosetup", "keyword": "prep", "name": null, "parameters": null, "subname": null}, {"block_type": 1, "content": "%configure\n%make_build", "keyword": "build", "name": null, "parameters": null, "subname": null}, {"block_type": 1, "content": "make check", "keyword": "check", "name": null, "parameters": null, "subname": null}, {"block_type": 1, "content": "rm -rf $RPM_BUILD_ROOT\n%make_install", "keyword": "install", "name": null, "parameters": null, "subname": null}, {"block_type": 1, "content": "%license add-license-file-here\n\n%doc README TODO", "keyword": "files", "name": null, "parameters": null, "subname": null}, {"block_type": 1, "content": ["* Wed Mar 22 2017 Nikola Valesova\n-"], "keyword": "changelog"}], "metastring": "#00%0           %2\n#01%0        %2\n#02%0        %2\n#03%0        %2\n\n#04%0        %2\n#05%0            %2\n#06%0        %2\n\n\n#10%0%4\n\n\n#11%0\n%4\n\n\n#12%0\n%4\n\n#07%0  %2\n#08%0       %2 \n\n\n#13%0\n%4\n\n\n#14%0\n%4\n\n\n#15%0\n%4\n\n\n\n#16%0\n%4 \n"}
