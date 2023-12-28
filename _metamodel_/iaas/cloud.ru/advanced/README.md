# Cloud.ru Advanced - реверс архитектуры 
***
Зависимости модуля: **seaf-core**

Описание услуг предоставляемых провайдером Cloud.ru в "регионе" **Advanced**. 
Регион **Advanced** - AWS-like инфраструктура на базе решений Huawei Cloud.


## Быстрый старт

Модуль позволяет выгружать и использовать данные о базовой инфраструктуре компании размещаемой в облачном провайдере Cloud.ru регион **Advanced**.
Из полученных данных формируются реестры потребляемых услуг и вся необходимая для работы с инфраструктурой информация, в том числе сетевые схемы.

### Модуль отвечает на вопросы
- **Как устроена моя инфраструктура?**  
  Модуль позволяет иметь под рукой актуальный срез информации о своей инфраструктуре. Поможет оперативно ответить на вопросы коллег или руководства.
- **Настроил ли я резервную копию или правило на фаере?**  
  На страницах сущностей доступна информации о расписании резервного копирования, сетевых правилах и т.д.
- **Кибера просят показать где развернуто это приложение и соответсвует ли проектное описание реальному?**  
  Все сущности которые могут являться компонентами прикладных сервисов (СУБД, брокеры, балансировщики, виртуальные машины) могут быть привязаны к прикладным сервисам с помощью сущности **links**.

### Как подготовить данные?

Сущности с 1 по 13 (в таблице ниже) заполняются автоматически с помощью Python скрипта поставляемого в пакете.

    Скрипт поставляется as-is как пример реализации  


Для того чтобы корректно произвести выгрузку и заполнить сущности не генерируемые автоматически вам потребуется:
- Создать объект сущности ЦОД базовой метамодели технической архитектуры (**seaf.ta.services.dc**), идентификатор данного объекта необходимо ввести в атрибут DC для заполняемых вручную объектов и использовать в скрипте для выгрузки данных.
- Создать объект сущности Офис базовой метамодели технической архитектуры (**seaf.ta.services.office**), идентификатор данного объекта используется в сущности VPN Connection.
- Заполнить объект сущности Связь (**seaf.ta.reverse.cloud_ru.advanced.links**) и привязать Прикладные компоненты к Техническим компонентам в метамодели расширения IaaS.Reverse.

Пример заполнения объекта сущности Связь
```yaml
seaf.ta.reverse.cloud_ru.advanced.links:
    sber.berezka.links.home_cinema.auth:
       app_id: sber.berezka.home_cinema.auth
       reverse_ta_id:
         - sber.berezka.ecss.62f713a4-1139-461f-8053-1df267861aef
         - sber.berezka.ecss.729d3b73-350c-4987-86ed-01d36b719c57
         - sber.berezka.rdss.0e493e5847714a14a313e215d9e59b15in03
         - sber.berezka.elbs.ad9af3b6-fd82-404e-8d6c-466660e92329
         - sber.berezka.ecss.e5e60a69-0653-4297-8799-ea0df4f0cacc
```
### Запуск скрипта выгрузки
1. Создать пользователя в Cloud.Advanced IAM с правами на чтение и выгрузите AK/SK ключи для подключения
к API. Подробнее: [Cloud.ru](https://support.hc.sbercloud.ru/en-us/devg/apisign/api-sign-provide-aksk.html)
2. Положить загруженный файл csv с ключами в корень папки API.

        Помните, это небезопасно и лучше использовать Vault или другое хранилище ключей!
3. Открыть в IDE папку API и в скрипте SberCloud-Python.py указать значения переменных для запуска
```python
cloudregion = 'ru-moscow-1'                                                 # Регион для вызова API
cloudproject = 'здесь должен быть идентификатор проекта/тенанта'            # ID проекта, можно найти в консоли или раскомментировать ниже секцию Cloud Project
credentials = "credentials.csv"                                             # Файл с учетными данными SberCloud
company_domain = 'berezka'                                                  # Префикс/домен компании для наименвоания сущностей
dc = 'идентификатор ЦОД/IaaS из сущности seaf.ta.services.dc'               # Идентификатор сущности
```
4. Выбрать необходимые сущности переключив значение соответсвующих переменных в true
```python
servers = False                         # Elastic Cloud Server
eip = False                             # Elastic IP (external ip addresses)
vault = False                           # Cloud Backup and Recovery vaults
backup_policy = False                   # Cloud Backup and Recovery policies
rds = False                             # Relational Database Service                     
natgateway = False                      # NAT Gateway
elb = False                             # Elastic Load Balance
cce = False                             # Cloud Container Engine
dms = False                             # Distributed Message Server
```
5. В результате выполнения скрипта данные будут сохранены в папку exports


## Структура каталогов
```console

|- _metamodel_                      - Подключенные пакеты метамоделей
|  |- iaas                          - Пакет метамодели
|  |  |- cloud.ru                   - Модель провайдера
|  |  |  |- advanced                - Регион или тип услуги (vmware/aws)
|  |  |  |  |- entities             - Сущности метамодели
|  |  |  |  |- functions            - Запросы написанные на JSONata
|  |  |  |  |- datasets             - Переиспользуемые датасеты
|  |  |  |  |- menu                 - Структура меню сущностей метамодели
|  |  |  |  |- presentations        - Презентационный слой сущностей метамодели
|  |  |- general                    - Общее для всех модулей 
|  |  |  |- menu                    - Общие для всех модулей меню
|  |  |  |- presentations           - Общие для всех модулей представления
|  |  |  |- bin                     - Инструментарий, скрипты
|  |- architecture                  - Архитектурные объекты поставляемые с пакетом
|  |  |- ta                         - Объекты сущностей
|  |- dochub.yaml                   - Корневой манифест пакета
|  |- README.md                     - Описание пакета
|  |- LICENSE                       - Лицензия под которой распространяется пакет
```
## Сущности

| №  | **Объект**          | **Наименование сущности**                          | **Описание**                                                                          |
|----|---------------------|----------------------------------------------------|---------------------------------------------------------------------------------------|
| 1  | **backup_policies** | 	seaf.ta.reverse.cloud_ru.advanced.backup_policies | 	Политики РК (расписания и привязка к vaults)                                         |
| 2  | **cces**            | 	seaf.ta.reverse.cloud_ru.advanced.cces	           | Кластеры kubernetes                                                                   |
| 3  | **dmss**            | 	seaf.ta.reverse.cloud_ru.advanced.dmss	           | Распределенные сервисы сообщений                                                      |
| 4  | **eips**            | 	seaf.ta.reverse.cloud_ru.advanced.eips	           | Elastic IPs                                                                           |
| 5  | **elbs**            | 	seaf.ta.reverse.cloud_ru.advanced.elbs	           | Elastic Load Balancers                                                                |
| 6  | **nat_gateways**    | 	seaf.ta.reverse.cloud_ru.advanced.nat_gateways	   | Nat Gateways                                                                          |
| 7  | **peerings**        | 	seaf.ta.reverse.cloud_ru.advanced.peerings	       | VPC Peerings                                                                          |
| 8  | **rdss**            | 	seaf.ta.reverse.cloud_ru.advanced.rdss	           | Relational Database Services                                                          |
| 9  | **security_groups** | 	seaf.ta.reverse.cloud_ru.advanced.security_groups | Группы безопасности                                                                   |
| 10 | **ecss**            | 	seaf.ta.reverse.cloud_ru.advanced.ecss            | Elastic Cloud Servers                                                                 |
| 11 | **subnets**         | 	seaf.ta.reverse.cloud_ru.advanced.subnets         | VPC Subnets                                                                           |
| 12 | **vaults**          | 	seaf.ta.reverse.cloud_ru.advanced.vaults          | Хранилища РК                                                                          |
| 13 | **vpcs**            | 	seaf.ta.reverse.cloud_ru.advanced.vpcs            | VPC                                                                                   |
| 14 | **vpn_connections** | 	seaf.ta.reverse.cloud_ru.advanced.vpn_connections | VPN соединения (заполняется вручную, нет API)                                         |
| 15 | **vpn_gateways**    | 	seaf.ta.reverse.cloud_ru.advanced.vpn_gateways    | VPN шлюзы (заполняется вручную, нет API)                                              |
| 16 | **links**           | seaf.ta.reverse.cloud_ru.advanced.links            | Сущность-связь прикладного компонента к техническому компоненту (заполняется вручную) |


## Схема
![Метамодель](@entity/seaf.ta.reverse.general/metamodel)