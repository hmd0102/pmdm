def create_model_friendly_benign(filename="benign_pass.pdf", num_pages=15):
    objects = []
    obj_id = 1

    # Catalog
    objects.append(f"""{obj_id} 0 obj
<< /Type /Catalog
   /Pages 2 0 R
>>
endobj
""")
    obj_id += 1

    # Pages root placeholder
    pages_id = obj_id
    objects.append("PAGES_PLACEHOLDER")
    obj_id += 1

    page_ids = []

    # Generate pages
    for i in range(num_pages):
        page_id = obj_id
        content_id = obj_id + 1

        page_ids.append(page_id)

        # Page
        objects.append(f"""{page_id} 0 obj
<< /Type /Page
   /Parent {pages_id} 0 R
   /MediaBox [0 0 612 792]
   /Contents {content_id} 0 R
   /Resources << /Font << /F1 999 0 R >> >>
>>
endobj
""")

        # Content (LÀM TO để tăng pdf_size)
        text_block = "\\n".join([f"(This is benign content line {j}) Tj" for j in range(20)])

        objects.append(f"""{content_id} 0 obj
<< /Length 1000 >>
stream
BT
/F1 12 Tf
72 720 Td
{text_block}
ET
endstream
endobj
""")

        obj_id += 2

    # Font (fixed id để reuse)
    objects.append(f"""999 0 obj
<< /Type /Font
   /Subtype /Type1
   /BaseFont /Helvetica
>>
endobj
""")

    # Info
    info_id = obj_id
    objects.append(f"""{info_id} 0 obj
<< /Producer (Benign Generator)
   /Title (Normal Document)
>>
endobj
""")
    obj_id += 1

    # Fix Pages
    kids = " ".join([f"{pid} 0 R" for pid in page_ids])
    pages_obj = f"""{pages_id} 0 obj
<< /Type /Pages
   /Kids [{kids}]
   /Count {num_pages}
>>
endobj
"""
    objects = [pages_obj if x == "PAGES_PLACEHOLDER" else x for x in objects]

    # Build PDF
    pdf_body = "%PDF-1.4\n" + "\n".join(objects)

    xref = f"""
xref
0 {obj_id}
0000000000 65535 f 
""" + "\n".join(["0000000000 00000 n " for _ in range(obj_id - 1)])

    trailer = f"""
trailer
<< /Size {obj_id}
   /Root 1 0 R
   /Info {info_id} 0 R
>>
startxref
0
%%EOF
"""

    with open(filename, "wb") as f:
        f.write((pdf_body + xref + trailer).encode("latin1"))

    print(f"Created {filename} (pages={num_pages}, objs~{obj_id})")


if __name__ == "__main__":
    create_model_friendly_benign()