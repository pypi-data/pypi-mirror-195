from pathlib import Path
from typing import Union, List

import fitz


class PDFConvertor:

    @staticmethod
    def convert(
            path: Union[str, Path], sort_by_position: bool = False
    ) -> List[str]:
        doc = fitz.open(path)
        page_count = int(doc.page_count)

        document = ""
        for i in range(page_count):
            page = doc[i]
            document += page.get_text("text", sort=sort_by_position) + "\f"

        pages = document.split("\f")[:-1]

        cleaned_pages = []
        for page in pages:
            lines = page.splitlines()
            cleaned_lines = []
            for line in lines:
                words = line.split()
                digits = [word for word in words if any(i.isdigit() for i in word)]

                if words and len(digits) / len(words) > 0.4 and not line.strip().endswith("."):
                    continue
                cleaned_lines.append(line)

            page = "\n".join(cleaned_lines)
            cleaned_pages.append(page)

        return cleaned_pages
