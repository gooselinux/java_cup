# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define _with_gcj_support 1

%define gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}

%define pkg_version     v10k
%define section         free

Name:           java_cup
Version:        0.10k
Release:        5%{?dist}
Epoch:          1
Summary:        Java source interpreter
License:        BSD and LGPLv2
Url:            http://www.cs.princeton.edu/%7Eappel/modern/java/CUP/
Source0:        http://www.cs.princeton.edu/%7Eappel/modern/java/CUP/%{name}_%{pkg_version}.tar.gz
Source1:        %{name}-build.xml
Patch0:         http://jflex.de/cup-ant-task.patch
BuildRequires:  ant
BuildRequires:  jpackage-utils >= 0:1.5
Group:          Development/Tools
%if ! %{gcj_support}
Buildarch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if %{gcj_support}
BuildRequires:          java-gcj-compat-devel
Requires(post):         java-gcj-compat
Requires(postun):       java-gcj-compat
%endif

%description
java_cup is a LALR Parser Generator for Java

%package javadoc
Summary:        Javadoc for java_cup
Group:          Documentation

%description javadoc
Javadoc for java_cup

%package manual
Summary:        Documentation for java_cup
Group:          Documentation

%description manual
Documentation for java_cup.

%prep
%setup -q -c -n %{name}-%{version}
%patch0 -p0 
install -m 644 %{SOURCE1} build.xml

# remove all binary files
find . -name "*.class" -exec rm -f {} \;

%build
ant
find . -name parser.cup -exec rm {} \;
ant javadoc

%install
rm -rf $RPM_BUILD_ROOT

# jar
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 dist/lib/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
install -m 644 dist/lib/%{name}-runtime.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-runtime-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do \
ln -sf ${jar} ${jar/-%{version}/}; done)

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr dist/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
(cd $RPM_BUILD_ROOT%{_javadocdir} && ln -sf %{name}-%{version} %{name})

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%if %{gcj_support}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%postun
%if %{gcj_support}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%files
%defattr(0644,root,root,0755)
%doc README LICENSE CHANGELOG
%{_javadir}/*

%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/java_cup-%{version}.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/java_cup-runtime-%{version}.jar.*
%endif

%files manual
%defattr(0644,root,root,0755)
%doc cup_logo.gif manual.html

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}

%changelog
* Mon Jan 11 2010 Andrew Overholt <overholt@redhat.com> 1:0.10k-5
- Add dist tag to release

* Mon Jan 11 2010 Andrew Overholt <overholt@redhat.com> 1:0.10k-4
- Remove ghost symlinking in %%post{,un}

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.10k-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.10k-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 15 2008 Lubomir Rintel <lkundrak@v3.sk> - 1:0.10k-1
- Fix the version to match upstream, so that FEver can be used

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:0.10-0.k.6.3
- drop repotag

* Sun Feb 17 2008 Lubomir Kundrak <lkundrak@redhat.com> - 1:0.10-0.k.6jpp.2
- Ant task
- Clean up to satisfy QA script and rpmlint

* Fri Aug 04 2006 Vivek Lakshmanan <vivekl@redhat.com> - 1:0.10-0.k.6jpp.1
- Re-sync with latest version from JPP.
- Partially adopt new naming convention.

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 1:0.10-0.k.5jpp_2fc
- Rebuilt

* Thu Jul 20 2006 Vivek Lakshmanan <vivekl@redhat.com> - 1:0.10-0.k.5jpp_1fc
- Re-sync with latest version from JPP.

* Wed Jul 19 2006 Vivek Lakshmanan <vivekl@redhat.com> - 1:0.10-0.k.4jpp_1fc
- Conditional native compilation for GCJ.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:0.10-0.k.1jpp_10fc
- rebuild

* Mon Mar  6 2006 Jeremy Katz <katzj@redhat.com> - 1:0.10-0.k.1jpp_9fc
- stop scriptlet spew

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:0.10-0.k.1jpp_8fc
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:0.10-0.k.1jpp_7fc
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan  3 2006 Jesse Keating <jkeating@redhat.com> 1:0.10-0.k.1jpp_6fc
- rebuilt again

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Jul 19 2005 Gary Benson <gbenson@redhat.com> 1:0.10-0.k.1jpp_5fc
- Build on ia64, ppc64, s390 and s390x.
- Switch to aot-compile-rpm.

* Tue Jun 28 2005 Gary Benson <gbenson@redhat.com> 1:0.10-0.k.1jpp_4fc
- BC-compile.

* Tue Jun 21 2005 Gary Benson <gbenson@redhat.com> 1:0.10-0.k.1jpp_3fc
- Remove classes from the tarball.

* Thu Nov  4 2004 Gary Benson <gbenson@redhat.com> 1:0.10-0.k.1jpp_2fc
- Build into Fedora.

* Thu Mar  4 2004 Frank Ch. Eigler <fche@redhat.com> 1:0.10-0.k.1jpp_1rh
- RH vacuuming

* Thu Jan 22 2004 David Walluck <david@anti-microsoft.org> 1:0.10-0.k.1jpp
- fix version/release (bump epoch)
- change License tag from Free to BSD-style
- add Distribution tag
- really update for JPackage 1.5

* Wed Mar 26 2003 Paul Nasrat <pauln@truemesh.com> 0.10k-1jpp
- for jpackage-utils 1.5
- New spec reverse engineered from binary rpms
