-- selectdb have not 'schema' to make a collection of table or view
{% macro selectdb__drop_schema(relation) -%}
  {%- call statement('drop_schema') -%}
    drop database if exists {{ relation.without_identifier().include(database=False) }} 
  {%- endcall -%}
{% endmacro %}


{% macro selectdb__create_schema(relation) -%}
  {%- call statement('create_schema') -%}
    create database if not exists {{ relation.without_identifier().include(database=False) }}
  {% endcall %}
{% endmacro %}
