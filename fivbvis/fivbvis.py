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
            return f'Fields="{fields}"'

        return ''

    def set_filter(self, filters):
        if filters is None:
            return ''

        filter_str = []
        for key, value in filters.items():
            # Convert snake_case to PascalCase for the XML attribute names
            xml_key = ''.join(word.capitalize() for word in key.split('_'))
            filter_str.append(f'{xml_key}="{value}"')

        # Combine all attributes
        if len(filter_str) > 0:
            filter_str = ' '.join(filter_str)
        else:
            filter_str = ''

        if filter_str:
            return f'<Filter {filter_str}/>'

        return ''

    def set_tags(self, tags):
        if tags:
            tags = urllib.parse.quote(tags)
            return f'<Filter><Tags>{tags}</Tags></Filter>'

        return ''

    def set_attributes(self, attributes):
        # Build attributes from kwargs
        attributes_str = []
        for key, value in attributes.items():
            # Convert snake_case to PascalCase for the XML attribute names
            xml_key = ''.join(word.capitalize() for word in key.split('_'))
            attributes_str.append(f'{xml_key}="{value}"')

        # Combine all attributes
        if len(attributes_str) > 0:
            all_attributes = ' '.join(attributes_str)
        else:
            all_attributes = ''
        
        return all_attributes

    def get(self, request_type, fields=None, filters=None, content_type='xml', new_format=False, **kwargs):
        
        filter_str = self.set_filter(filters)
        fields_str = self.set_fields(fields)       
        all_attributes = self.set_attributes(kwargs)
        all_attributes = all_attributes + ' ' + fields_str


        if filters:
            url = self.base_url + f'<Request Type="{request_type}" {all_attributes}>{filter_str}</Request>'
        else:
            url = self.base_url + f'<Request Type="{request_type}" {all_attributes}/>'
        
        print(url)
        result = self.make_request(url, request_type, content_type)

        if content_type == 'json':
            result = json.loads(result)

        return result

    def get_list_with_tags(self, request_type, fields, tags, content_type='xml'):
        fields = self.set_fields(fields)
        tags = self.set_tags(tags)

        url = self.base_url + f'<Request Type="{request_type}" {fields}>{tags}</Request>'
        return self.make_request(url, request_type, content_type)
