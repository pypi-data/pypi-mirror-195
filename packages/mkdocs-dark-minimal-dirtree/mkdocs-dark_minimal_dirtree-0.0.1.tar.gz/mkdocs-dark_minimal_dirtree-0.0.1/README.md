# Dark minimal dir tree

## How to install

```bash
python -m pip install mkdocs
python -m pip install mkdocs-dark-minimal-dir-tree
python -m mkdocs new my-project
cd my-project
nano mkdocs.yml
```

Insert `theme` key:

```yml
site_name: My Docs
theme: 
    name: dark_minimal_dir_tree
```

```bash
python -m mkdocs serve

# or

python -m mkdocs build
```

## Links

- https://pypi.org/project/mkdocs-dark-minimal-dir-tree/