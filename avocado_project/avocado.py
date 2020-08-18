import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("avocado.csv")
#데이터를 불러옵니다.

print("Columns of the data.")
print(data.columns)
#칼럼 중 4046은 가장 작은 아보카도, 4225는 조금 더 큰 거, 4770은 아주 큰 아보카도인 것 같습니다.

#계절마다 아보카도 사이즈 소비량이 변화가 있는지 궁금합니다.


avocadosOrigin = data.loc[:, ["Date", '4046', '4225', '4770']]

avocados = avocadosOrigin

avocadosDay = avocadosOrigin.copy()

#아보카도 사이즈에 따른 판매량과 날짜를 추출합니다.

avocados.loc[:, "Date"] = avocados.loc[:, "Date"].str.replace("-", "").str.slice(4, 6)

avocadosDay.loc[:, "Date"] = avocadosDay.loc[:, "Date"].str.replace("-", "").str.slice(6, 8)

#날짜 데이터를 2020-01-02에서 20200102꼴로 바꾼 다음, 슬라이싱을 하여 달과 일수만 출력합시다.

print(avocados.head())

avocadoGB = avocados.groupby(["Date"]).mean()

#같은 달의 데이터를 모두 평균 내어 봅시다.

avocadoGB = avocadoGB.reset_index()

#reset_index() 메소드를 통해 생긴 시리즈의 인덱스를 리셋합니다. 인덱스를 리셋하며 인덱스는 열로 하나 추가됩니다.

avocadoDayGB = avocadosDay.groupby(["Date"]).mean()

#같은 일의 데이터를 모두 평균 내어 봅시다.

avocadoDayGB = avocadoDayGB.reset_index()

#마찬가지로 reset_index() 메소드를 통해 생긴 시리즈의 인덱스를 리셋합니다. 인덱스를 리셋하며 인덱스는 열로 하나 추가됩니다.

print(avocadoGB.head())

print(avocadoDayGB.head())

fig, ax =plt.subplots()
#이렇게 하면 여러 개의 플롯을 겹치게 할 수 있습니다.

ax.plot(avocadoGB.loc[:, "Date"], avocadoGB.loc[:, "4046"].sub(avocadoGB.loc[:, "4046"].mean()).div(avocadoGB.loc[:, "4046"].std()),  label = "small")
# 판다스 시리즈는 길이가 같은 객체에 대해 연산이 가능합니다. 여기선 플롯 과정에서 정규화 과정을 거치겠습니다.
ax.plot(avocadoGB.loc[:, "Date"], avocadoGB.loc[:, "4225"].sub(avocadoGB.loc[:, "4225"].mean()).div(avocadoGB.loc[:, "4225"].std()), label = "medium")
ax.plot(avocadoGB.loc[:, "Date"], avocadoGB.loc[:, "4770"].sub(avocadoGB.loc[:, "4770"].mean()).div(avocadoGB.loc[:, "4770"].std()),  label = "big")

plt.legend()
#이렇게 하면 각 다른 데이터에 대한 레이블이 보입니다.

plt.show()
#이 커맨드를 하면 show 이전의 플롯 명령어가 실행됩니다.

fig2, ax2 =plt.subplots()

ax2.plot(avocadoDayGB.loc[:, "Date"], avocadoDayGB.loc[:, "4046"].sub(avocadoDayGB.loc[:, "4046"].mean()).div(avocadoDayGB.loc[:, "4046"].std()),  label = "small")
ax2.plot(avocadoDayGB.loc[:, "Date"], avocadoDayGB.loc[:, "4225"].sub(avocadoDayGB.loc[:, "4225"].mean()).div(avocadoDayGB.loc[:, "4225"].std()), label = "medium")
ax2.plot(avocadoDayGB.loc[:, "Date"], avocadoDayGB.loc[:, "4770"].sub(avocadoDayGB.loc[:, "4770"].mean()).div(avocadoDayGB.loc[:, "4770"].std()),  label = "big")
plt.legend()
plt.show()





