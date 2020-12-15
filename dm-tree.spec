Name     : dm-tree
Version  : 0.1.5
Release  : 6
URL      : https://files.pythonhosted.org/packages/70/0a/bc3e9865603332c525fc218aceb023762aeffc2a86ff99b347b67ee3f2a8/dm-tree-0.1.5.tar.gz
Source0  : https://files.pythonhosted.org/packages/70/0a/bc3e9865603332c525fc218aceb023762aeffc2a86ff99b347b67ee3f2a8/dm-tree-0.1.5.tar.gz
Summary  : Tree is a library for working with nested data structures.
Group    : Development/Tools
License  : Apache-2.0
Requires: six
BuildRequires : bazel
BuildRequires : buildreq-distutils3
BuildRequires : six
BuildRequires : absl-py
BuildRequires : attrs
BuildRequires : numpy
BuildRequires : wrapt

# SOURCES BEGIN
Source10: https://github.com/bazelbuild/bazel-skylib/archive/0.9.0.zip
Source11: https://mirror.bazel.build/github.com/bazelbuild/rules_cc/archive/8bd6cd75d03c01bb82561a96d9c1f9f7157b13d0.zip
Source12: https://mirror.bazel.build/github.com/bazelbuild/rules_java/archive/7cf3cefd652008d0a64a419c34c13bdca6c8f178.zip
Source13: https://github.com/pybind/pybind11/archive/v2.4.3.tar.gz
Source14: https://mirror.bazel.build/github.com/abseil/abseil-cpp/archive/111ca7060a6ff50115ca85b59f6b5d8c8c5e9105.tar.gz
# SOURCES END

Patch1: 0001-Relax-numpy-upper-bound-for-tests.patch

%description
tree is a library for working with nested data structures. In a way, tree
generalizes the builtin map function which only supports flat sequences, and
allows to apply a function to each "leaf" preserving the overall structure.tree
is a library for working with nested data structures. In a way, tree
generalizes the builtin map function which only supports flat sequences, and
allows to apply a function to each "leaf" preserving the overall structure.

%prep
%setup -q
%patch1 -p1

InstallCacheBazel() {
  sha256=$(sha256sum $1 | cut -f1 -d" ")
  mkdir -p /var/tmp/cache/content_addressable/sha256/$sha256
  cp $1 /var/tmp/cache/content_addressable/sha256/$sha256/file
}

# CACHE BAZEL BEGIN
InstallCacheBazel %{SOURCE10}
InstallCacheBazel %{SOURCE11}
InstallCacheBazel %{SOURCE12}
InstallCacheBazel %{SOURCE13}
InstallCacheBazel %{SOURCE14}
# CACHE BAZEL END

%build
export http_proxy=http://127.0.0.1:9/
export https_proxy=http://127.0.0.1:9/
export no_proxy=localhost,127.0.0.1,0.0.0.0
export LANG=C.UTF-8
export SOURCE_DATE_EPOCH=1602874026
export GCC_IGNORE_WERROR=1
export AR=gcc-ar
export RANLIB=gcc-ranlib
export NM=gcc-nm
export CFLAGS="$CFLAGS -O3 -ffat-lto-objects -flto=4 "
export FCFLAGS="$FFLAGS -O3 -ffat-lto-objects -flto=4 "
export FFLAGS="$FFLAGS -O3 -ffat-lto-objects -flto=4 "
export CXXFLAGS="$CXXFLAGS -O3 -ffat-lto-objects -flto=4 "
export MAKEFLAGS=%{?_smp_mflags}

cat > $HOME/.bazelrc << EOF
build --repository_cache=/var/tmp/cache
build --verbose_failures
EOF

# FIXME: bazel hits an error related with ccache (read-only file system)
export CC=/usr/bin/gcc

python3 setup.py build

%check
export http_proxy=http://127.0.0.1:9/
export https_proxy=http://127.0.0.1:9/
export no_proxy=localhost,127.0.0.1,0.0.0.0
export CC=/usr/bin/gcc

PYTHONPATH=%{buildroot}$(python -c "import sys; print(sys.path[-1])") python setup.py test

%install
export MAKEFLAGS=%{?_smp_mflags}
export CC=/usr/bin/gcc
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/share/package-licenses/dm-tree
cp %{_builddir}/dm-tree-0.1.5/LICENSE %{buildroot}/usr/share/package-licenses/dm-tree/2b8b815229aa8a61e483fb4ba0588b8b6c491890
python3 -tt setup.py build  install --root=%{buildroot}
echo ----[ mark ]----
cat %{buildroot}/usr/lib/python3*/site-packages/*/requires.txt || :
echo ----[ mark ]----
# make .so files executable so that debuginfo is generated
find %{buildroot} -name '*.so' -exec chmod -v +x {} \;

%files
%defattr(-,root,root,-)
/usr/lib/python3*/*
/usr/share/package-licenses/dm-tree/2b8b815229aa8a61e483fb4ba0588b8b6c491890
