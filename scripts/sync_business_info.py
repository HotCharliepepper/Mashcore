"""Synchronize server-visible public business details in every HTML footer.

Run this after editing assets/js/site-config.js. HTML is used as the public
source for storefront review, even when a crawler does not execute JavaScript.
"""
from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
config = (ROOT / "assets/js/site-config.js").read_text(encoding="utf-8")
values = {
    match.group(1): match.group(2)
    for match in re.finditer(r"^\s*(companyName|representative|registrationNumber|address|phone|email):\s*'([^']*)'", config, re.M)
}
fields = [
    ("companyName", "상호"),
    ("representative", "대표자"),
    ("registrationNumber", "사업자등록번호"),
    ("address", "사업장 주소"),
    ("phone", "전화"),
    ("email", "이메일"),
]
parts = ['<dl class="business-info" data-business-info="">']
for key, label in fields:
    value = values.get(key, "").strip()
    if not value:
        continue
    if key == "email":
        rendered = '<a href="mailto:' + escape(value, quote=True) + '">' + escape(value) + '</a>'
    else:
        rendered = escape(value)
    parts.append("<div><dt>" + label + "</dt><dd>" + rendered + "</dd></div>")
parts.append("</dl>")
footer = "".join(parts)
pattern = re.compile(r'<dl class="business-info" data-business-info=""(?: hidden="")?>.*?</dl>', re.S)
updated = []
for file in ROOT.rglob("index.html"):
    if ".git" in file.parts:
        continue
    text = file.read_text(encoding="utf-8")
    if not pattern.search(text):
        continue
    output = pattern.sub(lambda _: footer, text)
    if output != text:
        file.write_text(output, encoding="utf-8")
        updated.append(str(file.relative_to(ROOT)))
print("Business footers synchronized:", updated or "already current")
