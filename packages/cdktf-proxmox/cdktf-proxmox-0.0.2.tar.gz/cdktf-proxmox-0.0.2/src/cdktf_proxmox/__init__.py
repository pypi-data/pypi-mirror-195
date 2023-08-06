'''
# Terrafrom CDK Proxmox Provider

This is a repo that builds default CDKTF bindings for the awlsring/proxmox provider. It is semi auto-generated from the providers schema using methods pulled from the HashiCorp [cdktf-provider-project](https://github.com/cdktf/cdktf-provider-project)

This repo and the provider are still in development and should not be used in production.

As this matures, additional custom constructs will be added to this to speed up the creation of VMs and other resources.

## Links

* Provider Repo: https://github.com/awlsring/terraform-provider-proxmox
* Provider Registry: https://registry.terraform.io/providers/awlsring/proxmox/latest
* ConstructHub: https://constructs.dev/packages/@awlsring/cdktf-proxmox

## Available Packages

This provider is built for the following languages:

* Javascript/Typescript
* Python
* C#

Details on how to find these packages are below and on [ConstructHub](https://constructs.dev/packages/@awlsring/cdktf-proxmox)

### NPM

Javascript/Typescript package is available on NPM.

The npm package is viewable at https://www.npmjs.com/package/@awlsring/cdktf-proxmox

```bash
npm install @awlsring/cdktf-proxmox
```

### PyPi

Python package is available on PyPi.

The pypi package is viewable at https://pypi.org/project/cdktf-proxmox/

```bash
pip install cdktf-proxmox
```

### Nuget

C# package is available on Nuget.

The nuget package is viewable at https://www.nuget.org/packages/awlsring.CdktfProxmox/

```bash
dotnet add package awlsring.CdktfProxmox
```
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

__all__ = [
    "data_proxmox_lvm_storage_classes",
    "data_proxmox_lvm_thinpool_storage_classes",
    "data_proxmox_lvm_thinpools",
    "data_proxmox_lvms",
    "data_proxmox_network_bonds",
    "data_proxmox_network_bridges",
    "data_proxmox_nfs_storage_classes",
    "data_proxmox_node_storage_lvm_thinpools",
    "data_proxmox_node_storage_lvms",
    "data_proxmox_node_storage_nfs",
    "data_proxmox_node_storage_zfs",
    "data_proxmox_nodes",
    "data_proxmox_resource_pools",
    "data_proxmox_templates",
    "data_proxmox_virtual_machines",
    "data_proxmox_zfs_pools",
    "data_proxmox_zfs_storage_classes",
    "lvm",
    "lvm_storage_class",
    "lvm_thinpool",
    "lvm_thinpool_storage_class",
    "network_bond",
    "network_bridge",
    "nfs_storage_class",
    "provider",
    "resource_pool",
    "virtual_machine",
    "zfs_pool",
    "zfs_storage_class",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import data_proxmox_lvm_storage_classes
from . import data_proxmox_lvm_thinpool_storage_classes
from . import data_proxmox_lvm_thinpools
from . import data_proxmox_lvms
from . import data_proxmox_network_bonds
from . import data_proxmox_network_bridges
from . import data_proxmox_nfs_storage_classes
from . import data_proxmox_node_storage_lvm_thinpools
from . import data_proxmox_node_storage_lvms
from . import data_proxmox_node_storage_nfs
from . import data_proxmox_node_storage_zfs
from . import data_proxmox_nodes
from . import data_proxmox_resource_pools
from . import data_proxmox_templates
from . import data_proxmox_virtual_machines
from . import data_proxmox_zfs_pools
from . import data_proxmox_zfs_storage_classes
from . import lvm
from . import lvm_storage_class
from . import lvm_thinpool
from . import lvm_thinpool_storage_class
from . import network_bond
from . import network_bridge
from . import nfs_storage_class
from . import provider
from . import resource_pool
from . import virtual_machine
from . import zfs_pool
from . import zfs_storage_class
