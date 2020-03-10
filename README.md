Rebranding tool
===============

Replaces files and text inside files. Example layout file is in `mappings-example.yml`. Start by renaming this file to `mappings.yml` and changing
path inside to the real destination path (where target project resides).

Define files that needs to be replaced under `files:` section. Every `dst` file will be replaced by `src` file. `src` file is always relative to current directory, while `dst` is relative to a directory specified in `path`:

```
path: /some/directory
files:
 - src: source_file
   dst: destination_file
```

Configuration above will replace file `/some/directory/destination_file` with `./source_file`. 

Define text files that have text that needs to be replaced in `text:` section of configuration file. 
* `file` - path to destination file. Relative to `path` configuration option.
* `text` - text pattern (no regexps!) that will be replaced
* `replace` - replacement text

Exclude files that need to be excluded by defining them in `exclude:` section
