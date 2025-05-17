# parser_xml.py (placeholder)
from xml.etree import ElementTree as ET

def parse_generic_request(xml_string):
    try:
        ns = {'soap': 'http://schemas.xmlsoap.org/soap/envelope/', 'db': 'http://example.com/dbService'}
        root = ET.fromstring(xml_string)
        body = root.find('soap:Body', ns)
        request = body.find('.//db:genericDBRequest', ns)
        interface = request.find('interface').text
        operation = request.find('operation').text
        parameters_node = request.find('parameters')
        parameters = {}
        if parameters_node is not None:
            for child in parameters_node:
                parameters[child.tag] = child.text
        return {"interface": interface, "operation": operation, "parameters": parameters}
    except Exception as e:
        print(f"Error al parsear XML: {e}")
        return None