from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
from sklearn.svm import SVC

# set data
iris = datasets.load_iris()
x = iris.data

# set answer as category-data
y = iris.target

print(x.shape)
print(y.shape)
print(x[:5])
print(y[:5])

# データをランダムに並び替えたのち、訓練データ(割合8)とテストデータ(割合2)に分ける
x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8, test_size=0.2)

# スケーリング(標準化)を行う
scale = StandardScaler()
scale.fit(x_train)
x_train_std = scale.transform(x_train)
x_test_std = scale.transform(x_test)

# 訓練データを用いて分類器（Classifier）を作成する
classifier = SVC(kernel="linear")
classifier.fit(x_train_std, y_train)

# テストデータを分類器にかけて分類を実施する
y_pred = classifier.predict(x_test_std)

# 結果を表示する
print(y_pred)  # [1 1 2 1 2 2 0 2 1 1 0 2 0 1 0 2 1 2 1 0 0 1 2 0 0 2 2 2 1 0]
print(y_test)  # [1 1 2 1 2 2 0 2 2 1 0 2 0 1 0 2 2 2 2 0 0 1 2 0 0 2 1 2 1 0]
print(metrics.confusion_matrix(y_test, y_pred))
print(metrics.classification_report(y_test, y_pred))
