# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'product_description':
                value = adapter.get(field_name)
                if type(value) == 'str':
                    adapter[field_name] = value.strip()
                elif type(value) == 'tuple':
                    adapter[field_name] = value[0].strip()

        lowercase_keys = ['genre', 'product_type']
        for lowercase_key in lowercase_keys:
            adapter[lowercase_key] = adapter.get(lowercase_key).lower()

        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for price_key in price_keys:
            adapter[price_key] = float(adapter.get(price_key).replace('£', ''))

        availability_string = adapter.get('availability')
        split_string_array = availability_string.split('(')
        if len(split_string_array) < 2:
            adapter['availability'] = 0
        else:
            availability = split_string_array[1].split(' ')
            adapter['availability'] = int(availability[0])
        
        rating_string = adapter.get('rating')
        adapter['rating'] = self.rating_string_to_int(rating_string)

        return item

    def rating_string_to_int(self, rating_string):
        if rating_string == 'one':
            return 1
        elif rating_string == 'two':
            return 2
        elif rating_string == 'three':
            return 3
        elif rating_string == 'four':
            return 4
        elif rating_string == 'five':
            return 5
        elif rating_string == 'zero':
            return 0

