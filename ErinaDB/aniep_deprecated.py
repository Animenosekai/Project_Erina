'''
aniep.js by soruly
> https://github.com/soruly/aniep/blob/master/src/index.js

aniep.js translation to python by Anime no Sekai
Erina Project - 2020

Status: Unfinished
'''

import re

def episode_from_filename(filename):
  episode = None
  filename = filename.replace('.mp4', "") # remove file extension
  filename = filename.replace('.mov', "") # remove file extension
  filename = filename.replace('.mkv', "") # remove file extension
  filename = filename.replace('v2', "") # remove v2, v3 suffix
  filename = filename.replace('v3', "") # remove v2, v3 suffix
  filename = re.sub(r"(\d)v[0-5]", r"$1", filename) # remove v2 from 13v2 #i
  filename = re.sub(r'(\[\d{4,}])', '', filename) # remove years and dates like [2019] [20190301]
  # filename = filename.replace((\[[0-9a-f]{6,8}]), ""); # remove checksum like [c3cafe11]

  episode = re.search(r'^(\d{1,3})(?:-|~)(\d{1,3})$', filename) # 13.mp4
  if episode is not None:
    print('1')
    return episode.group()


  def kanjis_to_digit(kanjis):
    '''
    Translate kanjis number to digits from 0 to 100.
    i.e.  三十二 ==> 32
    '''
    kanjis_to_digit_data = {
      '一': 1,
      '二': 2,
      '三': 3,
      '四': 4,
      '五': 5,
      '六': 6,
      '七': 7,
      '八': 8,
      '九': 9,
      '十': 1,
    }
    unwanted = ['第', '話', '集', '话', '回', '夜', ' ']
    for kanji in unwanted:
      kanjis = kanjis.replace(kanji, '')
    kanjis = kanjis.replace('第', '').replace('話', '')
    digits = ''
    for character in range(len(kanjis)):
      if character + 1 == len(kanjis) and kanjis[character] == '十':
        if digits == '':
          digits = '10'
        else:
          digits = digits + '0'
      elif kanjis[character] == '十':
        if digits == '':
          digits = digits + str(kanjis_to_digit_data[kanjis[character]])
        else:
          pass
      else:
        digits = digits + str(kanjis_to_digit_data[kanjis[character]])
    return digits

  episode = re.search(r'第([一二三四五六七八九十]+)(?:集|話|话|回|夜)', filename) # 第三話
  if episode is not None:
    print('2')
    return kanjis_to_digit(episode.group())

  episode = re.search(r'第 *(\d+(?:\.\d)*) *(?:集|話|话|回|夜)', filename) # 第 13.5 話
  if episode is not None:
    kanjis = episode.group()
    unwanted = ['第', '話', '集', '话', '回', '夜', ' ']
    for kanji in unwanted:
      kanjis = kanjis.replace(kanji, '')
    print('3')
    return kanjis

  episode = re.search(r'第 *(\d+)-(\d+) *(?:集|話|话|回|夜)', filename) # 第 01-13 話
  if episode is not None:
    kanjis = episode.group()
    unwanted = ['第', '話', '集', '话', '回', '夜', ' ']
    for kanji in unwanted:
      kanjis = kanjis.replace(kanji, '')
    print('4')
    return kanjis

  episode = re.search(r'(?:s|v)\d{1,2}ep*(\d{1,2})', filename) # S03EP13 #i
  if episode is not None:
    print('5')
    return episode.group()

  # special case

  episode = re.search(r' - (\d\d(?:\.\d)*) *(?:Fin)* *\[720]', filename) # xxxx - 13 [720] #i
  if episode is not None:
    print('6')
    return episode.group().replace('-', '').replace(' ', '').replace('[720]', '').replace('[720p]', '')

  episode = re.search(r'\[(\d{1,3}(?:\.\d)*) *(?:END)*]', filename) # [13END]
  if episode is not None:
    print('7')
    return episode.group()

  episode = re.search(r'\[(\d{1,2})\((?:OVA|OAD)\)]', filename) # [13END]
  if episode is not None:
    print('8')
    return episode.group()

  episode = re.search(r'[^\w\d](?:OVA|OAD|SP|OP|ED|NCOP|NCED|EX|CM|PV|Preview|Yokoku|メニュー|Menu|エンディング|Movie)[-_ ]{0,1}(\d{1,2})[^\w\d]', filename) # [OVA1] #i
  if episode is not None:
    print('9')
    return episode.group()

  episode = re.search(r'【(\d+)】', filename) # 【13】
  if episode is not None:
    print('10')
    return episode.group()

  episode = re.search(r'「(\d+)」', filename) # 「13」
  if episode is not None:
    print('11')
    return episode.group()

  """
  episode = filename.match(\[(\d+)-(\d+)\((\d+)-(\d+)\)]); # xxxx[01-02(13-14)]xxxx
  if episode is not None:
    return [
      [parseFloat(episode[1]), parseFloat(episode[2])].sort((a, b) => a - b).join(","),
      [parseFloat(episode[3]), parseFloat(episode[4])].sort((a, b) => a - b).join(","),
    ]
      .sort((a, b) => parseFloat(a.split(",")[1]) - parseFloat(b.split(",")[1]))
      .join("|"); # "1,2|13,14"
  """

  """
  episode = filename.match(\[(\d+)\((?:EP\.)*(\d+)\)]); # xxxx[01(ep.13)]xxxx #i
  if episode is not None:
    return [parseFloat(episode[1]), parseFloat(episode[2])].sort((a, b) => a - b).join("|")
  """


  """
  episode = filename.match(\[(\d+)(?: |_|-)(?:S\d)(?: |_|-)(\d+)(?: END)*]); # xxxx[13 s2-01]xxxx #i
  if episode is not None:
    return [parseFloat(episode[1]), parseFloat(episode[2])].sort((a, b) => a - b).join("|")
  """

  episode = re.search(r'\[(\d+(?:\.\d)*)(?:-|&)(\d+(?:\.\d)*)(?:END)*]', filename) # xxxx[01-13END]xxxx
  if episode is not None:
    print('12')
    return episode.group()

  """
  episode = filename.match(\[(\d+)-(\d+)_(\d+)-(\d+)]); # xxxx[01-02_13-14]xxxx
  if episode is not None:
    return [
      [parseFloat(episode[1]), parseFloat(episode[2])].sort((a, b) => a - b).join(","),
      [parseFloat(episode[3]), parseFloat(episode[4])].sort((a, b) => a - b).join(","),
    ]
      .sort((a, b) => parseFloat(a.split(",")[1]) - parseFloat(b.split(",")[1]))
      .join("|"); # "1,2|13,14"
  """


  """
  episode = filename.match(\[(\d+)_(\d+)]); # xxxx[01_13]xxxx
  if episode is not None:
    return [parseFloat(episode[1]), parseFloat(episode[2])].sort((a, b) => a - b).join("|")
  """


  """
  episode = filename.match( - (\d{1,3}(?:\.\d)*) *\((?:s\d-)*(\d{1,3}(?:\.\d)*)\)); # xxxx - 01.5 (s1-13.5)xxxx #i
  if episode is not None:
    return [parseFloat(episode[1]), parseFloat(episode[2])].sort((a, b) => a - b).join("|")
  """


  episode = re.search(r'.+\[(\d{1,3}(?:\.\d)*)[^pPx]{0,4}]', filename) # xxxx[13.5yyyy]xxxx #i
  if episode is not None:
    print('13')
    return episode.group()

  episode = re.search(r'\[(\d{1,3})[ _-].+?]', filename) # xxxx[13-xxxx]xxxx
  if episode is not None:
    print('14')
    return episode.group()

  episode = re.search(r'\[[^]+_(\d{1,2})]', filename) # xxxx[xxxx_13]xxxx
  if episode is not None:
    print('15')
    return episode.group()

  episode = re.search(r' (\d\d) \[', filename) # xxxx 13 [
  if episode is not None:
    print('16')
    return episode.group()

  episode = re.search(r'(?: |\[|]|-)(\d\d)(?:\[|])', filename) # xxxx[ 13[xxxx
  if episode is not None:
    print('17')
    return episode.group()

  episode = re.search(r's\d-(\d{1,2})', filename) # xxxxs2-13xxxx #i
  if episode is not None:
    print('18')
    return episode.group()

  episode = re.search(r'(?:EP|Episode) *(\d{1,3}(?:\.\d\D)*)', filename) # xxxxEP 13.5xxxx #i
  if episode is not None:
    print('19')
    return episode.group()

  episode = re.search(r'^(\d{1,3}(?:\.\d)*) - ', filename) # 13.5 - xxxx
  if episode is not None:
    print('20')
    return episode.group()

  episode = re.search(r' - (\d+)[-~](\d+)', filename) # xxxx - 13-26xxxx
  if episode is not None:
    print('21')
    return episode.group()

  episode = re.search(r' - (\d{1,3}(?:\.\d)*)', filename) # xxxx - 13.5xxxx
  if episode is not None:
    print('22')
    return episode.group()

  episode = re.search(r'^(\d{1,3}(?:\.\d)*)\D', filename) # 13.5xxxx
  if episode is not None:
    print('23')
    return episode.group()

  episode = re.search(r'(?:#|＃)(\d{1,2})\D', filename) # xxxx#13xxxx
  if episode is not None:
    print('24')
    return episode.group()

  episode = re.search(r' (\d{1,3}(?:\.\d)*)[^xpP\]\d]{0,4} ', filename) # xxxx 13.5yyyy xxxx
  if episode is not None:
    print('25')
    return episode.group()

  episode = re.search(r'\W(\d{1,3})-(\d{1,3})$', filename) # xxxx01-13.mp4
  if episode is not None:
    print('26')
    return episode.group()

  episode = re.search(r'(\d{1,3})$', filename) # xxxx13.mp4
  if episode is not None:
    print('27')
    return episode.group()

  episode = re.search(r'\D\.(\d{1,3})\.\D', filename) # xxxx.13.xxxx
  if episode is not None:
    print('28')
    return episode.group()

  episode = re.search(r'\D(\d{1,3}) - ', filename) # xxxx13 - xxxx
  if episode is not None:
    print('29')
    return episode.group()

  episode = re.search(r'(?: |_)(\d{1,3})_', filename) # xxxx_13_xxxx
  if episode is not None:
    print('30')
    return episode.group()

  return None
