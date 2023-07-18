## Conda Export Tool

A simple tool that produces environment files for
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
