"""A simple tool that produces environment files for
easily sharing a conda environment. This script uses the PyYAML package.
Additionally, it was tested on Python 3.9 but I think it should work for
any version that supports f-strings.

The three main issues I wanted to solve about the built-in
conda env export tool are the following:

    - Not including pip installations when using flag `--from-history`
    - When using flag `--from-history`, package versions are often not
    included (depending on whether the user manually typed them)
    - When using --from-history flag, third-party channels are not included
    in the file.

I want to be able to do the following:
```sh
conda env export --from-history > environment.yml
```
and have a file that contains stricly the packages I installed (but including
those with pip). Additionally, those packages should have the version number
that was installed in the environment. This script solves that. 

Run the script inside the conda environment you want to export:

```sh
python conda_export.py --from-history --use-versions -o environment.yml
```
to get an output file with only manual imports but include version numbers.
If no output file name is provided, the output will be printed to the terminal.

The script also maintains normal Conda's env export functionality:
```sh 
python conda_export.py -o environment.yml
```

The command above is equivalent to running:
```sh
conda env export > environment.yml
```

Then:
```sh
python conda_export.py --from-history -o environment.yml
```

is equivalent almost like using:
```sh
conda env export --from-history > environment.yml
```
but including pip packages as well as conda channel.

Credits:
This script uses part of the gist you can find here:
https://gist.github.com/gwerbin/dab3cf5f8db07611c6e0aeec177916d8
 
particularly, I copied the `export_env` function.
"""
#===================================
#TODO: exchange PyYAML for a more modern implementation, such as ruamel.yaml package
import yaml
import pathlib

import subprocess
import sys
import argparse

from typing import Union
#===================================

def CLI() -> argparse.Namespace:
    '''Provides the command line interface for the script'''
    # create the top-level parser
    parser = argparse.ArgumentParser(prog='Conda Env Export Enhanced')
    parser.add_argument('-his','--from-history',action='store_true',help="Boolean flag to use --from-history flag with `conda env export`.")
    parser.add_argument('-nob','--no-builds',action='store_true',help="Apply --no-builds flag to `conda env export`.")
    parser.add_argument('-v','--use-versions',action='store_true',help="Boolean flag to include package version numbers when using --from-history flag")
    parser.add_argument('--verbose',action='store_true',help="Boolean flag to indicate if output to file should also be printed to terminal")
    
    parser.add_argument('--include-prefix', action='store_true', help="Boolean flag to include the `prefix` line that conda appends to an environment file")
    parser.add_argument('-n','--env-name',type=str,default=None, help="Give a name to the conda environment. If not provided, use current environment's name")
    parser.add_argument('-o','--output', type=str, default=None, help='Specify an output file to save with environment data. If not provided, it will be printed to the terminal')
    
    args = parser.parse_args()
    return args
     
def export_env(from_history:bool=False, no_builds:bool=False) -> dict[str, Union[str,list,dict]]:
    '''Run the command `conda env export` plus additional flags
    and get the output from the terminal. This function is mostly 
    copied from the gist I found online. Link above, in module docstring'''

    cmd = ['conda', 'env', 'export']
    if from_history:
        cmd.append('--from-history')
        if no_builds:
            raise ValueError('Cannot include build versions with "from history" mode')
    if not no_builds:
        cmd.append('--no-builds')
    cp = subprocess.run(cmd, stdout=subprocess.PIPE)
    try:
        cp.check_returncode()
    except:
        raise
    else:
        return yaml.safe_load(cp.stdout)

def _split_by_name_and_version(full_name:str, is_pip_package=False) -> dict:
    '''use is_pip_package to indicate if the package was installed by pip'''
    if is_pip_package:
        version_sign = '=='  #pip package versions use '=='
    else:
        version_sign = '='

    #-- split name into pieces
    if version_sign in full_name:
        values = full_name.split(version_sign)
    else:
        values = [full_name]
    
    #-- extract package name, version and other stuff
    package_name = values[0]
    try:
        package_version = values[1]
    except IndexError:
        package_version = None
    try:
        build_name = values[2]
    except IndexError:
        build_name = None
    
    return {'name'   : package_name, 
            'version': package_version, 
            'build'  : build_name,}

def _join_name_version(name_dict:dict, is_pip_package=False) -> str:
    if name_dict.get('build',None) is None:
        _build = ''

    _name = name_dict.get('name')
    _ver  = name_dict.get('version')

    if is_pip_package:
        join_sign = '=='
    else:
        join_sign = '='

    if len(_build) == 0:
        full_name = f"{_name}{join_sign}{_ver}"
    else:
        full_name = f"{_name}{join_sign}{_ver}{join_sign}{_build}"

    return full_name

def is_pip_section(dependency) -> bool:
    '''This function can be done in one line, 
    but it may be more readable this way.'''
    if isinstance(dependency, dict) and 'pip' in dependency:
        return True 
    return False

def get_pip_section(dependency_list:list) -> dict:
    for dependency in dependency_list:
        if isinstance(dependency, dict) and 'pip' in dependency:
            print(f"Dependency is (should be pip dict):\n{dependency}\n")
            return dependency
    return {}

def _create_split_dictionary(env_data:list) -> dict:
    #TODO:figure out a way to extract pip version and also have
    # another dict for pip installs (maybe use different keys): i.e.
    #       'pip' for the pip package, and 'pip_pkgs' for pip package list
    split_deps = dict()
    for package in env_data:
        if isinstance(package, str):
            name_split_dict = _split_by_name_and_version(package,)
            _name = name_split_dict.get('name')
            split_deps[_name] = name_split_dict  
        elif is_pip_section(package):
            split_deps['pip'] = dict()
            pkg_list = package['pip']
            for pkg_name in pkg_list:
                if isinstance(pkg_name, str):
                    name_split_dict = _split_by_name_and_version(pkg_name, is_pip_package=True)
                    _name = name_split_dict.get('name')
                    split_deps['pip'][_name] = name_split_dict
    return split_deps

def merge_dependencies(full_env, history_env, use_versions:bool) -> list:
    full_dependencies:list = full_env['dependencies']
    hist_dependencies:list = history_env['dependencies']

    #-- keep only package names
    split_full_deps = _create_split_dictionary(full_dependencies)
    split_hist_deps = _create_split_dictionary(hist_dependencies)

    #-- perform the actual merge
    _dependencies = []
    for item_key in split_full_deps:
        if item_key in split_hist_deps:
            if item_key=='pip':
                #TODO handle pip here
                pip_dict:dict = {'pip':[]}
                _dependencies.append('pip')   #this avoids a warning with conda install
                _dependencies.append(pip_dict)
                for _pip_item_key in split_full_deps[item_key]:
                    if use_versions:
                        pkg_object:dict = split_full_deps[item_key][_pip_item_key]
                        joined_pkg:str = _join_name_version(pkg_object, is_pip_package=True)
                        pip_dict['pip'].append(joined_pkg)
                    else:
                        pip_dict['pip'].append(_pip_item_key)
            else:
                if use_versions:
                    pkg_object:dict = split_full_deps[item_key]
                    joined_pkg:str = _join_name_version(pkg_object, is_pip_package=False)
                    _dependencies.append(joined_pkg)
                else:
                    _dependencies.append(item_key)

    return _dependencies

def produce_output(output_file:str, env_data:dict, verbose:bool):
    if output_file is None:
        yaml.dump(env_data, sys.stdout)
    else:
        with open(output_file, 'w') as f_handler:
            yaml.dump(env_data, f_handler)
        
        #-- print to terminal if selected by user
        if verbose:
            yaml.dump(env_data, sys.stdout)

def _replace_env_name(new_name:str, reference_env:dict, env_to_modify:dict, include_prefix:bool=True) -> dict:
    '''Modifies the `name` and `prefix` sections of Conda's 
    environment dictionary file'''
    if new_name is None:
        env_to_modify['name'] = reference_env['name']
        env_to_modify['prefix'] = reference_env['prefix']
    else:
        env_to_modify['name'] = new_name

        #-- modify prefix path
        _prefix_path = reference_env['prefix']
        original_path = pathlib.PurePath(_prefix_path)

        new_path = original_path.parent.joinpath(new_name)
        env_to_modify['prefix'] = str(new_path)


    if not include_prefix:
        env_to_modify.pop('prefix', 'Key `prefix` NOT found when trying to remove from dictionary')


    return env_to_modify


def main(args):
    #-- extract CLI flags
    from_history:bool = args.from_history
    no_builds   :bool = args.no_builds
    use_versions:bool = args.use_versions
    verbose     :bool = args.verbose

    include_prefix:bool = args.include_prefix
    env_name     :str  = args.env_name
    output_file  :str  = args.output

    full_env_output = export_env(from_history=False, no_builds=no_builds)

    #-- Maintain default conda env export functionality
    if not from_history:
        final_env_dict = export_env(from_history=False, no_builds=no_builds)
        #produce_output(output_file, full_env_output, verbose=verbose)
        #return

    elif from_history and not use_versions:  #return the standard --from-history response
        final_env_dict = export_env(from_history=True)  #from history
        final_env_dict['channels'] = full_env_output['channels']

        _pip_section = get_pip_section(full_env_output['dependencies'])
        if len(_pip_section.values()) > 0:  #this adds the pip part 
            final_env_dict['dependencies'].append(_pip_section)

        #produce_output(output_file, from_history_env, verbose=verbose)
        #return

    elif from_history and use_versions:
        #-- Create merged list of dependencies
        full_env_output:dict = export_env(from_history=False, no_builds=False)
        hist_env_output:dict = export_env(from_history=True)
        _merged_dependencies:list = merge_dependencies(full_env_output, hist_env_output, use_versions)
        
        #-- setup final env dictionary
        final_env_dict = dict()
        final_env_dict['name']         = full_env_output['name']
        final_env_dict['channels']     = full_env_output['channels']
        final_env_dict['dependencies'] = _merged_dependencies

        _pip_section = get_pip_section(full_env_output['dependencies'])
        if len(_pip_section.values()) > 0:  #this adds the pip part 
            final_env_dict['dependencies'].append(_pip_section)

        final_env_dict['prefix']       = full_env_output['prefix']

    #-- Modify name and prefix if specified
    final_env_dict = _replace_env_name(env_name, full_env_output, final_env_dict, include_prefix=include_prefix)

    #-- Output final result
    produce_output(output_file, final_env_dict, verbose=verbose)
    

if __name__ == '__main__':
    args = CLI()
    main(args) 