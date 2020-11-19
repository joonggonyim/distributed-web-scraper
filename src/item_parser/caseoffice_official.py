from absl import logging

def parse_description(description):
  """
  Example description:
  —-Sold out🚫—-
  Tricot comme des garcons non-collar wool jacket
  M size.
  condition : B+
  Made in japan. acrylic 70%, wool 30%. black color
  shoulder : 40cm , length : 54cm , bust : 43cm , waist : 43cm , sleeve : 61cm

  World wide shipping.
  Not included shipping costs. Thanks :)
  """
  try:
    item_data = dict()
    description_lines = description.split('\n')
    item_data['sold_out'] = 'sold out' in description_lines[0].lower()
    description_lines = (description_lines[1:] if item_data['sold_out'] else 
                         description_lines)
    item_data['name'] = description_lines[0]
    item_data['size'] = description_lines[1]
    item_data['condition'] = description_lines[2].split(':')[1].strip()
    item_data['origin'] = description_lines[3]
    item_data['dimensions'] = description_lines[4]
    return item_data
  except Exception as e:
    logging.error('Something went wrong while parsing. %s', e)
    return {}