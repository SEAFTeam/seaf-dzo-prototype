# Cloud Container Engine
***  
**Наименование**: {{name}}

| **Имя**  | **Flavor** | **HA (masters_qty)** | **Endpoints**                       | **Container Network** | **Service Network** | **Подсеть** | **VPC** | **DC/IaaS** |
|----------|------------|----------------------|-------------------------------------|-----------------------|---------------------|------------|---------|-------------|
| {{name}} | {{flavor}} | {{ha}}               | {{#endpoints}}{{url}}{{/endpoints}} | {{container_network}} | {{service_network}} | {{subnet}} | {{vpc}} |    {{DC}}   |

## Firewall Rules  

{{#security_groups}}
![Получаем данные об ACL](@entity/seaf.ta.reverse.cloud_ru.advanced.security_groups/table_view?id={{.}})

{{/security_groups}}

