
from PyInstaller.utils.hooks import (
    collect_submodules,
    copy_metadata,
    is_module_satisfies,
)

hiddenimports = collect_submodules('markdown.extensions')
hiddenimports += collect_submodules('markdown.extensions.meta')

# Markdown 3.3 introduced markdown.htmlparser submodule with hidden
# dependency on html.parser
if is_module_satisfies("markdown >= 3.3"):
    hiddenimports += ['html.parser']

# Extensions can be referenced by short names, e.g. "extra", through a mechanism
# using entry-points. Thus we need to collect the package metadata as well.
datas = copy_metadata("markdown")