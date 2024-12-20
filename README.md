# make-koyomi
暦を作るプロジェクトです

# 年情報
## 干支
ある年を西暦で表した値を10で割った余り、すなわち一の位を求め、下表から十干を割り出します。

| 余り (一の位) | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|--------------|---|---|---|---|---|---|---|---|---|---|
| 十干         | 庚| 辛| 壬| 癸| 甲| 乙| 丙| 丁| 戊| 己|

同様に、西暦で表した値を12で割った余りを求め、下表から十二支を割り出します。

| 余り | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|-----|---|---|---|---|---|---|---|---|---|---|----|----|
| 十二支 | 申 | 酉 | 戌 | 亥 | 子 | 丑 | 寅 | 卯 | 辰 | 巳 | 午 | 未 |

## 九星
年号から九星の番号(1~9)を計算する方法が実装されています。その計算方法は以下のようになっています。

### 桁和の計算

まず、年の各桁の数字を足し合わせて「桁和」を求めます。
これは sum_digits() という関数で実現されています。

#### 特別な扱い: 桁和が1の場合

桁和が1の場合は、特別に10として扱います。
これは、1は「一白水星」に対応するため、特別な扱いが必要となります

### 九星の番号の算出

最終的に得られた1桁の数値から、11を引くことで九星の番号(1~9)を求めます。
これは、九星が1~9の循環的な番号付けになっているためです。

以下の表を参考に手順で、年号から九星の番号を算出しています。
### 九星の表
| 九星番号 | 漢字 | 読み | 属性 | 方位 | 色 |
|----------|------|------|------|------|------|
| 1 | 一白水星 | いっぱくすいせい | 水 | 北 | 白 |
| 2 | 二黒土星 | じこくどせい | 土 | 南西 | 黒 |
| 3 | 三碧木星 | さんぺきもくせい | 木 | 東 | 碧 |
| 4 | 四緑木星 | しろくもくせい | 木 | 東南 | 緑 |
| 5 | 五黄土星 | ごおうどせい | 土 | 中央 | 黄 |
| 6 | 六白金星 | ろっぱくきんせい | 金 | 西北 | 白 |
| 7 | 七赤金星 | しちせききんせい | 金 | 西 | 赤 |
| 8 | 八白土星 | はっぱくどせい | 土 | 南 | 白 |
| 9 | 九紫火星 | きゅうしかせい | 火 | 南 | 紫 |

## 納音
| 用語 | 用語の読み | 干支 |
| --- | --- | --- |
| 海中金 | かいちゅうきん | 甲子・乙丑 |
| 爐中火 | ろちゅうか | 丙寅・丁卯 |
| 大林木 | たいりんぼく | 戊辰・己巳 |
| 路傍土 | ろぼうど | 庚午・辛未 |
| 釼鋒金 | じんぼうきん | 壬申・癸酉 |
| 山頭火 | さんとうか | 甲戌・乙亥 |
| 澗下水 | かんかすい | 丙子・丁丑 |
| 城頭土 | じょうとうど | 戊寅・己卯 |
| 白鑞金 | はくろうきん | 庚辰・辛巳 |
| 楊柳木 | ようりゅうぼく | 壬午・癸未 |
| 井泉水 | せいせんすい | 甲申・乙酉 |
| 屋上土 | おくじょうど | 丙戌・丁亥 |
| 霹靂火 | へきれきか | 戊子・己丑 |
| 松柏木 | しょうはくぼく | 庚寅・辛卯 |
| 長流水 | ちょうりゅうすい | 壬辰・癸巳 |
| 沙中金 | さちゅうきん | 甲午・乙未 |
| 山下火 | さんげか | 丙申・丁酉 |
| 平地木 | へいちぼく | 戊戌・己亥 |
| 壁上土 | へきじょうど | 庚子・辛丑 |
| 金箔金 | きんぱくきん | 壬寅・癸卯 |
| 覆燈火 | ふくとうか | 甲辰・乙巳 |
| 天河水 | てんがすい | 丙午・丁未 |
| 大駅土 | たいえきど | 戊申・己酉 |
| 釵釧金 | さいせんきん | 庚戌・辛亥 |
| 桑柘木 | そうしゃくもく | 壬子・癸丑 |
| 大溪水 | だいけいすい | 甲寅・乙卯 |
| 沙中土 | さちゅうど | 丙辰・丁巳 |
| 天上火 | てんじょうか | 戊午・己未 |
| 柘榴木 | ざくろぼく | 庚申・辛酉 |
| 大海水 | たいかいすい | 壬戌・癸亥 |

## 主な暦注事項（年中行事・祝祭など）
- 元旦
- 成人の日
- 建国記念日
- 春分の日
- 昭和の日
- 憲法記念日
- みどりの日
- こどもの日
- 海の日
- 山の日
- 敬老の日
- 秋分の日
- スポーツの日
- 文化の日
- 勤労感謝の日
 [休日の算出方法は内閣府のページ参照](https://www8.cao.go.jp/chosei/shukujitsu/gaiyou.html)

# 二十四節気

二十四節気（にじゅうしせっき）は、１年の太陽の黄道上の動きを視黄経の15度ごとに24等分して決められている。太陰太陽暦（旧暦）では季節を表すために用いられていた。また、閏月を設ける基準とされており、中気のない月を閏月としていた。全体を春夏秋冬の４つの季節に分け、さらにそれぞれを６つに分けて、節気（せっき）と中気（ちゅうき）を交互に配している。

| 名称 | 太陽黄経 |
|------|----------|
| 立春 (りっしゅん) | 315° |
| 雨水 (うすい) | 330° |
| 啓蟄 (けいちつ) | 345° |
| 春分 (しゅんぶん) | 0° |
| 清明 (せいめい) | 15° |
| 穀雨 (こくう) | 30° |
| 立夏 (りっか) | 45° |
| 小満 (しょうまん) | 60° |
| 芒種 (ぼうしゅ) | 75° |
| 夏至 (げし) | 90° |
| 小暑 (しょうしょ) | 105° |
| 大暑 (たいしょ) | 120° |
| 立秋 (りっしゅう) | 135° |
| 処暑 (しょしょ) | 150° |
| 白露 (はくろ) | 165° |
| 秋分 (しゅうぶん) | 180° |
| 寒露 (かんろ) | 195° |
| 霜降 (そうこう) | 210° |
| 立冬 (りっとう) | 225° |
| 小雪 (しょうせつ) | 240° |
| 大雪 (たいせつ) | 255° |
| 冬至 (とうじ) | 270° |
| 小寒 (しょうかん) | 285° |
| 大寒 (だいかん) | 300° |

# 月ごとの暦情報
## 干支
月初の日の干支を表示。日の干支は2024年1月1日の甲子から数える。
## 月の大小
31日の月を大として、30日以下の月を小としている。これはcalender.monthrangeで取得できる。

## 雑節（主な季節の変わり目）
### 節分
立春の前日。
### お彼岸
春分と秋分の前後の3日ずつの計7日のこと。初日を彼岸の入り、当日を中日（ちゅうにち）、終日を明けと呼ぶ。
### 土用
| 太陽黄経 | 説明 |
|----------|------|
| 27°, 117°, 207°, 297° | 太陰太陽暦では立春、立夏、立秋、立冬の前18日間を指した。最近では夏の土用だけを指すことが多い。 |

### 社日
| 春の社日 | 秋の社日 |
|----------|----------|
| 春分（3月21日頃）に最も近い戊の日 | 秋分（9月23日頃）に最も近い戊の日 |
### 八十八夜
立春から数えて88日目をいう。霜が降りることが少なくなる頃。
### 入梅
太陽黄経 : 80°<br>
太陰太陽暦では芒種の後の壬（みずのえ）の日。つゆの雨が降り始める頃。
### 半夏生
太陽黄経 : 100°<br>
太陰太陽暦では夏至より10日後とされていた。
### 二百十日
立春から数えて、210日目の日。
### 七夕
7月7日
### 伝統的七夕
太陰太陽暦にもとづく七夕を「伝統的七夕」と呼んでいます。
二十四節気の処暑（しょしょ＝太陽黄経が150度になる瞬間）を含む日かそれよりも前で、処暑に最も近い朔（さく＝新月）の瞬間を含む日から数えて7日目が「伝統的七夕」の日です。
[参考](https://www.nao.ac.jp/faq/a0310.html)

## 八専
日の干支が壬子（甲子から数えて49番目）から癸亥（同60番目）の間の12日間の中に干支共に同じ五行となる物が壬子、甲寅、乙卯、丁巳、己未、庚申、辛酉、癸亥と、8日あるために八専と総称されている。十干と十二支に五行を割り当てると、干支の気が重なる日が全部で12日ある。そのうち8日が壬子から癸亥までの12日間に集中している[1]ため、この期間は特別な期間であると考えられるようになった。同気が重なることを「専一」と言い、それが8日あることから「八専」と言う。八専の期間には同気の重ならない日が4日あり、これを「八専の間日（まび）」と言う。八専のうち間日を除く8日間は同気が重なる（比和）ことから吉はますます吉となり、凶はますます凶となるとされた。しかしその後、凶の性質のみが強調されるようになった。現在では何事も上手く行かない凶日とされている。間日は十方暮とは異なり、八専の影響は受けないとされている。

## 甲子
甲子は、六十干支順位表で一番目に位置する干支。甲子の日の夜は、子の刻（深夜12時）まで起きて、商売繁盛、五穀豊穣などを子（ネズミ）を使者とする大黒天に祈り、祀ります。また大豆・黒豆・二股大根食しました。この祭りは甲子待（きのえねまち）、甲子祭、甲子講などとも呼ばれています。
「きのえ」は十干、「ね」は十二支の初めであり、陰陽道ではこの組み合わせの干支が祭りを行う最も吉日と説きます。

## 庚申
庚申は、六十干支順位表で五七番目の干支。この日は庚申様を祀り、夜を徹して飲食などを行い、古くから無病息災や長寿など現世利益の信仰を集めてきました。庚申待（こうしんまち）、宵（よい）庚申とも呼ばれています。庚申講として金融組織にもなりました。

## 己巳
己巳は六十干支順位表で六番目の干支で、甲子・庚申と同様に六〇日に一度巡ってきます。この日は、巳（ヘビ）を使者とする弁財天を祀る日です。


# 使っているライブラリskyfieldのドキュメント
- https://rhodesmill.org/skyfield/toc.html

# skyfieldのドキュメントをknowledgeに入れたClaude Project
- https://claude.ai/project/705ab4ce-67b2-4f94-84ef-4c948e65aff1