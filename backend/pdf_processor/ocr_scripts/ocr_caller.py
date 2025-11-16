import fitz
import easyocr
from PIL import Image
import numpy as np

reader = easyocr.Reader(['ru', 'en'])

def group_blocks(blocks, y_threshold=20):

    blocks = sorted(blocks, key=lambda b: b["bounding_box"]["y"])
    lines = []
    current_line = []
    current_y = None

    for block in blocks:
        y = block["bounding_box"]["y"]
        if current_y is None:
            current_y = y

        if abs(y - current_y) <= y_threshold:
            current_line.append(block)
        else:
            current_line = sorted(current_line, key=lambda b: b["bounding_box"]["x"])
            lines.append(current_line)
            current_line = [block]
            current_y = y

    if current_line:
        current_line = sorted(current_line, key=lambda b: b["bounding_box"]["x"])
        lines.append(current_line)

    return lines


def process_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    output = {"pages": []}

    for i, page in enumerate(doc, start=1):
        zoom = 400 / 72
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)

        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img_np = np.array(img)

        result = reader.readtext(img_np, paragraph=False, contrast_ths=0.3, adjust_contrast=1.0)

        blocks = []
        for bbox, text, _ in result:
            (x1, y1), (_, _), (x2, y2), (_, _) = bbox
            blocks.append({
                "text": text,
                "bounding_box": {
                    "x": int(x1),
                    "y": int(y1),
                    "width": int(x2 - x1),
                    "height": int(y2 - y1),
                }
            })

        lines = group_blocks(blocks)

        output["pages"].append({
            "page_number": i,
            "lines": [
                [{"text": b["text"], "bounding_box": b["bounding_box"]} for b in line]
                for line in lines
            ]
        })

    doc.close()
    return output
