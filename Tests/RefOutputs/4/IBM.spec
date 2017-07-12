{"Comments": [{"block_type": 5, "content": "# This is a sample spec file for wget"}], "HeaderTags": [{"block_type": 0, "content": "%{buildroot}", "key": "BuildRoot", "option": null}, {"block_type": 0, "content": "GNU wget", "key": "Summary", "option": null}, {"block_type": 0, "content": "GPL", "key": "License", "option": null}, {"block_type": 0, "content": "%{name}", "key": "Name", "option": null}, {"block_type": 0, "content": "%{version}", "key": "Version", "option": null}, {"block_type": 0, "content": "%{release}", "key": "Release", "option": null}, {"block_type": 0, "content": "%{name}-%{version}.tar.gz", "key": "Source", "option": null}, {"block_type": 0, "content": "Development/Tools", "key": "Group", "option": null}], "MacroDefinitions": [{"block_type": 2, "body": "/home/strike/mywget", "keyword": "define", "name": "_topdir", "options": null}, {"block_type": 2, "body": "wget", "keyword": "define", "name": "name", "options": null}, {"block_type": 2, "body": "1", "keyword": "define", "name": "release", "options": null}, {"block_type": 2, "body": "1.12", "keyword": "define", "name": "version", "options": null}, {"block_type": 2, "body": "%{_topdir}/%{name}-%{version}-root", "keyword": "define", "name": "buildroot", "options": null}], "SectionTags": [{"block_type": 1, "content": "The GNU wget program downloads files from the Internet using the command-line.", "keyword": "description", "name": null, "parameters": null, "subname": null}, {"block_type": 1, "content": "%setup -q", "keyword": "prep", "name": null, "parameters": null, "subname": null}, {"block_type": 1, "content": "./configure\nmake", "keyword": "build", "name": null, "parameters": null, "subname": null}, {"block_type": 1, "content": "make install prefix=$RPM_BUILD_ROOT/usr", "keyword": "install", "name": null, "parameters": null, "subname": null}, {"block_type": 1, "content": "%defattr(-,root,root)\n/usr/local/bin/wget\n \n%doc %attr(0444,root,root) /usr/local/share/man/man1/wget.1", "keyword": "files", "name": null, "parameters": null, "subname": null}], "metastring": "#50%0\n \n#20%0 %1     %3\n#21%0 %1            %3 \n#22%0 %1     %3\n#23%0 %1     %3\n#24%0 %1 %3\n \n#00%0  %2\n#01%0        %2\n#02%0        %2\n#03%0           %2\n#04%0        %2\n#05%0        %2\n#06%0         %2\n#07%0          %2\n \n#10%0\n%4\n \n#11%0\n%4\n \n#12%0\n%4\n \n#13%0\n%4\n \n#14%0\n%4\n"}