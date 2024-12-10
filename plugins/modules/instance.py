#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2015, René Moser <mail@renemoser.net>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: instance
short_description: Manages instances and virtual machines on Apache CloudStack based clouds.
description:
    - Deploy, start, update, scale, restart, restore, stop and destroy instances.
author: René Moser (@resmo)
version_added: 0.1.0
options:
  name:
    description:
      - Host name of the instance. C(name) can only contain ASCII letters.
      - Name will be generated (UUID) by CloudStack if not specified and can not be changed afterwards.
      - Either C(name) or C(display_name) is required.
    type: str
  display_name:
    description:
      - Custom display name of the instances.
      - Display name will be set to I(name) if not specified.
      - Either I(name) or I(display_name) is required.
    type: str
  group:
    description:
      - Group in where the new instance should be in.
    type: str
  state:
    description:
      - State of the instance.
    type: str
    default: present
    choices: [ deployed, started, stopped, restarted, restored, destroyed, expunged, present, absent ]
  service_offering:
    description:
      - Name or id of the service offering of the new instance.
      - If not set, first found service offering is used.
    type: str
  cpu:
    description:
      - The number of CPUs to allocate to the instance, used with custom service offerings
    type: int
  cpu_speed:
    description:
      - The clock speed/shares allocated to the instance, used with custom service offerings
    type: int
  memory:
    description:
      - The memory allocated to the instance, used with custom service offerings
    type: int
  template:
    description:
      - Name, display text or id of the template to be used for creating the new instance.
      - Required when using I(state=present).
      - Mutually exclusive with I(iso) option.
    type: str
  iso:
    description:
      - Name or id of the ISO to be used for creating the new instance.
      - Required when using I(state=present).
      - Mutually exclusive with I(template) option.
    type: str
  template_filter:
    description:
      - Name of the filter used to search for the template or iso.
      - Used for params I(iso) or I(template) on I(state=present).
    type: str
    default: executable
    choices: [ all, featured, self, selfexecutable, sharedexecutable, executable, community ]
    aliases: [ iso_filter ]
  hypervisor:
    description:
      - Name the hypervisor to be used for creating the new instance.
      - Relevant when using I(state=present), but only considered if not set on ISO/template.
      - If not set or found on ISO/template, first found hypervisor will be used.
      - Possible values are C(KVM), C(VMware), C(BareMetal), C(XenServer), C(LXC), C(HyperV), C(UCS), C(OVM), C(Simulator).
    type: str
  keyboard:
    description:
      - Keyboard device type for the instance.
    type: str
    choices: [ 'de', 'de-ch', 'es', 'fi', 'fr', 'fr-be', 'fr-ch', 'is', 'it', 'jp', 'nl-be', 'no', 'pt', 'uk', 'us' ]
  networks:
    description:
      - List of networks to use for the new instance.
    type: list
    elements: str
    aliases: [ network ]
  ip_address:
    description:
      - IPv4 address for default instance's network during creation.
    type: str
  ip6_address:
    description:
      - IPv6 address for default instance's network.
    type: str
  ip_to_networks:
    description:
      - "List of mappings in the form I({'network': NetworkName, 'ip': 1.2.3.4})"
      - Mutually exclusive with I(networks) option.
    type: list
    elements: dict
    aliases: [ ip_to_network ]
  disk_offering:
    description:
      - Name of the disk offering to be used.
    type: str
  disk_size:
    description:
      - Disk size in GByte required if deploying instance from ISO.
    type: int
  root_disk_size:
    description:
      - "Root disk size in GByte required if deploying instance with KVM hypervisor and want resize the root disk size at startup
        (needs CloudStack >= 4.4, cloud-initramfs-growroot installed and enabled in the template)."
    type: int
  security_groups:
    description:
      - List of security groups the instance to be applied to.
    type: list
    elements: str
    aliases: [ security_group ]
  host:
    description:
      - Host on which an instance should be deployed or started on.
      - Only considered when I(state=started) or instance is running.
      - Requires root admin privileges.
    type: str
  cluster:
    description:
      - Cluster on which an instance should be deployed or started on.
      - Only considered when I(state=started) or instance is running.
      - Requires root admin privileges.
    type: str
    version_added: 2.3.0
  pod:
    description:
      - Pod on which an instance should be deployed or started on.
      - Only considered when I(state=started) or instance is running.
      - Requires root admin privileges.
    type: str
    version_added: 2.3.0
  domain:
    description:
      - Domain the instance is related to.
    type: str
  account:
    description:
      - Account the instance is related to.
    type: str
  project:
    description:
      - Name of the project the instance to be deployed in.
    type: str
  zone:
    description:
      - Name of the zone in which the instance should be deployed.
    type: str
    required: true
  ssh_keys:
    description:
      - List of names of SSH keys to be deployed on the new instance.
    type: list
    elements: str
    aliases: [ ssh_key ]
  affinity_groups:
    description:
      - Affinity groups names to be applied to the new instance.
    type: list
    elements: str
    aliases: [ affinity_group ]
  user_data:
    description:
      - Optional data (ASCII) that can be sent to the instance upon a successful deployment.
      - The data will be automatically base64 encoded.
      - Consider switching to HTTP_POST by using I(CLOUDSTACK_METHOD=post) to increase the HTTP_GET size limit of 2KB to 32 KB.
      - Mutually exclusive with I(user_data_name) option.
    type: str
  user_data_details:
    description:
      - Map used to specify the parameters values for the variables in userdata.
    type: dict
    version_added: 2.5.0
  user_data_name:
    description:
      - Name of user data to be used.
      - Mutually exclusive with I(user_data) option.
    type: str
    version_added: 2.5.0
  force:
    description:
      - Force stop/start the instance if required to apply changes, otherwise a running instance will not be changed.
    type: bool
    default: no
  allow_root_disk_shrink:
    description:
      - Enables a volume shrinkage when the new size is smaller than the old one.
    type: bool
    default: no
  tags:
    description:
      - List of tags. Tags are a list of dictionaries having keys C(key) and C(value).
      - "If you want to delete all tags, set a empty list e.g. I(tags: [])."
    type: list
    elements: dict
    aliases: [ tag ]
  poll_async:
    description:
      - Poll async jobs until job has finished.
    type: bool
    default: yes
  details:
    description:
      - Map to specify custom parameters.
    type: dict
extends_documentation_fragment:
- ngine_io.cloudstack.cloudstack
"""

EXAMPLES = """
# NOTE: Names of offerings and ISOs depending on the CloudStack configuration.
- name: create a instance from an ISO
  ngine_io.cloudstack.instance:
    name: web-vm-1
    iso: Linux Debian 7 64-bit
    hypervisor: VMware
    project: Integration
    zone: ch-zrh-ix-01
    service_offering: 1cpu_1gb
    disk_offering: PerfPlus Storage
    disk_size: 20
    networks:
      - Server Integration
      - Sync Integration
      - Storage Integration

- name: for changing a running instance, use the 'force' parameter
  ngine_io.cloudstack.instance:
    name: web-vm-1
    zone: zone01
    display_name: web-vm-01.example.com
    iso: Linux Debian 7 64-bit
    service_offering: 2cpu_2gb
    force: yes

# NOTE: user_data can be used to kickstart the instance using cloud-init yaml config.
- name: create or update a instance on Exoscale's public cloud using display_name.
  ngine_io.cloudstack.instance:
    display_name: web-vm-1
    zone: zone01
    template: Linux Debian 7 64-bit
    service_offering: Tiny
    ssh_key: john@example.com
    tags:
      - key: admin
        value: john
      - key: foo
        value: bar
    user_data: |
        #cloud-config
        packages:
          - nginx

- name: create an instance with multiple interfaces specifying the IP addresses
  ngine_io.cloudstack.instance:
    name: web-vm-1
    zone: zone01
    template: Linux Debian 7 64-bit
    service_offering: Tiny
    ip_to_networks:
      - network: NetworkA
        ip: 10.1.1.1
      - network: NetworkB
        ip: 192.0.2.1

- name: ensure an instance is stopped
  ngine_io.cloudstack.instance:
    name: web-vm-1
    zone: zone01
    state: stopped

- name: ensure an instance is running
  ngine_io.cloudstack.instance:
    name: web-vm-1
    zone: zone01
    state: started

- name: remove an instance
  ngine_io.cloudstack.instance:
    name: web-vm-1
    zone: zone01
    state: absent
"""

RETURN = """
---
id:
  description: UUID of the instance.
  returned: success
  type: str
  sample: 04589590-ac63-4ffc-93f5-b698b8ac38b6
name:
  description: Name of the instance.
  returned: success
  type: str
  sample: web-01
display_name:
  description: Display name of the instance.
  returned: success
  type: str
  sample: web-01
group:
  description: Group name of the instance is related.
  returned: success
  type: str
  sample: web
created:
  description: Date of the instance was created.
  returned: success
  type: str
  sample: 2014-12-01T14:57:57+0100
password_enabled:
  description: True if password setting is enabled.
  returned: success
  type: bool
  sample: true
password:
  description: The password of the instance if exists.
  returned: if available
  type: str
  sample: Ge2oe7Do
ssh_keys:
  description: Names of SSH key deployed to instance.
  returned: if available
  type: list
  sample: [key@work, key@home]
  version_added: 2.5.0
domain:
  description: Domain the instance is related to.
  returned: success
  type: str
  sample: example domain
account:
  description: Account the instance is related to.
  returned: success
  type: str
  sample: example account
project:
  description: Name of project the instance is related to.
  returned: success
  type: str
  sample: Production
default_ip:
  description: Default IP address of the instance.
  returned: success
  type: str
  sample: 10.23.37.42
default_ip6:
  description: Default IPv6 address of the instance.
  returned: if available
  type: str
  sample: 2a04:c43:c00:a07:4b4:beff:fe00:74
public_ip:
  description: Public IP address with instance via static NAT rule.
  returned: if available
  type: str
  sample: 1.2.3.4
iso:
  description: Name of ISO the instance was deployed with.
  returned: if available
  type: str
  sample: Debian-8-64bit
template:
  description: Name of template the instance was deployed with.
  returned: success
  type: str
  sample: Linux Debian 9 64-bit
template_display_text:
  description: Display text of template the instance was deployed with.
  returned: success
  type: str
  sample: Linux Debian 9 64-bit 200G Disk (2017-10-08-622866)
service_offering:
  description: Name of the service offering the instance has.
  returned: success
  type: str
  sample: 2cpu_2gb
zone:
  description: Name of zone the instance is in.
  returned: success
  type: str
  sample: ch-gva-2
state:
  description: State of the instance.
  returned: success
  type: str
  sample: Running
security_groups:
  description: Security groups the instance is in.
  returned: success
  type: list
  sample: '[ "default" ]'
affinity_groups:
  description: Affinity groups the instance is in.
  returned: success
  type: list
  sample: '[ "webservers" ]'
tags:
  description: List of resource tags associated with the instance.
  returned: success
  type: list
  sample: '[ { "key": "foo", "value": "bar" } ]'
hypervisor:
  description: Hypervisor related to this instance.
  returned: success
  type: str
  sample: KVM
host:
  description: Hostname of hypervisor an instance is running on.
  returned: success and instance is running
  type: str
  sample: host-01.example.com
instance_name:
  description: Internal name of the instance (ROOT admin only).
  returned: success
  type: str
  sample: i-44-3992-VM
user-data:
  description: Optional data sent to the instance.
  returned: success
  type: str
  sample: VXNlciBkYXRhIGV4YW1wbGUK
"""

import base64

from ansible.module_utils._text import to_bytes, to_text
from ansible.module_utils.basic import AnsibleModule

from ..module_utils.cloudstack import AnsibleCloudStack, cs_argument_spec, cs_required_together


class AnsibleCloudStackInstance(AnsibleCloudStack):

    def __init__(self, module):
        super(AnsibleCloudStackInstance, self).__init__(module)
        self.returns = {
            "group": "group",
            "hypervisor": "hypervisor",
            "instancename": "instance_name",
            "publicip": "public_ip",
            "passwordenabled": "password_enabled",
            "password": "password",
            "serviceofferingname": "service_offering",
            "isoname": "iso",
            "templatename": "template",
            "templatedisplaytext": "template_display_text",
            "keypairs": "ssh_keys",
            "hostname": "host",
        }
        self.instance = None
        self.template = None
        self.iso = None

    def get_service_offering_id(self):
        service_offering = self.module.params.get("service_offering")

        service_offerings = self.query_api("listServiceOfferings")
        if service_offerings:
            if not service_offering:
                return service_offerings["serviceoffering"][0]["id"]

            for s in service_offerings["serviceoffering"]:
                if service_offering in [s["name"], s["id"]]:
                    return s["id"]
        self.fail_json(msg="Service offering '%s' not found" % service_offering)

    def get_host_id(self):
        host_name = self.module.params.get("host")
        if not host_name:
            return None

        args = {
            "type": "routing",
            "zoneid": self.get_zone(key="id"),
        }
        hosts = self.query_api("listHosts", **args)
        if hosts:
            for h in hosts["host"]:
                if host_name in [h["name"], h["id"]]:
                    return h["id"]

        self.fail_json(msg="Host '%s' not found" % host_name)

    def get_cluster_id(self):
        cluster_name = self.module.params.get("cluster")
        if not cluster_name:
            return None

        args = {"zoneid": self.get_zone(key="id")}
        clusters = self.query_api("listClusters", **args)
        if clusters:
            for c in clusters["cluster"]:
                if cluster_name in [c["name"], c["id"]]:
                    return c["id"]

        self.fail_json(msg="Cluster '%s' not found" % cluster_name)

    def get_pod_id(self):
        pod_name = self.module.params.get("pod")
        if not pod_name:
            return None

        args = {"zoneid": self.get_zone(key="id")}
        pods = self.query_api("listPods", **args)
        if pods:
            for p in pods["pod"]:
                if pod_name in [p["name"], p["id"]]:
                    return p["id"]

        self.fail_json(msg="Pod '%s' not found" % pod_name)

    def get_template_or_iso(self, key=None):
        template = self.module.params.get("template")
        iso = self.module.params.get("iso")

        if not template and not iso:
            return None

        args = {
            "account": self.get_account(key="name"),
            "domainid": self.get_domain(key="id"),
            "projectid": self.get_project(key="id"),
            "zoneid": self.get_zone(key="id"),
            "isrecursive": True,
            "fetch_list": True,
        }

        if template:
            if self.template:
                return self._get_by_key(key, self.template)

            rootdisksize = self.module.params.get("root_disk_size")
            args["templatefilter"] = self.module.params.get("template_filter")
            args["fetch_list"] = True
            templates = self.query_api("listTemplates", **args)
            if templates:
                for t in templates:
                    if template in [t.get("displaytext", None), t["name"], t["id"]]:
                        if rootdisksize and t["size"] > rootdisksize * 1024**3:
                            continue
                        self.template = t
                        return self._get_by_key(key, self.template)

            if rootdisksize:
                more_info = " (with size <= %s)" % rootdisksize
            else:
                more_info = ""

            self.module.fail_json(msg="Template '%s' not found%s" % (template, more_info))

        elif iso:
            if self.iso:
                return self._get_by_key(key, self.iso)

            args["isofilter"] = self.module.params.get("template_filter")
            args["fetch_list"] = True
            isos = self.query_api("listIsos", **args)
            if isos:
                for i in isos:
                    if iso in [i["displaytext"], i["name"], i["id"]]:
                        self.iso = i
                        return self._get_by_key(key, self.iso)

            self.module.fail_json(msg="ISO '%s' not found" % iso)

    def get_instance(self, refresh=False):
        instance = self.instance
        if not instance or refresh:
            instance_name = self.get_or_fallback("name", "display_name")
            args = {
                "account": self.get_account(key="name"),
                "domainid": self.get_domain(key="id"),
                "projectid": self.get_project(key="id"),
                "fetch_list": True,
            }
            # Do not pass zoneid, as the instance name must be unique across zones.
            instances = self.query_api("listVirtualMachines", **args)
            if instances:
                for v in instances:
                    if instance_name.lower() in [v["name"].lower(), v["displayname"].lower(), v["id"]]:

                        if "keypairs" not in v:
                            v["keypairs"] = list()

                        # Workaround for keypairs not a list
                        if not isinstance(v["keypairs"], list):
                            v["keypairs"] = [v["keypairs"]]

                        self.instance = v
                        break

        return self.instance

    def get_user_data_id_by_name(self):
        name = self.module.params.get("user_data_name")
        if not name:
            return None

        args = {
            "account": self.get_account(key="name"),
            "domainid": self.get_domain(key="id"),
            "projectid": self.get_project(key="id"),
            "listall": True,
            # name or keyword is documented but not work on cloudstack 4.19
            # commented util will work it
            # 'name': name,
        }

        user_data_list = self.query_api("listUserData", **args)
        if user_data_list:
            for v in user_data_list.get("userdata") or []:
                if name in [v["name"], v["id"]]:
                    return v["id"]
        self.module.fail_json(msg="User data '%s' not found" % user_data_list)

    def _get_instance_user_data(self, instance):
        # Query the user data if we need to
        if "userdata" in instance:
            return instance["userdata"]

        user_data = ""
        if self.get_user_data() is not None and instance.get("id"):
            res = self.query_api("getVirtualMachineUserData", virtualmachineid=instance["id"])
            user_data = res["virtualmachineuserdata"].get("userdata", "")
        return user_data

    def get_iptonetwork_mappings(self):
        network_mappings = self.module.params.get("ip_to_networks")
        if network_mappings is None:
            return

        if network_mappings and self.module.params.get("networks"):
            self.module.fail_json(msg="networks and ip_to_networks are mutually exclusive.")

        network_names = [n["network"] for n in network_mappings]
        ids = self.get_network_ids(network_names)
        res = []
        for i, data in enumerate(network_mappings):
            res.append(dict(networkid=ids[i], **data))
        return res

    def get_ssh_keypair(self, name, key=None, fail_on_missing=True):
        args = {
            "domainid": self.get_domain("id"),
            "account": self.get_account("name"),
            "projectid": self.get_project("id"),
            "name": name,
        }
        ssh_key_pairs = self.query_api("listSSHKeyPairs", **args)
        if "sshkeypair" in ssh_key_pairs:
            return self._get_by_key(key=key, my_dict=ssh_key_pairs["sshkeypair"][0])

        elif fail_on_missing:
            self.module.fail_json(msg="SSH key not found: %s" % name)

    def ssh_keys_changed(self):
        ssh_keys = self.module.params.get("ssh_keys")
        if ssh_keys is None:
            return False

        instance_ssh_keys = self.instance.get("keypairs") or [self.instance.get("keypair") or ""]

        param_ssh_key_fingerprints = [self.get_ssh_keypair(key="fingerprint", name=ssh_key) for ssh_key in ssh_keys]

        for instance_ssh_key in instance_ssh_keys:

            if not ssh_keys:
                return True

            # Get fingerprint for keypair of instance but do not fail if inexistent.
            instance_ssh_key_fingerprint = self.get_ssh_keypair(key="fingerprint", name=instance_ssh_key, fail_on_missing=False)
            if not instance_ssh_key_fingerprint:
                return True

            # Compare fingerprints to ensure the keypair changed
            if instance_ssh_key_fingerprint not in param_ssh_key_fingerprints:
                return True
        return False

    def security_groups_changed(self):
        security_groups = self.module.params.get("security_groups")
        if security_groups is None:
            return False

        security_groups = [s.lower() for s in security_groups]
        instance_security_groups = self.instance.get("securitygroup") or []

        instance_security_group_names = []
        for instance_security_group in instance_security_groups:
            if instance_security_group["name"].lower() not in security_groups:
                return True
            else:
                instance_security_group_names.append(instance_security_group["name"].lower())

        for security_group in security_groups:
            if security_group not in instance_security_group_names:
                return True
        return False

    def get_network_ids(self, network_names=None):
        if network_names is None:
            network_names = self.module.params.get("networks")

        if not network_names:
            return None

        args = {
            "account": self.get_account(key="name"),
            "domainid": self.get_domain(key="id"),
            "projectid": self.get_project(key="id"),
            "zoneid": self.get_zone(key="id"),
            "fetch_list": True,
        }
        networks = self.query_api("listNetworks", **args)
        if not networks:
            self.module.fail_json(msg="No networks available")

        network_ids = []
        network_displaytexts = []
        for network_name in network_names:
            for n in networks:
                if network_name in [n["displaytext"], n["name"], n["id"]]:
                    network_ids.append(n["id"])
                    network_displaytexts.append(n["name"])
                    break

        if len(network_ids) != len(network_names):
            self.module.fail_json(msg="Could not find all networks, networks list found: %s" % network_displaytexts)

        return network_ids

    def present_instance(self, start_vm=True):
        instance = self.get_instance()

        if not instance:
            instance = self.deploy_instance(start_vm=start_vm)
        else:
            instance = self.recover_instance(instance=instance)
            instance = self.update_instance(instance=instance, start_vm=start_vm)

        # In check mode, we do not necessarily have an instance
        if instance:
            instance = self.get_instance(refresh=True)
            instance = self.ensure_tags(resource=instance, resource_type="UserVm")
            # refresh instance data
            self.instance = instance

        return instance

    def get_user_data(self):
        user_data = self.module.params.get("user_data")
        if user_data is not None:
            user_data = to_text(base64.b64encode(to_bytes(user_data)))
        return user_data

    def get_details(self):
        details = self.module.params.get("details")

        cpu = self.module.params.get("cpu")
        cpu_speed = self.module.params.get("cpu_speed")
        memory = self.module.params.get("memory")

        if any([cpu, cpu_speed, memory]):
            if details is None:
                details = {}

            if cpu:
                details["cpuNumber"] = cpu

            if cpu_speed:
                details["cpuSpeed"] = cpu_speed

            if memory:
                details["memory"] = memory

        return details

    def deploy_instance(self, start_vm=True):
        self.result["changed"] = True
        networkids = self.get_network_ids()
        if networkids is not None:
            networkids = ",".join(networkids)

        args = {}
        args["templateid"] = self.get_template_or_iso(key="id")
        if not args["templateid"]:
            self.module.fail_json(msg="Template or ISO is required.")

        args["zoneid"] = self.get_zone(key="id")
        args["serviceofferingid"] = self.get_service_offering_id()
        args["account"] = self.get_account(key="name")
        args["domainid"] = self.get_domain(key="id")
        args["projectid"] = self.get_project(key="id")
        args["diskofferingid"] = self.get_disk_offering(key="id")
        args["networkids"] = networkids
        args["iptonetworklist"] = self.get_iptonetwork_mappings()
        args["userdata"] = self.get_user_data()
        args["userdataid"] = self.get_user_data_id_by_name()
        args["userdatadetails"] = self.module.params.get("user_data_details")
        args["keyboard"] = self.module.params.get("keyboard")
        args["ipaddress"] = self.module.params.get("ip_address")
        args["ip6address"] = self.module.params.get("ip6_address")
        args["name"] = self.module.params.get("name")
        args["displayname"] = self.get_or_fallback("display_name", "name")
        args["group"] = self.module.params.get("group")
        args["keypairs"] = self.module.params.get("ssh_keys")
        args["size"] = self.module.params.get("disk_size")
        args["startvm"] = start_vm
        args["rootdisksize"] = self.module.params.get("root_disk_size")
        args["affinitygroupnames"] = self.module.params.get("affinity_groups")
        args["details"] = self.get_details()
        args["securitygroupnames"] = self.module.params.get("security_groups")
        args["hostid"] = self.get_host_id()
        args["clusterid"] = self.get_cluster_id()
        args["podid"] = self.get_pod_id()

        template_iso = self.get_template_or_iso()
        if template_iso and "hypervisor" not in template_iso:
            args["hypervisor"] = self.get_hypervisor()

        instance = None
        if not self.module.check_mode:
            instance = self.query_api("deployVirtualMachine", **args)

            poll_async = self.module.params.get("poll_async")
            if poll_async:
                instance = self.poll_job(instance, "virtualmachine")
        return instance

    def update_instance(self, instance, start_vm=True):
        # Service offering data
        args_service_offering = {
            "id": instance["id"],
        }
        if self.module.params.get("service_offering"):
            args_service_offering["serviceofferingid"] = self.get_service_offering_id()
        service_offering_changed = self.has_changed(args_service_offering, instance)

        # Instance UserData
        if self.module.params.get("user_data_name") is not None:
            args_instance_update = {"id": instance["id"], "userdataid": self.get_user_data_id_by_name()}
        else:
            args_instance_update = {"id": instance["id"], "userdata": self.get_user_data()}
            instance["userdata"] = self._get_instance_user_data(instance)

        if self.module.params.get("user_data_details"):
            args_instance_update["userdatadetails"] = self.module.params.get("user_data_details")

        args_instance_update["ostypeid"] = self.get_os_type(key="id")
        if self.module.params.get("group"):
            args_instance_update["group"] = self.module.params.get("group")
        if self.module.params.get("display_name"):
            args_instance_update["displayname"] = self.module.params.get("display_name")
        instance_changed = self.has_changed(args_instance_update, instance)

        ssh_keys_changed = self.ssh_keys_changed()

        security_groups_changed = self.security_groups_changed()

        # Volume data
        args_volume_update = {}
        root_disk_size = self.module.params.get("root_disk_size")
        root_disk_size_changed = False

        if root_disk_size is not None:
            args = {
                "type": "ROOT",
                "virtualmachineid": instance["id"],
                "account": instance.get("account"),
                "domainid": instance.get("domainid"),
                "projectid": instance.get("projectid"),
            }
            res = self.query_api("listVolumes", **args)
            [volume] = res["volume"]

            size = volume["size"] >> 30

            args_volume_update["id"] = volume["id"]
            args_volume_update["size"] = root_disk_size

            shrinkok = self.module.params.get("allow_root_disk_shrink")
            if shrinkok:
                args_volume_update["shrinkok"] = shrinkok

            root_disk_size_changed = root_disk_size != size

        changed = [
            service_offering_changed,
            instance_changed,
            security_groups_changed,
            ssh_keys_changed,
            root_disk_size_changed,
        ]

        if any(changed):
            force = self.module.params.get("force")
            instance_state = instance["state"].lower()
            if instance_state == "stopped" or force:
                self.result["changed"] = True
                if not self.module.check_mode:

                    # Ensure VM has stopped
                    instance = self.stop_instance()
                    instance = self.poll_job(instance, "virtualmachine")
                    self.instance = instance

                    # Change service offering
                    if service_offering_changed:
                        res = self.query_api("changeServiceForVirtualMachine", **args_service_offering)
                        instance = res["virtualmachine"]
                        self.instance = instance

                    # Update VM
                    if instance_changed or security_groups_changed:
                        if security_groups_changed:
                            args_instance_update["securitygroupnames"] = ",".join(self.module.params.get("security_groups"))
                        res = self.query_api("updateVirtualMachine", **args_instance_update)
                        instance = res["virtualmachine"]
                        self.instance = instance

                    # Reset SSH key
                    if ssh_keys_changed:
                        # SSH key data
                        args_ssh_key = {
                            "id": instance["id"],
                            "projectid": self.get_project(key="id"),
                            "keypairs": self.module.params.get("ssh_keys"),
                        }
                        instance = self.query_api("resetSSHKeyForVirtualMachine", **args_ssh_key)
                        instance = self.poll_job(instance, "virtualmachine")
                        self.instance = instance

                    # Root disk size
                    if root_disk_size_changed:
                        async_result = self.query_api("resizeVolume", **args_volume_update)
                        self.poll_job(async_result, "volume")

                    # Start VM again if it was running before
                    if instance_state == "running" and start_vm:
                        instance = self.start_instance()
            else:
                self.module.warn(
                    "Changes won't be applied to running instances. " "Use force=true to allow the instance %s to be stopped/started." % instance["name"]
                )

        # migrate to other host
        host_changed = all(
            [
                instance["state"].lower() in ["starting", "running"],
                instance.get("hostname") is not None,
                self.module.params.get("host") is not None,
                self.module.params.get("host") != instance.get("hostname"),
            ]
        )
        if host_changed:
            self.result["changed"] = True
            args_host = {
                "virtualmachineid": instance["id"],
                "hostid": self.get_host_id(),
            }
            if not self.module.check_mode:
                res = self.query_api("migrateVirtualMachine", **args_host)
                instance = self.poll_job(res, "virtualmachine")

        return instance

    def recover_instance(self, instance):
        if instance["state"].lower() in ["destroying", "destroyed"]:
            self.result["changed"] = True
            if not self.module.check_mode:
                res = self.query_api("recoverVirtualMachine", id=instance["id"])
                instance = res["virtualmachine"]
        return instance

    def absent_instance(self):
        instance = self.get_instance()
        if instance:
            if instance["state"].lower() not in ["expunging", "destroying", "destroyed"]:
                self.result["changed"] = True
                if not self.module.check_mode:
                    res = self.query_api("destroyVirtualMachine", id=instance["id"])

                    poll_async = self.module.params.get("poll_async")
                    if poll_async:
                        instance = self.poll_job(res, "virtualmachine")
        return instance

    def expunge_instance(self):
        instance = self.get_instance()
        if instance:
            res = {}
            if instance["state"].lower() in ["destroying", "destroyed"]:
                self.result["changed"] = True
                if not self.module.check_mode:
                    res = self.query_api("destroyVirtualMachine", id=instance["id"], expunge=True)

            elif instance["state"].lower() not in ["expunging"]:
                self.result["changed"] = True
                if not self.module.check_mode:
                    res = self.query_api("destroyVirtualMachine", id=instance["id"], expunge=True)

            poll_async = self.module.params.get("poll_async")
            if poll_async:
                res = self.poll_job(res, "virtualmachine")
        return instance

    def stop_instance(self):
        instance = self.get_instance()
        # in check mode instance may not be instantiated
        if instance:
            if instance["state"].lower() in ["stopping", "stopped"]:
                return instance

            if instance["state"].lower() in ["starting", "running"]:
                self.result["changed"] = True
                if not self.module.check_mode:
                    instance = self.query_api("stopVirtualMachine", id=instance["id"])

                    poll_async = self.module.params.get("poll_async")
                    if poll_async:
                        instance = self.poll_job(instance, "virtualmachine")
        return instance

    def start_instance(self):
        instance = self.get_instance()
        # in check mode instance may not be instantiated
        if instance:
            if instance["state"].lower() in ["starting", "running"]:
                return instance

            if instance["state"].lower() in ["stopped", "stopping"]:
                self.result["changed"] = True
                if not self.module.check_mode:
                    args = {
                        "id": instance["id"],
                        "hostid": self.get_host_id(),
                    }
                    instance = self.query_api("startVirtualMachine", **args)

                    poll_async = self.module.params.get("poll_async")
                    if poll_async:
                        instance = self.poll_job(instance, "virtualmachine")
        return instance

    def restart_instance(self):
        instance = self.get_instance()
        # in check mode instance may not be instantiated
        if instance:
            if instance["state"].lower() in ["running", "starting"]:
                self.result["changed"] = True
                if not self.module.check_mode:
                    instance = self.query_api("rebootVirtualMachine", id=instance["id"])

                    poll_async = self.module.params.get("poll_async")
                    if poll_async:
                        instance = self.poll_job(instance, "virtualmachine")

            elif instance["state"].lower() in ["stopping", "stopped"]:
                instance = self.start_instance()
        return instance

    def restore_instance(self):
        instance = self.get_instance()
        self.result["changed"] = True
        # in check mode instance may not be instantiated
        if instance:
            args = {}
            args["templateid"] = self.get_template_or_iso(key="id")
            args["virtualmachineid"] = instance["id"]
            res = self.query_api("restoreVirtualMachine", **args)

            poll_async = self.module.params.get("poll_async")
            if poll_async:
                instance = self.poll_job(res, "virtualmachine")
        return instance

    def get_result(self, resource):
        resource = self.get_instance(refresh=True)
        super(AnsibleCloudStackInstance, self).get_result(resource)
        if resource:
            self.result["user_data"] = self._get_instance_user_data(resource)
            if "securitygroup" in resource:
                security_groups = []
                for securitygroup in resource["securitygroup"]:
                    security_groups.append(securitygroup["name"])
                self.result["security_groups"] = security_groups
            if "affinitygroup" in resource:
                affinity_groups = []
                for affinitygroup in resource["affinitygroup"]:
                    affinity_groups.append(affinitygroup["name"])
                self.result["affinity_groups"] = affinity_groups
            if "nic" in resource:
                for nic in resource["nic"]:
                    if nic["isdefault"]:
                        if "ipaddress" in nic:
                            self.result["default_ip"] = nic["ipaddress"]
                        if "ip6address" in nic:
                            self.result["default_ip6"] = nic["ip6address"]
        return self.result


def main():
    argument_spec = cs_argument_spec()
    argument_spec.update(
        dict(
            name=dict(),
            display_name=dict(),
            group=dict(),
            state=dict(choices=["present", "deployed", "started", "stopped", "restarted", "restored", "absent", "destroyed", "expunged"], default="present"),
            service_offering=dict(),
            cpu=dict(type="int"),
            cpu_speed=dict(type="int"),
            memory=dict(type="int"),
            template=dict(),
            iso=dict(),
            template_filter=dict(
                default="executable",
                aliases=["iso_filter"],
                choices=["all", "featured", "self", "selfexecutable", "sharedexecutable", "executable", "community"],
            ),
            networks=dict(type="list", elements="str", aliases=["network"]),
            ip_to_networks=dict(type="list", elements="dict", aliases=["ip_to_network"]),
            ip_address=dict(),
            ip6_address=dict(),
            disk_offering=dict(),
            disk_size=dict(type="int"),
            root_disk_size=dict(type="int"),
            keyboard=dict(type="str", choices=["de", "de-ch", "es", "fi", "fr", "fr-be", "fr-ch", "is", "it", "jp", "nl-be", "no", "pt", "uk", "us"]),
            hypervisor=dict(),
            host=dict(),
            cluster=dict(),
            pod=dict(),
            security_groups=dict(type="list", elements="str", aliases=["security_group"]),
            affinity_groups=dict(type="list", elements="str", aliases=["affinity_group"]),
            domain=dict(),
            account=dict(),
            project=dict(),
            user_data=dict(),
            user_data_name=dict(),
            user_data_details=dict(type="dict"),
            zone=dict(required=True),
            ssh_keys=dict(type="list", elements="str", aliases=["ssh_key"], no_log=False),
            force=dict(type="bool", default=False),
            tags=dict(type="list", elements="dict", aliases=["tag"]),
            details=dict(type="dict"),
            poll_async=dict(type="bool", default=True),
            allow_root_disk_shrink=dict(type="bool", default=False),
        )
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_together=cs_required_together(),
        required_one_of=(["display_name", "name"],),
        mutually_exclusive=(
            ["template", "iso"],
            ["user_data", "user_data_name"],
        ),
        supports_check_mode=True,
    )

    ainstance = AnsibleCloudStackInstance(module)

    state = module.params.get("state")

    if state in ["absent", "destroyed"]:
        instance = ainstance.absent_instance()

    elif state in ["expunged"]:
        instance = ainstance.expunge_instance()

    elif state in ["restored"]:
        ainstance.present_instance()
        instance = ainstance.restore_instance()

    elif state in ["present", "deployed"]:
        instance = ainstance.present_instance()

    elif state in ["stopped"]:
        ainstance.present_instance(start_vm=False)
        instance = ainstance.stop_instance()

    elif state in ["started"]:
        ainstance.present_instance()
        instance = ainstance.start_instance()

    elif state in ["restarted"]:
        ainstance.present_instance()
        instance = ainstance.restart_instance()

    if instance and "state" in instance and instance["state"].lower() == "error":
        module.fail_json(msg="Instance named '%s' in error state." % module.params.get("name"))

    result = ainstance.get_result(instance)
    module.exit_json(**result)


if __name__ == "__main__":
    main()