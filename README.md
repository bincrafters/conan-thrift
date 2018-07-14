[![Download](https://api.bintray.com/packages/helmesjo/public-conan/thrift%3Ahelmesjo/images/download.svg) ](https://bintray.com/helmesjo/public-conan/thrift%3Ahelmesjo/_latestVersion)
[![Build Status](https://travis-ci.org/helmesjo/conan-thrift.svg?branch=stable%2F0.11.0)](https://travis-ci.org/helmesjo/conan-thrift)
[![Build status](https://ci.appveyor.com/api/projects/status/github/helmesjo/conan-thrift?branch=stable%2F0.11.0&svg=true)](https://ci.appveyor.com/project/helmesjo/conan-thrift)

[Conan.io](https://conan.io) package recipe for [*thrift*](https://thrift.apache.org/).

Thrift is a lightweight,                     language-independent software                     stack with an associated code                     generation mechanism for RPC.

The packages generated with this **conanfile** can be found on [Bintray](https://bintray.com/helmesjo/public-conan/thrift%3Ahelmesjo).

## For Users: Use this package

### Basic setup

    $ conan install thrift/0.11.0@helmesjo/stable

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    thrift/0.11.0@helmesjo/stable

    [generators]
    cmake

Complete the installation of requirements for your project running:

    $ mkdir build && cd build && conan install ..

Note: It is recommended that you run conan install from a build directory and not the root of the project directory.  This is because conan generates *conanbuildinfo* files specific to a single build configuration which by default comes from an autodetected default profile located in ~/.conan/profiles/default .  If you pass different build configuration options to conan install, it will generate different *conanbuildinfo* files.  Thus, they should not be added to the root of the project, nor committed to git.

## For Packagers: Publish this Package

The example below shows the commands used to publish to helmesjo conan repository. To publish to your own conan respository (for example, after forking this git repository), you will need to change the commands below accordingly.

## Build and package

The following command both runs all the steps of the conan file, and publishes the package to the local system cache.  This includes downloading dependencies from "build_requires" and "requires" , and then running the build() method.

    $ conan create helmesjo/stable


### Available Options
| Option        | Default | Possible Values  |
| ------------- |:----------------- |:------------:|
| with_qt4      | False |  [True, False] |
| with_qt5      | False |  [True, False] |
| build_libraries      | True |  [True, False] |
| build_examples      | False |  [True, False] |
| with_boost_static      | False |  [True, False] |
| build_compiler      | True |  [True, False] |
| with_zlib      | True |  [True, False] |
| with_python      | False |  [True, False] |
| with_libevent      | True |  [True, False] |
| shared      | False |  [True, False] |
| build_testing      | False |  [True, False] |
| with_java      | False |  [True, False] |
| with_boostthreads      | False |  [True, False] |
| fPIC      | True |  [True, False] |
| with_c_glib      | False |  [True, False] |
| with_haskell      | False |  [True, False] |
| with_plugin      | False |  [True, False] |
| with_stdthreads      | True |  [True, False] |
| build_tutorials      | False |  [True, False] |
| with_boost_smart_ptr      | False |  [True, False] |
| with_openssl      | True |  [True, False] |
| with_boost_functional      | False |  [True, False] |
| with_cpp      | True |  [True, False] |

## Add Remote

    $ conan remote add helmesjo "https://api.bintray.com/conan/helmesjo/public-conan"

## Upload

    $ conan upload thrift/0.11.0@helmesjo/stable --all -r helmesjo


## Conan Recipe License

NOTE: The conan recipe license applies only to the files of this recipe, which can be used to build and package thrift.
It does *not* in any way apply or is related to the actual software being packaged.

[MIT](https://github.com/helmesjo/conan-thrift/blob/testing/0.11.0/LICENSE)
