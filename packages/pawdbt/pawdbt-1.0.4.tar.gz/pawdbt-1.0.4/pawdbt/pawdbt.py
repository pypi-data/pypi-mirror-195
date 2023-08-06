#!/usr/bin/env python
# coding: utf-8

# automated version with user prompt
import argparse
import yaml
import subprocess
import os
from tqdm import tqdm
from prettytable import PrettyTable
from halo import Halo

VERSION = '1.0.4'
AUTHOR = 'Dan Wilson'
NAME = 'pawdbt'

# Global Vars
flag_list = [('-s', '--select', str), ('-d', '--save-doc-blocks-in', str), ('-o', '--always-overwrite', bool),
             ('-r', '--run-models', bool)]

pong = {
    "interval": 80,
    "frames": [
        "▐⠂       ▌",
        "▐⠈       ▌",
        "▐ ⠂      ▌",
        "▐ ⠠      ▌",
        "▐  ⡀     ▌",
        "▐  ⠠     ▌",
        "▐   ⠂    ▌",
        "▐   ⠈    ▌",
        "▐    ⠂   ▌",
        "▐    ⠠   ▌",
        "▐     ⡀  ▌",
        "▐     ⠠  ▌",
        "▐      ⠂ ▌",
        "▐      ⠈ ▌",
        "▐       ⠂▌",
        "▐       ⠠▌",
        "▐       ⡀▌",
        "▐      ⠠ ▌",
        "▐      ⠂ ▌",
        "▐     ⠈  ▌",
        "▐     ⠂  ▌",
        "▐    ⠠   ▌",
        "▐    ⡀   ▌",
        "▐   ⠠    ▌",
        "▐   ⠂    ▌",
        "▐  ⠈     ▌",
        "▐  ⠂     ▌",
        "▐ ⠠      ▌",
        "▐ ⡀      ▌",
        "▐⠠       ▌"
    ]
}


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_current_dir():
    try:
        directory = os.getcwd()
        return directory
    except OSError:
        print("Error: Unable to get current directory")
        return None


def get_file_path(path, name, type, required_folder_name=None):
    if not isinstance(path, str):
        raise TypeError("The 'path' parameter must be a string")
    if not isinstance(name, str):
        raise TypeError("The 'name' parameter must be a string")
    if not isinstance(type, str):
        raise TypeError("The 'type' parameter must be a string")
    if required_folder_name is not None and not isinstance(required_folder_name, str):
        raise TypeError("The 'required_folder_name' parameter must be a string or None")

    for root, dirs, files in os.walk(path):
        if required_folder_name is None or required_folder_name in root.split(os.path.sep):
            for file in files:
                file_name, file_type = file.split('.')
                if file_name == name and file_type == type:
                    return os.path.join(root, file)
    return None


def get_file_contents_by_line(path):
    try:
        with open(path, encoding='utf-8') as file:
            return file.readlines()
    except OSError:
        print(f"Error: Unable to open file {path}")
        return None


def find_text_between_delimiters(line, start_delim, end_delim):
    if not isinstance(line, str):
        raise TypeError("The 'line' parameter must be a string")
    if not isinstance(start_delim, str):
        raise TypeError("The 'start_delim' parameter must be a string")
    if not isinstance(end_delim, str):
        raise TypeError("The 'end_delim' parameter must be a string")

    start_index = line.find(start_delim)
    end_index = line.find(end_delim)

    if start_index == -1 or end_index == -1:
        return None

    found_text = line[start_index + len(start_delim):end_index].strip()

    return found_text


def get_all_dry_doc_blocks(cd):
    dry_md_path = get_file_path(cd, 'dry', 'md', '_docs')
    dry_file_lines = get_file_contents_by_line(dry_md_path)

    dry_blocks = []

    for line in dry_file_lines:
        stripped_of_jinja = find_text_between_delimiters(line, '{% docs', '%}')
        if stripped_of_jinja and stripped_of_jinja.startswith('dry_'):
            dry_blocks.append(stripped_of_jinja)

    return dry_blocks


def run_command_get_output(command):
    try:
        completed_process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                           check=True)
        return completed_process.stdout
    except subprocess.CalledProcessError as error:
        raise RuntimeError(f"Command execution failed with return code {error.returncode}: {error.stderr}")
    except OSError as error:
        raise RuntimeError(f"OSError: {error}")


def is_dbt_project_healthy():
    cmd = ['dbt', 'debug']
    output = run_command_get_output(cmd)
    if output and 'All checks passed!' in output:
        return True
    else:
        return False


def return_flag_values(flag_list):
    try:
        parser = argparse.ArgumentParser()
        for short_flag, long_flag, data_type in flag_list:
            parser.add_argument(short_flag, long_flag, dest=long_flag.lstrip('-'), type=data_type, nargs='?')
        args = parser.parse_args()

        return {long_flag.lstrip('-'): value for long_flag, value in vars(args).items() if value is not None}
    except Exception as error:
        raise RuntimeError(f"Error: {error}")


def get_models_by_identifier_type(type, selector):
    cmd = ['dbt', '--quiet', 'ls', '--resource-type', f"model", '--output', f"{type}", '--select', f"{selector}"]
    lines = run_command_get_output(cmd).splitlines()

    return lines


def get_domain_name(path):
    try:
        second_dir = path.split(os.sep)[1]
        return second_dir
    except (IndexError, TypeError):
        print("Error: invalid path format")
        return None


def get_relation_columns_and_datatype(relation):
    cmd = ['dbt', 'run-operation', 'get_relation_columns_and_datatype', '--args', f'relation: "{relation}"']
    lines = run_command_get_output(cmd).splitlines()

    cols = []
    types = []

    for line in lines:
        clean_line = find_text_between_delimiters(line, '{', '}')
        if clean_line:
            column_name, data_type = clean_line.split(':')
            cols.append(column_name)
            types.append(data_type)

    return cols, types


class MyDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)

    def write_line_break(self, data=None):
        super().write_line_break(data)
        if len(self.indents) == 1:
            super().write_line_break()


def create_relation_yml(relation, relation_path, columns, dry_columns, data_types):
    col_list = []
    for i in range(len(columns)):

        col_doc_block = get_domain_name(relation_path) + '_' + columns[i]

        for dry_col in dry_columns:
            if 'dry_' + columns[i] == dry_col:
                col_doc_block = dry_col

        col_dict = {
            'name': columns[i],
            'description': f'{{{{ doc("{col_doc_block}") }}}}',
            'tests': [
                {
                    'dbt_expectations.expect_column_values_to_be_of_type': {
                        'column_type': data_types[i]
                    }
                }
            ]
        }
        col_list.append(col_dict)

    data = {
        'version': 2,
        'models': [
            {
                'name': relation,
                'description': f'{{{{ doc("{relation}") }}}}',
                'tests': [
                    {
                        'dbt_expectations.expect_table_column_count_to_equal': {
                            'value': len(columns)
                        }
                    }
                ],
                'columns': col_list
            }
        ]
    }

    yaml_str = yaml.dump(data, Dumper=MyDumper, sort_keys=False)

    return yaml_str


def generate_column_md(column_name):
    lines = ['{{% docs {} %}}'.format(column_name),
             '{% enddocs %}']

    return '\n\n'.join(lines)


def create_relation_md(relation_name, relation_path, selected_models, selected_paths, dry_arr, doc_blocks_in_relation):
    full_md = ''
    header_lines = [
        '{{% docs {} %}}'.format(relation_name),
        '## Overview',
        '### Unique Key:',
        '### Partitioned by:',
        '### Contains PII:',
        '### Granularity:',
        '### Update Frequency:',
        '### Example Queries:',
        '{% enddocs %}'
    ]

    full_md += '\n\n'.join(header_lines)

    doc_columns = []
    doc_blocks = []

    if doc_blocks_in_relation:
        if relation_name == doc_blocks_in_relation:
            relation_domain = get_domain_name(relation_path)
            for i, model in tqdm(enumerate(selected_models), total=len(selected_models), desc="Fetching all doc blocks",
                                 colour="green"):
                if relation_domain == get_domain_name(selected_paths[i]):
                    tqdm.write(f"Fetching column docs from {model}...")
                    columns, types = get_relation_columns_and_datatype(model)
                    for column in columns:
                        add_doc = True
                        for dry_column in dry_arr:
                            if 'dry_' + column == dry_column:
                                add_doc = False
                        if add_doc:
                            if column not in doc_columns:
                                doc_columns.append(column)

            for column in doc_columns:
                doc_blocks.append(generate_column_md(relation_domain + '_' + column))

            full_md += '\n\n' + '\n\n'.join(doc_blocks)

    return full_md


def header_and_info(selector, doc_blocks_in_relation, always_overwrite, run_models):
    table = PrettyTable()
    table.field_names = ['Package', 'Created By', 'Version', 'Selector', 'Doc Blocks Saved To', 'Force Overwrite?',
                         'Run Models?']
    table.add_row([NAME, AUTHOR, VERSION, selector, doc_blocks_in_relation, str(always_overwrite), str(run_models)])
    print(table)


def create_file(relation_path, extension, str, always_overwrite):
    dir_path, file_name = os.path.split(relation_path)
    file_name_no_ext = os.path.splitext(file_name)[0]
    new_file_name = file_name_no_ext + "." + extension
    file_path = os.path.join(dir_path, new_file_name)
    mode = 'w'
    while os.path.exists(file_path) and not always_overwrite:
        print(f"\n\nThe file {file_path} already exists. Do you want to:")
        print("1. Overwrite the file")
        print("2. Append to the file")
        print("3. Ignore the file")
        action = input("Choice (1,2,3): ")
        if action.lower() == "1":
            mode = "w"
            break
        elif action.lower() == "2":
            mode = "a"
            break
        elif action.lower() == "3":
            return
        else:
            print("Invalid choice. Please choose 1, 2, or 3.")
    with open(file_path, mode) as f:
        f.write(str)


def run_selector(selector):
    cmd = ['dbt', 'run', '--select', f'+{selector}']
    try:
        run_command_get_output(cmd)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def main_yaml():
    if is_dbt_project_healthy():

        clear_terminal()

        cd = get_current_dir()
        dry_arr = get_all_dry_doc_blocks(cd)
        flag_values = return_flag_values(flag_list)
        selector = flag_values.get('select', None)
        doc_blocks_in_relation = flag_values.get('save-doc-blocks-in', None)
        always_overwrite = flag_values.get('always-overwrite', False)
        run_models = flag_values.get('run-models', False)

        header_and_info(selector, doc_blocks_in_relation, always_overwrite, run_models)

        if run_models:
            for i in tqdm(range(1), total=1, desc="Running selector to create models", colour="green"):
                run_selector(selector)

        spinner = Halo(text="Gathering Models...", spinner=pong)
        spinner.start()

        selected_models = get_models_by_identifier_type('name', selector)
        selected_paths = get_models_by_identifier_type('path', selector)

        spinner.stop()

        ymls = []
        mds = []

        for i, relation in tqdm(enumerate(selected_models), total=len(selected_models), desc="Processing relations",
                                colour="green"):
            tqdm.write(f"Processing {relation}...")
            columns, types = get_relation_columns_and_datatype(relation)
            yml = create_relation_yml(relation, selected_paths[i], columns, dry_arr, types)
            md = create_relation_md(relation, selected_paths[i], selected_models, selected_paths, dry_arr,
                                    doc_blocks_in_relation)
            ymls.append(yml)
            mds.append(md)

        for i, relation in tqdm(enumerate(selected_models), total=len(selected_models), desc="Writing YAML & MD Files",
                                colour="green"):
            create_file(selected_paths[i], 'yml', ymls[i], always_overwrite)
            create_file(selected_paths[i], 'md', mds[i], always_overwrite)
    else:
        quit()


if __name__ == "__main__":
    main_yaml()
