import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ──────────────────────────────────────────────
# 페이지 설정
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="PBTD 카카오모먼트 주간 분석",
    page_icon="📊",
    layout="wide",
)

st.title("📊 PBTD 카카오모먼트 주간 분석")
st.caption("W1 (3/23~3/29) vs W2 (3/30~4/5) | ROAS = 에어브릿지 ROAS × 1.763 (보정계수)")

# ──────────────────────────────────────────────
# 캠페인 요약 데이터
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

# W2 비용 보정 (에어브릿지 실제 비용 기준)
# W1: 34,529,439원 (DB 일치), W2: 32,374,233원 (DB 31,697,407 → 에어브릿지 32,374,233)
W2_DB_COST = 31_697_407
W2_AIRBRIDGE_COST = 32_374_233
W2_RATIO = W2_AIRBRIDGE_COST / W2_DB_COST

df.loc[df["주차"] == "W2", "비용"] = (df.loc[df["주차"] == "W2", "비용"] * W2_RATIO).round(0).astype(int)
# kakao 합계 W2는 정확히 에어브릿지 값으로 설정
df.loc[(df["주차"] == "W2") & (df["캠페인"] == "kakao 합계"), "비용"] = W2_AIRBRIDGE_COST

# ──────────────────────────────────────────────
# 광고그룹별 데이터
# ──────────────────────────────────────────────
ADGROUP_RAW = [
    # bizboard_da_pr_pbtd-retarget-purchase
    {"캠페인": "bizboard-retarget", "광고그룹": "lecaf_selection", "주차": "W1", "Impressions": 1360280, "Clicks": 8544, "Cost (Channel)": 2207395, "회원가입": 2, "구매완료": 228, "구매액": 7557532, "구매유저(App)": 124, "구매유저(Web)": 97},
    {"캠페인": "bizboard-retarget", "광고그룹": "lecaf_selection", "주차": "W2", "Impressions": 4470125, "Clicks": 17995, "Cost (Channel)": 4570768, "회원가입": 14, "구매완료": 532, "구매액": 18043420, "구매유저(App)": 271, "구매유저(Web)": 242},
    {"캠페인": "bizboard-retarget", "광고그룹": "br_sub_rowen", "주차": "W1", "Impressions": 78671, "Clicks": 1390, "Cost (Channel)": 510852, "회원가입": 0, "구매완료": 33, "구매액": 1462631, "구매유저(App)": 28, "구매유저(Web)": 0},
    {"캠페인": "bizboard-retarget", "광고그룹": "br_sub_rowen", "주차": "W2", "Impressions": 22608, "Clicks": 509, "Cost (Channel)": 167591, "회원가입": 0, "구매완료": 3, "구매액": 138913, "구매유저(App)": 2, "구매유저(Web)": 1},
    {"캠페인": "bizboard-retarget", "광고그룹": "ct_runningshoes", "주차": "W1", "Impressions": 217740, "Clicks": 2093, "Cost (Channel)": 758905, "회원가입": 0, "구매완료": 57, "구매액": 2047838, "구매유저(App)": 49, "구매유저(Web)": 8},
    {"캠페인": "bizboard-retarget", "광고그룹": "ct_runningshoes", "주차": "W2", "Impressions": 882368, "Clicks": 3319, "Cost (Channel)": 1538139, "회원가입": 1, "구매완료": 97, "구매액": 3465146, "구매유저(App)": 79, "구매유저(Web)": 13},
    {"캠페인": "bizboard-retarget", "광고그룹": "4890509-product", "주차": "W1", "Impressions": 124180, "Clicks": 763, "Cost (Channel)": 539287, "회원가입": 0, "구매완료": 35, "구매액": 1215375, "구매유저(App)": 23, "구매유저(Web)": 9},
    {"캠페인": "bizboard-retarget", "광고그룹": "4890509-product", "주차": "W2", "Impressions": 72150, "Clicks": 495, "Cost (Channel)": 319586, "회원가입": 0, "구매완료": 13, "구매액": 366764, "구매유저(App)": 8, "구매유저(Web)": 3},
    {"캠페인": "bizboard-retarget", "광고그룹": "4890514-product", "주차": "W1", "Impressions": 1672030, "Clicks": 5515, "Cost (Channel)": 1763519, "회원가입": 2, "구매완료": 164, "구매액": 5032676, "구매유저(App)": 91, "구매유저(Web)": 67},
    {"캠페인": "bizboard-retarget", "광고그룹": "4890514-product", "주차": "W2", "Impressions": 1240019, "Clicks": 2739, "Cost (Channel)": 962289, "회원가입": 0, "구매완료": 57, "구매액": 1753922, "구매유저(App)": 38, "구매유저(Web)": 19},
    {"캠페인": "bizboard-retarget", "광고그룹": "4890554-product", "주차": "W1", "Impressions": 39875, "Clicks": 384, "Cost (Channel)": 260281, "회원가입": 0, "구매완료": 11, "구매액": 337331, "구매유저(App)": 9, "구매유저(Web)": 2},
    {"캠페인": "bizboard-retarget", "광고그룹": "4890554-product", "주차": "W2", "Impressions": 9308, "Clicks": 61, "Cost (Channel)": 38192, "회원가입": 0, "구매완료": 2, "구매액": 54800, "구매유저(App)": 1, "구매유저(Web)": 1},
    {"캠페인": "bizboard-retarget", "광고그룹": "4890556-product", "주차": "W1", "Impressions": 34269, "Clicks": 432, "Cost (Channel)": 271825, "회원가입": 0, "구매완료": 10, "구매액": 326488, "구매유저(App)": 7, "구매유저(Web)": 3},
    {"캠페인": "bizboard-retarget", "광고그룹": "4890556-product", "주차": "W2", "Impressions": 73594, "Clicks": 449, "Cost (Channel)": 330190, "회원가입": 0, "구매완료": 16, "구매액": 668645, "구매유저(App)": 11, "구매유저(Web)": 5},
    {"캠페인": "bizboard-retarget", "광고그룹": "4890562-product", "주차": "W1", "Impressions": 56038, "Clicks": 396, "Cost (Channel)": 400612, "회원가입": 0, "구매완료": 24, "구매액": 754971, "구매유저(App)": 20, "구매유저(Web)": 3},
    {"캠페인": "bizboard-retarget", "광고그룹": "4890562-product", "주차": "W2", "Impressions": 42071, "Clicks": 206, "Cost (Channel)": 179057, "회원가입": 0, "구매완료": 1, "구매액": 67000, "구매유저(App)": 1, "구매유저(Web)": 0},
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
    # bizboard_da_pr_pbtd-ua-purchase
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
    # display_da_pr_pbtd-retarget-purchase
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

# W2 비용 보정 (에어브릿지 기준)
adf.loc[adf["주차"] == "W2", "비용"] = (adf.loc[adf["주차"] == "W2", "비용"] * W2_RATIO).round(0).astype(int)

# 보정계수
ROAS_FACTOR = 1.763

# 광고그룹 성과 지표 (비용 = 실제 집행 비용, ROAS = 에어브릿지 ROAS × 1.763)
adf["CTR"] = adf.apply(lambda r: r["Clicks"] / r["Impressions"] * 100 if r["Impressions"] > 0 else 0, axis=1)
adf["CPC"] = adf.apply(lambda r: r["비용"] / r["Clicks"] if r["Clicks"] > 0 else 0, axis=1)
adf["가입 CVR"] = adf.apply(lambda r: r["회원가입"] / r["Clicks"] * 100 if r["Clicks"] > 0 else 0, axis=1)
adf["가입 CPA"] = adf.apply(lambda r: r["비용"] / r["회원가입"] if r["회원가입"] > 0 else 0, axis=1)
adf["구매 CVR"] = adf.apply(lambda r: r["구매완료"] / r["Clicks"] * 100 if r["Clicks"] > 0 else 0, axis=1)
adf["구매 CPA"] = adf.apply(lambda r: r["비용"] / r["구매완료"] if r["구매완료"] > 0 else 0, axis=1)
adf["ROAS"] = adf.apply(lambda r: r["구매액"] / r["비용"] * ROAS_FACTOR * 100 if r["비용"] > 0 else 0, axis=1)
adf["ARPPU"] = adf.apply(lambda r: r["구매액"] / r["구매유저 합계"] if r["구매유저 합계"] > 0 else 0, axis=1)

# 캠페인 요약 지표 (비용 = 실제 집행 비용, ROAS = 에어브릿지 ROAS × 1.763)
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

# 차트 상단 텍스트 잘림 방지를 위한 기본 레이아웃
CHART_MARGIN = dict(t=50, b=40, l=10, r=10)

# ──────────────────────────────────────────────
# 유틸리티
# ──────────────────────────────────────────────

def fmt_num(v, fmt_type="int"):
    if fmt_type == "int":
        return f"{v:,.0f}"
    if fmt_type == "won":
        return f"{v:,.0f}원"
    if fmt_type == "pct":
        return f"{v:.2f}%"
    return str(v)


def safe_pct_change(v1, v2):
    if v1 == 0:
        return None
    return (v2 - v1) / v1 * 100


def apply_chart_margin(fig, height=400):
    """모든 차트에 상단 여백을 적용하여 텍스트 잘림 방지"""
    fig.update_layout(
        margin=CHART_MARGIN,
        height=height,
    )
    # y축이 있는 세로 막대 차트: 상단 20% 여유
    if fig.data and hasattr(fig.data[0], "orientation") and fig.data[0].orientation == "h":
        fig.update_xaxes(rangemode="tozero", autorange=True)
        fig.update_layout(margin=dict(t=50, b=40, l=200, r=60))
    else:
        fig.update_yaxes(rangemode="tozero")
        # 최대값 기준 상단 여유 확보
        all_y = []
        for trace in fig.data:
            if hasattr(trace, "y") and trace.y is not None:
                all_y.extend([v for v in trace.y if v is not None and isinstance(v, (int, float))])
        if all_y:
            max_y = max(all_y)
            fig.update_yaxes(range=[0, max_y * 1.2])
    return fig


# ──────────────────────────────────────────────
# 핵심 KPI 카드
# ──────────────────────────────────────────────
st.markdown("---")
st.subheader("핵심 KPI (kakao 합계)")

total = df[df["캠페인"] == "kakao 합계"]
w1 = total[total["주차"] == "W1"].iloc[0]
w2 = total[total["주차"] == "W2"].iloc[0]

kpi_cols = st.columns(6)
kpis = [
    ("비용", w1["비용"], w2["비용"], "won"),
    ("구매완료", w1["구매완료"], w2["구매완료"], "int"),
    ("구매액", w1["구매액"], w2["구매액"], "won"),
    ("ROAS", w1["ROAS"], w2["ROAS"], "pct"),
    ("구매 CPA", w1["구매 CPA"], w2["구매 CPA"], "won"),
    ("ARPPU", w1["ARPPU"], w2["ARPPU"], "won"),
]

for col, (label, v1, v2, ft) in zip(kpi_cols, kpis):
    with col:
        st.metric(
            label=label,
            value=fmt_num(v2, ft),
            delta=f"{(v2 - v1) / v1 * 100:+.1f}%" if v1 != 0 else "N/A",
            delta_color="normal" if label not in ("구매 CPA", "비용") else "inverse",
        )

# ──────────────────────────────────────────────
# 탭 구성
# ──────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 유입", "👤 가입", "🔄 가입→구매", "💰 구매", "🔍 광고그룹별 성과", "📋 원본 데이터"
])

# ──────────────── 유입 탭 ────────────────
with tab1:
    st.subheader("유입 지표 — CTR, CPC")

    col1, col2 = st.columns(2)

    with col1:
        fig = go.Figure()
        for camp in CAMPAIGNS:
            camp_df = df[df["캠페인"] == camp]
            fig.add_trace(go.Bar(
                name=camp, x=camp_df["주차"], y=camp_df["CTR"],
                marker_color=COLORS[camp],
                text=[f"{v:.2f}%" for v in camp_df["CTR"]],
                textposition="outside",
            ))
        fig.update_layout(title="CTR (클릭률)", yaxis_title="%", barmode="group", height=400)
        apply_chart_margin(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure()
        for camp in CAMPAIGNS:
            camp_df = df[df["캠페인"] == camp]
            fig.add_trace(go.Bar(
                name=camp, x=camp_df["주차"], y=camp_df["CPC"],
                marker_color=COLORS[camp],
                text=[f"{v:,.0f}원" for v in camp_df["CPC"]],
                textposition="outside",
            ))
        fig.update_layout(title="CPC (클릭당 비용)", yaxis_title="원", barmode="group", height=400)
        apply_chart_margin(fig)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### 노출 & 클릭 추이")
    col3, col4 = st.columns(2)
    with col3:
        fig = go.Figure()
        for camp in CAMPAIGNS:
            camp_df = df[df["캠페인"] == camp]
            fig.add_trace(go.Bar(
                name=camp, x=camp_df["주차"], y=camp_df["Impressions"],
                marker_color=COLORS[camp],
                text=[f"{v/1_000_000:.1f}M" for v in camp_df["Impressions"]],
                textposition="outside",
            ))
        fig.update_layout(title="Impressions (노출수)", yaxis_title="회", barmode="group", height=400)
        apply_chart_margin(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        fig = go.Figure()
        for camp in CAMPAIGNS:
            camp_df = df[df["캠페인"] == camp]
            fig.add_trace(go.Bar(
                name=camp, x=camp_df["주차"], y=camp_df["Clicks"],
                marker_color=COLORS[camp],
                text=[f"{v:,.0f}" for v in camp_df["Clicks"]],
                textposition="outside",
            ))
        fig.update_layout(title="Clicks (클릭수)", yaxis_title="회", barmode="group", height=400)
        apply_chart_margin(fig)
        st.plotly_chart(fig, use_container_width=True)

# ──────────────── 가입 탭 ────────────────
with tab2:
    st.subheader("가입 지표 — CVR, CPA")

    col1, col2 = st.columns(2)

    with col1:
        fig = go.Figure()
        for camp in CAMPAIGNS:
            camp_df = df[df["캠페인"] == camp]
            fig.add_trace(go.Bar(
                name=camp, x=camp_df["주차"], y=camp_df["가입 CVR"],
                marker_color=COLORS[camp],
                text=[f"{v:.3f}%" for v in camp_df["가입 CVR"]],
                textposition="outside",
            ))
        fig.update_layout(title="가입 CVR (회원가입 / Clicks)", yaxis_title="%", barmode="group", height=400)
        apply_chart_margin(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure()
        for camp in CAMPAIGNS:
            camp_df = df[df["캠페인"] == camp]
            fig.add_trace(go.Bar(
                name=camp, x=camp_df["주차"], y=camp_df["가입 CPA"],
                marker_color=COLORS[camp],
                text=[f"{v:,.0f}원" for v in camp_df["가입 CPA"]],
                textposition="outside",
            ))
        fig.update_layout(title="가입 CPA (비용 / 회원가입)", yaxis_title="원", barmode="group", height=400)
        apply_chart_margin(fig)
        st.plotly_chart(fig, use_container_width=True)

    st.info("💡 retarget 캠페인은 기존 유저 대상이라 가입 수가 극소수입니다. **ua 캠페인 기준**으로 보는 것이 적절합니다.")

# ──────────────── 가입→구매 탭 ────────────────
with tab3:
    st.subheader("가입→구매 전환율 (ua 캠페인)")
    st.caption("리타겟팅 캠페인은 기존 유저 대상이라 가입이 극소수 → CVR이 비정상적으로 높아 ua만 표시합니다.")

    ua_df = df[df["캠페인"] == "bizboard-ua"]
    ua_w1 = ua_df[ua_df["주차"] == "W1"].iloc[0]
    ua_w2 = ua_df[ua_df["주차"] == "W2"].iloc[0]

    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.metric("가입→구매 CVR (W2)", f"{ua_w2['가입→구매 CVR']:.1f}%",
                  delta=f"{ua_w2['가입→구매 CVR'] - ua_w1['가입→구매 CVR']:+.1f}%p")
    with kpi2:
        st.metric("회원가입 (W2)", f"{int(ua_w2['회원가입']):,}명",
                  delta=f"{(ua_w2['회원가입'] - ua_w1['회원가입']) / ua_w1['회원가입'] * 100:+.1f}%")
    with kpi3:
        st.metric("구매완료 (W2)", f"{int(ua_w2['구매완료']):,}건",
                  delta=f"{(ua_w2['구매완료'] - ua_w1['구매완료']) / ua_w1['구매완료'] * 100:+.1f}%")

    col1, col2 = st.columns(2)

    with col1:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=ua_df["주차"], y=ua_df["가입→구매 CVR"],
            marker_color=["#5B8FF9", "#FF6B6B"],
            text=[f"{v:.1f}%" for v in ua_df["가입→구매 CVR"]],
            textposition="outside", width=0.4,
        ))
        fig.update_layout(title="가입→구매 CVR 추이", yaxis_title="%", height=400,
                         yaxis_range=[0, max(ua_df["가입→구매 CVR"]) * 1.3])
        apply_chart_margin(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="회원가입", x=ua_df["주차"], y=ua_df["회원가입"],
            marker_color="#5B8FF9", text=[f"{int(v):,}명" for v in ua_df["회원가입"]],
            textposition="outside",
        ))
        fig.add_trace(go.Bar(
            name="구매완료", x=ua_df["주차"], y=ua_df["구매완료"],
            marker_color="#FF6B6B", text=[f"{int(v):,}건" for v in ua_df["구매완료"]],
            textposition="outside",
        ))
        fig.update_layout(title="회원가입 vs 구매완료", yaxis_title="건", barmode="group", height=400)
        apply_chart_margin(fig)
        st.plotly_chart(fig, use_container_width=True)

# ──────────────── 구매 탭 ────────────────
with tab4:
    st.subheader("구매 지표 — CVR, CPA, ROAS, ARPPU")

    col1, col2 = st.columns(2)

    with col1:
        fig = go.Figure()
        for camp in CAMPAIGNS:
            camp_df = df[df["캠페인"] == camp]
            fig.add_trace(go.Bar(
                name=camp, x=camp_df["주차"], y=camp_df["구매 CVR"],
                marker_color=COLORS[camp],
                text=[f"{v:.2f}%" for v in camp_df["구매 CVR"]],
                textposition="outside",
            ))
        fig.update_layout(title="구매 CVR (구매완료 / Clicks)", yaxis_title="%", barmode="group", height=400)
        apply_chart_margin(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure()
        for camp in CAMPAIGNS:
            camp_df = df[df["캠페인"] == camp]
            fig.add_trace(go.Bar(
                name=camp, x=camp_df["주차"], y=camp_df["구매 CPA"],
                marker_color=COLORS[camp],
                text=[f"{v:,.0f}원" for v in camp_df["구매 CPA"]],
                textposition="outside",
            ))
        fig.update_layout(title="구매 CPA (비용 / 구매완료)", yaxis_title="원", barmode="group", height=400)
        apply_chart_margin(fig)
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        fig = go.Figure()
        for camp in CAMPAIGNS:
            camp_df = df[df["캠페인"] == camp]
            fig.add_trace(go.Bar(
                name=camp, x=camp_df["주차"], y=camp_df["ROAS"],
                marker_color=COLORS[camp],
                text=[f"{v:.0f}%" for v in camp_df["ROAS"]],
                textposition="outside",
            ))
        fig.add_hline(y=100, line_dash="dash", line_color="red", annotation_text="손익분기 100%")
        fig.update_layout(title="ROAS (에어브릿지 ROAS × 1.763)", yaxis_title="%", barmode="group", height=400)
        apply_chart_margin(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        fig = go.Figure()
        for camp in CAMPAIGNS:
            camp_df = df[df["캠페인"] == camp]
            fig.add_trace(go.Bar(
                name=camp, x=camp_df["주차"], y=camp_df["ARPPU"],
                marker_color=COLORS[camp],
                text=[f"{v:,.0f}원" for v in camp_df["ARPPU"]],
                textposition="outside",
            ))
        fig.update_layout(title="ARPPU (구매액 / 구매유저수)", yaxis_title="원", barmode="group", height=400)
        apply_chart_margin(fig)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### 구매액 vs 비용")
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    for camp in CAMPAIGNS:
        camp_df = df[df["캠페인"] == camp]
        fig.add_trace(go.Bar(
            name=f"{camp} 구매액", x=[f"{camp}<br>{w}" for w in camp_df["주차"]],
            y=camp_df["구매액"].values, marker_color=COLORS[camp], opacity=0.8,
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            name=f"{camp} Cost", x=[f"{camp}<br>{w}" for w in camp_df["주차"]],
            y=camp_df["비용"].values, mode="markers+lines",
            marker=dict(size=10, color=COLORS[camp]), line=dict(dash="dot"),
        ), secondary_y=True)
    fig.update_layout(title="캠페인별 구매액(막대) vs 비용(점선)", height=450, barmode="group")
    fig.update_yaxes(title_text="구매액 (원)", secondary_y=False)
    fig.update_yaxes(title_text="비용 (원)", secondary_y=True)
    fig.update_layout(margin=CHART_MARGIN)
    st.plotly_chart(fig, use_container_width=True)

# ──────────────── 광고그룹별 성과 탭 ────────────────
with tab5:
    st.subheader("🔍 광고그룹별 성과 분석")

    selected_camp = st.selectbox("캠페인 선택", CAMPAIGNS, index=0)
    camp_adf = adf[adf["캠페인"] == selected_camp]
    adgroups = sorted(camp_adf["광고그룹"].unique())

    # 지표 선택
    metric_option = st.radio(
        "지표 선택",
        ["구매 (ROAS, CPA, CVR)", "유입 (CTR, CPC)", "비용 & 구매액"],
        horizontal=True,
    )

    if metric_option == "구매 (ROAS, CPA, CVR)":
        # ROAS 비교 차트
        st.markdown("#### 광고그룹별 ROAS 비교")
        fig = go.Figure()
        for week, color in WEEK_COLORS.items():
            week_data = camp_adf[camp_adf["주차"] == week].sort_values("ROAS", ascending=True)
            fig.add_trace(go.Bar(
                name=week, y=week_data["광고그룹"], x=week_data["ROAS"],
                orientation="h", marker_color=color,
                text=[f"{v:.0f}%" for v in week_data["ROAS"]],
                textposition="outside",
            ))
        fig.add_vline(x=100, line_dash="dash", line_color="red", annotation_text="손익분기")
        fig.update_layout(barmode="group", height=max(400, len(adgroups) * 45), xaxis_title="ROAS %",
                         margin=dict(l=200))
        apply_chart_margin(fig)
        st.plotly_chart(fig, use_container_width=True)

        # 구매 CPA 비교 차트
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 광고그룹별 구매 CPA")
            fig = go.Figure()
            for week, color in WEEK_COLORS.items():
                week_data = camp_adf[(camp_adf["주차"] == week) & (camp_adf["구매 CPA"] > 0)].sort_values("구매 CPA", ascending=True)
                fig.add_trace(go.Bar(
                    name=week, y=week_data["광고그룹"], x=week_data["구매 CPA"],
                    orientation="h", marker_color=color,
                    text=[f"{v:,.0f}원" for v in week_data["구매 CPA"]],
                    textposition="outside",
                ))
            fig.update_layout(barmode="group", height=max(400, len(adgroups) * 40),
                             xaxis_title="원", margin=dict(l=200))
            apply_chart_margin(fig)
        st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### 광고그룹별 구매 CVR")
            fig = go.Figure()
            for week, color in WEEK_COLORS.items():
                week_data = camp_adf[camp_adf["주차"] == week].sort_values("구매 CVR", ascending=True)
                fig.add_trace(go.Bar(
                    name=week, y=week_data["광고그룹"], x=week_data["구매 CVR"],
                    orientation="h", marker_color=color,
                    text=[f"{v:.2f}%" for v in week_data["구매 CVR"]],
                    textposition="outside",
                ))
            fig.update_layout(barmode="group", height=max(400, len(adgroups) * 40),
                             xaxis_title="%", margin=dict(l=200))
            apply_chart_margin(fig)
        st.plotly_chart(fig, use_container_width=True)

    elif metric_option == "유입 (CTR, CPC)":
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 광고그룹별 CTR")
            fig = go.Figure()
            for week, color in WEEK_COLORS.items():
                week_data = camp_adf[(camp_adf["주차"] == week) & (camp_adf["CTR"] > 0)].sort_values("CTR", ascending=True)
                fig.add_trace(go.Bar(
                    name=week, y=week_data["광고그룹"], x=week_data["CTR"],
                    orientation="h", marker_color=color,
                    text=[f"{v:.2f}%" for v in week_data["CTR"]],
                    textposition="outside",
                ))
            fig.update_layout(barmode="group", height=max(400, len(adgroups) * 40),
                             xaxis_title="%", margin=dict(l=200))
            apply_chart_margin(fig)
        st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### 광고그룹별 CPC")
            fig = go.Figure()
            for week, color in WEEK_COLORS.items():
                week_data = camp_adf[(camp_adf["주차"] == week) & (camp_adf["CPC"] > 0)].sort_values("CPC", ascending=True)
                fig.add_trace(go.Bar(
                    name=week, y=week_data["광고그룹"], x=week_data["CPC"],
                    orientation="h", marker_color=color,
                    text=[f"{v:,.0f}원" for v in week_data["CPC"]],
                    textposition="outside",
                ))
            fig.update_layout(barmode="group", height=max(400, len(adgroups) * 40),
                             xaxis_title="원", margin=dict(l=200))
            apply_chart_margin(fig)
        st.plotly_chart(fig, use_container_width=True)

    else:  # 비용 & 구매액
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 광고그룹별 비용")
            fig = go.Figure()
            for week, color in WEEK_COLORS.items():
                week_data = camp_adf[(camp_adf["주차"] == week) & (camp_adf["비용"] > 0)].sort_values("비용", ascending=True)
                fig.add_trace(go.Bar(
                    name=week, y=week_data["광고그룹"], x=week_data["비용"],
                    orientation="h", marker_color=color,
                    text=[f"{v/10000:,.0f}만원" for v in week_data["비용"]],
                    textposition="outside",
                ))
            fig.update_layout(barmode="group", height=max(400, len(adgroups) * 40),
                             xaxis_title="원", margin=dict(l=200))
            apply_chart_margin(fig)
        st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### 광고그룹별 구매액")
            fig = go.Figure()
            for week, color in WEEK_COLORS.items():
                week_data = camp_adf[(camp_adf["주차"] == week) & (camp_adf["구매액"] > 0)].sort_values("구매액", ascending=True)
                fig.add_trace(go.Bar(
                    name=week, y=week_data["광고그룹"], x=week_data["구매액"],
                    orientation="h", marker_color=color,
                    text=[f"{v/10000:,.0f}만원" for v in week_data["구매액"]],
                    textposition="outside",
                ))
            fig.update_layout(barmode="group", height=max(400, len(adgroups) * 40),
                             xaxis_title="원", margin=dict(l=200))
            apply_chart_margin(fig)
        st.plotly_chart(fig, use_container_width=True)

    # 광고그룹별 상세 데이터 테이블
    st.markdown("---")
    st.markdown("#### 상세 데이터 테이블")

    show_df = camp_adf[["광고그룹", "주차", "Impressions", "Clicks", "비용",
                         "회원가입", "구매완료", "구매액", "CTR", "CPC", "구매 CVR", "구매 CPA", "ROAS", "ARPPU"]].copy()

    # 포맷팅
    fmt_show = show_df.copy()
    fmt_show["Impressions"] = fmt_show["Impressions"].apply(lambda x: f"{x:,.0f}")
    fmt_show["Clicks"] = fmt_show["Clicks"].apply(lambda x: f"{x:,.0f}")
    fmt_show["비용"] = fmt_show["비용"].apply(lambda x: f"{x:,.0f}원")
    fmt_show["회원가입"] = fmt_show["회원가입"].apply(lambda x: f"{x:,.0f}")
    fmt_show["구매완료"] = fmt_show["구매완료"].apply(lambda x: f"{x:,.0f}")
    fmt_show["구매액"] = fmt_show["구매액"].apply(lambda x: f"{x:,.0f}원")
    fmt_show["CTR"] = fmt_show["CTR"].apply(lambda x: f"{x:.2f}%")
    fmt_show["CPC"] = fmt_show["CPC"].apply(lambda x: f"{x:,.0f}원" if x > 0 else "-")
    fmt_show["구매 CVR"] = fmt_show["구매 CVR"].apply(lambda x: f"{x:.2f}%")
    fmt_show["구매 CPA"] = fmt_show["구매 CPA"].apply(lambda x: f"{x:,.0f}원" if x > 0 else "-")
    fmt_show["ROAS"] = fmt_show["ROAS"].apply(lambda x: f"{x:.0f}%" if x > 0 else "-")
    fmt_show["ARPPU"] = fmt_show["ARPPU"].apply(lambda x: f"{x:,.0f}원" if x > 0 else "-")

    st.dataframe(fmt_show.sort_values(["광고그룹", "주차"]), use_container_width=True, hide_index=True,
                 height=min(800, len(fmt_show) * 38 + 40))

    # W1→W2 증감률 테이블
    st.markdown("#### W1 → W2 증감률")
    change_rows = []
    for ag in adgroups:
        ag_data = camp_adf[camp_adf["광고그룹"] == ag]
        w1_data = ag_data[ag_data["주차"] == "W1"]
        w2_data = ag_data[ag_data["주차"] == "W2"]
        if len(w1_data) == 0 or len(w2_data) == 0:
            continue
        w1r = w1_data.iloc[0]
        w2r = w2_data.iloc[0]
        row = {"광고그룹": ag}
        for m in ["Impressions", "Clicks", "비용", "구매완료", "구매액", "구매 CVR", "구매 CPA", "ROAS", "ARPPU"]:
            pct = safe_pct_change(w1r[m], w2r[m])
            row[m] = f"{pct:+.1f}%" if pct is not None else "-"
        change_rows.append(row)

    if change_rows:
        st.dataframe(pd.DataFrame(change_rows), use_container_width=True, hide_index=True)

# ──────────────── 원본 데이터 탭 ────────────────
with tab6:
    st.subheader("캠페인 요약 데이터")

    display_df = df.copy()
    won_cols = ["비용", "구매액", "가입 CPA", "구매 CPA", "ARPPU", "CPC"]
    pct_cols = ["CTR", "가입 CVR", "가입→구매 CVR", "구매 CVR", "ROAS"]

    for c in won_cols:
        display_df[c] = display_df[c].apply(lambda x: f"{x:,.0f}원")
    for c in pct_cols:
        display_df[c] = display_df[c].apply(lambda x: f"{x:.2f}%")
    for c in ["Impressions", "Clicks", "회원가입", "구매완료", "구매유저(App)", "구매유저(Web)", "구매유저 합계"]:
        display_df[c] = display_df[c].apply(lambda x: f"{x:,.0f}")

    st.dataframe(display_df, use_container_width=True, hide_index=True, height=350)

    st.markdown("#### W1 → W2 증감률")
    change_data = []
    metrics = [
        ("Impressions", "int"), ("Clicks", "int"), ("비용", "won"),
        ("회원가입", "int"), ("구매완료", "int"), ("구매액", "won"),
        ("구매 CVR", "pct"), ("구매 CPA", "won"), ("ROAS", "pct"), ("ARPPU", "won"),
    ]
    for camp in CAMPAIGNS + ["kakao 합계"]:
        row = {"캠페인": camp}
        camp_df_local = df[df["캠페인"] == camp]
        w1_row = camp_df_local[camp_df_local["주차"] == "W1"].iloc[0]
        w2_row = camp_df_local[camp_df_local["주차"] == "W2"].iloc[0]
        for metric, _ in metrics:
            v1, v2 = w1_row[metric], w2_row[metric]
            if v1 != 0:
                pct = (v2 - v1) / v1 * 100
                row[metric] = f"{pct:+.1f}%"
            else:
                row[metric] = "N/A"
        change_data.append(row)

    change_df = pd.DataFrame(change_data)
    st.dataframe(change_df, use_container_width=True, hide_index=True)

# ──────────────────────────────────────────────
# 인사이트 섹션
# ──────────────────────────────────────────────
st.markdown("---")
st.subheader("💡 핵심 인사이트")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### ✅ 긍정적 변화")
    st.markdown("""
    - **구매 CVR** 1.74% → 2.10% (+20.7%) 전환 효율 개선
    - **구매 CPA** 11,236원 → 9,183원 (-18.3%) 비용 절감
    - **bizboard-ua** 구매 +100%, ROAS 362%→456% 성장세
    - **lecaf_selection** (ua): 가입 393건, 가입CPA 3,104원으로 가장 효율적
    - **lecaf_selection** (retarget): ROAS 604%→696%, 구매 +133% 확대
    - **ct_runningshoes** (display): ROAS 435%→576% 개선
    """)

with col2:
    st.markdown("#### ⚠️ 주의 필요")
    st.markdown("""
    - **display-retarget 전반 급감**: 노출 -43%, 구매액 -54%
    - **br_stoneisland** (display): 비용 -80%, 구매 -85% 거의 중단
    - **ct_athleredition** (display): 비용 -92%, 구매 -95%
    - **ct_highbrand** (display): W2 실질적 소진 없음
    - **ARPPU 전반 하락**: 63,403원→49,070원 (-22.6%)
    - **4890562-product**: 구매 24건→1건, CPA 8배 악화
    """)

st.markdown("---")
st.subheader("📌 다음 액션 제안")
st.markdown("""
1. **display-retarget** 예산/소재 변경 이력 확인 → br_stoneisland, ct_athleredition 급감 원인 파악
2. **bizboard-ua lecaf_selection** 예산 증액 검토 → 가입CPA 3,104원, 가입→구매 전환 양호
3. **ct_pgacutterbuck** (display): W2 구매 121건, ROAS 444%로 안정적 → 예산 유지/증액 검토
4. **ARPPU 하락 원인** → 구매 상품 카테고리/할인율 변화 추가 조회
5. W2 신규 광고그룹(ct_hiking, ct_shortsleeve, ct_warehouserelease) 초기 성과 모니터링
""")
