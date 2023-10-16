from apig_sdk import signer
import requests
import csv
import json
import yaml


cloudregion = 'ru-moscow-1'                                                 # Регион для вызова API
cloudproject = 'здесь должен быть идентификатор проекта/тенанта'            # ID проекта, можно найти в консоли или раскомментировать ниже секцию Cloud Project
credentials = "credentials.csv"                                             # Файл с учетными данными SberCloud
company_domain = 'berezka'                                                  # Префикс/домен компании для наименвоания сущностей
dc = 'идентификатор ЦОД/IaaS из сущности seaf.ta.services.dc'               # Идентификатор сущности

tenant = cloudproject
########### Выберем услуги

servers = False                         # Elastic Cloud Server
eip = False                             # Elastic IP (external ip addresses)
vault = False                           # Cloud Backup and Recovery vaults
backup_policy = False                   # Cloud Backup and Recovery policies
rds = False                             # Relational Database Service                     
natgateway = False                      # NAT Gateway
elb = False                             # Elastic Load Balance
cce = True                              # Cloud Container Engine
dms = False                             # Distributed Message Server

#############       Must        #############
secgroups = True                        # Security Groups
vpcs = True                            # VPC
subnets = True                         # Subnets 
peer = True                            # VPC peerings
#############   End of Must     #############

class IndentDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(IndentDumper, self).increase_indent(flow, False)


def get_scloud(**kwarg):
    ''' Getting SberCloud Data With REST API
        Use params to properly read the data
'''
    # Getting creds from csv
    with open(credentials) as credentials_file:              
        csv_reader = csv.DictReader(credentials_file, delimiter=",")
        for row in csv_reader:
            user_name = row['User Name']
            access_key = row['Access Key Id']
            secret_key = row['Secret Access Key']
    ######################################################
    # Creating Signature object for further use as a request        
    sig = signer.Signer()
    sig.Key = access_key
    sig.Secret = secret_key
    ######################################################

    # Working with request according to parameters set
    if kwarg['service'] == 'ecs' and kwarg['item'] == None and kwarg['s_type'] == None:
        cloud_query = f"https://{kwarg['service']}.{kwarg['region']}.hc.sbercloud.ru/v1/{kwarg['project']}/cloudservers/detail?limit=50"
        paginated = True                                           # Setting paginated output to True
    elif kwarg['service'] == 'ecs' and kwarg['s_type'] == 'nic':
        cloud_query = f"https://{kwarg['service']}.{kwarg['region']}.hc.sbercloud.ru/v1/{kwarg['project']}/cloudservers/{kwarg['item']}/os-interface"
        paginated = False  
    elif kwarg['service'] == 'vpc' and kwarg['s_type'] == None:        
        cloud_query = f"https://{kwarg['service']}.{kwarg['region']}.hc.sbercloud.ru/v1/{kwarg['project']}/vpcs"
        paginated = False
    elif kwarg['service'] == 'eip' and kwarg['s_type'] == None:
        cloud_query = f"https://vpc.{kwarg['region']}.hc.sbercloud.ru/v1/{kwarg['project']}/publicips"
        paginated = False
    elif kwarg['service'] == 'evs':
        cloud_query = f"https://{kwarg['service']}.{kwarg['region']}.hc.sbercloud.ru/v2/{kwarg['project']}/os-vendor-volumes/{kwarg['item']}"
        paginated = False
    elif kwarg['service'] == 'vpc' and kwarg['s_type'] == 'subnet':
        cloud_query = f"https://{kwarg['service']}.{kwarg['region']}.hc.sbercloud.ru/v1/{kwarg['project']}/subnets"
        paginated = False
    elif kwarg['service'] == 'vpc' and kwarg['s_type'] == 'security-groups':
        cloud_query = f"https://{kwarg['service']}.{kwarg['region']}.hc.sbercloud.ru/v1/{kwarg['project']}/{kwarg['s_type']}"
        paginated = False
    elif kwarg['service'] == 'vpc' and kwarg['s_type'] == 'peering':
        cloud_query = f"https://{kwarg['service']}.{kwarg['region']}.hc.sbercloud.ru/v2.0/vpc/peerings"
        paginated = False
    elif kwarg['service'] == 'vpc' and kwarg['s_type'] == 'routes':
        cloud_query = f"https://{kwarg['service']}.{kwarg['region']}.hc.sbercloud.ru/v2.0/vpc/routes"
        paginated = False
    elif kwarg['service'] == 'cbr' and kwarg['s_type'] == 'vault':
        cloud_query = f"https://{kwarg['service']}.{kwarg['region']}.hc.sbercloud.ru/v3/{kwarg['project']}/vaults"
        paginated = False
    elif kwarg['service'] == 'cbr' and kwarg['s_type'] == 'policy':
        cloud_query = f"https://{kwarg['service']}.{kwarg['region']}.hc.sbercloud.ru/v3/{kwarg['project']}/policies"
        paginated = False
    elif kwarg['service'] == 'rds' and kwarg['s_type'] == None:
        cloud_query = f"https://{kwarg['service']}.{kwarg['region']}.hc.sbercloud.ru/v3/{kwarg['project']}/instances"
        paginated = False
    elif kwarg['service'] == 'iam':
        cloud_query = f"https://{kwarg['service']}.{kwarg['region']}.hc.sbercloud.ru/v3/projects"
        paginated = False
    elif kwarg['service'] == 'vpc' and kwarg['s_type'] == 'port' and kwarg['item'] != None:
        cloud_query = f"https://{kwarg['service']}.{kwarg['region']}.hc.sbercloud.ru/v1/ports/{kwarg['item']}"
        paginated = False
    elif kwarg['service'] == 'vpc' and kwarg['s_type'] == 'ports':
        cloud_query = f"https://{kwarg['service']}.{kwarg['region']}.hc.sbercloud.ru/v1/ports?device_id={kwarg['item']}"
        paginated = False 
    elif kwarg['service'] == 'vpc' and kwarg['s_type'] == 'port_filter' and kwarg['item'] != None:
        cloud_query = f"https://{kwarg['service']}.{kwarg['region']}.hc.sbercloud.ru/v1/ports?{kwarg['item']}"
        paginated = False
    elif kwarg['service'] == 'vpc' and kwarg['s_type'] == 'privateips':
        cloud_query = f"https://{kwarg['service']}.{kwarg['region']}.hc.sbercloud.ru/v1/{kwarg['project']}/subnets/{kwarg['item']}/privateips"
        paginated = False
    elif kwarg['service'] == 'nat' and kwarg['s_type'] == 'gateway' and kwarg['item'] == None: 
        cloud_query = f"https://{kwarg['service']}.{kwarg['region']}.hc.sbercloud.ru/v2/{kwarg['project']}/nat_gateways"
        paginated = False
    elif kwarg['service'] == 'nat' and (kwarg['s_type'] == 'snat' or kwarg['s_type'] == 'dnat'): 
        cloud_query = f"https://{kwarg['service']}.{kwarg['region']}.hc.sbercloud.ru/v2/{kwarg['project']}/{kwarg['s_type']}_rules"
        paginated = False
    elif kwarg['service'] == 'elb' and kwarg['s_type'] == 'lb': 
        cloud_query = f"https://{kwarg['service']}.{kwarg['region']}.hc.sbercloud.ru/v2/{kwarg['project']}/elb/loadbalancers"
        paginated = False
    elif kwarg['service'] == 'elb' and kwarg['s_type'] in ['pools', 'listeners', 'poolmembers']: 
        if kwarg['s_type'] == 'poolmembers':
            cloud_query = f"https://{kwarg['service']}.{kwarg['region']}.hc.sbercloud.ru/v2/{kwarg['project']}/elb/pools/{kwarg['item']}/members"
        elif kwarg['s_type'] == 'pools' and kwarg['item'] == None:
            cloud_query = f"https://{kwarg['service']}.{kwarg['region']}.hc.sbercloud.ru/v2/{kwarg['project']}/elb/pools"
        else:
            cloud_query = f"https://{kwarg['service']}.{kwarg['region']}.hc.sbercloud.ru/v2/{kwarg['project']}/elb/{kwarg['s_type']}/{kwarg['item']}"
        paginated = False
    elif kwarg['service'] == 'elb' and kwarg['s_type'] == 'l7policies':
        if kwarg['item'] != None:
            cloud_query = f"https://{kwarg['service']}.{kwarg['region']}.hc.sbercloud.ru/v2/{kwarg['project']}/elb/l7policies?{kwarg['item']}"
        else:
            cloud_query = f"https://{kwarg['service']}.{kwarg['region']}.hc.sbercloud.ru/v2/{kwarg['project']}/elb/l7policies"
        paginated = False
    elif kwarg['service'] == 'cce':
        if kwarg['s_type'] == 'clusters': 
            cloud_query = f"https://{kwarg['service']}.{kwarg['region']}.hc.sbercloud.ru/api/v3/projects/{kwarg['project']}/clusters"
        paginated = False
    elif kwarg['service'] == 'dms':
        cloud_query = f"https://{kwarg['service']}.{kwarg['region']}.hc.sbercloud.ru/v1.0/{kwarg['project']}/instances"
        paginated = False
    ######################################################
    
    if cloud_query != None:
        r = signer.HttpRequest("GET", cloud_query)
        if kwarg['project'] != None:
            r.headers = {"X-Project-Id": kwarg['project']}
        if kwarg['service'] == 'cce':
            r.headers = {"Content-Type": "application/json;charset=utf-8"}
        sig.Sign(r)
        resp = requests.request(r.method, r.scheme + "://" + r.host + r.uri, headers=r.headers, data=r.body)
        result = ''
        jsondata = json.loads(resp.text)
        if kwarg['service'] == 'ecs' and kwarg['s_type'] == None:
            jsondata_ecs = jsondata['servers']
        if paginated == True:
            pages = (jsondata['count'] // 50) + (jsondata['count'] % 50 > 0)
            if pages > 1:
                page = 2
                while page <= pages:
                    cloud_query = f"https://{kwarg['service']}.{kwarg['region']}.hc.sbercloud.ru/v1/{kwarg['project']}/cloudservers/detail?limit=50&offset={page}"
                    page += 1
                    r = signer.HttpRequest("GET", cloud_query)
                    r.headers = {"X-Project-Id": kwarg['project']}
                    sig.Sign(r)
                    resp = requests.request(r.method, r.scheme + "://" + r.host + r.uri, headers=r.headers, data=r.body)
                    temp = json.loads(resp.text)
                    jsondata_ecs += temp['servers']
                jsondata = jsondata_ecs
            else:
                jsondata = jsondata_ecs
        #print(resp.status_code, resp.reason)
        return jsondata

########### Cloud Project Section ##########
#cloudprojects = get_scloud(service='iam', s_type='iam', region=cloudregion, project=None, item=None)
# #print(cloudproject)

########### End Of Cloud Project Section ###########


#############################################
###############  Сервисное  #################
#############################################
ports = False                           # Network Ports - only for service needs
privateips = False                      # Private IP Addresses - only for service needs
s1 = False
routes = False

if routes == True:
    y = get_scloud(service='vpc', s_type='routes', region=cloudregion, project=cloudproject, item=None)
    print(y)

if privateips == True:
    privateips = get_scloud(service='vpc', s_type='privateips', region=cloudregion, project=cloudproject, item='87371e52-f096-4fff-a085-d70782e38706')
    print(privateips)

if ports == True:
    port = '18f854e2-1189-44ba-ab12-ddf88d788de7'
    ports = get_scloud(service='vpc', s_type='port_filter', region=cloudregion, project=cloudproject, item=f"id={port}")
    print(ports)

if s1 == True: 
    interface = get_scloud(service='ecs', s_type='nic', region=cloudregion, project=cloudproject, item='96646bd6-bc01-4dd7-868e-cb336abaee07')
    print(interface)
#############################################
#############  Сервисное конец  #############
#############################################

#########     Distributed Message Services Export    #########
if dms == True:
    dmss = get_scloud(service='dms', s_type=None, region=cloudregion, project=cloudproject, item=None)
    
    result = {'seaf.ta.reverse.cloud_ru.advanced.dmss':{}}
    for dms in dmss['instances']:
        id = dms['instance_id']

        if 'management_connect_address' in dms:
            mca = dms['management_connect_address']
        else: 
            mca = ''

        yaml_structure = {
            'id': id,
            'name': dms['name'],
            'engine': dms['engine'],
            'engine_version': dms['engine_version'],
            'port': dms['port'],
            'address': dms['connect_address'],
            'vpc_id': dms['vpc_id'],
            'subnet_id': dms['subnet_id'],
            'status': dms['status'],
            'type': dms['type'],
            'specification': dms['specification'],
            'security_groups': [dms['security_group_id']],
            'available_az': dms['available_zones'],
            'storage_space': dms['storage_space'],
            'total_storage_space': dms['total_storage_space'],
            'used_storage_space': dms['used_storage_space'],
            'storage_spec_code': dms['storage_spec_code'],
            'management': mca,
            'support_features': dms['support_features'],
            'node_num': dms['node_num'],
            'disk_encrypted': dms['disk_encrypted'],
            'tenant': tenant,
            'DC': dc
        }
        result['seaf.ta.reverse.cloud_ru.advanced.dmss'][f"sber.{company_domain}.dmss.{id}"] = yaml_structure

    with open('exports/dmss.yaml', 'w', encoding='utf-8') as outfile:
        yaml.dump(result, outfile, indent=4, default_flow_style=False, sort_keys=False, Dumper=IndentDumper, explicit_end=False, explicit_start=False)


#########    End of Distributed Message Services Section   #########

#########     Security Groups Export    #########
if secgroups == True:
    secgroups = get_scloud(service='vpc', s_type='security-groups', region=cloudregion, project=cloudproject, item=None)
    result = {'seaf.ta.reverse.cloud_ru.advanced.security_groups':{}}
    for sg in secgroups['security_groups']:
        id = sg['id']
        yaml_structure = {
            'id': id,
            'name': sg['name'],
            'description': sg['description'],
            'rules':[],
            'tenant': tenant,
            'DC': dc
        }

        rules = []
        for rule in sg['security_group_rules']:

            if rule['port_range_max'] and rule['port_range_min'] != None:
                if rule['port_range_max'] == rule['port_range_min']:
                    protocol_port = rule['port_range_max']
                else:
                    protocol_port = f"{rule['port_range_max']} -  {rule['port_range_min']}"
            else:
                protocol_port = 'All'

            tmp = {
                        'description': rule['description'],
                        'direction': rule['direction'], 
						'ethertype': rule['ethertype'], 
                        'protocol_port': protocol_port,
						'protocol': rule['protocol'], 
						'remote_group_id': rule['remote_group_id'], 
						'remote_ip_prefix': rule['remote_ip_prefix'],
                        'remote_address_group_id': rule['remote_address_group_id']
            }

            rules.append(tmp)

        yaml_structure['rules'] = rules
        result['seaf.ta.reverse.cloud_ru.advanced.security_groups'][f"sber.{company_domain}.security_groups.{id}"] = yaml_structure

    with open('exports/security_groups.yaml', 'w', encoding='utf-8') as outfile:
        yaml.dump(result, outfile, indent=4, default_flow_style=False, sort_keys=False, Dumper=IndentDumper, explicit_end=False, explicit_start=False)

#########    End of Security Groups Section   #########

#########     Cloud Container Engines Export    #########
if cce == True:
    cces = get_scloud(service='cce', s_type='clusters', region=cloudregion, project=cloudproject, item=None)
    result = {'seaf.ta.reverse.cloud_ru.advanced.cces':{}}
    for cce in cces['items']:
        id = cce['metadata']['uid']

        master_az = []
        for az in cce['spec']['masters']:
            if az['availabilityZone'] not in master_az:
                master_az.append(az['availabilityZone'])

        endpoints = []
        addresses = []
        for ep in cce['status']['endpoints']:
            endpoints.append(ep)
            address = ep['url'].split('//', 1)[1].split(':')[0]
            if address not in addresses:
                addresses.append(address)

        if 'platformVersion' in cce['spec']:
            pv = cce['spec']['platformVersion']
        else:
            pv = ''

        yaml_structure = {
            'name': cce['metadata']['name'],
            'id': cce['metadata']['uid'],
            'alias': cce['metadata']['alias'],
            'flavor': cce['spec']['flavor'],
            'version': cce['spec']['version'],
            'platform_version': pv,
            'vpc_id': cce['spec']['hostNetwork']['vpc'],
            'subnet_id': cce['spec']['hostNetwork']['subnet'],
            'addresses': addresses,
            'security_groups': cce['spec']['hostNetwork']['SecurityGroup'],
            'container_network': cce['spec']['containerNetwork']['cidr'],
            'service_network': cce['spec']['serviceNetwork']['IPv4CIDR'],
            'authentication': cce['spec']['authentication']['mode'],
            'masters_az': master_az,
            'supportistio': cce['spec']['supportIstio'],
            'endpoints': endpoints,
            'tenant': tenant,
            'DC': dc
        }
    
        result['seaf.ta.reverse.cloud_ru.advanced.cces'][f"sber.{company_domain}.cces.{id}"] = yaml_structure

    with open('exports/cces.yaml', 'w', encoding='utf-8') as outfile:
        yaml.dump(result, outfile, indent=4, default_flow_style=False, sort_keys=False, Dumper=IndentDumper, explicit_end=False, explicit_start=False)

#########    End of Cloud Container Engines Section   #########

#########     NAT Gateway Export    #########
if natgateway == True:
    natgateways = get_scloud(service='nat', s_type='gateway', region=cloudregion, project=cloudproject, item=None)
    snatrules = get_scloud(service='nat', s_type='snat', region=cloudregion, project=cloudproject, item=None)
    dnatrules = get_scloud(service='nat', s_type='dnat', region=cloudregion, project=cloudproject, item=None)
    result = {'seaf.ta.reverse.cloud_ru.advanced.nat_gateways':{}}
    for gw in natgateways['nat_gateways']:
        port = get_scloud(service='vpc', s_type='port_filter', region=cloudregion, project=cloudproject, item=f"device_id={gw['id']}")
        id = gw['id']
        snrules = []
        for snatrule in snatrules['snat_rules']:
            if snatrule['nat_gateway_id'] == id:
                eipid = snatrule['floating_ip_id'].split(',')
                eipaddress = snatrule['floating_ip_address'].split(',')
                if 'cidr' in snatrule:
                    cidr = snatrule['cidr']
                else:
                    cidr = ''
                tmp_yaml = {
                    'id': snatrule['id'],
                    'eip_id': [],
                    'eip_address': [],
                    'status': snatrule['status'],
                    'subnet_id': snatrule['network_id'],
                    'cidr': cidr,
                    'source_type': snatrule['source_type']
                }
                snrules.append(tmp_yaml)
                tmp_yaml['eip_id'] = eipid
                tmp_yaml['eip_address'] = eipaddress
        yaml_structure = {
            'id': gw['id'],
            'name': gw['name'],
            'description': gw['description'],
            'subnet_id': gw['internal_network_id'],
            'status': gw['status'],
            'address': port['ports'][0]['fixed_ips'][0]['ip_address'],
            'snat_rules': [],
            'dnat_rules': [],
            'tenant': gw['tenant_id'],
            'DC': dc
        }
        yaml_structure['snat_rules'] = snrules
        result['seaf.ta.reverse.cloud_ru.advanced.nat_gateways'][f"sber.{company_domain}.nat_gateways.{id}"] = yaml_structure

    with open('exports/nat_gateways.yaml', 'w', encoding='utf-8') as outfile:
        yaml.dump(result, outfile, indent=4, default_flow_style=False, sort_keys=False, Dumper=IndentDumper, explicit_end=False, explicit_start=False)
#########    End of Servers Section   #########

######### Elastic Load Balance Export #########
if elb == True:
    elbs = get_scloud(service='elb', s_type='lb', region=cloudregion, project=cloudproject, item=None)
    result = {'seaf.ta.reverse.cloud_ru.advanced.elbs':{}}
    for elb in elbs['loadbalancers']:
        id = elb['id']
        listeners = []
        pools = []
        fwpolicy = []
        for listener in elb['listeners']:
            listeners.append(get_scloud(service='elb', s_type='listeners', region=cloudregion, project=cloudproject, item=listener['id'])['listener'])
            print(listener['id'])
            forwardingpolicies = get_scloud(service='elb', s_type='l7policies', region=cloudregion, project=cloudproject, item=None)
            if forwardingpolicies != None:
                fwpolicy.append(forwardingpolicies)
        for pool in elb['pools']:
            pools.append(get_scloud(service='elb', s_type='pools', region=cloudregion, project=cloudproject, item=pool['id'])['pool'])

        port = get_scloud(service='vpc', s_type='port', region=cloudregion, project=cloudproject, item=elb['vip_port_id'])
        
        vips = []
        tmp = get_scloud(service='vpc', s_type='port_filter', region=cloudregion, project=cloudproject, item=f"fixed_ips=subnet_id={port['port']['fixed_ips'][0]['subnet_id']}")
        ip = elb['vip_address']
        for item in tmp['ports']:
            for ippair in item['allowed_address_pairs']:
                if ippair['ip_address'] == ip:
                    if item['fixed_ips'][0]['ip_address'] not in vips:
                        vips.append(item['fixed_ips'][0]['ip_address'])

        yaml_structure = {
            'id': id,
            'name': elb['name'],
            'description': elb['description'],
            'subnet_id': port['port']['network_id'],
            'port_id': elb['vip_port_id'],
            'address': elb['vip_address'],
            'operating_status': elb['operating_status'],
            'provisioning_status': elb['provisioning_status'],
            'listeners': [],
            'pools': [],
            'tags': [],
            'forwardingpolicy': [],
            'tenant': elb['tenant_id'],
            'DC': dc,
        }

        for listener in listeners:
            tmp = {
                'id': listener['id'],
                'name': listener['name'],
                'default_pool_id': listener['default_pool_id'],
                'protocol_port': listener['protocol_port'],
                'protocol': listener['protocol']
            }
            yaml_structure['listeners'].append(tmp)
        for pool in pools:
            tmp = {
                'id': pool['id'],
                'name': pool['name'],
                'lb_algorithm': pool['lb_algorithm'],
                'members': []
            }
            members = get_scloud(service='elb', s_type='poolmembers', region=cloudregion, project=cloudproject, item=pool['id'])
            if 'members' in members:
                for member in members['members']:
                    tmp2 = {
                        'id': member['id'],
                        'address': member['address'],
                        'name': member['name']
                    }
                    tmp['members'].append(tmp2)
            yaml_structure['pools'].append(tmp)
        result['seaf.ta.reverse.cloud_ru.advanced.elbs'][f"sber.{company_domain}.elbs.{id}"] = yaml_structure
    with open('exports/elbs.yaml', 'w', encoding='utf-8') as outfile:
        yaml.dump(result, outfile, indent=4, default_flow_style=False, sort_keys=False, Dumper=IndentDumper, explicit_end=False, explicit_start=False)

######### End of Elastic Load Balance Section ###########

######### Servers Export #########
if servers == True:
    servers = get_scloud(service='ecs', region=cloudregion, project=cloudproject, item=None, s_type=None)
    result = {'seaf.ta.reverse.cloud_ru.advanced.ecss':{}}

    eips = get_scloud(service='eip', s_type=None, region=cloudregion, project=cloudproject, item=None)

    for server in servers:
        print(server['name'])
        ports = []
        vips = []
        for nic in server["addresses"]:
            for portid in server['addresses'][nic]:
                physical_port = get_scloud(service='vpc', s_type='port', region=cloudregion, project=cloudproject, item=portid['OS-EXT-IPS:port_id'])

                for fixed_ip in physical_port['port']['fixed_ips']:
                    tmp = {'network_id': physical_port['port']['network_id'], 'subnet_id': fixed_ip['subnet_id'], 'ip_address': fixed_ip['ip_address']}
                    if tmp not in ports:
                        ports.append(tmp)

        for port in ports:
            tmp = get_scloud(service='vpc', s_type='port_filter', region=cloudregion, project=cloudproject, item=f"device_owner=neutron:VIP_PORT&fixed_ips=subnet_id={port['subnet_id']}")
            ip = port['ip_address']
            for item in tmp['ports']:
                for ippair in item['allowed_address_pairs']:
                    if ippair['ip_address'] == ip:
                        if item['fixed_ips'][0]['ip_address'] not in vips:
                            vips.append(item['fixed_ips'][0]['ip_address'])
        
        for eip in eips['publicips']:
            if 'private_ip_address' in eip:
                if eip['private_ip_address'] in vips:
                    if eip['public_ip_address'] not in vips:
                        vips.append(eip['public_ip_address'])

        id = server['id']
        yaml_structure = {
                        'id': server['id'],
                        'name': server['name'],
                        'description': server['description'],
                        'flavor': server['flavor']['id'],
                        'os':{'type': server['metadata']['os_type'], 'bit': server['metadata']['os_bit']},
                        'vpc_id': server['metadata']['vpc_id'],
                        'az': server['OS-EXT-AZ:availability_zone'], 
                        'cpu': {'cores': int(server['flavor']['vcpus']), 'frequency': '', 'arch': ''},
                        'ram': int(server['flavor']['ram']), 
                        'nic_qty': int(),
                        'addresses': [],
                        'subnets': [],
                        'disks': [],
                        'tags': [],
                        'security_groups': [],
                        'type': "vm",
                        'tenant': tenant,
                        'DC': dc
                        }
        
        yaml_secgroups = []
        for sg in server['security_groups']:
            if sg['id'] not in yaml_secgroups:
                yaml_secgroups.append(sg['id'])

        yaml_ip = []
        
        nic_ports = []
        for nic in server["addresses"]:
            for item in server['addresses'][nic]:
                yaml_ip.append(item['addr'])
                if item['OS-EXT-IPS:port_id'] not in nic_ports:
                    nic_ports.append(item['OS-EXT-IPS:port_id'])

        nic_count = int(len(nic_ports))

        for vip in vips:
            yaml_ip.append(vip)
            
        yaml_subnets =[]
        for port in ports:
            if port['network_id'] not in yaml_subnets:
                yaml_subnets.append(port['network_id'])

        yaml_disks = []
        for disk in server["os-extended-volumes:volumes_attached"]:
            evs_obj = get_scloud(service='evs', region=cloudregion, project=cloudproject, item=disk['id'])
            yaml_disks.append({disk['id']:{ 
                        'device': disk['device'], 
                        'size': evs_obj['volume']['size'], 
                        'az': evs_obj['volume']['availability_zone'],
                        'type': evs_obj['volume']['volume_type']
                    }})
            
        yaml_tags = []
        for tag in server['tags']:
            key = tag.split("=",1)[0]
            value = tag.split("=",1)[1]
            yaml_tags.append({'key': key, 'value': value})
        
        yaml_structure['security_groups'] = yaml_secgroups
        yaml_structure['nic_qty'] = nic_count
        yaml_structure['addresses'] = yaml_ip
        yaml_structure['disks'] = yaml_disks
        yaml_structure['tags'] = yaml_tags
        yaml_structure['subnets'] = yaml_subnets
        result['seaf.ta.reverse.cloud_ru.advanced.ecss'][f"sber.{company_domain}.ecss.{id}"] = yaml_structure

    with open('exports/ecss.yaml', 'w', encoding='utf-8') as outfile:
        yaml.dump(result, outfile, indent=4, default_flow_style=False, sort_keys=False, Dumper=IndentDumper, explicit_end=False, explicit_start=False)
####### End of Servers Export ########

######### Export VPCS #########
if vpcs == True:
    vpcs = get_scloud(service='vpc', region=cloudregion, s_type=None, project=cloudproject, item=None)
    result = {'seaf.ta.reverse.cloud_ru.advanced.vpcs':{}}
    for vpc in vpcs['vpcs']:
        id = vpc['id']
        yaml_vpc = {
            'id': id,
            'name': vpc['name'],
            'cidr': vpc['cidr'],
            'description': vpc['description'],
            'tenant': tenant,
            'DC': dc
        }
        result['seaf.ta.reverse.cloud_ru.advanced.vpcs'][f"sber.{company_domain}.vpcs.{id}"] = yaml_vpc
    with open('exports/vpcs.yaml', 'w', encoding='utf-8') as outfile:
        yaml.dump(result, outfile, indent=4, default_flow_style=False, sort_keys=False, Dumper=IndentDumper, explicit_end=False, explicit_start=False)
######### End of VPCS export #########

######### Subnets Export #########
if subnets == True:
    subnets = get_scloud(service='vpc', region=cloudregion, project=cloudproject, s_type='subnet', item=None)
    result = {'seaf.ta.reverse.cloud_ru.advanced.subnets':{}}
    for subnet in subnets['subnets']:
        id = subnet['id']
        yaml_subnet = {
            'id': id,
            'name': subnet['name'],
            'cidr': subnet['cidr'],
            'description': subnet['description'],
            'gateway': subnet['gateway_ip'],
            'dns_list': subnet['dnsList'],
            'vpc': subnet['vpc_id'],
            'tenant': tenant,
            'DC': dc
        }
        result['seaf.ta.reverse.cloud_ru.advanced.subnets'][f"sber.{company_domain}.subnets.{id}"] = yaml_subnet
    with open('exports/subnets.yaml', 'w', encoding='utf-8') as outfile:
            yaml.dump(result, outfile, indent=4, default_flow_style=False, sort_keys=False, Dumper=IndentDumper, explicit_end=False, explicit_start=False)
######### End of Subnets export #########

######### VPC Peers Export #########
if peer == True:
    peerings = get_scloud(service='vpc', region=cloudregion, project=cloudproject, s_type='peering', item=None)
    result = {'seaf.ta.reverse.cloud_ru.advanced.peerings':{}}
    for peering in peerings['peerings']:
        id = peering['id']
        yaml_peering = {
            'id': id,
            'name': peering['name'],
            'request_vpc': peering['request_vpc_info']['vpc_id'],
            'accept_vpc': peering['accept_vpc_info']['vpc_id'],
            'description': peering['description'],
            'status': peering['status'],
            'tenant': tenant,
            'DC': dc
        }
        result['seaf.ta.reverse.cloud_ru.advanced.peerings'][f"sber.{company_domain}.peerings.{id}"] = yaml_peering
    with open('exports/peerings.yaml', 'w', encoding='utf-8') as outfile:
            yaml.dump(result, outfile, indent=4, default_flow_style=False, sort_keys=False, Dumper=IndentDumper, explicit_end=False, explicit_start=False)
######### End of VPC Peers export #########

######### Elastic IPs Export #########
if eip == True:
    eips = get_scloud(service='eip', s_type=None, region=cloudregion, project=cloudproject, item=None)
    result = {'seaf.ta.reverse.cloud_ru.advanced.eips':{}}

    for eip in eips['publicips']:
        id = eip['id']
        if 'private_ip_address' in eip: 
            int_address = eip['private_ip_address'] 
        else: int_address = ''
        if 'port_id' in eip:
            port = eip['port_id']
        else: port = ''
        yaml_eip = {
            'id': id,
            'type': eip['type'],
            'port_id': port,
            'ext_address': eip['public_ip_address'],
            'int_address': int_address,
            'limit': {'type': eip['bandwidth_share_type'],
                      'throughput': eip['bandwidth_size'],
                      'rule_id': eip['bandwidth_id'],
                      'rule_name': eip['bandwidth_name']
            },
            'tenant': tenant,
            'DC': dc
        }
        result['seaf.ta.reverse.cloud_ru.advanced.eips'][f"sber.{company_domain}.eips.{id}"] = yaml_eip
    with open('exports/eips.yaml', 'w', encoding='utf-8') as outfile:
        yaml.dump(result, outfile, indent=4, default_flow_style=False, sort_keys=False, Dumper=IndentDumper, explicit_end=False, explicit_start=False)
######### End of Elastic IPs export #########

######### Backup Vaults Export #########
if vault == True:
    vaults = get_scloud(service='cbr', region=cloudregion, project=cloudproject, s_type='vault', item=None)
    result = {'seaf.ta.reverse.cloud_ru.advanced.vaults':{}}
    for vault in vaults['vaults']:
        id = vault['id']
        yaml_vault = {
            'id': id,
            'name': vault['name'],
            'description': vault['description'],
            'resources': vault['resources'],
            'tenant': tenant,
            'DC': dc
        }
        result['seaf.ta.reverse.cloud_ru.advanced.vaults'][f"sber.{company_domain}.vaults.{id}"] = yaml_vault
    with open('exports/vaults.yaml', 'w', encoding='utf-8') as outfile:
            yaml.dump(result, outfile, indent=4, default_flow_style=False, sort_keys=False, Dumper=IndentDumper, explicit_end=False, explicit_start=False)
######### End of Backup Vaults export #########

######### Backup policy Export #########
if backup_policy == True:
    bpolicy = get_scloud(service='cbr', region=cloudregion, project=cloudproject, s_type='policy', item=None)
    result = {'seaf.ta.reverse.cloud_ru.advanced.backup_policies':{}}
    for policy in bpolicy['policies']:
        id = policy['id']
        yaml_vault = {
            'id': id,
            'name': policy['name'],
            'operation_type': policy['operation_type'],
            'enabled': policy['enabled'],
            'operation_definition': policy['operation_definition'],
            'trigger': policy['trigger'],
            'associated_vaults': policy['associated_vaults'],
            'tenant': tenant,
            'DC': dc
        }
        result['seaf.ta.reverse.cloud_ru.advanced.backup_policies'][f"sber.{company_domain}.backup_policies.{id}"] = yaml_vault
    with open('exports/backup_policies.yaml', 'w', encoding='utf-8') as outfile:
            yaml.dump(result, outfile, indent=4, default_flow_style=False, sort_keys=False, Dumper=IndentDumper, explicit_end=False, explicit_start=False)
######### End of Backup Policies export #########

######### Relational Dtabase as a Service Export #########
if rds == True:
    rdses = get_scloud(service='rds', region=cloudregion, project=cloudproject, s_type=None, item=None)
    result = {'seaf.ta.reverse.cloud_ru.advanced.rdss':{}}
    for db in rdses['instances']:
        id = db['id']
        yaml_db = {
            'id': id,
            'name': db['name'],
            'status': db['status'],
            'type': db['type'],
            'datastore': db['datastore'],
            'vpc_id': db['vpc_id'],
            'subnet_id': db['subnet_id'],
            'volume': db['volume'],
            'private_ips': db['private_ips'],
            'public_ips': db['public_ips'],
            'nodes': db['nodes'],
            'flavor': db['flavor_ref'],
            'switch_strategy': db['switch_strategy'],
            'backup_strategy': db['backup_strategy'],
            'az': db['region'],
            'tags': db['tags'],
            'tenant': tenant,
            'DC': dc
        }
        result['seaf.ta.reverse.cloud_ru.advanced.rdss'][f"sber.{company_domain}.rdss.{id}"] = yaml_db
    with open('exports/rdss.yaml', 'w', encoding='utf-8') as outfile:
            yaml.dump(result, outfile, indent=4, default_flow_style=False, sort_keys=False, Dumper=IndentDumper, explicit_end=False, explicit_start=False)
######### End of Relational Database as a service export #########
