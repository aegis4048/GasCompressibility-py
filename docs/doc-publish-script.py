from distutils.dir_util import copy_tree

from_dir = 'build/html'
to_dir = 'GasCompressibiltiy-py-docs'

copy_tree(from_dir, to_dir)

# run this script before publishing to documentation page

# git rm --cached GasCompressibiltiy-py-docs -r
# git submodule add https://github.com/aegis4048/GasCompressibiltiy-py-docs.git GasCompressibiltiy-py-docs

