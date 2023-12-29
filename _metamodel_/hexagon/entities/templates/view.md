{{#error}}
###### View

---
:warning: {{.}}
{{/error}}

{{^error}}
###### View :id: {{vId}}

---
# {{body.title}}
{{body.description}}

{{#modes}}
###### {{#row}}{{#.}}{{#selected}}=={{title}}== | {{/selected}}{{^selected}}[{{title}}](/entities/hexV/view?id={{vId}}&mode={{chain}}) | {{/selected}}{{/.}}{{/row}}

{{#row}}{{#.}}{{#selected}}{{description}}{{/selected}}{{/.}}{{/row}}
{{/modes}}


![](@entity/hexV/pattern_graph?data={{resView.pattern}})

---

![](@entity/hexV/landscape_graph?data={{resView.landscape}})

{{/error}}

