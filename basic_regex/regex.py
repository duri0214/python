import re


def regex(input_value: str, patterns: str, separators: str = ',') -> bool:
    """
    あいまい検索・複数検索に対応した正規表現処理
    @param input_value:
    @param patterns:
    @param separators:
    @return: patterns をつかって input_value から hit できたら True
    """
    patterns = [re.escape(x) for x in re.split(f'[{separators}]', patterns)]

    return re.search('|'.join(patterns), input_value) is not None
