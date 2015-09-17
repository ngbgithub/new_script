#!/bin/bash

# This is a little quick-and-dirty.  It is expected that this script
#   will be run from within share/new_script.

# Set up some useful variables.
output_dir=doc
conf_py=$output_dir/conf.py
module_path=$(pwd)/../../bin

# Note that this won't work quite right if there is a module with the
#   same name as an executable script, e.g. "foo/" and "foo.py".

# Run sphinx-apidoc
sphinx-apidoc \
    --module-first \
    --full \
    --doc-project=cooklrn \
    --doc-author="John Doe" \
    --doc-version="000.001" \
    --doc-release="000.001.001" \
    --output-dir=$output_dir \
    $module_path \
    || exit -1

# Note: The following steps will have to be done manually:

#   - The copyright line in conf.py may have to be fixed to not be
#     equal to the authors
#
#   - Any executable script rst files will have to be renamed to
#     reflect their installed names, and the first line of the rst
#     file will have to be changed to something like "foo script"
#
#   - Intersphinx has to be enabled by adding 'spinx.ext.intersphinx'
#     to the extensions list.  (Note that we add some intersphinx
#     mapping below.)


# Update sys.path in conf.py appropriately.  The following can in
#   principle be done in one line, but I think the two-step process is
#   *way* more readable.

# First, insert a newline before the "General configuration" line.
#   Note that using \n evidently works on Linux but not OS X, so we
#   use a literal newline.

#sed -i '' 's/^\(# -- General configuration\)/XXREPLACE_MEXXX\
#\1/' $conf_py

# Now actually insert our update to sys.path.

#sed -i '' "s%XXREPLACE_MEXXX%sys.path.insert(0, os.path.abspath('$module_path'))%" $conf_py

echo "" >> $conf_py
echo "sys.path.insert(0, os.path.abspath('$module_path'))" >> $conf_py

# Add some intersphinx configuration.
echo "intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}" >> $conf_py
