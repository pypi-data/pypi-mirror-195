<div id="top"></div>

# Frontier Smart API and Firmware Analysis Tools

![LastEdit](https://img.shields.io:/static/v1?label=LastEdit&message=03/05/2023&color=9cf)
![Platform](https://img.shields.io:/static/v1?label=Platforms&message=Linux|Windows&color=yellowgreen)
[![Documentation Status](https://readthedocs.org/projects/frontier-smart-api/badge/?version=latest)](https://frontier-smart-api.readthedocs.io/en/latest/?badge=latest)
![PyPi](https://img.shields.io:/static/v1?label=PyPi&message=0.3.2&color=green)

The project `fsapi-tools` bundles different utilites that can be used to interact with Frontier-Smart devices and to inspect their firmware binaries. In addition to that, an ECMAScript decompiler wrapper is included so that compiled files can be edited as well. 

**Note**: The decompiler was initially forked from the [dead0007](https://github.com/molnarg/dead0007/blob/master/README.md) repository.

Allthough there are some repositories that focus on that specific API, the implementation provided here contains all available `Nodes` that were invented/developed by Frontier Smart. The nodes were converted from `java` source code (The [Tool](apk/node_converter.py) is also in this repository).

In order to use the tools provided by this repository, almost all available firmware binaries have been collected and stored in the [frontier-smart-firmwares](https://github.com/MatrixEditor/frontier-smart-firmwares) repository. Most of them were forked from [here](https://github.com/cweiske/frontier-silicon-firmwares). 

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#documents">Documents</a></li>
    <li>
      <a href="#overview">Overview</a>
    </li>
    <li>
      <a href="#tools">Tools</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

---
## Documents

A detailed review of the firmware binaries that are used to update Frontier Smart devicesis provided in the following document: [`firmware-2.0`](https://github.com/MatrixEditor/frontier-smart-api/blob/main/docs/firmware-2.0.md). The FSAPI (NetRemoteApi) by Frontier-Smart is described here: [frontier-smart-api documentation](https://frontier-smart-api.readthedocs.io/). For decompiling the ECMAScript

**Notice (UNIX only)**: Since version `0.2.0` there is another sub-module placed in the `fsapi` directory - named `ecmascript`. Its functionalities are described in the [fsapi.ecmascript](https://frontier-smart-api.readthedocs.io/en/latest/api/ecmascript/) part of the documentation.

## Overview
---

As stated above, this repository provides a uitlity to interact with the FSAPI (Frontier Smart API):

```python
from fsapi.netremote import *

# At first, we have to declare our device
radio = RadioHttp('127.0.0.1')

# To query the friendly name of a radio, simple call netremote_request
result = netremote_request(GET, nodes.BaseSysInfoFriendlyName, radio)

# The result will be of type "BaseSysInfoFriendlyName"
node = result.content
print("FriendlyName:", node.value)
```

List nodes and editable nodes can be queried as well (with `LIST_GET_NEXT` and `SET`). Make sure you read the API-Docs before applying random values to editable nodes ([link](https://frontier-smart-api.readthedocs.io/en/latest/api/netremote/index.html)).

To be able to parse ISU firmware files, an instance of an `ISUInspector` should  be created. The simplest way is to define a string that contains the product specification:

```python
from fsapi.isu import *

# get the inspector instance for ir-mmi-FS2026-...
inspector = get_instance('ir/mmi/FS2026')

# To inspect file we need a ISUFileBuffer
buf = ISUFileBuffer("ir-mmi-FS2026-...isu.bin")

# load an ISUHeader object and print the loaded data
header = inspector.get_header(buf, verbose=True)
print(header)
```

See more examples and usage information on this library at the API-Docs [here](https://frontier-smart-api.readthedocs.io).

## Tools

There are three tools included in this repository: `fsapi.isu`,  `fsapi` and `fsapi.ecmascript`. These can be installed directly via pip:

```bash
$ pip install fsapi-tools
```

If you want to clone this repository and install the development version of this repository, follow the next instructions.

#### __Prerequisites__

Make sure you have installed the latest version of python `setuptools` and `pip`:
```bash
$ pip install setuptools
```

#### __Installation__

This respository uses setuptools to install the python packages locally. All dependnecies used by the provided libraries should be installed by default. To install the preferred package, just type the following command:

```bash
$ pip install .
``` 

This command should install the selected library to the local site-packages. Now, you are good to go - execute the module with

```bash
python3 -m $module --help
```


### ISUInspector
---

```console
$ python3 -m fsapi.isu --help
usage: __main__.py [-h] -if IF [-of OF] [--verbose] [-insp INSP] [--header] [--archive] [-e] [--core]

optional arguments:
  -h, --help            show this help message and exit
  -if IF                The input file (optional *.isu.bin or *.ota.bin extension)
  -of OF                The output file (Format: XML).
  --verbose, -v         Prints useful information during the specified process.
  --insp INSP, -I INSP  Sets the ISUInspector descriptor, which will be used to retrieve the inspector instance.

information gathering:
  --header, -H          Parses the header of the given file and extracts information.
  --archive, -A         Parses the directory archive.

extract data:
  -e, --extract         Extract data (usually combined with other parameters).
  --core, -C            Extract the compressed core partition source.
```

<details>
<summary>Example of <code>fsapi.isu</code>:</summary>

```console
$ python3 -m fsapi.isu -if bin/FS2026/0500/ir-mmi-FS2026-0500-0015.2.5.15.EX44478-1B9.isu.bin -H -v
  ╦╔═╗╦ ╦   ╦┌┐┌┌─┐┌─┐┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║╚═╗║ ║───║│││└─┐├─┘├┤ │   │ │ │├┬┘
  ╩╚═╝╚═╝   ╩┘└┘└─┘┴  └─┘└─┘ ┴ └─┘┴└─
───────────────────────────────────────────

[+] Analyzing ISU File header...
  - MeOS Version: 1
  - Version: '2.5.15.EX44478-1B9'
    | SDK Version: IR2.5.15 SDK
    | Revision: 44478
    | Branch: None
  - Customisation: 'ir-mmi-FS2026-0500-0015'
    | DeviceType: internet radio
    | Interface: multi media interface
    | Module: Venice 6 (version=0500)

[+] SystemEntries:
  - SysEntry: type=0, partition=1, web_partition=False
  - SysEntry: type=0, partition=2, web_partition=True
  - SysEntry: type=1, partition=14, web_partition=False

[+] Declared Fields:
  - DecompBuffer: Buffer=2957053952
  - CompSize: Size=1384319
  - DecompSize: Size=2621504
  - CodeSize: Size=7760
  - CompBuffer: Buffer=2952790016
```

</details>

---

### FSAPI

```console
$ python3 -m fsapi --help
usage: __main__.py [-h] [-W PIN] [-v] {explore,isu,get,set,list} ... target

A python implementation of the FSAPI with all possible nodes. You can execute the fsapi.isu or fsapi.ecmascript module by typing the same command but with their module name.

positional arguments:
  {explore,isu,get,set,list}
                        sub-commands:
    explore             Node Exploration
    isu                 ISU Firmware Context
    get                 Request a simple property
    set                 Apply a value to a stored property.
    list                Query property lists

optional arguments:
  -h, --help            show this help message and exit

Global options:
  target                The host address in IPv4 format.
  -W PIN, --pin PIN     A PIN used by the device (default 1234).
  -v, --verbose         Prints useful information during the specified process.
```
    
<details>
<summary>Example of <code>fsapi</code>:</summary>

```console
$ python3 -m fsapi set -n netRemote.sys.info.friendlyName --args value:MedionIR $IP_ADDRESS
[+] fsapiResponse of netRemote.sys.info.friendlyName:
    - status: FS_OK

$ python3 -m fsapi get -n netRemote.sys.info.friendlyName $IP_ADDRESS
[+] fsapiResponse of netRemote.sys.info.friendlyName:
    - status: FS_OK
    - value: MedionIR
    - readonly: False
    - notifying: True

$ python3 -m fsapi isu --find $IP_ADDRESS

[+] Generating current URL...
    - url: https://update.wifiradiofrontier.com/Update.aspx?f=/updates/ir-mmi-FS2026-0500-0549.2.12.25c.EX72088-1A12.isu.bin
```

</details>

---

### ECMAScript

This module/tool is still under development and can cause errors an execution. Also, this tool can only be called on UNIX systems that are able to execute the `./decompiler/ecma-decompiler` binary.

```console
$ py -m fsapi.ecmascript --help
usage: __main__.py [-h] [-d] [-o OUT] [--use-decompiler DECOMPATH] [-r] path

positional arguments:
  path                  The target file that will be used to operate on.

optional arguments:
  -h, --help            show this help message and exit
  -d, --decompile       Indicates that the given input file should be decompiled.
  -o OUT, --out OUT     The path were the decompiled output should be saved.

  --use-decompiler DECOMPATH
                        Specifies the path to the decompiler.
  -r, --recurse         Indicates that all files in the given directory should be decompiled
```


<!-- LICENSE -->
## License

Distributed under the MIT License. See `MIT.txt` for more information.

