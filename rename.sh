#!/bin/bash

set -x

orig_modname=new_script
dest_modname=foo

orig_scriptname=script
dest_scriptname=bar


# Call sed to fix the module name inside the files:

read -d '' files <<EOF
./README.md
./setup.py
./Makefile.in
./bin/$orig_scriptname
./bin/$orig_modname/__init__.py
./bin/$orig_modname/boilerplate.py
./bin/$orig_modname/conf.py
./bin/$orig_modname/date_file_handler.py
./bin/$orig_modname/test/__init__.py
./bin/$orig_modname/test/test_boilerplate.py
./etc/$orig_modname/${orig_scriptname}_logging.conf
EOF

for f in $files ; do

    # Linux:
    #sed -i -e "s/$orig_modname/$dest_modname/g" $f || exit $?

    # OS X:
    sed -i '' -e "s/$orig_modname/$dest_modname/g" $f || exit $?

done

# Rename the appropriate directories according to the new module name.

read -d '' dirs <<EOF
./bin/$orig_modname
./etc/$orig_modname
./share/$orig_modname
EOF

for d in $dirs ; do

    mv $d $(dirname $d)/$dest_modname || exit $?

done

# Call sed and rename files according to the new script name.

# Linux:
#sed -i -e "s/${orig_scriptname}_logging/${dest_scriptname}_logging/g" \
#   ./bin/$orig_scriptname || exit $?
#sed -i -e "s/${orig_scriptname}_logging/${dest_scriptname}_logging/g" \
#   setup.py || exit $?

# OS X:
sed -i='' -e "s/${orig_scriptname}_logging/${dest_scriptname}_logging/g" \
   ./bin/$orig_scriptname || exit $?
sed -i='' -e "s/${orig_scriptname}_logging/${dest_scriptname}_logging/g" \
   setup.py || exit $?

mv ./bin/$orig_scriptname ./bin/$dest_scriptname || exit $?

mv ./etc/$dest_modname/${orig_scriptname}_logging.conf \
        ./etc/$dest_modname/${dest_scriptname}_logging.conf || exit $?



