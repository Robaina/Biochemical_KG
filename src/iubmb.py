import xml.etree.ElementTree as ET
import html


def parse_inner_xml(text):
    try:
        # Wrapping the text in a root tag and parsing it
        wrapped_text = f"<root>{text}</root>"
        root = ET.fromstring(wrapped_text)
        return "".join(
            root.itertext()
        )  # Extracting and concatenating all text within the XML
    except ET.ParseError:
        return text  # Return the original text if parsing fails


def extract_ec_numbers(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    ec_dict = {}

    for table_data in root.findall(".//table_data"):
        for row in table_data.findall("row"):
            row_fields = {}
            ec_number = None
            has_reaction = False

            for field in row.findall("field"):
                field_name = field.get("name")
                field_value = html.unescape(field.text) if field.text else ""

                # Parse inner XML/HTML content
                field_value = parse_inner_xml(field_value)

                if field_name == "ec_num":
                    ec_number = field_value
                elif field_name == "reaction":
                    has_reaction = True

                row_fields[field_name] = field_value

            if ec_number and has_reaction:
                ec_dict[ec_number] = row_fields

    return ec_dict
