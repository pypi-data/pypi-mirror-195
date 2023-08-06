from unittest import TestCase
from .custom_assert import OVERRIDE

import re
import os


class TestReadme(TestCase):
    def test_readme_svgs(self):
        with open('README.md', 'r', encoding='utf-8') as f:
            readme = f.read()
        codes = re.findall(
            r"(?<=```py\n).*?(?=```)",
            readme,
            re.MULTILINE | re.DOTALL
        )

        for code in codes:
            if OVERRIDE:
                exec(code)
                continue

            svg_path = re.findall(
                r"(?<=write_svg\(.).*?(?=.\))",
                code,
            )
            assert len(svg_path) == 1
            svg_path = svg_path[0]

            svg_dummy_path = svg_path + '.dummy'
            code = code.replace(svg_path, svg_dummy_path)

            assert os.path.isfile(svg_path)
            assert not os.path.isfile(svg_dummy_path)

            try:
                exec(code)

                with open(svg_path, 'r') as f:
                    svg = f.read()

                with open(svg_dummy_path, 'r') as f:
                    dummy_svg = f.read()

                self.assertEqual(svg, dummy_svg)
                os.remove(svg_dummy_path)
            except Exception as e:
                os.remove(svg_dummy_path)
                raise e
