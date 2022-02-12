import datetime
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta


def convert_iso_to_ymdhms(iso_ymdhms: str) -> str:
    """
    @param iso_ymdhms: 2019-02-06T06:00:00+09:00
    @return: タイムゾーンつきの文字列のフォーマットをdatetime str に変える 2019/02/06 06:00:00
    """
    return datetime.fromisoformat(iso_ymdhms).strftime("%Y/%m/%d %H:%M:%S")


def convert_sjis2utf8(file_full_path: str) -> None:
    """
    @param file_full_path:
    @return: テキストファイルを sjis から utf8 に変換します
    """
    temp = file_full_path + '.swp'
    os.rename(file_full_path, temp)
    stream_in = open(temp, 'rb')
    stream_out = open(file_full_path, 'wb')
    for line in stream_in:
        stream_out.write(line.decode('sjis').encode('utf8'))
    stream_in.close()
    stream_out.close()
    os.remove(temp)


def get_now_ym() -> str:
    """
    @return: str systemYMを返します 202202
    """
    ret = datetime.today()
    return datetime.strftime(ret, '%Y%m')


def get_add_ym(i):
    """
    @param i: 増減させる月数
    @return: systemYMに i を加味した値を返します 202203"""
    ret = datetime.today() + relativedelta(months=i)
    return datetime.strftime(ret, '%Y%m')


def convert_to_formal(yyyymmdd):
    """
    @param yyyymmdd:
    @return: yyyymmddからyyyy/mm/ddへ変換
    """
    return datetime.strptime(yyyymmdd, '%Y%m%d').strftime('%Y/%m/%d')


def convert_to_ymd(date_formal):
    """
    @param date_formal:
    @return: yyyy/mm/ddからyyyymmddへ変換
    """
    return datetime.strftime(date_formal, '%Y%m%d')


def count_work_day(yyyymmdd_st, yyyymmdd_en, workday='1111100'):
    """
    第1周目) 最初の端切れ（土-日）
    第2周目) 掛け算でパターン計算できる範囲（月-日）。平日の数は 5
    第3周目) 最後の端切れ（月-火）。平日の数は 2
    と3段階で数字の連結を作ると「00 + (1111100 * multiple) + 11」
    @param yyyymmdd_st: 2022/2/12(土)
    @param yyyymmdd_en: 2022/2/22(火)
    @param workday: 1111100は土日が休みであることを表す bit
    @return: stからenの範囲のうちworkdayが1の場所をカウントして返す 7
    """
    day_range = (datetime.strptime(yyyymmdd_st, '%Y%m%d'), datetime.strptime(yyyymmdd_en, '%Y%m%d'))
    # range are 25 days
    day_range_cnt = (day_range[1]-day_range[0]).days + 1
    # A) 00
    combine = workday[day_range[0].weekday():]
    # B) (1111100 * multiple)
    multiple = (day_range_cnt - len(combine)) // 7
    combine += workday * multiple
    # C) 11
    combine += workday[:(day_range_cnt - len(combine)) % 7]
    return combine.count('1')


def is_over_lap(yyyymmdd_sten1sten2):
    """
    例：20190401-20190415,20190410-20190430 のように指定します
    @param yyyymmdd_sten1sten2:
    @return: 2つの期間が重なり合うかどうかを判定する。例えばMHIの号機期間の重複判定にも使えます
    """
    ymd1 = yyyymmdd_sten1sten2.split(',')[0].split('-')
    ymd2 = yyyymmdd_sten1sten2.split(',')[1].split('-')
    return ymd2[0] <= ymd1[1] and ymd1[0] <= ymd2[1]
