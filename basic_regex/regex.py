import re


def regex(input_value: str, patterns: str, separators: str = ',') -> bool:
    """
    あいまい検索・複数検索に対応した正規表現処理
    @param input_value: 正規表現をかけられるテキスト
    @param patterns: 正規表現をかけるパターン（複数指定可能）
    @param separators: パターンが複数指定されていた場合にわけるための文字
    @return: patterns をつかって input_value から hit できたら True
    """
    patterns = [re.escape(x) for x in re.split(f'[{separators}]', patterns)]

    return re.search('|'.join(patterns), input_value) is not None
