from helpers import render_vtest

from neoscore.common import *

neoscore.setup()

text = """
<p>
test paragraph 1
</p>
<p align=right>
test paragraph 2, aligned right!
and <span style="color: red">with coloring</span>!
</p>
"""

rt = RichText((Mm(0), Mm(0)), None, text, Mm(20))

render_vtest("rich_text")
