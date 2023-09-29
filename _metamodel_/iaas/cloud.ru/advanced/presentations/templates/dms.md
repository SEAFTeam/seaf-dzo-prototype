# Distributed Message Service
***  
**Наименование**: {{name}}

| **Имя**  | **Движок** | **HA**   | **Порт** | **IP адрес** | **Подсеть** | **VPC** | **DC/IaaS** |
|----------|------------|----------|----------|--------------|-------------|---------|-------------|
| {{name}} | {{engine}} | {{type}} | {{port}} | {{address}}  | {{subnet}}  | {{vpc}} | {{DC}}      |


## Firewall Rules  

{{#security_groups}}
![Получаем данные об ACL](@entity/seaf.ta.reverse.cloud_ru.advanced.security_groups/table_view?id={{.}})

{{/security_groups}}

