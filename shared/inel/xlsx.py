"""Write and read simple .xlsx sheets with the standard library.

Enough for annotation workbooks: one sheet, text cells, a frozen header row,
dropdown lists on coding columns, and protected ID columns. Excel, LibreOffice,
Numbers and Google Sheets all read these files. Reading accepts files saved back
by any of them (shared strings or inline strings).
"""
import re
import zipfile
from xml.sax.saxutils import escape

_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
_CTRL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def col_letter(i):
    s = ""
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def _cell(ref, value, style):
    v = escape(_CTRL.sub("", str(value)))
    return f'<c r="{ref}" t="inlineStr" s="{style}"><is><t xml:space="preserve">{v}</t></is></c>'


def write(path, header, rows, dropdowns=None, editable=None, widths=None):
    """dropdowns: {column name: [allowed values]}. editable: names of columns left unlocked."""
    dropdowns = dropdowns or {}
    editable = set(editable or ())
    widths = widths or {}
    style = {h: (2 if h in editable else 1) for h in header}
    lines = []
    lines.append("<row r=\"1\">" + "".join(_cell(f"{col_letter(j)}1", h, 3) for j, h in enumerate(header)) + "</row>")
    for i, r in enumerate(rows, 2):
        lines.append(f'<row r="{i}">' + "".join(
            _cell(f"{col_letter(j)}{i}", r.get(h, ""), style[h]) for j, h in enumerate(header)) + "</row>")
    last = len(rows) + 1
    cols = "".join(f'<col min="{j + 1}" max="{j + 1}" width="{widths.get(h, 14)}" customWidth="1"/>'
                   for j, h in enumerate(header))
    dv = ""
    if dropdowns and rows:
        items = []
        for j, h in enumerate(header):
            if h in dropdowns:
                formula = '"' + ",".join(dropdowns[h]) + '"'
                if len(formula) > 255:
                    raise ValueError(f"dropdown for {h} is longer than Excel allows")
                rng = f"{col_letter(j)}2:{col_letter(j)}{last}"
                items.append(f'<dataValidation type="list" allowBlank="1" showErrorMessage="1" '
                             f'errorTitle="Not in codebook" error="Pick a value from the list." sqref="{rng}">'
                             f'<formula1>{escape(formula)}</formula1></dataValidation>')
        dv = f'<dataValidations count="{len(items)}">{"".join(items)}</dataValidations>'
    sheet = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
             f'<worksheet xmlns="{_NS}"><sheetViews><sheetView workbookViewId="0">'
             f'<pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>'
             f'<cols>{cols}</cols><sheetData>{"".join(lines)}</sheetData>'
             f'<sheetProtection sheet="1" objects="1" scenarios="1" formatColumns="0" autoFilter="0" sort="0"/>'
             f'{dv}</worksheet>')
    styles = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><styleSheet xmlns="{_NS}">'
              '<fonts count="2"><font><sz val="11"/><name val="Calibri"/></font>'
              '<font><b/><sz val="11"/><name val="Calibri"/></font></fonts>'
              '<fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill>'
              '<fill><patternFill patternType="solid"><fgColor rgb="FFFFF2CC"/><bgColor indexed="64"/></patternFill></fill></fills>'
              '<borders count="1"><border/></borders><cellStyleXfs count="1"><xf/></cellStyleXfs>'
              '<cellXfs count="4"><xf/>'
              '<xf applyAlignment="1" applyProtection="1"><alignment wrapText="1" vertical="top"/><protection locked="1"/></xf>'
              '<xf fillId="2" applyFill="1" applyAlignment="1" applyProtection="1"><alignment wrapText="1" vertical="top"/><protection locked="0"/></xf>'
              '<xf fontId="1" applyFont="1" applyProtection="1"><protection locked="1"/></xf>'
              '</cellXfs><cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>'
              '</styleSheet>')
    files = {
        "[Content_Types].xml": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
            '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
            '</Types>'),
        "_rels/.rels": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
            '</Relationships>'),
        "xl/workbook.xml": (
            f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="{_NS}" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            '<sheets><sheet name="items" sheetId="1" r:id="rId1"/></sheets></workbook>'),
        "xl/_rels/workbook.xml.rels": (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
            '</Relationships>'),
        "xl/worksheets/sheet1.xml": sheet,
        "xl/styles.xml": styles,
    }
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, body in files.items():
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, body)


def read(path):
    """First sheet as a list of dicts keyed by the header row."""
    import xml.etree.ElementTree as ET
    q = f"{{{_NS}}}"
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        shared = []
        if "xl/sharedStrings.xml" in names:
            for si in ET.fromstring(z.read("xl/sharedStrings.xml")).iter(q + "si"):
                shared.append("".join(t.text or "" for t in si.iter(q + "t")))
        sheet_name = sorted(n for n in names if n.startswith("xl/worksheets/sheet"))[0]
        root = ET.fromstring(z.read(sheet_name))
    grid = []
    for row in root.iter(q + "row"):
        cells = {}
        for c in row.iter(q + "c"):
            col = re.match(r"[A-Z]+", c.get("r")).group(0)
            idx = 0
            for ch in col:
                idx = idx * 26 + ord(ch) - 64
            t = c.get("t")
            if t == "inlineStr":
                val = "".join(x.text or "" for x in c.iter(q + "t"))
            else:
                v = c.find(q + "v")
                val = "" if v is None else (v.text or "")
                if t == "s" and val:
                    val = shared[int(val)]
            cells[idx - 1] = val
        grid.append([cells.get(i, "") for i in range(max(cells) + 1)] if cells else [])
    if not grid:
        return []
    header = grid[0]
    return [{h: (r[i] if i < len(r) else "") for i, h in enumerate(header)} for r in grid[1:] if any(r)]
