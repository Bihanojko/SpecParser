{"Comments": [{"block_type": 5, "content": "# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required"}, {"block_type": 5, "content": "# If go_compiler is not set to 1, there is no virtual provide. Use golang instead."}], "Conditions": [{"block_type": 6, "else_body": [], "else_keyword": null, "end_keyword": "endif", "expression": "! 0%{?gobuild:1}", "keyword": "if"}], "HeaderTags": [{"block_type": 0, "content": "gofed", "key": "Name", "option": null}, {"block_type": 0, "content": "1.0.0", "key": "Version", "option": null}, {"block_type": 0, "content": "0.9.rc1%{?dist}", "key": "Release", "option": null}, {"block_type": 0, "content": "Tool for development of golang devel packages", "key": "Summary", "option": null}, {"block_type": 0, "content": "GPLv2+", "key": "License", "option": null}, {"block_type": 0, "content": "https://github.com/%{project}/%{repo}", "key": "URL", "option": null}, {"block_type": 0, "content": "https://github.com/%{project}/%{repo}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz", "key": "Source0", "option": null}, {"block_type": 0, "content": "https://github.com/%{project}/%{cmdsignature_repo}/archive/%{cmdsignature_commit}/%{cmdsignature_repo}-%{cmdsignature_shortcommit}.tar.gz", "key": "Source1", "option": null}, {"block_type": 0, "content": "https://github.com/%{project}/%{gofedlib_repo}/archive/%{gofedlib_commit}/%{gofedlib_repo}-%{gofedlib_shortcommit}.tar.gz", "key": "Source2", "option": null}, {"block_type": 0, "content": "https://github.com/%{project}/%{gofedresources_repo}/archive/%{gofedresources_commit}/%{gofedresources_repo}-%{gofedresources_shortcommit}.tar.gz", "key": "Source3", "option": null}, {"block_type": 0, "content": "https://github.com/%{project}/%{gofedinfra_repo}/archive/%{gofedinfra_commit}/%{gofedinfra_repo}-%{gofedinfra_shortcommit}.tar.gz", "key": "Source4", "option": null}, {"block_type": 0, "content": "set-correct-paths.patch", "key": "Patch0", "option": null}, {"block_type": 0, "content": "%{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 %{arm}}", "key": "ExclusiveArch", "option": null}, {"block_type": 0, "content": "%{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}", "key": "BuildRequires", "option": null}, {"block_type": 0, "content": "python >= 2.7.5", "key": "BuildRequires", "option": null}, {"block_type": 0, "content": "python-devel", "key": "BuildRequires", "option": null}, {"block_type": 0, "content": "python-setuptools", "key": "BuildRequires", "option": null}, {"block_type": 0, "content": "python >= 2.7.5, bash, wget, rpmdevtools, rpmlint", "key": "Requires", "option": null}, {"block_type": 0, "content": "coreutils, rpm-build, openssh-clients, tar", "key": "Requires", "option": null}, {"block_type": 0, "content": "%{name}-cmd-dnfs-base = %{version}-%{release}", "key": "Requires", "option": null}, {"block_type": 0, "content": "python-cmdsignature = %{version}-%{release}", "key": "Requires", "option": null}, {"block_type": 0, "content": "%{name}-infra = %{version}-%{release}", "key": "Requires", "option": null}, {"block_type": 0, "content": "%{name}-base = %{version}-%{release}", "key": "Requires", "option": null}, {"block_type": 0, "content": "bash-completion", "key": "Requires", "option": null}, {"block_type": 0, "content": "gofed < 1.0.0", "key": "Conflicts", "option": null}], "MacroConditions": [{"block_type": 3, "condition": "!?", "content": "%global license %doc", "ending": "", "name": "_licensedir"}], "MacroDefinitions": [{"block_type": 2, "body": "0", "keyword": "global", "name": "_dwz_low_mem_die_limit", "options": null}, {"block_type": 2, "body": "github", "keyword": "global", "name": "provider", "options": null}, {"block_type": 2, "body": "com", "keyword": "global", "name": "provider_tld", "options": null}, {"block_type": 2, "body": "ingvagabund", "keyword": "global", "name": "project", "options": null}, {"block_type": 2, "body": "gofed", "keyword": "global", "name": "repo", "options": null}, {"block_type": 2, "body": "%{provider}.%{provider_tld}/%{project}/%{repo}", "keyword": "global", "name": "provider_prefix", "options": null}, {"block_type": 2, "body": "33207573a1875bc828da3f863e1de439d7af8166", "keyword": "global", "name": "cmdsignature_commit", "options": null}, {"block_type": 2, "body": "%(c=%{cmdsignature_commit}; echo ${c:0:7})", "keyword": "global", "name": "cmdsignature_shortcommit", "options": null}, {"block_type": 2, "body": "c2e5b00ebc01616820e571aa554429b1461dc2c4", "keyword": "global", "name": "gofedlib_commit", "options": null}, {"block_type": 2, "body": "%(c=%{gofedlib_commit}; echo ${c:0:7})", "keyword": "global", "name": "gofedlib_shortcommit", "options": null}, {"block_type": 2, "body": "7e414c78930a81167dc2cd4d3e9adb79eeed38a6", "keyword": "global", "name": "gofedresources_commit", "options": null}, {"block_type": 2, "body": "%(c=%{gofedresources_commit}; echo ${c:0:7})", "keyword": "global", "name": "gofedresources_shortcommit", "options": null}, {"block_type": 2, "body": "6bff7ae54535689e2ade3d0bd3d33d903a2190b9", "keyword": "global", "name": "gofedinfra_commit", "options": null}, {"block_type": 2, "body": "%(c=%{gofedinfra_commit}; echo ${c:0:7})", "keyword": "global", "name": "gofedinfra_shortcommit", "options": null}, {"block_type": 2, "body": "48d80fe18e643be7bd3ebc6ece22a6a07bb188d1", "keyword": "global", "name": "commit", "options": null}, {"block_type": 2, "body": "%(c=%{commit}; echo ${c:0:7})", "keyword": "global", "name": "shortcommit", "options": null}, {"block_type": 2, "body": "cmdsignature", "keyword": "global", "name": "cmdsignature_repo", "options": null}, {"block_type": 2, "body": "gofedlib", "keyword": "global", "name": "gofedlib_repo", "options": null}, {"block_type": 2, "body": "resources", "keyword": "global", "name": "gofedresources_repo", "options": null}, {"block_type": 2, "body": "infra", "keyword": "global", "name": "gofedinfra_repo", "options": null}, {"AP": [["! 0%{?gobuild:1}", 1]], "block_type": 2, "body": "go build -ldflags \"${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\\\n')\" -a -v -x %{?**};", "keyword": "define", "name": "gobuild", "options": "(o:)"}], "SectionTags": [{"block_type": 1, "content": "Tool to automize packaging of golang devel source codes.\nThe main goal is to automatize packaging, i.e. provide spec file generators,\ndiscovery of tests, imported and provided packages,\ncheck of up-to-date state of dependencies,\npreparation of review and\ncheck of spec file (gofed lint).", "keyword": "description", "name": null, "parameters": null, "subname": null}, {"block_type": 1, "content": [{"block_type": 0, "content": "Set of basic commands definitions", "key": "Summary", "option": null}, {"block_type": 0, "content": "noarch", "key": "BuildArch", "option": null}, {"block_type": 1, "content": "Basic gofed commands definition", "keyword": "description", "name": "cmd-dnfs-base", "parameters": null, "subname": null}], "keyword": "package", "parameters": null, "subname": "cmd-dnfs-base"}, {"block_type": 1, "content": [{"block_type": 0, "content": "Set of build commands definitions", "key": "Summary", "option": null}, {"block_type": 0, "content": "noarch", "key": "BuildArch", "option": null}, {"block_type": 1, "content": "Build gofed commands definition", "keyword": "description", "name": "cmd-dnfs-build", "parameters": null, "subname": null}], "keyword": "package", "parameters": null, "subname": "cmd-dnfs-build"}, {"block_type": 1, "content": [{"block_type": 0, "content": "Set of scan commands definitions", "key": "Summary", "option": null}, {"block_type": 0, "content": "noarch", "key": "BuildArch", "option": null}, {"block_type": 1, "content": "Scan gofed commands definition", "keyword": "description", "name": "cmd-dnfs-scan", "parameters": null, "subname": null}], "keyword": "package", "parameters": null, "subname": "cmd-dnfs-scan"}, {"block_type": 1, "content": [{"block_type": 0, "content": "Implementation of base commands for gofed", "key": "Summary", "option": null}, {"block_type": 0, "content": "noarch", "key": "BuildArch", "option": null}, {"block_type": 1, "content": "Basic commands", "keyword": "description", "name": "base", "parameters": null, "subname": null}], "keyword": "package", "parameters": null, "subname": "base"}, {"block_type": 1, "content": [{"block_type": 0, "content": "Set of commands for scanning golang projects", "key": "Summary", "option": null}, {"block_type": 0, "content": "%{name} = %{version}-%{release}", "key": "Requires", "option": null}, {"block_type": 0, "content": "%{name}-cmd-dnfs-scan = %{version}-%{release}", "key": "Requires", "option": null}, {"block_type": 0, "content": "python-cmdsignature = %{version}-%{release}", "key": "Requires", "option": null}, {"block_type": 0, "content": "graphviz", "key": "Requires", "option": null}, {"block_type": 0, "content": "noarch", "key": "BuildArch", "option": null}, {"block_type": 0, "content": "gofed-scan < 1.0.0", "key": "Conflicts", "option": null}, {"block_type": 1, "content": "Subpackage providing commands for scanning of golang project, i.e.\ncomparison of APIs of two golang projects,\ngenerator of xml files representing exported symbols and\nscan of golang packages and generator of dependency graph.", "keyword": "description", "name": "scan", "parameters": null, "subname": null}], "keyword": "package", "parameters": null, "subname": "scan"}, {"block_type": 1, "content": [{"block_type": 0, "content": "Set of commands for building golang projects", "key": "Summary", "option": null}, {"block_type": 0, "content": "%{name} = %{version}-%{release}", "key": "Requires", "option": null}, {"block_type": 0, "content": "%{name}-cmd-dnfs-build = %{version}-%{release}", "key": "Requires", "option": null}, {"block_type": 0, "content": "python-cmdsignature = %{version}-%{release}", "key": "Requires", "option": null}, {"block_type": 0, "content": "noarch", "key": "BuildArch", "option": null}, {"block_type": 0, "content": "gofed-build < 1.0.0", "key": "Conflicts", "option": null}, {"block_type": 1, "content": "Subpackage providing commands for scratch builds, builds,\npulls, pushes, updates, overrides and other commands\nthat can be used for package maitainance.\n\nThe commands support running one command on multiple branches at once.", "keyword": "description", "name": "build", "parameters": null, "subname": null}], "keyword": "package", "parameters": null, "subname": "build"}, {"block_type": 1, "content": [{"block_type": 0, "content": "Gofedlib", "key": "Summary", "option": null}, {"block_type": 0, "content": "python-fedora python-jinja2 python-markupsafe", "key": "BuildRequires", "option": null}, {"block_type": 0, "content": "python-fedora python-jinja2 python-markupsafe python-PyGithub python2-hglib", "key": "Requires", "option": null}, {"block_type": 1, "content": "Gofedlib", "keyword": "description", "name": "gofedlib", "parameters": null, "subname": null}], "keyword": "package", "parameters": null, "subname": "gofedlib"}, {"block_type": 1, "content": [{"block_type": 0, "content": "Gofed resources", "key": "Summary", "option": null}, {"block_type": 0, "content": "python2-hglib", "key": "BuildRequires", "option": null}, {"block_type": 0, "content": "python2-hglib", "key": "Requires", "option": null}, {"block_type": 0, "content": "%{name}-gofedlib = %{version}-%{release}", "key": "Requires", "option": null}, {"block_type": 0, "content": "noarch", "key": "BuildArch", "option": null}, {"block_type": 1, "content": "Gofed resources", "keyword": "description", "name": "resources", "parameters": null, "subname": null}], "keyword": "package", "parameters": null, "subname": "resources"}, {"block_type": 1, "content": [{"block_type": 0, "content": "Gofed infra", "key": "Summary", "option": null}, {"block_type": 0, "content": "python-jsonschema koji GitPython python-pycurl python2-hglib python-gitdb", "key": "BuildRequires", "option": null}, {"block_type": 0, "content": "python-jsonschema koji GitPython python-pycurl python2-hglib python-gitdb", "key": "Requires", "option": null}, {"block_type": 0, "content": "%{name}-gofedlib = %{version}-%{release}", "key": "Requires", "option": null}, {"block_type": 0, "content": "%{name}-resources = %{version}-%{release}", "key": "Requires", "option": null}, {"block_type": 0, "content": "noarch", "key": "BuildArch", "option": null}, {"block_type": 1, "content": "Gofed infra", "keyword": "description", "name": "infra", "parameters": null, "subname": null}], "keyword": "package", "parameters": null, "subname": "infra"}, {"block_type": 1, "content": [{"block_type": 0, "content": "Run gofed commands as a container", "key": "Summary", "option": null}, {"block_type": 0, "content": "%{name}-cmd-dnfs-base = %{version}-%{release}", "key": "Requires", "option": null}, {"block_type": 0, "content": "python-cmdsignature = %{version}-%{release}", "key": "Requires", "option": null}, {"block_type": 0, "content": "docker", "key": "Requires", "option": null}, {"block_type": 0, "content": "noarch", "key": "BuildArch", "option": null}, {"block_type": 0, "content": "%{ix86} x86_64 %{arm} aarch64 ppc64le s390x %{mips}", "key": "ExclusiveArch", "option": null}, {"block_type": 1, "content": "Run gofed commands as a container", "keyword": "description", "name": "docker", "parameters": null, "subname": null}], "keyword": "package", "parameters": null, "subname": "docker"}, {"block_type": 1, "content": [{"block_type": 0, "content": "Command signature python module", "key": "Summary", "option": null}, {"block_type": 0, "content": "noarch", "key": "BuildArch", "option": null}, {"block_type": 0, "content": "PyYAML", "key": "BuildRequires", "option": null}, {"block_type": 0, "content": "python >= 2.7.5", "key": "Requires", "option": null}, {"block_type": 0, "content": "PyYAML", "key": "Requires", "option": null}, {"block_type": 1, "content": "Command signature python module", "keyword": "description", "name": null, "parameters": "n", "subname": "python-cmdsignature"}], "keyword": "package", "parameters": "n", "subname": "python-cmdsignature"}, {"block_type": 1, "content": "%setup -q -n %{cmdsignature_repo}-%{cmdsignature_commit} -T -b 1\n%setup -q -n %{gofedlib_repo}-%{gofedlib_commit} -T -b 2\n%setup -q -n %{gofedresources_repo}-%{gofedresources_commit} -T -b 3\n%setup -q -n %{gofedinfra_repo}-%{gofedinfra_commit} -T -b 4\n%setup -q -n %{repo}-%{commit}\n%patch0 -p1", "keyword": "prep", "name": null, "parameters": null, "subname": null}, {"block_type": 1, "content": "pushd ../%{cmdsignature_repo}-%{cmdsignature_commit}\n%{__python2} setup.py build\npopd\n\npushd ../%{gofedlib_repo}-%{gofedlib_commit}\npushd gofedlib/go/symbolsextractor\n%gobuild -o parseGo parseGo.go\npopd\n%{__python2} setup.py build\npopd\n\npushd ../%{gofedresources_repo}-%{gofedresources_commit}\n%{__python2} setup.py build\npopd\n\npushd ../%{gofedinfra_repo}-%{gofedinfra_commit}\n%{__python2} setup.py build\npopd", "keyword": "build", "name": null, "parameters": null, "subname": null}, {"block_type": 1, "content": "# install cmdsignature as standard python module\npushd ../%{cmdsignature_repo}-%{cmdsignature_commit}\n%{__python2} setup.py install --skip-build --root %{buildroot}\npopd\n\npushd ../%{gofedlib_repo}-%{gofedlib_commit}\n%{__python2} setup.py install --skip-build --root %{buildroot}\npopd\n\npushd ../%{gofedresources_repo}-%{gofedresources_commit}\n%{__python2} setup.py install --skip-build --root %{buildroot}\npopd\n\npushd ../%{gofedinfra_repo}-%{gofedinfra_commit}\n%{__python2} setup.py install --skip-build --root %{buildroot}\npopd\n\n# copy command definitions under gofed-cmd-dnf-[base|build|scan]\nmkdir -p %{buildroot}/usr/share/%{name}/\ncp -rpav cmd %{buildroot}/usr/share/%{name}/.\ncp -pav *.py %{buildroot}/usr/share/%{name}/.\n\n# install binaries\ninstall -m 755 -d %{buildroot}/%{_bindir}\ncp -pav gofed %{buildroot}/usr/bin/gofed\ncp -pav gofed-docker %{buildroot}/usr/bin/gofed-docker\n\n# TODO: generate bash completion via cmdsignature\n# TODO: generate man pages via cmdsignature\n\ncp -r modules %{buildroot}/usr/share/%{name}/.\n# copy config\nmkdir -p %{buildroot}%{_sysconfdir}\ncp config/gofed.conf %{buildroot}%{_sysconfdir}/.\nmkdir -p %{buildroot}/usr/share/%{name}/config\ncp config/gofed.conf %{buildroot}/usr/share/%{name}/config/.\n# directory for local database\ninstall -m 755 -d %{buildroot}/%{_sharedstatedir}/%{name}\n# copy golang list and native imports\ncp -r data %{buildroot}%{_sharedstatedir}/%{name}/.\n# working directory under /var/lib/gofed\ninstall -m 775 -d %{buildroot}/%{_sharedstatedir}/%{name}/resource_provider\ninstall -m 775 -d %{buildroot}/%{_sharedstatedir}/%{name}/resource_client\ninstall -m 775 -d %{buildroot}/%{_sharedstatedir}/%{name}/storage\ninstall -m 775 -d %{buildroot}/%{_sharedstatedir}/%{name}/simplefilestorage\n# man pages\nmkdir -p %{buildroot}/usr/share/man/man1\ncp docs/gofed.1 %{buildroot}/usr/share/man/man1/gofed.1", "keyword": "install", "name": null, "parameters": null, "subname": null}, {"block_type": 1, "content": "export PYTHONPATH=%{buildroot}/%{python2_sitelib}:%{buildroot}/usr/share/gofed:%{buildroot}/usr/share\n./hack/test-cmd.sh\nrm $(find %{buildroot}/usr/share/%{name} -iname \"*.py[c|o]\")\nrm -r %{buildroot}/usr/share/%{name}/config", "keyword": "check", "name": null, "parameters": null, "subname": null}, {"block_type": 1, "content": "getent group gofed >/dev/null || groupadd -r gofed\ngetent passwd gofed >/dev/null || useradd -r -g gofed -d / -s /sbin/nologin \\\n        -c \"Gofed user\" gofed\n\n#define license tag if not already defined", "keyword": "pre", "name": null, "parameters": null, "subname": null}, {"block_type": 1, "content": "/usr/share/%{name}/cmd/README.md\n/usr/share/%{name}/cmd/repo2spec/*.yml\n/usr/share/%{name}/cmd/fetch/*.yml\n/usr/share/%{name}/cmd/create-tracker/*.yml\n/usr/share/%{name}/cmd/ggi/*.yml\n/usr/share/%{name}/cmd/inspect/*.yml\n/usr/share/%{name}/cmd/check-deps/*.yml\n/usr/share/%{name}/cmd/lint/*.yml\n/usr/share/%{name}/cmd/review-request/*.yml\n/usr/share/%{name}/cmd/clean-resources/*.yml\n/usr/share/%{name}/cmd/base.yml", "keyword": "files", "name": "cmd-dnfs-base", "parameters": null, "subname": null}, {"block_type": 1, "content": "/usr/share/%{name}/cmd/tools/*.yml\n/usr/share/%{name}/cmd/bump-spec/*.yml\n/usr/share/%{name}/cmd/wizard/*.yml\n/usr/share/%{name}/cmd/build.yml", "keyword": "files", "name": "cmd-dnfs-build", "parameters": null, "subname": null}, {"block_type": 1, "content": "/usr/share/%{name}/cmd/goapidiff/*.yml\n/usr/share/%{name}/cmd/approx-deps/*.yml\n/usr/share/%{name}/cmd/scan-deps/*.yml\n/usr/share/%{name}/cmd/scan-distro/*.yml\n/usr/share/%{name}/cmd/scan-packages/*.yml\n/usr/share/%{name}/cmd/unit-test/*.yml\n/usr/share/%{name}/cmd/scan.yml", "keyword": "files", "name": "cmd-dnfs-scan", "parameters": null, "subname": null}, {"block_type": 1, "content": "/usr/share/%{name}/cmd/version/version.py\n/usr/share/%{name}/cmd/repo2spec/*.py\n/usr/share/%{name}/cmd/repo2spec/bitbucket2gospec\n/usr/share/%{name}/cmd/repo2spec/github2gospec\n/usr/share/%{name}/cmd/repo2spec/googlecode2gospec\n/usr/share/%{name}/cmd/fetch/*.py\n/usr/share/%{name}/cmd/create-tracker/*.py\n/usr/share/%{name}/cmd/ggi/*.py\n/usr/share/%{name}/cmd/inspect/*.py\n/usr/share/%{name}/cmd/check-deps/*.py\n/usr/share/%{name}/cmd/lint/*.py\n/usr/share/%{name}/cmd/review-request/*.py\n/usr/share/%{name}/cmd/clean-resources/*.py\n#%{_sysconfdir}/bash_completion.d/gofed-base_bash_completion\n/usr/share/man/man1/gofed.1.gz", "keyword": "files", "name": "base", "parameters": null, "subname": null}, {"block_type": 1, "content": "/usr/share/%{name}/cmd/tools/*.py\n/usr/share/%{name}/cmd/tools/bbobranches\n/usr/share/%{name}/cmd/tools/build\n/usr/share/%{name}/cmd/tools/gcp\n/usr/share/%{name}/cmd/tools/pull\n/usr/share/%{name}/cmd/tools/push\n/usr/share/%{name}/cmd/tools/scratch-build\n/usr/share/%{name}/cmd/tools/update\n/usr/share/%{name}/cmd/bump-spec/*.py\n/usr/share/%{name}/cmd/wizard/*.py\n#%{_sysconfdir}/bash_completion.d/gofed-build_bash_completion", "keyword": "files", "name": "build", "parameters": null, "subname": null}, {"block_type": 1, "content": "/usr/share/%{name}/cmd/goapidiff/*.py\n/usr/share/%{name}/cmd/approx-deps/*.py\n/usr/share/%{name}/cmd/scan-deps/*.py\n/usr/share/%{name}/cmd/scan-distro/*.py\n/usr/share/%{name}/cmd/scan-packages/*.py\n/usr/share/%{name}/cmd/unit-test/*.py\n#%{_sysconfdir}/bash_completion.d/gofed-scan_bash_completion", "keyword": "files", "name": "scan", "parameters": null, "subname": null}, {"block_type": 1, "content": "%license LICENSE \n%{python2_sitelib}/gofedlib\n%{python2_sitelib}/gofedlib-?.?.???-py2.7.egg-info\n%{_bindir}/gofedlib-cli", "keyword": "files", "name": "gofedlib", "parameters": null, "subname": null}, {"block_type": 1, "content": "%license LICENSE \n%{python2_sitelib}/gofedresources\n%{python2_sitelib}/gofedresources-?.?.?-py2.7.egg-info", "keyword": "files", "name": "resources", "parameters": null, "subname": null}, {"block_type": 1, "content": "%license LICENSE \n%{python2_sitelib}/gofedinfra\n%{python2_sitelib}/gofedinfra-?.?.?-py2.7.egg-info", "keyword": "files", "name": "infra", "parameters": null, "subname": null}, {"block_type": 1, "content": "%license LICENSE \n%{python2_sitelib}/cmdsignature\n%{python2_sitelib}/cmdsignature-?.?.?-py2.7.egg-info", "keyword": "files", "name": null, "parameters": "n", "subname": "python-cmdsignature"}, {"block_type": 1, "content": "%{_bindir}/gofed-docker", "keyword": "files", "name": "docker", "parameters": null, "subname": null}, {"block_type": 1, "content": "%license LICENSE\n%doc *.md\n%config(noreplace) /etc/gofed.conf\n/usr/share/%{name}/modules\n#%{_mandir}/man1/gofed.1.gz\n%attr(-, gofed, gofed) %{_sharedstatedir}/%{name}\n/usr/bin/%{name}\n/usr/share/%{name}/*.py", "keyword": "files", "name": null, "parameters": null, "subname": null}, {"block_type": 1, "content": ["* Wed Mar 01 2017 Jan Chaloupka <jchaloup@redhat.com> - 1.0.0-0.9.rc1\n- Provide a simple man page\n  resolves: #1426854", "* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-0.8.rc1\n- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild", "* Wed Jan 25 2017 Jan Chaloupka <jchaloup@redhat.com> - 1.0.0-0.7.rc1\n- Bump to a7766e5587800fc3b49c46149605cd95a98eb31b\n  resolves: #1416407", "* Tue Dec 27 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 1.0.0-0.6.rc1\n- Compile the docker one only for supported arches", "* Tue Oct 04 2016 jchaloup <jchaloup@redhat.com> - 1.0.0-0.5.rc1\n- create missing directories under /var/lib/gofed", "* Fri Sep 23 2016 jchaloup <jchaloup@redhat.com> - 1.0.0-0.4.rc1\n- extend the list of known deps directories with vendor (upstream #117)", "* Thu Sep 22 2016 jchaloup <jchaloup@redhat.com> - 1.0.0-0.3.rc1\n- Add missing deps, minor fixes", "* Wed Sep 21 2016 jchaloup <jchaloup@redhat.com> - 1.0.0-0.2.rc1\n- Bump deps, conflict with older gofed", "* Sun Sep 18 2016 jchaloup <jchaloup@redhat.com> - 1.0.0-0.rc1.1\n- Update to gofed infrastructure", "* Thu Jul 21 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.10-5\n- https://fedoraproject.org/wiki/Changes/golang1.7", "* Wed Apr 06 2016 jchaloup <jchaloup@redhat.com> - 0.0.10-4\n- Define gobuild macro if not defined (for other distros without go-srpm-macros)", "* Mon Feb 22 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.10-3\n- https://fedoraproject.org/wiki/Changes/golang1.6", "* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.10-2\n- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild", "* Wed Nov 18 2015 jchaloup <jchaloup@redhat.com> - 0.0.10-1\n- Update to 0.0.10", "* Thu Sep 17 2015 jchaloup <jchaloup@redhat.com> - 0.0.9-3\n- Bump to upstream 04cd8f0c083e3e80bbe17fc4acd2192a1628a5be", "* Thu Sep 10 2015 jchaloup <jchaloup@redhat.com> - 0.0.9-2\n- Define license macro if not defined", "* Thu Sep 10 2015 jchaloup <jchaloup@redhat.com> - 0.0.9-1\n- Updated to version 0.0.9", "* Mon Aug 31 2015 jchaloup <jchaloup@redhat.com> - 0.0.8-3\n- Add -d option when copying symlinks. Otherwise symlinks are followed.", "* Sat Aug 29 2015 jchaloup <jchaloup@redhat.com> - 0.0.8-2\n- Add missing symlinks", "* Fri Aug 21 2015 jchaloup <jchaloup@redhat.com> - 0.0.8-1\n- Updated to version 0.0.8", "* Sat Aug 01 2015 jchaloup <jchaloup@redhat.com> - 0.0.7-1\n- Updated to version 0.0.7", "* Sat Jul 11 2015 jchaloup <jchaloup@redhat.com> - 0.0.6-1\n- Updated to version 0.0.6", "* Tue Jun 23 2015 jchaloup <jchaloup@redhat.com> - 0.0.5-1\n- Updated to version 0.0.5", "* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.4-2\n- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild", "* Tue Jun 09 2015 jchaloup <jchaloup@redhat.com> - 0.0.4-1\n- Update to version 0.0.4\n  related: #1204614", "* Sat May 09 2015 jchaloup <jchaloup@redhat.com> - 0.0.3-1\n- Update to version 0.0.3\n  related: #1204614", "* Thu Apr 02 2015 jchaloup <jchaloup@redhat.com> - 0.0.1-0.1.git62b0051\n- Update to version 0.0.1\n  related: #1204614", "* Mon Mar 23 2015 jchaloup <jchaloup@redhat.com> - 0-0.1.gitcab0f0b\n- Initial commit for Fedora\n  resolves: #1204614"], "keyword": "changelog"}], "metastring": "#20%0 %1 %3\n#21%0 %1        %3\n#22%0 %1    %3\n#23%0 %1        \t%3\n#24%0 %1            %3\n#25%0 %1 %3\n\n#26%0 %1 %3\n#27%0 %1 %3\n\n#28%0 %1 %3\n#29%0 %1 %3\n\n#210%0 %1 %3\n#211%0 %1 %3\n\n#212%0 %1 %3\n#213%0 %1 %3\n\n#214%0 %1 %3\n#215%0 %1     %3\n\n#216%0 %1 %3\n#217%0 %1 %3\n#218%0 %1 %3\n#219%0 %1 %3\n\n#60%0 %1\n#220%0 %1%2 %3 \n#60%5\n\n#00%0 %1%2 %3 \n#01%0\t\t%2\n#02%0\t%2\n#03%0\t%2\n#04%0\t%2\n#05%0\t%2\n#06%0\t\t%2\n#07%0\t%2\n#08%0\t%2\n#09%0\t%2\n#010%0\t%2\n#011%0\t%2\n\n#50%0         %2\n\n#012%0\n#51%0  %2\n#013%0\n#014%0  %2\n\n#015%0  %2\n#016%0  %2\n#017%0  %2\n\n#018%0 %2\n#019%0 %2\n\n#020%0 %2\n#021%0 %2\n#022%0 %2\n#023%0 %2\n#024%0 %2\n\n#10%0 %2\n\n#11%0\n%4\n\n#12%0 %3\n%4#13%0 %2\n#14%0 %2\n\n#15%0 %1\n%4\n\n#16%0 %3\n%4#17%0 %2\n#18%0 %2\n\n#19%0 %1\n%4\n\n#110%0 %3\n%4#111%0 %2\n#112%0 %2\n\n#113%0 %1\n%4\n\n#114%0 %3\n%4#115%0 %2\n#116%0 %2\n\n#30%0 %1\n%4\n\n#117%0 %3\n%4#118%0 %2\n#119%0 %2\n#120%0 %2\n#121%0 %2\n#122%0 %2\n#123%0 %2\n#124%0 %2\n\n\n#125%0 %1\n%4\n\n#126%0 %3\n%4#127%0 %2\n#128%0 %2\n#129%0 %2\n"}