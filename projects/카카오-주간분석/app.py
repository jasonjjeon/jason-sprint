import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ──────────────────────────────────────────────
# 페이지 설정
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="카카오 주간 마케팅 분석",
    page_icon="📊",
    layout="wide",
)

st.title("📊 카카오 주간 마케팅 분석")
st.caption("W1 (3/23~3/29) vs W2 (3/30~4/5) | Cost Payback = Cost Channel ÷ 1.763")

# ──────────────────────────────────────────────
# 데이터 정의
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
    "Cost (Channel)": [21_690_419, 23_643_311, 2_394_221, 2_719_175, 10_444_799, 5_334_921, 34_529_439, 31_697_407],
    "Cost (Payback)": [12_303_130, 13_410_840, 1_358_038, 1_542_357, 5_924_446, 3_026_047, 19_585_615, 17_979_244],
    "회원가입": [7, 16, 251, 427, 5, 3, 263, 446],
    "구매완료": [1_127, 1_449, 107, 214, 509, 295, 1_743, 1_958],
    "구매액": [66_387_990, 63_758_221, 4_914_681, 7_037_535, 31_049_160, 14_185_722, 102_351_831, 84_981_478],
    "구매유저(App)": [744, 931, 29, 47, 351, 203, 1_124, 1_181],
    "구매유저(Web)": [277, 396, 74, 162, 106, 64, 457, 622],
}

df = pd.DataFrame(RAW)
df["구매유저 합계"] = df["구매유저(App)"] + df["구매유저(Web)"]

# 성과 지표 계산
df["CTR"] = df["Clicks"] / df["Impressions"] * 100
df["CPC"] = df["Cost (Payback)"] / df["Clicks"]
df["가입 CVR"] = df["회원가입"] / df["Clicks"] * 100
df["가입 CPA"] = df["Cost (Payback)"] / df["회원가입"]
df["가입→구매 CVR"] = df["구매완료"] / df["회원가입"] * 100
df["구매 CVR"] = df["구매완료"] / df["Clicks"] * 100
df["구매 CPA"] = df["Cost (Payback)"] / df["구매완료"]
df["ROAS"] = df["구매액"] / df["Cost (Payback)"] * 100
df["ARPPU"] = df["구매액"] / df["구매유저 합계"]

CAMPAIGNS = ["bizboard-retarget", "bizboard-ua", "display-retarget"]
COLORS = {"bizboard-retarget": "#FAE100", "bizboard-ua": "#3C1E1E", "display-retarget": "#FF6B35"}
WEEK_COLORS = {"W1": "#5B8FF9", "W2": "#FF6B6B"}

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


def calc_change(w1, w2):
    if w1 == 0:
        return "N/A"
    change = (w2 - w1) / w1 * 100
    arrow = "▲" if change > 0 else "▼" if change < 0 else "→"
    color = "red" if change < 0 else "green" if change > 0 else "gray"
    return f":{color}[{arrow} {abs(change):.1f}%]"


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
    ("Cost (Payback)", w1["Cost (Payback)"], w2["Cost (Payback)"], "won"),
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
            delta_color="normal" if label not in ("구매 CPA", "Cost (Payback)") else "inverse",
        )

# ──────────────────────────────────────────────
# 탭 구성
# ──────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 유입", "👤 가입", "🔄 가입→구매", "💰 구매", "📋 원본 데이터"])

# ──────────────── 유입 탭 ────────────────
with tab1:
    st.subheader("유입 지표 — CTR, CPC")

    col1, col2 = st.columns(2)

    with col1:
        fig = go.Figure()
        for camp in CAMPAIGNS:
            camp_df = df[df["캠페인"] == camp]
            fig.add_trace(go.Bar(
                name=camp,
                x=camp_df["주차"],
                y=camp_df["CTR"],
                marker_color=COLORS[camp],
                text=[f"{v:.2f}%" for v in camp_df["CTR"]],
                textposition="outside",
            ))
        fig.update_layout(title="CTR (클릭률)", yaxis_title="%", barmode="group", height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure()
        for camp in CAMPAIGNS:
            camp_df = df[df["캠페인"] == camp]
            fig.add_trace(go.Bar(
                name=camp,
                x=camp_df["주차"],
                y=camp_df["CPC"],
                marker_color=COLORS[camp],
                text=[f"{v:,.0f}원" for v in camp_df["CPC"]],
                textposition="outside",
            ))
        fig.update_layout(title="CPC (클릭당 비용)", yaxis_title="원", barmode="group", height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Impressions & Clicks 추이
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
        fig.update_layout(title="가입 CPA (Cost Payback / 회원가입)", yaxis_title="원", barmode="group", height=400)
        st.plotly_chart(fig, use_container_width=True)

    st.info("💡 retarget 캠페인은 기존 유저 대상이라 가입 수가 극소수입니다. **ua 캠페인 기준**으로 보는 것이 적절합니다.")

# ──────────────── 가입→구매 탭 ────────────────
with tab3:
    st.subheader("가입→구매 전환율 (ua 캠페인)")
    st.caption("리타겟팅 캠페인은 기존 유저 대상이라 가입이 극소수 → CVR이 비정상적으로 높아 ua만 표시합니다.")

    ua_df = df[df["캠페인"] == "bizboard-ua"]
    ua_w1 = ua_df[ua_df["주차"] == "W1"].iloc[0]
    ua_w2 = ua_df[ua_df["주차"] == "W2"].iloc[0]

    # KPI 카드
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
            textposition="outside",
            width=0.4,
        ))
        fig.update_layout(title="가입→구매 CVR 추이", yaxis_title="%", height=400,
                         yaxis_range=[0, max(ua_df["가입→구매 CVR"]) * 1.3])
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
        fig.update_layout(title="구매 CPA (Cost Payback / 구매완료)", yaxis_title="원", barmode="group", height=400)
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
        fig.update_layout(title="ROAS (구매액 / Cost Payback)", yaxis_title="%", barmode="group", height=400)
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
        st.plotly_chart(fig, use_container_width=True)

    # 구매액 & 비용 비교
    st.markdown("#### 구매액 vs Cost (Payback)")
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    for camp in CAMPAIGNS:
        camp_df = df[df["캠페인"] == camp]
        fig.add_trace(go.Bar(
            name=f"{camp} 구매액", x=[f"{camp}<br>{w}" for w in camp_df["주차"]],
            y=camp_df["구매액"].values, marker_color=COLORS[camp], opacity=0.8,
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            name=f"{camp} Cost", x=[f"{camp}<br>{w}" for w in camp_df["주차"]],
            y=camp_df["Cost (Payback)"].values, mode="markers+lines",
            marker=dict(size=10, color=COLORS[camp]), line=dict(dash="dot"),
        ), secondary_y=True)
    fig.update_layout(title="캠페인별 구매액(막대) vs Cost Payback(점선)", height=450, barmode="group")
    fig.update_yaxes(title_text="구매액 (원)", secondary_y=False)
    fig.update_yaxes(title_text="Cost Payback (원)", secondary_y=True)
    st.plotly_chart(fig, use_container_width=True)

# ──────────────── 원본 데이터 탭 ────────────────
with tab5:
    st.subheader("원본 데이터")

    display_df = df.copy()
    won_cols = ["Cost (Channel)", "Cost (Payback)", "구매액", "가입 CPA", "구매 CPA", "ARPPU", "CPC"]
    pct_cols = ["CTR", "가입 CVR", "가입→구매 CVR", "구매 CVR", "ROAS"]

    for c in won_cols:
        display_df[c] = display_df[c].apply(lambda x: f"{x:,.0f}원")
    for c in pct_cols:
        display_df[c] = display_df[c].apply(lambda x: f"{x:.2f}%")
    for c in ["Impressions", "Clicks", "회원가입", "구매완료", "구매유저(App)", "구매유저(Web)", "구매유저 합계"]:
        display_df[c] = display_df[c].apply(lambda x: f"{x:,.0f}")

    st.dataframe(display_df, use_container_width=True, hide_index=True, height=350)

    # W1 vs W2 증감률 테이블
    st.markdown("#### W1 → W2 증감률")
    change_data = []
    metrics = [
        ("Impressions", "int"), ("Clicks", "int"), ("Cost (Payback)", "won"),
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
    - **가입 CPA** ua 기준 5,411원→3,611원 효율적
    """)

with col2:
    st.markdown("#### ⚠️ 주의 필요")
    st.markdown("""
    - **display-retarget 급감**: 노출 -43%, 구매액 -54%
    - **ROAS 하락**: 522% → 473% (-9.3%)
    - **ARPPU 전반 하락**: 63,403원→49,070원 (-22.6%)
    - **bizboard-retarget**: 구매↑ but 구매액↓ (저가 전환 가능성)
    """)

st.markdown("---")
st.subheader("📌 다음 액션 제안")
st.markdown("""
1. **display-retarget** 예산/소재 변경 이력 확인 → W2 급감 원인 파악
2. **bizboard-ua** 성장세 활용 → 예산 증액 검토 (가입 CPA 3,611원)
3. **ARPPU 하락 원인 분석** → 구매 상품 카테고리/할인율 변화 추가 조회
""")
