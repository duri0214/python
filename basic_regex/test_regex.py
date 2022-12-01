from unittest import TestCase
from basic_regex.regex import regex


class Test(TestCase):
    def test_regex_01(self):
        """
        Hitする
        """
        input_values = 'aaa_data bbb_data ccc'
        patterns = 'data'
        separators = ',、'
        self.assertTrue(regex(input_values, patterns, separators))

    def test_regex_02(self):
        """
        Hitしない
        """
        input_values = 'aaa_data bbb_data ccc'
        patterns = 'hoge!'
        separators = ',、'
        self.assertFalse(regex(input_values, patterns, separators))

    def test_regex_03(self):
        """
        patternが単数
        """
        input_values = 'aaa_data bbb_data ccc_data'
        patterns = 'data,zzz'
        separators = ',、'
        self.assertTrue(regex(input_values, patterns, separators))

    def test_regex_04(self):
        """
        patternが複数
        """
        input_values = 'aaa_data bbb_data ccc_data'
        patterns = 'data,zzz'
        separators = ',、'
        self.assertTrue(regex(input_values, patterns, separators))

    def test_regex_05(self):
        """
        separators指定なし
        """
        input_values = 'aaa_data bbb_data ccc_data'
        patterns = 'data,zzz'
        self.assertTrue(regex(input_values, patterns))

    def test_regex_06(self):
        """
        正規表現のエスケープ文字が混入している
        """
        input_values = r'aaa_data .^$|\[({+abc"?bbb_data'
        patterns = '+abc'
        self.assertTrue(regex(input_values, patterns))
