# Сервер
***  
**Наименование**: {{name}}

| Наименование | IP адреса                                        | Subnet     | VPC     | DC/IaaS |
|--------------|--------------------------------------------------|------------|---------|---------|
| {{name}}     | {{#ip_addresses}}{{address}},  {{/ip_addresses}} | {{subnet}} | {{vpc}} | {{DC}}  |


## Описание  
{{description}}

## Backup Policies
![Получаем данные о резервном копировании](@entity/seaf.ta.reverse.cloud_ru.advanced.backup_policies/server_backup?id={{id}})

## Firewall Rules  

{{#sg}}
**{{name}}**
![Получаем данные об ACL](@entity/seaf.ta.reverse.cloud_ru.advanced.security_groups/table_view?id={{sg_id}})

{{/sg}}

