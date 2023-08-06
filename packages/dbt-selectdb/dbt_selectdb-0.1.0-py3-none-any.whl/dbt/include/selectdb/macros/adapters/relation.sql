{% macro selectdb__engine() -%}
    {% set label = 'ENGINE' %}
    {% set engine = config.get('engine', 'OLAP') %}
    {{ label }} = {{ engine }}
{%- endmacro %}

{% macro selectdb__partition_by() -%}
  {% set cols = config.get('partition_by') %}
  {% set partition_type = config.get('partition_type', 'RANGE') %}
  {% if cols is not none %}
    PARTITION BY {{ partition_type }} (
      {% for col in cols %}
        {{ col }}{% if not loop.last %},{% endif %}
      {% endfor %}
    )(
        {% set init = config.get('partition_by_init', validator=validation.any[list]) %}
        {% if init is not none %}
          {% for row in init %}
            {{ row }}{% if not loop.last %},{% endif %}
          {% endfor %}
        {% endif %}
    )
  {% endif %}
{%- endmacro %}

{% macro selectdb__duplicate_key() -%}
  {% set cols = config.get('duplicate_key', validator=validation.any[list]) %}
  {% if cols is not none %}
    DUPLICATE KEY (
      {% for item in cols %}
        {{ item }}
      {% if not loop.last %},{% endif %}
      {% endfor %}
    )
  {% endif %}
{%- endmacro %}

{% macro selectdb__unique_key() -%}
  {% set cols = config.get('unique_key', validator=validation.any[list]) %}
  {% if cols is not none %}
    UNIQUE KEY (
      {% for item in cols %}
        {{ item }}
      {% if not loop.last %},{% endif %}
      {% endfor %}
    )
  {% endif %}
{%- endmacro %}

{% macro selectdb__distributed_by(column_names) -%}
  {% set label = 'DISTRIBUTED BY HASH' %}
  {% set engine = config.get('engine', validator=validation.any[basestring]) %}
  {% set cols = config.get('distributed_by', validator=validation.any[list]) %}
  {% set buckets = config.get('buckets', validator=validation.any[int]) %}
  {% if cols is none and engine in [none,'OLAP'] %}
    {% set cols = column_names %}
  {% endif %}
  {% if cols  %}
    {{ label }} (
      {% for item in cols %}
        {{ item }}{% if not loop.last %},{% endif %}
      {% endfor %}
    ) 
    {% if buckets is not none  %}
      BUCKETS {{ buckets }}
    {% endif %}
  {% endif %}
{%- endmacro %}

{% macro selectdb__properties() -%}
  {% set properties = config.get('properties', validator=validation.any[dict]) %}
  {% if properties is not none %}
    PROPERTIES (
        {% for key, value in properties.items() %}
          "{{ key }}" = "{{ value }}"{% if not loop.last %},{% endif %}
        {% endfor %}
    )
  {% endif %}
{%- endmacro%}

{% macro selectdb__drop_relation(relation) -%}
    {% set relation_type = relation.type %}
    {% if relation_type is none %}
        {% set relation_type = 'table' %}
    {% endif %}
    {% call statement('drop_relation', auto_begin=False) %}
    drop {{ relation_type }} if exists {{ relation }}
    {% endcall %}
{%- endmacro %}

{% macro selectdb__truncate_relation(relation) -%}
    {% call statement('truncate_relation') %}
      truncate table {{ relation }}
    {% endcall %}
{%- endmacro %}

{% macro selectdb__rename_relation(from_relation, to_relation) -%}
  {% call statement('drop_relation') %}
    drop {{ to_relation.type }} if exists {{ to_relation }}
  {% endcall %}
  {% call statement('rename_relation') %}
    {% if to_relation.is_view %}
    {% set results = run_query('show create view ' + from_relation.render() ) %}
    create view {{ to_relation }} as {{ results[0]['Create View'].replace(from_relation.table, to_relation.table).split('AS',1)[1] }}
    {% else %}
    alter table {{ from_relation }} rename {{ to_relation.table }}
    {% endif %}
  {% endcall %}

  {% if to_relation.is_view %}
    {% call statement('rename_relation_end_drop_old') %}
      drop view if exists {{ from_relation }}
    {% endcall %}
  {% endif %}

  {%- endmacro %}

{% macro selectdb__timestimp_id() -%}
 {{ return( (modules.datetime.datetime.now() ~ "").replace('-','').replace(':','').replace('.','').replace(' ','') ) }}
{%- endmacro %}

{% macro selectdb__with_label() -%}
  {% set lable_suffix_id = config.get('label_id', validator=validation.any[basestring]) %}
  {% if lable_suffix_id in [none,'DEFAULT'] %}
    WITH LABEL dbt_selectdb_label_{{selectdb__timestimp_id()}}
  {% else %}
    WITH LABEL dbt_selectdb_label_{{ lable_suffix_id }}
  {% endif %}  
{%- endmacro %}

{% macro selectdb__get_or_create_relation(database, schema, identifier, type) %}
  {%- set target_relation = adapter.get_relation(database=database, schema=schema, identifier=identifier) %}
  
  {% if target_relation %}
    {% do return([true, target_relation]) %}
  {% endif %}
  
  {%- set new_relation = api.Relation.create(
      database=none,
      schema=schema,
      identifier=identifier,
      type=type
  ) -%}
  {% do return([false, new_relation]) %}
{% endmacro %}

{% macro catalog_source(catalog,database,table) -%}
  `{{catalog}}`.`{{database}}`.`{{table}}` 
{%- endmacro %}
