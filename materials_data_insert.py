import csv
import re

import hm
import hm.entities as ent

model = hm.Model()


def _parse_numeric(value):
    if value is None:
        return None

    text = value.strip()
    if not text:
        return None

    try:
        return float(text)
    except ValueError:
        match = re.search(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", text)
        if match is None:
            return None
        return float(match.group(0))


def _get_row_value(row, *headers):
    for header in headers:
        if header in row:
            return row.get(header)
    return None


def _get_unique_name(base_name, name_counts):
    name_counts[base_name] = name_counts.get(base_name, 0) + 1
    index = name_counts[base_name]
    if index == 1:
        return base_name
    return f"{base_name}{index}"


def material_variables_from_row(row):
    # material_name is composed from two CSV headers: Material + Type
    material_base = (_get_row_value(row, "Material", "material") or "").strip()
    material_type = (_get_row_value(row, "Type", "type") or "").strip()
    material_name = "_".join(part for part in [material_base, material_type] if part)
    if not material_name:
        material_name = "material"

    mat8_e1 = _parse_numeric(_get_row_value(row, "E1", "e1"))
    mat8_e2 = _parse_numeric(_get_row_value(row, "E2", "e2"))
    mat8_nu12 = _parse_numeric(_get_row_value(row, "NU12", "nu12"))
    mat8_g12 = _parse_numeric(_get_row_value(row, "G12", "g12"))
    mat8_g1z = _parse_numeric(_get_row_value(row, "G1Z", "g1z", "MAT8_G1Z"))
    mat8_g2z = _parse_numeric(_get_row_value(row, "G2Z", "g2z", "MAT8_G2Z"))
    mat8_rho = _parse_numeric(_get_row_value(row, "Rho", "rho"))
    mat8_xt = _parse_numeric(_get_row_value(row, "Xt", "xt"))
    mat8_xc = _parse_numeric(_get_row_value(row, "Xc", "xc"))
    mat8_yt = _parse_numeric(_get_row_value(row, "Yt", "yt"))
    mat8_yc = _parse_numeric(_get_row_value(row, "Yc", "yc"))
    mat8_s = _parse_numeric(_get_row_value(row, "S", "s"))

    # comment_array is composed from the CSV headers: Model/Comment + thickness
    comment_array = []
    model_comment = (_get_row_value(row, "Model/Comment", "model/comment") or "").strip()
    thickness = (_get_row_value(row, "thickness", "Thickness") or "").strip()
    if model_comment:
        comment_array.append(model_comment)
    if thickness:
        comment_array.append(f"thickness={thickness}")

    return {
        "material_name": material_name,
        "mat8_e1": mat8_e1,
        "mat8_e2": mat8_e2,
        "mat8_nu12": mat8_nu12,
        "mat8_g12": mat8_g12,
        "mat8_g1z": mat8_g1z,
        "mat8_g2z": mat8_g2z,
        "mat8_rho": mat8_rho,
        "mat8_xt": mat8_xt,
        "mat8_xc": mat8_xc,
        "mat8_yt": mat8_yt,
        "mat8_yc": mat8_yc,
        "mat8_s": mat8_s,
        "comment_array": comment_array,
    }


def material_create(material_values):
    material_name = material_values["material_name"]
    mat8_e1 = material_values["mat8_e1"]
    mat8_e2 = material_values["mat8_e2"]
    mat8_nu12 = material_values["mat8_nu12"]
    mat8_g12 = material_values["mat8_g12"]
    mat8_g1z = material_values["mat8_g1z"]
    mat8_g2z = material_values["mat8_g2z"]
    mat8_rho = material_values["mat8_rho"]
    mat8_xt = material_values["mat8_xt"]
    mat8_xc = material_values["mat8_xc"]
    mat8_yt = material_values["mat8_yt"]
    mat8_yc = material_values["mat8_yc"]
    mat8_s = material_values["mat8_s"]
    comment_array = material_values["comment_array"]

    material = ent.Material(model, cardimage="MAT8", name=material_name)
    if mat8_e1 is not None:
        material.MAT8_E1 = mat8_e1
    if mat8_e2 is not None:
        material.MAT8_E2 = mat8_e2
    if mat8_nu12 is not None:
        material.MAT8_NU12 = mat8_nu12
    if mat8_g12 is not None:
        material.MAT8_G12 = mat8_g12
    if mat8_g1z is not None:
        material.MAT8_G1Z = mat8_g1z
    if mat8_g2z is not None:
        material.MAT8_G2Z = mat8_g2z
    if mat8_rho is not None:
        material.MAT8_RHO = mat8_rho
    if mat8_xt is not None:
        material.MAT8_Xt = mat8_xt
    if mat8_xc is not None:
        material.MAT8_Xc = mat8_xc
    if mat8_yt is not None:
        material.MAT8_Yt = mat8_yt
    if mat8_yc is not None:
        material.MAT8_Yc = mat8_yc
    if mat8_s is not None:
        material.MAT8_S = mat8_s
    material.COMMENT_OPTION = 2
    if comment_array:
        material.COMMENT_ARRAY = comment_array

    return material


def iter_material_rows(csv_file_path="material_data.csv"):
    with open(csv_file_path, newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if not any((value or "").strip() for value in row.values()):
                continue
            yield row


def main(csv_file_path="material_data.csv"):
    created_materials = []
    name_counts = {}
    for row in iter_material_rows(csv_file_path):
        material_values = material_variables_from_row(row)
        material_values["material_name"] = _get_unique_name(
            material_values["material_name"],
            name_counts,
        )
        created_materials.append(material_create(material_values))
    return created_materials


if __name__ == "__main__":
    main()
    
