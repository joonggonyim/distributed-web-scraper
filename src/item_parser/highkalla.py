import re


def parse_update_time(description):
  """Parses the update time.

  If update related keywords are detected in parse_description, this function
  will be called to extract the actual update time.
  
  example:
  -------------------------
  Highkalla new update✨

  화려한 가을과 겨울

  Time 8:00
  -------------------------
  HighKalla Tomorrow Update🍂
  #WinterCoat

  내일은 우리들의 겨울을 따뜻하게 책임져 줄, 아름다운 브랜드 코트들을 준비했습니다. 기대해주세요🥰✨
  -------------------------
  Highkalla new update✨

  화요일 업데이트 하이-앤드 브랜드 제품들과 함께 합니다. 클랙식한 스타일부터 캐주얼한 느낌까지 다양하게 준비 했어요 잠시 후 8시 만나요🎶
  -------------------------
  """
  # Try to extract time
  # regex = 'pm ?\d:?\d{,2}'
  #   pm8:00, pm 8:00, pm8, pm 8
  # regex = '\d:?\d{,2} ?pm'
  #   8:00pm, 8:00 pm, 8pm, 8 pm
  # regex = '\d시'
  #   8시
  # regex = '[T|t]ime ?\d:?\d{,2}'
  #   'Time 8:00', 'Time 8', 'Time8:00', 'Time8',
  #   'time 8:00', 'time 8', 'time8:00', 'time8'
  times_found = []
  for line in description.split('\n'):
    regex = r'pm ?\d:?\d{,2}|\d:?\d{,2} ?pm|\d시|[T|t]ime ?\d:?\d{,2}'
    found = re.findall(regex, line)
    if found:
      times_found += found
  return {'update_times': times_found}


def parse_description(description):
  """
  Example description:
  Burberry 노바체크슬리브 싱글코트
  💜sold out
  어깨(레글런)약47 가슴57 총장110
  울80 나일론20
  .
  문의DM
  #burberry
  """
  if 'update' in description.lower():
    return parse_update_time(description)
  item_data = dict()
  description_lines = description.split('\n')
  item_data['name'] = description_lines[0]
  item_data['sold_out'] = 'sold out' in description_lines[1].lower()

  return item_data