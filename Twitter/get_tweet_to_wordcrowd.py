import csv
import tweepy
import MeCab
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def get_tweet(screen_name, count):
    with open('api_setting/credentials.txt', mode='r') as f:
        consumer_key = f.readline().strip()
        consumer_secret = f.readline().strip()
        access_token_key = f.readline().strip()
        access_token_secret = f.readline().strip()

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    results = api.user_timeline(screen_name=screen_name, count=count)

    f = open('output.txt', 'w', encoding='UTF-8', newline='\n')
    writer = csv.writer(f)
    for result in results:
        writer.writerow([result.text.strip()])
    f.close()


def analyze_tweet():
    # Mecabを使用して、形態素解析
    mecab = MeCab.Tagger("-Ochasen")

    # "名詞", "動詞", "形容詞", "副詞"を格納するリスト
    words = []

    # ファイルを読込み
    with open('output.txt', 'r', encoding="UTF-8") as f:

        reader = f.readline()

        while reader:
            # Mecabで形態素解析を実施
            node = mecab.parseToNode(reader)

            while node:
                # 取得する単語種
                word_type = node.feature.split(",")[0]
                if word_type in ["名詞", "動詞", "形容詞", "副詞"]:
                    words.append(node.surface)
                node = node.next

            reader = f.readline()

    # wordcloudで出力するフォントを指定
    font_path = r"C:\WINDOWS\Fonts\meiryo.ttc"

    txt = " ".join(words)

    # ストップワードの設定　※これは検索キーワードによって除外したほうがいい単語を設定
    stop_words = ['https', 'RT', u'説明', u'データ', u'する']

    # 解析した単語、ストップワードを設定、背景の色は黒にしてます
    word_cloud = WordCloud(background_color="black", font_path=font_path, stopwords=set(stop_words),
                           width=800, height=600).generate(txt)

    plt.imshow(word_cloud)
    plt.axis("off")
    plt.savefig('output.png')


if __name__ == '__main__':
    get_tweet(screen_name='duri0214', count=10)
    analyze_tweet()
