import httpx
import json
import urllib

class FivbVis():
    def __init__(self):
        self.base_url = 'https://www.fivb.org/Vis2009/XmlRequest.asmx?Request='

    def make_request(self, url, request_type, content_type):
        accepted_content_types = ['json', 'xml']

        if content_type not in accepted_content_types:
            raise ValueError(f'{content_type}: The provided value is not accepted.')

        headers = {'Accept': f'application/{content_type}'}
        response = httpx.get(url, headers=headers, timeout=20.0)

        if content_type == 'xml':
            return response.text
        elif content_type == 'json':
            return json.dumps(response.json(), ensure_ascii=False)

    def set_fields(self, fields):
        if fields:
            # Clean up multi-line strings and extra whitespace
            # Split by any whitespace and rejoin with single spaces
            cleaned_fields = ' '.join(fields.split())
            return f'Fields="{cleaned_fields}"'

        return ''

    def set_filter(self, filters):
        if not filters:
            return ''

        filter_attributes = []
        for key, value in filters.items():
            # Convert snake_case to PascalCase for the XML attribute names
            xml_key = ''.join(word.capitalize() for word in key.split('_'))
            filter_attributes.append(f'{xml_key}="{value}"')

        filter_str = ' '.join(filter_attributes)
        return f'<Filter {filter_str}/>'

    def set_tags(self, tags):
        if tags:
            tags = urllib.parse.quote(tags)
            return f'<Filter><Tags>{tags}</Tags></Filter>'

        return ''

    def set_attributes(self, attributes):
        """Convert kwargs to XML attributes, converting snake_case to PascalCase."""
        if not attributes:
            return ''
        
        attributes_list = []
        for key, value in attributes.items():
            xml_key = ''.join(word.capitalize() for word in key.split('_'))
            attributes_list.append(f'{xml_key}="{value}"')
        
        return ' '.join(attributes_list)

    def get(self, request_type, fields=None, filters=None, content_type='xml', **kwargs):
        """Make a GET request to the FIVB VIS Web Service."""
        # Build all parts of the request
        filter_str = self.set_filter(filters)
        fields_str = self.set_fields(fields)
        attributes_str = self.set_attributes(kwargs)
        
        # Combine attributes and fields
        all_attributes = f'{attributes_str} {fields_str}'.strip()

        # Build URL based on whether we have filters
        if filters:
            url = self.base_url + f'<Request Type="{request_type}" {all_attributes}>{filter_str}</Request>'
        else:
            url = self.base_url + f'<Request Type="{request_type}" {all_attributes}/>'
        
        result = self.make_request(url, request_type, content_type)

        # Parse JSON if needed
        if content_type == 'json':
            result = json.loads(result)

        return result

    def get_list_with_tags(self, request_type, fields, tags, content_type='xml'):
        fields = self.set_fields(fields)
        tags = self.set_tags(tags)

        url = self.base_url + f'<Request Type="{request_type}" {fields}>{tags}</Request>'
        return self.make_request(url, request_type, content_type)
