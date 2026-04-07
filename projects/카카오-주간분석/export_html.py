"""PBTD 카카오모먼트 주간 분석 → HTML 보고서 (Streamlit 대시보드와 동일 구성)"""
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ──────────────────────────────────────────────
# 데이터 (app.py와 동일)
# ──────────────────────────────────────────────
RAW = {
    "캠페인": [
        "bizboard-retarget", "bizboard-retarget",
        "bizboard-ua", "bizboard-ua",
        "display-retarget", "display-retarget",
        "kakao 합계", "kakao 합계",
    ],
    "주차": ["W1", "W2", "W1", "W2", "W1", "W2", "W1", "W2"],
    "Impressions": [8_909_505, 11_116_000, 1_618_645, 2_892_869, 1_494_490, 850_437, 12_022_640, 14_859_306],
    "Clicks": [61_178, 65_497, 11_900, 12_653, 26_972, 15_252, 100_050, 93_402],
    "비용": [21_690_419, 23_643_311, 2_394_221, 2_719_175, 10_444_799, 5_334_921, 34_529_439, 31_697_407],
    "회원가입": [7, 16, 251, 427, 5, 3, 263, 446],
    "구매완료": [1_127, 1_449, 107, 214, 509, 295, 1_743, 1_958],
    "구매액": [66_387_990, 63_758_221, 4_914_681, 7_037_535, 31_049_160, 14_185_722, 102_351_831, 84_981_478],
    "구매유저(App)": [744, 931, 29, 47, 351, 203, 1_124, 1_181],
    "구매유저(Web)": [277, 396, 74, 162, 106, 64, 457, 622],
}
df = pd.DataFrame(RAW)
df["구매유저 합계"] = df["구매유저(App)"] + df["구매유저(Web)"]

W2_DB_COST = 31_697_407
W2_AIRBRIDGE_COST = 32_374_233
W2_RATIO = W2_AIRBRIDGE_COST / W2_DB_COST
df.loc[df["주차"] == "W2", "비용"] = (df.loc[df["주차"] == "W2", "비용"] * W2_RATIO).round(0).astype(int)
df.loc[(df["주차"] == "W2") & (df["캠페인"] == "kakao 합계"), "비용"] = W2_AIRBRIDGE_COST

ROAS_FACTOR = 1.763
df["CTR"] = df["Clicks"] / df["Impressions"] * 100
df["CPC"] = df["비용"] / df["Clicks"]
df["가입 CVR"] = df["회원가입"] / df["Clicks"] * 100
df["가입 CPA"] = df["비용"] / df["회원가입"]
df["가입→구매 CVR"] = df["구매완료"] / df["회원가입"] * 100
df["구매 CVR"] = df["구매완료"] / df["Clicks"] * 100
df["구매 CPA"] = df["비용"] / df["구매완료"]
df["ROAS"] = df["구매액"] / df["비용"] * ROAS_FACTOR * 100
df["ARPPU"] = df["구매액"] / df["구매유저 합계"]

CAMPAIGNS = ["bizboard-retarget", "bizboard-ua", "display-retarget"]
COLORS = {"bizboard-retarget": "#FAE100", "bizboard-ua": "#3C1E1E", "display-retarget": "#FF6B35"}
WEEK_COLORS = {"W1": "#5B8FF9", "W2": "#FF6B6B"}
MARGIN = dict(t=50, b=40, l=10, r=10)

# 광고그룹 데이터
ADGROUP_RAW = [
    {"캠페인": "bizboard-retarget", "광고그룹": "lecaf_selection", "주차": "W1", "Impressions": 1360280, "Clicks": 8544, "Cost (Channel)": 2207395, "회원가입": 2, "구매완료": 228, "구매액": 7557532, "구매유저(App)": 124, "구매유저(Web)": 97},
    {"캠페인": "bizboard-retarget", "광고그룹": "lecaf_selection", "주차": "W2", "Impressions": 4470125, "Clicks": 17995, "Cost (Channel)": 4570768, "회원가입": 14, "구매완료": 532, "구매액": 18043420, "구매유저(App)": 271, "구매유저(Web)": 242},
    {"캠페인": "bizboard-retarget", "광고그룹": "br_sub_rowen", "주차": "W1", "Impressions": 78671, "Clicks": 1390, "Cost (Channel)": 510852, "회원가입": 0, "구매완료": 33, "구매액": 1462631, "구매유저(App)": 28, "구매유저(Web)": 0},
    {"캠페인": "bizboard-retarget", "광고그룹": "br_sub_rowen", "주차": "W2", "Impressions": 22608, "Clicks": 509, "Cost (Channel)": 167591, "회원가입": 0, "구매완료": 3, "구매액": 138913, "구매유저(App)": 2, "구매유저(Web)": 1},
    {"캠페인": "bizboard-retarget", "광고그룹": "ct_runningshoes", "주차": "W1", "Impressions": 217740, "Clicks": 2093, "Cost (Channel)": 758905, "회원가입": 0, "구매완료": 57, "구매액": 2047838, "구매유저(App)": 49, "구매유저(Web)": 8},
    {"캠페인": "bizboard-retarget", "광고그룹": "ct_runningshoes", "주차": "W2", "Impressions": 882368, "Clicks": 3319, "Cost (Channel)": 1538139, "회원가입": 1, "구매완료": 97, "구매액": 3465146, "구매유저(App)": 79, "구매유저(Web)": 13},
    {"캠페인": "bizboard-retarget", "광고그룹": "4890514-product", "주차": "W1", "Impressions": 1672030, "Clicks": 5515, "Cost (Channel)": 1763519, "회원가입": 2, "구매완료": 164, "구매액": 5032676, "구매유저(App)": 91, "구매유저(Web)": 67},
    {"캠페인": "bizboard-retarget", "광고그룹": "4890514-product", "주차": "W2", "Impressions": 1240019, "Clicks": 2739, "Cost (Channel)": 962289, "회원가입": 0, "구매완료": 57, "구매액": 1753922, "구매유저(App)": 38, "구매유저(Web)": 19},
    {"캠페인": "bizboard-retarget", "광고그룹": "4890570-product", "주차": "W1", "Impressions": 131155, "Clicks": 1492, "Cost (Channel)": 677295, "회원가입": 0, "구매완료": 43, "구매액": 1355408, "구매유저(App)": 25, "구매유저(Web)": 15},
    {"캠페인": "bizboard-retarget", "광고그룹": "4890570-product", "주차": "W2", "Impressions": 236901, "Clicks": 1618, "Cost (Channel)": 897339, "회원가입": 0, "구매완료": 61, "구매액": 2330256, "구매유저(App)": 43, "구매유저(Web)": 15},
    {"캠페인": "bizboard-retarget", "광고그룹": "ct_now", "주차": "W1", "Impressions": 249105, "Clicks": 4523, "Cost (Channel)": 1509030, "회원가입": 0, "구매완료": 109, "구매액": 4214608, "구매유저(App)": 68, "구매유저(Web)": 33},
    {"캠페인": "bizboard-retarget", "광고그룹": "ct_now", "주차": "W2", "Impressions": 390563, "Clicks": 7087, "Cost (Channel)": 1853426, "회원가입": 0, "구매완료": 98, "구매액": 4033374, "구매유저(App)": 66, "구매유저(Web)": 28},
    {"캠페인": "bizboard-retarget", "광고그룹": "br_cpcompany", "주차": "W1", "Impressions": 811570, "Clicks": 4239, "Cost (Channel)": 2336360, "회원가입": 0, "구매완료": 57, "구매액": 6634683, "구매유저(App)": 47, "구매유저(Web)": 7},
    {"캠페인": "bizboard-retarget", "광고그룹": "br_cpcompany", "주차": "W2", "Impressions": 797176, "Clicks": 4918, "Cost (Channel)": 2347737, "회원가입": 1, "구매완료": 55, "구매액": 5117426, "구매유저(App)": 45, "구매유저(Web)": 4},
    {"캠페인": "bizboard-retarget", "광고그룹": "br_stoneisland", "주차": "W1", "Impressions": 1931318, "Clicks": 9696, "Cost (Channel)": 2745739, "회원가입": 2, "구매완료": 51, "구매액": 7507039, "구매유저(App)": 45, "구매유저(Web)": 5},
    {"캠페인": "bizboard-retarget", "광고그룹": "br_stoneisland", "주차": "W2", "Impressions": 1025542, "Clicks": 4020, "Cost (Channel)": 2284654, "회원가입": 0, "구매완료": 61, "구매액": 5156358, "구매유저(App)": 53, "구매유저(Web)": 3},
    {"캠페인": "bizboard-retarget", "광고그룹": "ct_highbrand", "주차": "W1", "Impressions": 1166299, "Clicks": 8487, "Cost (Channel)": 2921391, "회원가입": 0, "구매완료": 80, "구매액": 15958954, "구매유저(App)": 71, "구매유저(Web)": 3},
    {"캠페인": "bizboard-retarget", "광고그룹": "ct_highbrand", "주차": "W2", "Impressions": 643931, "Clicks": 2886, "Cost (Channel)": 1722924, "회원가입": 0, "구매완료": 37, "구매액": 3996378, "구매유저(App)": 30, "구매유저(Web)": 1},
    {"캠페인": "bizboard-retarget", "광고그룹": "ct_athleredition", "주차": "W1", "Impressions": 249944, "Clicks": 1365, "Cost (Channel)": 950689, "회원가입": 0, "구매완료": 28, "구매액": 1982203, "구매유저(App)": 24, "구매유저(Web)": 0},
    {"캠페인": "bizboard-retarget", "광고그룹": "ct_athleredition", "주차": "W2", "Impressions": 225285, "Clicks": 1121, "Cost (Channel)": 809551, "회원가입": 0, "구매완료": 23, "구매액": 1350754, "구매유저(App)": 17, "구매유저(Web)": 3},
    {"캠페인": "bizboard-retarget", "광고그룹": "ct_benefit", "주차": "W1", "Impressions": 75230, "Clicks": 914, "Cost (Channel)": 452987, "회원가입": 0, "구매완료": 29, "구매액": 1565655, "구매유저(App)": 26, "구매유저(Web)": 1},
    {"캠페인": "bizboard-retarget", "광고그룹": "ct_benefit", "주차": "W2", "Impressions": 172658, "Clicks": 2651, "Cost (Channel)": 873239, "회원가입": 0, "구매완료": 49, "구매액": 2822285, "구매유저(App)": 44, "구매유저(Web)": 4},
    {"캠페인": "bizboard-retarget", "광고그룹": "ct_hiking", "주차": "W2", "Impressions": 51742, "Clicks": 2374, "Cost (Channel)": 397871, "회원가입": 0, "구매완료": 29, "구매액": 1174457, "구매유저(App)": 21, "구매유저(Web)": 7},
    {"캠페인": "bizboard-retarget", "광고그룹": "ct_shortsleeve", "주차": "W2", "Impressions": 22071, "Clicks": 586, "Cost (Channel)": 264129, "회원가입": 0, "구매완료": 14, "구매액": 647293, "구매유저(App)": 11, "구매유저(Web)": 0},
    {"캠페인": "bizboard-retarget", "광고그룹": "ct_warehouserelease", "주차": "W2", "Impressions": 69715, "Clicks": 1625, "Cost (Channel)": 565963, "회원가입": 0, "구매완료": 37, "구매액": 1521212, "구매유저(App)": 30, "구매유저(Web)": 5},
    {"캠페인": "bizboard-retarget", "광고그룹": "3570214-product", "주차": "W1", "Impressions": 383846, "Clicks": 5914, "Cost (Channel)": 1994223, "회원가입": 0, "구매완료": 86, "구매액": 5148521, "구매유저(App)": 65, "구매유저(Web)": 16},
    {"캠페인": "bizboard-retarget", "광고그룹": "3570214-product", "주차": "W2", "Impressions": 312453, "Clicks": 4801, "Cost (Channel)": 1726771, "회원가입": 0, "구매완료": 94, "구매액": 4628815, "구매유저(App)": 80, "구매유저(Web)": 8},
    {"캠페인": "bizboard-retarget", "광고그룹": "ct_pgacutterbuck", "주차": "W1", "Impressions": 319636, "Clicks": 4933, "Cost (Channel)": 1353617, "회원가입": 1, "구매완료": 72, "구매액": 2741360, "구매유저(App)": 52, "구매유저(Web)": 18},
    {"캠페인": "bizboard-retarget", "광고그룹": "ct_pgacutterbuck", "주차": "W2", "Impressions": 355720, "Clicks": 6037, "Cost (Channel)": 1793895, "회원가입": 0, "구매완료": 98, "구매액": 3997591, "구매유저(App)": 66, "구매유저(Web)": 26},
    {"캠페인": "bizboard-ua", "광고그룹": "ct_athleredition", "주차": "W1", "Impressions": 181301, "Clicks": 1324, "Cost (Channel)": 325565, "회원가입": 15, "구매완료": 1, "구매액": 15900, "구매유저(App)": 1, "구매유저(Web)": 0},
    {"캠페인": "bizboard-ua", "광고그룹": "ct_athleredition", "주차": "W2", "Impressions": 272877, "Clicks": 1432, "Cost (Channel)": 218085, "회원가입": 12, "구매완료": 2, "구매액": 272300, "구매유저(App)": 1, "구매유저(Web)": 1},
    {"캠페인": "bizboard-ua", "광고그룹": "lecaf_selection", "주차": "W1", "Impressions": 716573, "Clicks": 4038, "Cost (Channel)": 938386, "회원가입": 180, "구매완료": 93, "구매액": 3275250, "구매유저(App)": 18, "구매유저(Web)": 74},
    {"캠페인": "bizboard-ua", "광고그룹": "lecaf_selection", "주차": "W2", "Impressions": 2471478, "Clicks": 9851, "Cost (Channel)": 2151001, "회원가입": 393, "구매완료": 202, "구매액": 6404168, "구매유저(App)": 41, "구매유저(Web)": 157},
    {"캠페인": "bizboard-ua", "광고그룹": "ct_cpcompany", "주차": "W1", "Impressions": 192746, "Clicks": 2065, "Cost (Channel)": 412901, "회원가입": 20, "구매완료": 8, "구매액": 821782, "구매유저(App)": 5, "구매유저(Web)": 2},
    {"캠페인": "bizboard-ua", "광고그룹": "ct_cpcompany", "주차": "W2", "Impressions": 50512, "Clicks": 560, "Cost (Channel)": 132344, "회원가입": 4, "구매완료": 1, "구매액": 54767, "구매유저(App)": 1, "구매유저(Web)": 0},
    {"캠페인": "bizboard-ua", "광고그룹": "ct_highbrand", "주차": "W1", "Impressions": 222125, "Clicks": 1511, "Cost (Channel)": 285843, "회원가입": 12, "구매완료": 2, "구매액": 35275, "구매유저(App)": 2, "구매유저(Web)": 0},
    {"캠페인": "bizboard-ua", "광고그룹": "ct_highbrand", "주차": "W2", "Impressions": 26425, "Clicks": 217, "Cost (Channel)": 83434, "회원가입": 1, "구매완료": 1, "구매액": 69780, "구매유저(App)": 1, "구매유저(Web)": 0},
    {"캠페인": "bizboard-ua", "광고그룹": "ct_stoneisland", "주차": "W1", "Impressions": 305900, "Clicks": 2962, "Cost (Channel)": 431526, "회원가입": 24, "구매완료": 3, "구매액": 766474, "구매유저(App)": 3, "구매유저(Web)": 0},
    {"캠페인": "bizboard-ua", "광고그룹": "ct_stoneisland", "주차": "W2", "Impressions": 71577, "Clicks": 593, "Cost (Channel)": 134311, "회원가입": 4, "구매완료": 0, "구매액": 0, "구매유저(App)": 0, "구매유저(Web)": 0},
    {"캠페인": "display-retarget", "광고그룹": "ct_runningshoes", "주차": "W1", "Impressions": 169524, "Clicks": 6533, "Cost (Channel)": 1712334, "회원가입": 2, "구매완료": 90, "구매액": 4227172, "구매유저(App)": 61, "구매유저(Web)": 24},
    {"캠페인": "display-retarget", "광고그룹": "ct_runningshoes", "주차": "W2", "Impressions": 115797, "Clicks": 3559, "Cost (Channel)": 1057788, "회원가입": 3, "구매완료": 67, "구매액": 3455343, "구매유저(App)": 50, "구매유저(Web)": 13},
    {"캠페인": "display-retarget", "광고그룹": "4890522-product", "주차": "W1", "Impressions": 285680, "Clicks": 2459, "Cost (Channel)": 953219, "회원가입": 2, "구매완료": 55, "구매액": 2456874, "구매유저(App)": 35, "구매유저(Web)": 18},
    {"캠페인": "display-retarget", "광고그룹": "4890522-product", "주차": "W2", "Impressions": 75100, "Clicks": 496, "Cost (Channel)": 212396, "회원가입": 0, "구매완료": 13, "구매액": 484634, "구매유저(App)": 11, "구매유저(Web)": 2},
    {"캠페인": "display-retarget", "광고그룹": "ct_now", "주차": "W1", "Impressions": 251281, "Clicks": 2114, "Cost (Channel)": 610189, "회원가입": 0, "구매완료": 40, "구매액": 1516358, "구매유저(App)": 24, "구매유저(Web)": 12},
    {"캠페인": "display-retarget", "광고그룹": "ct_now", "주차": "W2", "Impressions": 218541, "Clicks": 1684, "Cost (Channel)": 608697, "회원가입": 0, "구매완료": 29, "구매액": 1185793, "구매유저(App)": 26, "구매유저(Web)": 2},
    {"캠페인": "display-retarget", "광고그룹": "br_cpcompany", "주차": "W1", "Impressions": 159986, "Clicks": 2316, "Cost (Channel)": 1139594, "회원가입": 0, "구매완료": 38, "구매액": 2716378, "구매유저(App)": 30, "구매유저(Web)": 3},
    {"캠페인": "display-retarget", "광고그룹": "br_cpcompany", "주차": "W2", "Impressions": 131296, "Clicks": 917, "Cost (Channel)": 625725, "회원가입": 0, "구매완료": 7, "구매액": 677759, "구매유저(App)": 7, "구매유저(Web)": 0},
    {"캠페인": "display-retarget", "광고그룹": "br_stoneisland", "주차": "W1", "Impressions": 245976, "Clicks": 4456, "Cost (Channel)": 2364170, "회원가입": 0, "구매완료": 62, "구매액": 6526156, "구매유저(App)": 56, "구매유저(Web)": 2},
    {"캠페인": "display-retarget", "광고그룹": "br_stoneisland", "주차": "W2", "Impressions": 62160, "Clicks": 716, "Cost (Channel)": 466685, "회원가입": 0, "구매완료": 9, "구매액": 470100, "구매유저(App)": 7, "구매유저(Web)": 0},
    {"캠페인": "display-retarget", "광고그룹": "ct_highbrand", "주차": "W1", "Impressions": 75408, "Clicks": 680, "Cost (Channel)": 462030, "회원가입": 0, "구매완료": 8, "구매액": 255535, "구매유저(App)": 8, "구매유저(Web)": 0},
    {"캠페인": "display-retarget", "광고그룹": "ct_highbrand", "주차": "W2", "Impressions": 1246, "Clicks": 16, "Cost (Channel)": 14334, "회원가입": 0, "구매완료": 0, "구매액": 0, "구매유저(App)": 0, "구매유저(Web)": 0},
    {"캠페인": "display-retarget", "광고그룹": "ct_athleredition", "주차": "W1", "Impressions": 111918, "Clicks": 1236, "Cost (Channel)": 1008937, "회원가입": 0, "구매완료": 21, "구매액": 5510815, "구매유저(App)": 18, "구매유저(Web)": 0},
    {"캠페인": "display-retarget", "광고그룹": "ct_athleredition", "주차": "W2", "Impressions": 10907, "Clicks": 66, "Cost (Channel)": 76121, "회원가입": 0, "구매완료": 1, "구매액": 84900, "구매유저(App)": 1, "구매유저(Web)": 0},
    {"캠페인": "display-retarget", "광고그룹": "ct_pgacutterbuck", "주차": "W1", "Impressions": 194717, "Clicks": 7178, "Cost (Channel)": 2194326, "회원가입": 1, "구매완료": 191, "구매액": 7703582, "구매유저(App)": 132, "구매유저(Web)": 50},
    {"캠페인": "display-retarget", "광고그룹": "ct_pgacutterbuck", "주차": "W2", "Impressions": 235390, "Clicks": 7798, "Cost (Channel)": 2273175, "회원가입": 0, "구매완료": 121, "구매액": 5723224, "구매유저(App)": 82, "구매유저(Web)": 31},
]

adf = pd.DataFrame(ADGROUP_RAW)
adf.rename(columns={"Cost (Channel)": "비용"}, inplace=True)
adf["구매유저 합계"] = adf["구매유저(App)"] + adf["구매유저(Web)"]
adf.loc[adf["주차"] == "W2", "비용"] = (adf.loc[adf["주차"] == "W2", "비용"] * W2_RATIO).round(0).astype(int)

adf["CTR"] = adf.apply(lambda r: r["Clicks"] / r["Impressions"] * 100 if r["Impressions"] > 0 else 0, axis=1)
adf["CPC"] = adf.apply(lambda r: r["비용"] / r["Clicks"] if r["Clicks"] > 0 else 0, axis=1)
adf["구매 CVR"] = adf.apply(lambda r: r["구매완료"] / r["Clicks"] * 100 if r["Clicks"] > 0 else 0, axis=1)
adf["구매 CPA"] = adf.apply(lambda r: r["비용"] / r["구매완료"] if r["구매완료"] > 0 else 0, axis=1)
adf["ROAS"] = adf.apply(lambda r: r["구매액"] / r["비용"] * ROAS_FACTOR * 100 if r["비용"] > 0 else 0, axis=1)
adf["ARPPU"] = adf.apply(lambda r: r["구매액"] / r["구매유저 합계"] if r["구매유저 합계"] > 0 else 0, axis=1)

# ──────────────────────────────────────────────
# 차트 헬퍼
# ──────────────────────────────────────────────
DARK_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#e0e0e0",
    title_font_color="#ffffff",
    legend_font_color="#e0e0e0",
    xaxis=dict(gridcolor="#2d2f36", zerolinecolor="#2d2f36"),
    yaxis=dict(gridcolor="#2d2f36", zerolinecolor="#2d2f36"),
)

def fig_html(fig, height=400):
    all_y = [v for t in fig.data for v in (t.y if hasattr(t, "y") and t.y is not None else []) if isinstance(v, (int, float))]
    fig.update_layout(margin=MARGIN, height=height, **DARK_LAYOUT)
    if all_y:
        fig.update_yaxes(range=[0, max(all_y) * 1.2])
    return fig.to_html(full_html=False, include_plotlyjs=False)

def fig_html_h(fig, height=400):
    """가로 막대용"""
    all_x = [v for t in fig.data for v in (t.x if hasattr(t, "x") and t.x is not None else []) if isinstance(v, (int, float))]
    fig.update_layout(height=height, **DARK_LAYOUT)
    if all_x:
        fig.update_xaxes(range=[0, max(all_x) * 1.25])
    return fig.to_html(full_html=False, include_plotlyjs=False)

def pct_change(v1, v2):
    if v1 == 0: return "N/A"
    return f"{(v2-v1)/v1*100:+.1f}%"

# ──────────────────────────────────────────────
# KPI
# ──────────────────────────────────────────────
w1 = df[(df["캠페인"] == "kakao 합계") & (df["주차"] == "W1")].iloc[0]
w2 = df[(df["캠페인"] == "kakao 합계") & (df["주차"] == "W2")].iloc[0]

kpis = [
    ("비용", f"{w2['비용']:,.0f}원", pct_change(w1['비용'], w2['비용']), True),
    ("구매완료", f"{w2['구매완료']:,.0f}건", pct_change(w1['구매완료'], w2['구매완료']), False),
    ("구매액", f"{w2['구매액']:,.0f}원", pct_change(w1['구매액'], w2['구매액']), False),
    ("ROAS", f"{w2['ROAS']:.2f}%", pct_change(w1['ROAS'], w2['ROAS']), False),
    ("구매 CPA", f"{w2['구매 CPA']:,.0f}원", pct_change(w1['구매 CPA'], w2['구매 CPA']), True),
    ("ARPPU", f"{w2['ARPPU']:,.0f}원", pct_change(w1['ARPPU'], w2['ARPPU']), False),
]

kpi_html = ""
for label, value, delta, inverse in kpis:
    if delta == "N/A":
        color = "#6b7280"
    elif inverse:
        color = "#22c55e" if delta.startswith("-") else "#ef4444"
    else:
        color = "#22c55e" if delta.startswith("+") else "#ef4444"
    kpi_html += f'<div class="kpi"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><div class="kpi-delta" style="color:{color}">{delta}</div></div>'

# ──────────────────────────────────────────────
# 탭1: 유입
# ──────────────────────────────────────────────
fig = go.Figure()
for c in CAMPAIGNS:
    d = df[df["캠페인"] == c]
    fig.add_trace(go.Bar(name=c, x=d["주차"], y=d["CTR"], marker_color=COLORS[c], text=[f"{v:.2f}%" for v in d["CTR"]], textposition="outside"))
fig.update_layout(title="CTR (클릭률)", yaxis_title="%", barmode="group")
ch_ctr = fig_html(fig)

fig = go.Figure()
for c in CAMPAIGNS:
    d = df[df["캠페인"] == c]
    fig.add_trace(go.Bar(name=c, x=d["주차"], y=d["CPC"], marker_color=COLORS[c], text=[f"{v:,.0f}원" for v in d["CPC"]], textposition="outside"))
fig.update_layout(title="CPC (클릭당 비용)", yaxis_title="원", barmode="group")
ch_cpc = fig_html(fig)

fig = go.Figure()
for c in CAMPAIGNS:
    d = df[df["캠페인"] == c]
    fig.add_trace(go.Bar(name=c, x=d["주차"], y=d["Impressions"], marker_color=COLORS[c], text=[f"{v/1e6:.1f}M" for v in d["Impressions"]], textposition="outside"))
fig.update_layout(title="Impressions (노출수)", yaxis_title="회", barmode="group")
ch_imp = fig_html(fig)

fig = go.Figure()
for c in CAMPAIGNS:
    d = df[df["캠페인"] == c]
    fig.add_trace(go.Bar(name=c, x=d["주차"], y=d["Clicks"], marker_color=COLORS[c], text=[f"{v:,.0f}" for v in d["Clicks"]], textposition="outside"))
fig.update_layout(title="Clicks (클릭수)", yaxis_title="회", barmode="group")
ch_clk = fig_html(fig)

# ──────────────────────────────────────────────
# 탭2: 가입 (ua만)
# ──────────────────────────────────────────────
ua_join = df[df["캠페인"] == "bizboard-ua"]
fig = go.Figure()
fig.add_trace(go.Bar(x=ua_join["주차"], y=ua_join["가입 CVR"], marker_color=["#5B8FF9","#FF6B6B"],
                     text=[f"{v:.2f}%" for v in ua_join["가입 CVR"]], textposition="outside", width=0.4))
fig.update_layout(title="가입 CVR (회원가입 / Clicks)", yaxis_title="%")
ch_join_cvr = fig_html(fig)

fig = go.Figure()
fig.add_trace(go.Bar(x=ua_join["주차"], y=ua_join["가입 CPA"], marker_color=["#5B8FF9","#FF6B6B"],
                     text=[f"{v:,.0f}원" for v in ua_join["가입 CPA"]], textposition="outside", width=0.4))
fig.update_layout(title="가입 CPA (비용 / 회원가입)", yaxis_title="원")
ch_join_cpa = fig_html(fig)

# ──────────────────────────────────────────────
# 탭3: 가입→구매 (ua만)
# ──────────────────────────────────────────────
ua = df[df["캠페인"] == "bizboard-ua"]
fig = go.Figure()
fig.add_trace(go.Bar(x=ua["주차"], y=ua["가입→구매 CVR"], marker_color=["#5B8FF9","#FF6B6B"],
                     text=[f"{v:.1f}%" for v in ua["가입→구매 CVR"]], textposition="outside", width=0.4))
fig.update_layout(title="가입→구매 CVR 추이 (ua)", yaxis_title="%")
ch_j2p_cvr = fig_html(fig)

fig = go.Figure()
fig.add_trace(go.Bar(name="회원가입", x=ua["주차"], y=ua["회원가입"], marker_color="#5B8FF9",
                     text=[f"{int(v):,}명" for v in ua["회원가입"]], textposition="outside"))
fig.add_trace(go.Bar(name="구매완료", x=ua["주차"], y=ua["구매완료"], marker_color="#FF6B6B",
                     text=[f"{int(v):,}건" for v in ua["구매완료"]], textposition="outside"))
fig.update_layout(title="회원가입 vs 구매완료 (ua)", yaxis_title="건", barmode="group")
ch_j2p_bar = fig_html(fig)

# ──────────────────────────────────────────────
# 탭4: 구매
# ──────────────────────────────────────────────
fig = go.Figure()
for c in CAMPAIGNS:
    d = df[df["캠페인"] == c]
    fig.add_trace(go.Bar(name=c, x=d["주차"], y=d["구매 CVR"], marker_color=COLORS[c], text=[f"{v:.2f}%" for v in d["구매 CVR"]], textposition="outside"))
fig.update_layout(title="구매 CVR (구매완료 / Clicks)", yaxis_title="%", barmode="group")
ch_buy_cvr = fig_html(fig)

fig = go.Figure()
for c in CAMPAIGNS:
    d = df[df["캠페인"] == c]
    fig.add_trace(go.Bar(name=c, x=d["주차"], y=d["구매 CPA"], marker_color=COLORS[c], text=[f"{v:,.0f}원" for v in d["구매 CPA"]], textposition="outside"))
fig.update_layout(title="구매 CPA (비용 / 구매완료)", yaxis_title="원", barmode="group")
ch_buy_cpa = fig_html(fig)

fig = go.Figure()
for c in CAMPAIGNS:
    d = df[df["캠페인"] == c]
    fig.add_trace(go.Bar(name=c, x=d["주차"], y=d["ROAS"], marker_color=COLORS[c], text=[f"{v:.0f}%" for v in d["ROAS"]], textposition="outside"))
fig.add_hline(y=500, line_dash="dash", line_color="red", annotation_text="OKR 500%")
fig.update_layout(title="ROAS (에어브릿지 ROAS × 1.763)", yaxis_title="%", barmode="group")
ch_roas = fig_html(fig)

fig = go.Figure()
for c in CAMPAIGNS:
    d = df[df["캠페인"] == c]
    fig.add_trace(go.Bar(name=c, x=d["주차"], y=d["ARPPU"], marker_color=COLORS[c], text=[f"{v:,.0f}원" for v in d["ARPPU"]], textposition="outside"))
fig.update_layout(title="ARPPU (구매액 / 구매유저수)", yaxis_title="원", barmode="group")
ch_arppu = fig_html(fig)

fig = make_subplots(specs=[[{"secondary_y": True}]])
for c in CAMPAIGNS:
    d = df[df["캠페인"] == c]
    fig.add_trace(go.Bar(name=f"{c} 구매액", x=[f"{c}<br>{w}" for w in d["주차"]], y=d["구매액"].values, marker_color=COLORS[c], opacity=0.8), secondary_y=False)
    fig.add_trace(go.Scatter(name=f"{c} 비용", x=[f"{c}<br>{w}" for w in d["주차"]], y=d["비용"].values, mode="markers+lines", marker=dict(size=10, color=COLORS[c]), line=dict(dash="dot")), secondary_y=True)
fig.update_layout(title="캠페인별 구매액(막대) vs 비용(점선)", barmode="group", margin=MARGIN, height=450, **DARK_LAYOUT)
fig.update_yaxes(title_text="구매액 (원)", secondary_y=False)
fig.update_yaxes(title_text="비용 (원)", secondary_y=True)
ch_rev_cost = fig.to_html(full_html=False, include_plotlyjs=False)

# ──────────────────────────────────────────────
# 탭5: 광고그룹별 (캠페인별 ROAS 가로 막대)
# ──────────────────────────────────────────────
adgroup_sections = ""
for camp in CAMPAIGNS:
    camp_data = adf[adf["캠페인"] == camp]
    adgroups = sorted(camp_data["광고그룹"].unique())
    h = max(400, len(adgroups) * 45)

    # ROAS
    fig = go.Figure()
    for wk, color in WEEK_COLORS.items():
        wd = camp_data[camp_data["주차"] == wk].sort_values("ROAS", ascending=True)
        fig.add_trace(go.Bar(name=wk, y=wd["광고그룹"], x=wd["ROAS"], orientation="h", marker_color=color,
                             text=[f"{v:.0f}%" for v in wd["ROAS"]], textposition="outside"))
    fig.add_vline(x=500, line_dash="dash", line_color="red", annotation_text="OKR 500%")
    fig.update_layout(barmode="group", height=h, xaxis_title="ROAS %", margin=dict(t=50,b=40,l=200,r=60), title=f"{camp} — ROAS")
    roas_ch = fig_html_h(fig, h)

    # CPA
    fig = go.Figure()
    for wk, color in WEEK_COLORS.items():
        wd = camp_data[(camp_data["주차"] == wk) & (camp_data["구매 CPA"] > 0)].sort_values("구매 CPA", ascending=True)
        fig.add_trace(go.Bar(name=wk, y=wd["광고그룹"], x=wd["구매 CPA"], orientation="h", marker_color=color,
                             text=[f"{v:,.0f}원" for v in wd["구매 CPA"]], textposition="outside"))
    fig.update_layout(barmode="group", height=h, xaxis_title="원", margin=dict(t=50,b=40,l=200,r=60), title=f"{camp} — 구매 CPA")
    cpa_ch = fig_html_h(fig, h)

    # 테이블
    show = camp_data[["광고그룹","주차","Impressions","Clicks","비용","구매완료","구매액","CTR","CPC","구매 CVR","구매 CPA","ROAS","ARPPU"]].copy()
    for col, fmt in [("Impressions","{:,.0f}"),("Clicks","{:,.0f}"),("비용","{:,.0f}원"),("구매완료","{:,.0f}"),("구매액","{:,.0f}원"),
                     ("CTR","{:.2f}%"),("CPC","{:,.0f}원"),("구매 CVR","{:.2f}%"),("구매 CPA","{:,.0f}원"),("ROAS","{:.0f}%"),("ARPPU","{:,.0f}원")]:
        show[col] = show[col].apply(lambda x: fmt.format(x) if x > 0 else "-")
    tbl = show.sort_values(["광고그룹","주차"]).to_html(index=False, border=0)

    adgroup_sections += f"""
    <div class="camp-section">
        <h3>{camp}</h3>
        <div class="chart-grid"><div class="chart-box">{roas_ch}</div><div class="chart-box">{cpa_ch}</div></div>
        <div class="chart-full" style="overflow-x:auto">{tbl}</div>
    </div>"""

# ──────────────────────────────────────────────
# 탭6: 원본 데이터
# ──────────────────────────────────────────────
tbl_main = df[["캠페인","주차","Impressions","Clicks","비용","회원가입","구매완료","구매액","CTR","CPC","구매 CVR","구매 CPA","ROAS","ARPPU"]].copy()
for col, fmt in [("Impressions","{:,.0f}"),("Clicks","{:,.0f}"),("비용","{:,.0f}원"),("회원가입","{:,.0f}"),("구매완료","{:,.0f}"),("구매액","{:,.0f}원"),
                 ("CTR","{:.2f}%"),("CPC","{:,.0f}원"),("구매 CVR","{:.2f}%"),("구매 CPA","{:,.0f}원"),("ROAS","{:.2f}%"),("ARPPU","{:,.0f}원")]:
    tbl_main[col] = tbl_main[col].apply(lambda x: fmt.format(x))
tbl_main_html = tbl_main.to_html(index=False, border=0).replace("kakao 합계", "<strong>kakao 합계</strong>")

change_rows = []
for camp in CAMPAIGNS + ["kakao 합계"]:
    row = {"캠페인": camp}
    cd = df[df["캠페인"] == camp]
    r1, r2 = cd[cd["주차"]=="W1"].iloc[0], cd[cd["주차"]=="W2"].iloc[0]
    for m in ["Impressions","Clicks","비용","구매완료","구매액","구매 CVR","구매 CPA","ROAS","ARPPU"]:
        row[m] = pct_change(r1[m], r2[m])
    change_rows.append(row)
tbl_change_html = pd.DataFrame(change_rows).to_html(index=False, border=0).replace("kakao 합계", "<strong>kakao 합계</strong>")

# ──────────────────────────────────────────────
# HTML 조합
# ──────────────────────────────────────────────
html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PBTD 카카오모먼트 주간 분석</title>
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:-apple-system,'Pretendard','Noto Sans KR',sans-serif; background:#0f1117; color:#e0e0e0; padding:24px; max-width:1400px; margin:0 auto; }}
h1 {{ font-size:28px; margin-bottom:4px; color:#ffffff; }}
h2 {{ color:#e0e0e0; }}
.subtitle {{ color:#9ca3af; font-size:14px; margin-bottom:24px; }}
.kpi-row {{ display:grid; grid-template-columns:repeat(6,1fr); gap:12px; margin-bottom:28px; }}
.kpi {{ background:#1a1c23; border-radius:12px; padding:16px; border:1px solid #2d2f36; }}
.kpi-label {{ font-size:12px; color:#9ca3af; }}
.kpi-value {{ font-size:20px; font-weight:700; margin:4px 0; color:#ffffff; }}
.kpi-delta {{ font-size:13px; font-weight:600; }}
/* 탭 */
.tabs {{ display:flex; gap:0; border-bottom:2px solid #2d2f36; margin-bottom:24px; }}
.tab {{ padding:10px 20px; cursor:pointer; font-size:14px; font-weight:600; color:#6b7280; border-bottom:3px solid transparent; margin-bottom:-2px; transition:all .2s; }}
.tab:hover {{ color:#e0e0e0; }}
.tab.active {{ color:#ffffff; border-bottom-color:#FAE100; }}
.tab-content {{ display:none; }}
.tab-content.active {{ display:block; }}
.section {{ margin-bottom:32px; }}
.section h2 {{ font-size:18px; margin-bottom:16px; }}
.chart-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-bottom:20px; }}
.chart-box {{ background:#1a1c23; border-radius:12px; padding:14px; border:1px solid #2d2f36; }}
.chart-full {{ background:#1a1c23; border-radius:12px; padding:14px; border:1px solid #2d2f36; margin-bottom:20px; }}
.camp-section {{ margin-bottom:32px; }}
.camp-section h3 {{ font-size:16px; margin-bottom:12px; padding:8px 12px; background:#FAE100; color:#0f1117; border-radius:8px; }}
table {{ width:100%; border-collapse:collapse; font-size:12px; color:#e0e0e0; }}
th {{ background:#2d2f36; color:#ffffff; padding:8px 6px; text-align:right; white-space:nowrap; }}
th:first-child,th:nth-child(2) {{ text-align:left; }}
td {{ padding:6px; border-bottom:1px solid #2d2f36; text-align:right; white-space:nowrap; }}
td:first-child,td:nth-child(2) {{ text-align:left; font-weight:600; }}
tr:hover {{ background:#262830; }}
.note {{ background:#1e293b; border:1px solid #334155; border-radius:8px; padding:12px; font-size:13px; color:#93c5fd; margin:12px 0; }}
.insight-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-bottom:20px; }}
.insight-box {{ background:#1a1c23; border-radius:12px; padding:16px; border:1px solid #2d2f36; }}
.insight-box h3 {{ font-size:15px; margin-bottom:10px; color:#ffffff; }}
.insight-box ul {{ padding-left:18px; line-height:1.8; font-size:13px; }}
.action-box {{ background:#1c1a0e; border:1px solid #854d0e; border-radius:12px; padding:16px; }}
.action-box h3 {{ font-size:15px; margin-bottom:10px; color:#fbbf24; }}
.action-box ol {{ padding-left:18px; line-height:2; font-size:13px; }}
.footer {{ text-align:center; color:#6b7280; font-size:11px; margin-top:40px; padding-top:16px; border-top:1px solid #2d2f36; }}
@media(max-width:768px){{ .kpi-row{{grid-template-columns:repeat(3,1fr);}} .chart-grid,.insight-grid{{grid-template-columns:1fr;}} }}
</style>
</head>
<body>

<h1>📊 PBTD 카카오모먼트 주간 분석</h1>
<p class="subtitle">W1 (3/23~3/29) vs W2 (3/30~4/5) | ROAS = 에어브릿지 ROAS × 1.763 (보정계수)</p>
<div class="kpi-row">{kpi_html}</div>

<!-- 탭 -->
<div class="tabs">
    <div class="tab active" onclick="switchTab('tab1',this)">📈 유입</div>
    <div class="tab" onclick="switchTab('tab2',this)">👤 가입</div>
    <div class="tab" onclick="switchTab('tab3',this)">🔄 가입→구매</div>
    <div class="tab" onclick="switchTab('tab4',this)">💰 구매</div>
    <div class="tab" onclick="switchTab('tab5',this)">🔍 광고그룹별</div>
    <div class="tab" onclick="switchTab('tab6',this)">📋 원본 데이터</div>
</div>

<div id="tab1" class="tab-content active">
    <h2>유입 지표 — CTR, CPC</h2>
    <div class="chart-grid"><div class="chart-box">{ch_ctr}</div><div class="chart-box">{ch_cpc}</div></div>
    <h2>노출 & 클릭 추이</h2>
    <div class="chart-grid"><div class="chart-box">{ch_imp}</div><div class="chart-box">{ch_clk}</div></div>
</div>

<div id="tab2" class="tab-content">
    <h2>가입 지표 — CVR, CPA (ua 캠페인)</h2>
    <p style="color:#9ca3af;font-size:13px;margin-bottom:16px">리타겟팅 캠페인은 기존 유저 대상이라 가입이 극소수 → ua만 표시합니다.</p>
    <div class="chart-grid"><div class="chart-box">{ch_join_cvr}</div><div class="chart-box">{ch_join_cpa}</div></div>
</div>

<div id="tab3" class="tab-content">
    <h2>가입→구매 전환율 (ua 캠페인)</h2>
    <p style="color:#6b7280;font-size:13px;margin-bottom:16px">리타겟팅 캠페인은 기존 유저 대상이라 가입이 극소수 → CVR이 비정상적으로 높아 ua만 표시합니다.</p>
    <div class="chart-grid"><div class="chart-box">{ch_j2p_cvr}</div><div class="chart-box">{ch_j2p_bar}</div></div>
</div>

<div id="tab4" class="tab-content">
    <h2>구매 지표 — CVR, CPA, ROAS, ARPPU</h2>
    <div class="chart-grid"><div class="chart-box">{ch_buy_cvr}</div><div class="chart-box">{ch_buy_cpa}</div></div>
    <div class="chart-grid"><div class="chart-box">{ch_roas}</div><div class="chart-box">{ch_arppu}</div></div>
    <h2>구매액 vs 비용</h2>
    <div class="chart-full">{ch_rev_cost}</div>
</div>

<div id="tab5" class="tab-content">
    <h2>🔍 광고그룹별 성과 분석</h2>
    {adgroup_sections}
</div>

<div id="tab6" class="tab-content">
    <h2>캠페인 요약 데이터</h2>
    <div class="chart-full" style="overflow-x:auto">{tbl_main_html}</div>
    <h2>W1 → W2 증감률</h2>
    <div class="chart-full" style="overflow-x:auto">{tbl_change_html}</div>
</div>

<!-- 인사이트 (항상 표시) -->
<hr style="border:none;border-top:1px solid #e5e7eb;margin:32px 0">
<h2>💡 핵심 인사이트</h2>
<div class="insight-grid">
    <div class="insight-box">
        <h3>✅ 긍정적 변화</h3>
        <ul>
            <li><strong>구매 CVR</strong> 1.74% → 2.10% (+20.7%) 전환 효율 개선</li>
            <li><strong>구매 CPA</strong> 비용 기준 하락, 효율 개선</li>
            <li><strong>bizboard-ua</strong> 구매 +100%, ROAS 성장세</li>
            <li><strong>lecaf_selection</strong> (ua) 가입 393건, 가장 효율적</li>
            <li><strong>ct_runningshoes</strong> (display) ROAS 개선</li>
        </ul>
    </div>
    <div class="insight-box">
        <h3>⚠️ 주의 필요</h3>
        <ul>
            <li><strong>display-retarget 전반 급감</strong>: 노출 -43%, 구매액 -54%</li>
            <li><strong>ROAS 하락</strong>: 522.59% → 462.78%</li>
            <li><strong>ARPPU 전반 하락</strong>: 객단가 감소 추세</li>
            <li><strong>br_stoneisland</strong> (display) 비용 -80%, 구매 -85%</li>
            <li><strong>4890562-product</strong> 구매 24건→1건 급감</li>
        </ul>
    </div>
</div>
<div class="action-box">
    <h3>📌 다음 액션 제안</h3>
    <ol>
        <li><strong>display-retarget</strong> 예산/소재 변경 이력 확인 → 급감 원인 파악</li>
        <li><strong>bizboard-ua lecaf_selection</strong> 예산 증액 검토 → 가입 효율 우수</li>
        <li><strong>ct_pgacutterbuck</strong> (display) 안정적 ROAS → 예산 유지/증액 검토</li>
        <li><strong>ARPPU 하락 원인</strong> → 구매 상품 카테고리/할인율 변화 추가 분석</li>
        <li>W2 신규 광고그룹 (ct_hiking, ct_shortsleeve, ct_warehouserelease) 초기 성과 모니터링</li>
    </ol>
</div>

<div class="footer">PBTD 카카오모먼트 주간 분석 | 데이터 기준: 에어브릿지 | 생성일: 2026-04-07</div>

<script>
function switchTab(id, el) {{
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.getElementById(id).classList.add('active');
    el.classList.add('active');
    // plotly 차트 리사이즈
    setTimeout(() => window.dispatchEvent(new Event('resize')), 50);
}}
</script>
</body>
</html>"""

output_path = "/Users/jeon/workspace/projects/카카오-주간분석/2026-04-07_PBTD_카카오모먼트_주간분석.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)
print(f"생성 완료: {output_path}")
