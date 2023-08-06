<!--
SPDX-FileCopyrightText: 2022 Freemelt AB <opensource@freemelt.com>

SPDX-License-Identifier: Apache-2.0
-->

# OBFlib-Python

OBFlib-Python is a Python library for verifying, reading and manipulating OBF files. It also has an
accompanying command-line utility, `obftool`.

OBF (Open Build File) is a format that works as a blueprint and recipe for building objects in an
electron beam powder bed fusion (E-PBF) 3D printer.

## Installation

### Bullseye

OBFlib-Python can be installed as a Debian package on Debian Bullseye. The package resides in the
public apt repository:

```shell
echo "deb http://apt.opensource.freemelt.com/debian bullseye main" | sudo tee -a /etc/apt/sources.list.d/freemelt.list > /dev/null
curl http://apt.opensource.freemelt.com/debian/archive.gpg.key | sudo tee /etc/apt/trusted.gpg.d/freemelt-opensource.gpg > /dev/null

sudo apt update
sudo apt install python3-obflib
```

_NOTE: The above commands for installation on Debian Bullseye currently do not work since there is no
working pipeline for publishing to the Bullseye channel on the public apt repository. It should
however work to just replace `bullseye` with `buster` in the first command, since the same OBFLib
package works on both Buster on Bullseye._

### Debian Buster

OBFlib-Python can also be installed as a Debian package on Debian Buster but requires extra steps.

```shell
echo "deb http://apt.opensource.freemelt.com/debian buster main" | sudo tee -a /etc/apt/sources.list.d/freemelt.list > /dev/null
curl http://apt.opensource.freemelt.com/debian/archive.gpg.key | sudo tee /etc/apt/trusted.gpg.d/freemelt-opensource.gpg > /dev/null

echo 'deb http://deb.debian.org/debian buster-backports main' | sudo tee -a /etc/apt/sources.list > /dev/null
echo 'deb http://deb.debian.org/debian bullseye main' | sudo tee -a /etc/apt/sources.list > /dev/null

sudo tee /etc/apt/preferences.d/buster-first.pref > /dev/null << EOF
Package: *
Pin: release n=bullseye
Pin-Priority: -1

Package: python3-jsonschema
Pin: release n=buster-backports
Pin-Priority: 500

Package: python3-semantic-version
Pin: release n=bullseye
Pin-Priority: 500
EOF

sudo apt update
sudo apt install python3-obflib
```

Obflib can also be installed through pip via
[GitLab's internal package registry](https://docs.gitlab.com/ee/user/packages/pypi_repository/index.html#install-a-pypi-package).

```shell
pip3 install --index-url https://gitlab.com/api/v4/projects/33702591/packages/pypi/simple obflib
```

## API Documentation

Once obflib is installed as a Debian package, its API documentation can be viewed with the following
command:

```shell
obftool api-docs
```

## Usage

Obflib can be used as a Python library or with the command-line tool `obftool`.

### Python example

```
>>> import obflib
>>> messages = obflib.verify("openbuildfile/examples/standard.obf")
>>> messages.to_json()
'{"errors": {}, "warnings": {}, "isValid": true}'
>>> messages.is_valid()
True
>>> with obflib.OBF("openbuildfile/examples/standard.obf") as obf:
...     manifest = obf.manifest()
...     build_info = obf.build_info()
...
>>> manifest['name']
'Test Rod'
>>> len(build_info['layers'])
2
```

### Command-line examples

Verify an OBF:

```
> obftool verify openbuildfile/examples/standard.obf
The file openbuildfile/examples/standard.obf appears to be a valid OBF file.
> obftool verify openbuildfile/examples/invalid.obf
ERRORS in openbuildfile/examples/invalid.obf:
manifest.json/modules/defect-detector: 'modules/freemelt_defect_detector/modulez.json' does not exist in the OBF
manifest.json: 'version' is a required property
buildInfo.json/files/preHeat: 'nonexistent-file.obp' does not exist in the OBF
buildInfo.json/files/file7: 'obp/file7.obp' does not exist in the OBF
buildProcessors/buildProcessors.json/buildProcessors/simple/version: 'latest' is not a valid npm semver range. See https://github.com/npm/node-semver#ranges.
buildProcessors/buildProcessors.json/buildProcessors/complexer/entryPoint: 'buildProcessors/bob/bob-complex.lua' does not exist in the OBF
buildProcessors/buildProcessors.json/buildProcessors/complexer/args: '[amount=40]' is not of type 'array'
machineCapabilities.json/buildModule/platform: 760 is not of type 'object'
modules/freemelt_nir_thermometer/module.json: 'author' is a required property

Warnings in openbuildfile/examples/invalid.obf:
manifest.json/author: This recommended property is missing
manifest.json/license: This recommended property is missing
modules/freemelt_nir_thermometer/module.json: An object in this file contains duplicates of the key 'license'
modules/freemelt_defect_detector/module.json: This file appears to be unused

The file openbuildfile/examples/invalid.obf is not a valid OBF file.
```

Converting a BOSS configuration to an OBF using the proof-of-concept converter:

```
> obftool convert path/to/BOSS_files/ converted.obf
Adding obp: path/to/BOSS_files/TestBars11Layer1.obp
Adding obp: path/to/BOSS_files/TestBars13Layer1.obp
Adding obp: path/to/BOSS_files/TestBars7Layer1.obp
Adding obp: path/to/BOSS_files/preheat.obp
Adding obp: path/to/BOSS_files/plateheat.obp
Adding obp: path/to/BOSS_files/TestBars0Layer1.obp
Adding obp: path/to/BOSS_files/TestBars3Layer1.obp
Adding obp: path/to/BOSS_files/TestBars6Layer1.obp
Adding obp: path/to/BOSS_files/TestBars15Layer1.obp
Adding obp: path/to/BOSS_files/TestBars1Layer1.obp
Adding obp: path/to/BOSS_files/TestBars14Layer1.obp
Adding obp: path/to/BOSS_files/TestBars10Layer1.obp
Adding obp: path/to/BOSS_files/TestBars9Layer1.obp
Adding obp: path/to/BOSS_files/TestBars4Layer1.obp
Adding obp: path/to/BOSS_files/TestBars2Layer1.obp
Adding obp: path/to/BOSS_files/TestBars12Layer1.obp
Adding obp: path/to/BOSS_files/TestBars5Layer1.obp
Adding obp: path/to/BOSS_files/TestBars8Layer1.obp
Adding obp: path/to/BOSS_files/postheat.obp
Done! Wrote OBF to 'converted.obf'.
```

Converting a BOSS configuration to an OBF using the proof-of-concept converter with a custom Lua
script and setting a custom name:

```
> obftool convert path/to/BOSS_files/ converted.obf --bob-script example=build.lua --name 'Custom Build'
Using name 'Custom Build'
Using build script 'build.lua' as 'example'
Adding obp: path/to/BOSS_files/TestBars11Layer1.obp
Adding obp: path/to/BOSS_files/TestBars13Layer1.obp
Adding obp: path/to/BOSS_files/TestBars7Layer1.obp
Adding obp: path/to/BOSS_files/preheat.obp
Adding obp: path/to/BOSS_files/plateheat.obp
Adding obp: path/to/BOSS_files/TestBars0Layer1.obp
Adding obp: path/to/BOSS_files/TestBars3Layer1.obp
Adding obp: path/to/BOSS_files/TestBars6Layer1.obp
Adding obp: path/to/BOSS_files/TestBars15Layer1.obp
Adding obp: path/to/BOSS_files/TestBars1Layer1.obp
Adding obp: path/to/BOSS_files/TestBars14Layer1.obp
Adding obp: path/to/BOSS_files/TestBars10Layer1.obp
Adding obp: path/to/BOSS_files/TestBars9Layer1.obp
Adding obp: path/to/BOSS_files/TestBars4Layer1.obp
Adding obp: path/to/BOSS_files/TestBars2Layer1.obp
Adding obp: path/to/BOSS_files/TestBars12Layer1.obp
Adding obp: path/to/BOSS_files/TestBars5Layer1.obp
Adding obp: path/to/BOSS_files/TestBars8Layer1.obp
Adding obp: path/to/BOSS_files/postheat.obp
Done! Wrote OBF to 'converted.obf'.
```

## Contributing

OBFlib-Python uses docker compose to set up a development environment. Follow the below steps
for getting started with contributing to OBFlib-Python.

### Prerequisites

First install Docker and Docker Compose. If you are on Ubuntu, the following steps should do it:

```bash
sudo apt remove docker docker-engine docker.io containerd runc
sudo apt update
sudo apt install ca-certificates curl gnupg lsb-release
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo usermod -aG docker $USER
```

The last line above is needed in order to run the tests without password.
To get the added group working for your user, you can log out and in, or:

```bash
exec su -l $USER
```

### Set up the development environment

Set up the basic development environment using the following command:

```shell
make prepare-dev
```

Note: You might have to add pip's user site bin directory to `$PATH` for the above command to work.
On e.g. Ubuntu, this is done by adding the following line to `~/.bashrc` or equivalent:

```
export PATH=~/.local/bin:$PATH
```

In general, commands for running tests, linting, etc. should be run in the Docker container started
by `make prepare-dev`. This can be accomplished in (at least) two ways: Either by entering a bash
shell inside the container:

```shell
make enter-docker
```

Or by running just the desired command inside the container:

```shell
docker compose exec debian <command>
```

### Testing

Test any changes by running the command:

```commandline
make test
```

### Linting

Check code style and formatting with the following command:

```commandline
make lint
```

These checks will also be performed automatically on each commit with the pre-commit hooks that are
installed with `make prepare-dev`.

### Generating API documentation

The API documentation can be generated and previewed with

```commandline
docker compose exec debian make api-docs
xdg-open api-docs/index.html
```

The API documentation is also built automatically for every CI pipeline. The above command therefore
does not normally need to be run unless you need the documentation locally.

### Releasing

All new commits are built and packaged to be published on the public Debian repository on the
unstable "branch".

To publish a packaged stable version of the library, tag it (use `-a` for an annotated tag) and a
Debian package will be published on the public Debian repository on the stable "branch". For this
to trigger, the tag must start with `v`. Update `debian/changelog` using `dch` before releasing. For
example:

```shell
dch --newversion 0.5.0 -D stable -m
git commit ... # First, commit as usual
git tag -a v0.5.0
git push --follow-tags
```

### Dependencies

When adding dependencies to the project, they are to be added both in setup.py as pip packages and
in Dockerfile as debian packages. In the dockerfile they are to be added alongside the other debian
packages.

The dh-python tool translates the dependencies in setup.py to debian package names when we build a
deb package. The duplication between setup.py and the Dockerfile is to ensure that the development
environment is using the same versions as the actual machine.

### CI

The CI environment currently has no mechanism for building the Docker image as part of the pipeline.
Thus, the image used in CI needs to be kept up-to-date manually.

Whenever a change is made in the dockerfiles or related files, rebuild and push the Docker images
with

```shell
make docker-push
```

### IDE setup

#### VS Code

Make sure that there is no venv folder in the directory and
install [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

To open the directory through docker press ctrl+shift+p and write the
command `Remote-Containers: Open Folder in Container...`.

This enables testing and debugging through VSCode in the docker container. Testing can be easily
configured by following the steps in the testing panel.

#### PyCharm

For proper integration with PyCharm, the Professional version is needed.

You also need to have the command `docker-compose` version installed, as opposed to the newer version which is invoked
with `docker compose` (notice the space). If you installed Docker through the official APT repository on Ubuntu, this
can be accomplished by just installing the package `docker-compose`. Both versions can coexist without any problems.

To set it up, **add a new interpreter** by going to  _Settings_ -> _Project: nir-temperature-sensor_ -> _Python Interpreter_
and clicking at the settings icon and then `Add`. Then select `Docker Compose`. If necessary, add a Docker server (the default settings should be fine
if you're not doing anything special). Set _Service_ to `debian` and _Python interpreter path_ to `python3`.

Now you should be able to run scripts and tests, as well as debug them, from within PyCharm.
Note that whenever you start a script (including any test), PyCharm restarts the Docker Compose service running the gRPC
server. This means that you will have to start it again afterwards if you want it to keep running.
