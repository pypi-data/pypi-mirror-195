{% materialization incremental, adapter='selectdb' %}
  {% set unique_key = config.get('unique_key', validator=validation.any[list]) %}
  {%- set inserts_only = config.get('inserts_only') -%}

  {% set target_relation = this.incorporate(type='table') %}


  {% set existing_relation = load_relation(this) %}
  {% set tmp_relation = make_temp_relation(this) %}

  {{ run_hooks(pre_hooks, inside_transaction=False) }}

  {{ run_hooks(pre_hooks, inside_transaction=True) }}

  {% set to_drop = [] %}

  {% if unique_key is none or inserts_only  %}
        {% set build_sql = tmp_insert(tmp_relation, target_relation, unique_key=none) %}
  {% elif existing_relation is none %}
      {% set build_sql = selectdb__create_unique_table_as(False, target_relation, sql) %}
  {% elif existing_relation.is_view or should_full_refresh() %}
      {#-- Make sure the backup doesn't exist so we don't encounter issues with the rename below #}
      {% set backup_identifier = existing_relation.identifier ~ "__dbt_backup" %}
      {% set backup_relation = existing_relation.incorporate(path={"identifier": backup_identifier}) %}
      {% do adapter.drop_relation(backup_relation) %}
      {% do adapter.rename_relation(target_relation, backup_relation) %}
      {% set build_sql = selectdb__create_unique_table_as(False, target_relation, sql) %}
      {% do to_drop.append(backup_relation) %}
  {% else %}
      {% set build_show_create = show_create( target_relation, statement_name="table_model") %}
        {% call statement('table_model' , fetch_result=True)  %}
            {{ build_show_create }}
        {% endcall %}
      {%- set table_create_obj = load_result('table_model') -%}
      {% if not is_unique_model(table_create_obj) %}
            {% do exceptions.raise_compiler_error("selectdb table:"~ target_relation ~ ", model must be 'UNIQUE'" ) %}
      {% endif %}
      {% do run_query(create_table_as(True, tmp_relation, sql)) %}
      {% do to_drop.append(tmp_relation) %}

      {% do adapter.expand_target_column_types(
             from_relation=tmp_relation,
             to_relation=target_relation) %}
      {% set build_sql = tmp_insert(tmp_relation, target_relation, unique_key=unique_key) %}
  {% endif %}

  {% call statement("main") %}
      {{ build_sql }}
  {% endcall %}


  {% do persist_docs(target_relation, model) %}
  {{ run_hooks(post_hooks, inside_transaction=True) }}
  {% do adapter.commit() %}
  {% for rel in to_drop %}
      {% do selectdb__drop_relation(rel) %}
  {% endfor %}
  {{ run_hooks(post_hooks, inside_transaction=False) }}
  {{ return({'relations': [target_relation]}) }}

{%- endmaterialization %}



