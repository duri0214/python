import os
from datetime import datetime

import chardet
from unittest import TestCase
from Util.util import convert_iso_to_ymdhms, convert_sjis2utf8, get_add_ym, convert_to_formal, convert_to_ymd, \
    count_work_day, is_over_lap, get_now_ym


class Test(TestCase):
    def test_convert_iso_to_ymdhms(self):
        temp = '2019-02-06T06:00:00+09:00'
        expected = '2019/02/06 06:00:00'
        self.assertEqual(expected, convert_iso_to_ymdhms(temp))

    def test_convert_sjis2utf8(self):
        os.makedirs('temp', exist_ok=True)
        temp_file = 'temp/sjis.txt'
        with open(temp_file, 'w', encoding='shift_jis') as f:
            f.write('このファイルはシフトJISでエンコードされています\n')
        with open(temp_file, 'rb') as f:
            expected = 'SHIFT_JIS'
            self.assertEqual(expected, chardet.detect(f.read())['encoding'])
        convert_sjis2utf8(temp_file)
        with open(temp_file, 'rb') as f:
            expected = 'utf-8'
            self.assertEqual(expected, chardet.detect(f.read())['encoding'])

    def test_get_now_ym(self):
        # today is 2022/2/13
        self.assertEqual('202202', get_now_ym())

    def test_get_add_ym(self):
        self.assertEqual('202201', get_add_ym(-1))
        self.assertEqual('202203', get_add_ym(1))

    def test_convert_to_formal(self):
        self.assertEqual('2022/02/13', convert_to_formal('20220213'))

    def test_convert_to_ymd(self):
        self.assertEqual('20220213', convert_to_ymd(datetime.today()))

    def test_count_work_day(self):
        self.assertEqual(7, count_work_day('20220212', '20220222'))

    def test_is_over_lap(self):
        self.assertTrue(is_over_lap('20190401-20190430,20190410-20190420'))
        self.assertTrue(is_over_lap('20190401-20190415,20190410-20190430'))
        self.assertTrue(is_over_lap('20190410-20190430,20190401-20190415'))
        self.assertFalse(is_over_lap('20190401-20190409,20190410-20190430'))
        self.assertFalse(is_over_lap('20190410-20190430,20190401-20190409'))
