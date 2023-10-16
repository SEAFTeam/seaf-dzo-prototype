###### :orange_book: hex_queries.md

---
# Запросы к графу (TBD)

Запросы имеют имеют строго 3-х уровневую структуру:
```yaml
    .....
        hexQ:
            seaf.ba.ttl | mm.party.hexQ | mm.party:              # все ttl-объекты | вложенный запрос | конкретный ttl-объект
                EVERY|ANY|ONE|NONE<=|=>[label]:                  # условие направление наименование(опционально)
                    seaf.ba.ttl | mm.party.hexQ | mm.party:      # все ttl-объекты | вложенный запрос | конкретный ttl-объект
```

