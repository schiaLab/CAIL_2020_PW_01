import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

stocks = pd.read_csv("skh.csv", thousands= ",") # 주식 데이터를 불러옵니다.
weather = pd.read_csv("weather.csv") #날씨 데이터도 불러옵니다.


#현재 weather 데이터셋과 skh 데이터베이스의 날짜가 완벽히 일치하지 않습니다.
#이렇게 되면 두 데이터셋을 비교하거나 병합할 수 없기 때문에, 동일한 날짜의 데이터를 같은 열에 넣을 예정입니다.

stocks.loc[:, "date"] = stocks.loc[:, "date"].str.replace('년 ', '').str.replace('월 ', '').str.replace('일', '')
#이렇게 년, 월, 일과 공백란을 지우면, 20110101처럼 날짜와 일대일대응되는 날짜가 나옵니다.


weather.loc[:, "date"] = weather.loc[:, "date"].str.replace('-', '')
#weather는 대시 기호로 나누어져 있으니, 대시 대신에 빈 문자열을 넣어주면 완성됩니다.



weather = weather.iloc[:, 2:]
#날씨 데이터 중 파이썬이 읽지 못하는 데이터가 있는 것 같습니다. 일단 눈대중으로 칼럼 인덱스를 골라 제거합니다.



newData = pd.merge(stocks.loc[: , ["date", "end"]], weather)
#이제 두 데이터셋을 병합합니다. 주의할 점은, 두 데이터셋에 같은 이름의 칼럼을 중심으로 두 데이터셋이 병합된다는 점입니다.



newData = newData.dropna().iloc[::-1, :]
#나중에 쓸 넘파이 메소드에서 에러가 나지 않도록 NaN 값을 가진 열을 모두 지워주고, 시간 순으로 정렬되도록 인덱스를 거꾸로 셉니다.

newData2 = newData.iloc[:, [2, 3]]
newData = newData.iloc[:, 1]



newData = np.array(newData.diff()[1:])
#전날과 오늘 주가를 빼는 작업을 진행해 봅니다. 판다스에선 .diff() 메소드를 통해 이를 지원합니다.




newData = (newData - newData.mean())/newData.std()
#데이터를 정규화해줍니다.

humi = newData2.iloc[1:, 0].to_numpy()
#상대습도 데이터를 분리해 넘파이 어레이로 바꾼 다음, 특별한 변수에 저장해 줍니다.

sun = newData2.iloc[1:, 1].to_numpy()
#일조량 데이터도 마찬가지로 해줍니다.


esti11 = ((humi - humi.mean()) / humi.std())
esti12 = ((sun - sun.mean())/sun.std())

#위의 코드 앞의 샵을 지워주면 일조량 간의 차이를 비교할 수 있습니다.

esti2 = ((sun - sun.mean())/sun.std()) - ((humi - humi.mean())/humi.std())
#esti2 변수에는 일조량과 습도를 뺀 값을 넣어봅시다.

esti11 = esti11[1:]
esti12 = esti12[1:]
esti2 =  esti2[1:]

newData = np.abs(newData[1:])


print("humi vs stock:", np.corrcoef(esti11, newData)[1, 0])
print("sun vs stock: ", np.corrcoef(esti12, newData)[1, 0])
print("(humi-sun) vs stock", np.corrcoef(esti2, newData)[1, 0])
#변수 간의 상관계수를 출력합니다. 두 변수 간의 상관계수는 0,1 혹은 1,0에 위치합니다.

plt.plot(esti11, newData, 'o')

plt.show()

plt.plot(esti12, newData, 'o')

plt.show()
#단일한 날씨 데이터(일조량 아님 상대습도)와 주가변동간의 관계를 그래프를 통해 확인해 봅시다.

plt.plot(esti2, newData, 'o')

plt.show()
#자신이 만들어본 날씨 데이터 간의 조합으로 주가 변동 간의 관계를 보다 잘 짚어봅시다.