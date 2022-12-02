from unittest import TestCase
from basic_regex.regex import regex


class Test(TestCase):
    def test_regex_01(self):
        """
        Hitする（あいまい・単数）
        """
        input_values = 'aaa_data bbb_data ccc'
        patterns = 'data'
        separators = ',、'
        self.assertTrue(regex(input_values, patterns, separators))

    def test_regex_02(self):
        """
        Hitする（あいまい・複数）
        """
        input_values = 'aaa_data bbb_data ccc_data'
        patterns = 'data,zzz'
        separators = ',、'
        self.assertTrue(regex(input_values, patterns, separators))

    def test_regex_03(self):
        """
        Hitする（完全一致・単数）
        """
        input_values = 'aaa_data bbb_data ccc_data'
        patterns = 'aaa_data bbb_data ccc_data'
        separators = ',、'
        self.assertTrue(regex(input_values, patterns, separators))

    def test_regex_04(self):
        """
        Hitする（完全一致・複数）
        """
        input_values = 'aaa_data bbb_data ccc_data'
        patterns = 'aaa_data bbb_data ccc_data,zzz'
        separators = ',、'
        self.assertTrue(regex(input_values, patterns, separators))

    def test_regex_05(self):
        """
        Hitしない
        """
        input_values = 'aaa_data bbb_data ccc'
        patterns = '!data!'
        separators = ',、'
        self.assertFalse(regex(input_values, patterns, separators))

    def test_regex_06(self):
        """
        separators指定なし
        """
        input_values = 'aaa_data bbb_data ccc_data'
        patterns = 'data,zzz'
        self.assertTrue(regex(input_values, patterns))

    def test_regex_07(self):
        """
        正規表現のエスケープ文字が混入している
        """
        input_values = r'aaa_data .^$|\[({+abc"?bbb_data'
        patterns = '+abc'
        self.assertTrue(regex(input_values, patterns))
