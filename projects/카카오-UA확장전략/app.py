import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="UA 확장 전략 (카카오·메타·구글)", layout="wide")

# ─── 커스텀 스타일 ───
st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; }
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 1.2rem; border-radius: 12px; text-align: center;
        border: 1px solid #0f3460; margin-bottom: 0.5rem;
    }
    .metric-card h3 { color: #94a3b8; font-size: 0.85rem; margin: 0; }
    .metric-card h1 { color: #e2e8f0; font-size: 1.8rem; margin: 0.3rem 0 0 0; }
    .metric-green h1 { color: #22c55e; }
    .metric-blue h1 { color: #3b82f6; }
    .metric-yellow h1 { color: #eab308; }
    .metric-red h1 { color: #ef4444; }
    .tier-1 { border-left: 4px solid #22c55e; padding-left: 12px; margin-bottom: 8px; }
    .tier-2 { border-left: 4px solid #eab308; padding-left: 12px; margin-bottom: 8px; }
    .tier-3 { border-left: 4px solid #3b82f6; padding-left: 12px; margin-bottom: 8px; }
    .tier-new { border-left: 4px solid #a855f7; padding-left: 12px; margin-bottom: 8px; }
    .gap-ok { background: #052e16; border: 1px solid #22c55e; border-radius: 8px; padding: 12px; margin: 6px 0; }
    .gap-warn { background: #422006; border: 1px solid #eab308; border-radius: 8px; padding: 12px; margin: 6px 0; }
    .gap-danger { background: #450a0a; border: 1px solid #ef4444; border-radius: 8px; padding: 12px; margin: 6px 0; }
    .section-header {
        background: linear-gradient(90deg, #1e3a5f, transparent);
        padding: 8px 16px; border-radius: 8px; margin: 1.5rem 0 1rem 0;
    }
    .channel-kakao { background: linear-gradient(90deg, #3A1D00, transparent); padding: 8px 16px; border-radius: 8px; margin: 1.5rem 0 1rem 0; }
    .channel-meta { background: linear-gradient(90deg, #1A1D5A, transparent); padding: 8px 16px; border-radius: 8px; margin: 1.5rem 0 1rem 0; }
    .channel-google { background: linear-gradient(90deg, #1A3D1A, transparent); padding: 8px 16px; border-radius: 8px; margin: 1.5rem 0 1rem 0; }
</style>
""", unsafe_allow_html=True)

# ─── 헤더 ───
st.title("UA 확장 전략")
st.caption("기준 기간: 2026.03.09 ~ 04.06 | 보정계수 1.76 (카카오만 적용) | RT 목표 보정 ROAS 500% · UA 목표 보정 ROAS 400% | 메타·구글은 Raw ROAS")

tab_gap, tab_overview, tab_kakao, tab_meta, tab_google = st.tabs([
    "목표 대비 갭 분석", "전체 현황", "카카오 (UA + 앱설치)", "메타 (앱설치-구매)", "구글 (앱설치-구매)"
])


# ═══════════════════════════════════════════════════════════════
# TAB 0: 목표 대비 갭 분석
# ═══════════════════════════════════════════════════════════════
with tab_gap:
    st.markdown('<div class="section-header"><h3>목표 대비 갭 분석 (14주차: 3/31~4/6 기준)</h3></div>', unsafe_allow_html=True)
    st.markdown("> **목표**: 카카오 RT 보정 ROAS **500%** · UA 보정 ROAS **400%** | 메타·구글은 Raw ROAS (보정 없음) | 카카오 UA 일예산 500만")

    # ─── 1. 채널별 목표 대비 현황 ───
    st.markdown("### 1. 채널별 효율 갭")

    gap_df = pd.DataFrame({
        "채널": ["카카오 RT (PBTD)", "카카오 PBTD UA", "카카오 기존 UA", "메타 앱구매", "구글 앱설치"],
        "14주차 일평균 비용": ["419만", "38만", "521만", "32만", "53만"],
        "목표 일예산": ["현행 유지", "500만", "현행 유지", "확장 예정", "80만 (확장)"],
        "예산 갭": ["-", "-462만 (부족)", "-", "-", "-27만 (부족)"],
        "ROAS": ["보정 484%", "보정 442%", "보정 461%", "Raw 367%", "Raw 413%"],
        "목표 ROAS": ["보정 500%", "보정 400%", "보정 400%", "- (보정 없음)", "- (보정 없음)"],
        "ROAS 갭": ["-16%p", "+42%p", "+61%p", "-", "-"],
        "판정": ["미달", "달성 (볼륨 부족)", "달성", "참고", "참고"],
    })
    st.dataframe(gap_df, use_container_width=True, hide_index=True)

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        fig_gap_roas = go.Figure()
        # 카카오만 보정 ROAS, 메타/구글은 Raw ROAS
        channels_k = ["카카오 RT\n(보정)", "카카오\nPBTD UA\n(보정)", "카카오\n기존 UA\n(보정)"]
        roas_k = [484, 442, 461]
        targets_k = [500, 400, 400]
        colors_k = ["#ef4444", "#22c55e", "#22c55e"]  # RT 미달
        fig_gap_roas.add_trace(go.Bar(x=channels_k, y=roas_k, marker_color=colors_k,
            text=[f"{v}%" for v in roas_k], textposition="outside", name="실적 (보정)"))
        fig_gap_roas.add_trace(go.Scatter(x=channels_k, y=targets_k, mode="markers",
            marker=dict(symbol="line-ew-open", size=20, color="#ef4444", line=dict(width=3)),
            name="목표"))
        fig_gap_roas.update_layout(title="카카오 보정 ROAS: 목표 vs 실적 (14주차)", height=380,
            template="plotly_dark", yaxis_title="보정 ROAS (%)",
            legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(fig_gap_roas, use_container_width=True)

    with col_g2:
        fig_gap_budget = go.Figure()
        ch_b = ["카카오 RT", "카카오\nPBTD UA", "카카오\n기존 UA", "메타\n앱구매", "구글\n앱설치"]
        target_b = [419, 500, 521, 50, 80]
        actual_b = [419, 38, 521, 32, 53]
        fig_gap_budget.add_trace(go.Bar(x=ch_b, y=target_b, name="목표 일예산", marker_color="#3b82f6", opacity=0.5))
        fig_gap_budget.add_trace(go.Bar(x=ch_b, y=actual_b, name="실제 일예산", marker_color="#22c55e"))
        fig_gap_budget.update_layout(title="일예산: 목표 vs 실적 (14주차, 만원)", height=380,
            template="plotly_dark", barmode="group", yaxis_title="일예산 (만원)",
            legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(fig_gap_budget, use_container_width=True)

    # ─── 2. 광고그룹별 ROAS 갭 (비효율 진단) ───
    st.markdown("### 2. RT 비효율 광고그룹 진단 (14주차, 보정 ROAS 500% 미달)")

    underperform = pd.DataFrame({
        "광고그룹명": [
            "male3564-2601_br_cpcompany-promotion",
            "male3564-2601_br_stoneisland-promotion",
            "male4069-2601_ct_pgacutterbuck-promotion (BB)",
            "male3564-2512_ct_now-promotion (display)",
            "male3064-4890514-product",
            "male3564-2604_ct_shortsleeve-promotion",
            "male3064-4890509-product",
            "male3064-4890562-product",
        ],
        "캠페인": ["RT (bizboard)", "RT (bizboard)", "RT (bizboard)", "RT (display)",
                  "RT (bizboard)", "RT (bizboard)", "RT (bizboard)", "RT (bizboard)"],
        "14주 비용": ["246만", "235만", "178만", "63만", "81만", "50만", "27만", "9만"],
        "보정ROAS": ["387%", "399%", "369%", "380%", "325%", "304%", "199%", "54%"],
        "목표 갭(vs 500%)": ["-113%p", "-101%p", "-131%p", "-120%p", "-175%p", "-196%p", "-301%p", "-446%p"],
        "원인": [
            "CPC 494원 과다, 프리미엄 브랜드 UA 전환 낮음",
            "CPC 548원 과다, 객단가는 높으나 전환율 저조",
            "Bizboard CPC 304원 상승, Display 대비 비효율",
            "Display CPC 370원 상승 (전주 대비), 전환 30건으로 감소",
            "상품 단위 타겟, 전환수 50건이나 매출 낮음 (저단가 상품)",
            "시즌 초기라 학습 부족, CPC 459원 과다",
            "상품 단위, CPC 614원 과다 + 전환 13건 소량",
            "상품 단위, CPC 682원 + 전환 1건 → 사실상 실패",
        ],
    })
    st.dataframe(underperform, use_container_width=True, hide_index=True)

    # ─── 비효율 시각화 ───
    under_viz = pd.DataFrame({
        "광고그룹": ["cpcompany", "stoneisland", "pgacutterbuck(BB)", "now(disp)",
                    "상품4890514", "shortsleeve", "상품4890509", "상품4890562"],
        "보정ROAS(%)": [387, 399, 369, 380, 325, 304, 199, 54],
        "비용(만)": [246, 235, 178, 63, 81, 50, 27, 9],
        "CPC": [494, 548, 304, 370, 360, 459, 614, 682],
    })
    fig_under = px.scatter(under_viz, x="CPC", y="보정ROAS(%)", size="비용(만)", text="광고그룹",
        color_discrete_sequence=["#ef4444"], size_max=40)
    fig_under.add_hline(y=500, line_dash="dash", line_color="#22c55e", annotation_text="RT 목표 500%")
    fig_under.add_vline(x=400, line_dash="dash", line_color="#eab308", annotation_text="CPC 경고선")
    fig_under.update_traces(textposition="top center", textfont_size=10)
    fig_under.update_layout(title="비효율 광고그룹: CPC vs ROAS (우하단이 위험)", height=400,
        template="plotly_dark", xaxis_title="CPC (원)", yaxis_title="보정 ROAS (%)")
    st.plotly_chart(fig_under, use_container_width=True)

    # ─── 3. 금주 해결안 ───
    st.markdown("### 3. 금주(4/7~4/13) 즉시 액션")

    st.markdown('<div class="gap-danger">', unsafe_allow_html=True)
    st.markdown("""
    **즉시 중단/축소 (비용 절감 → UA 예산으로 전환)**

    | 광고그룹명 | 액션 | 절감 예산 | 근거 |
    |-----------|------|----------|------|
    | `male3064-4890562-product` | **중단** | 일 1.3만 | ROAS 54%, 전환 1건, 회생 불가 |
    | `male3064-4890509-product` | **중단** | 일 3.9만 | ROAS 199%, CPC 614원, 전환 부족 |
    | `male3564-2604_ct_shortsleeve-promotion` | **예산 50% 축소** | 일 3.6만 | ROAS 304%, 시즌 초기 학습 대기 |
    | `male3064-4890514-product` | **예산 30% 축소** | 일 3.5만 | ROAS 325%, 저단가 상품 비효율 |
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="gap-warn">', unsafe_allow_html=True)
    st.markdown("""
    **소재 교체/CPC 조정 (효율 개선)**

    | 광고그룹명 | 액션 | 기대 효과 | 근거 |
    |-----------|------|----------|------|
    | `male3564-2601_br_cpcompany-promotion` | CPC 상한 400원 설정 + 소재 교체 | ROAS 387% → 500%+ | CPC 494원이 핵심 원인 |
    | `male3564-2601_br_stoneisland-promotion` | CPC 상한 400원 설정 + 소재 교체 | ROAS 399% → 500%+ | CPC 548원, 목표 대비 -101%p |
    | `male4069-2601_ct_pgacutterbuck-promotion (BB)` | Bizboard 예산 축소 → Display로 이동 | ROAS 369% → 448%+ | Display는 ROAS 448% (목표 근접) |
    | `male3564-2512_ct_now-promotion (display)` | 소재 리프레시 | ROAS 380% → 500%+ | CPC 상승이 원인, 소재 피로도 |
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="gap-ok">', unsafe_allow_html=True)
    st.markdown("""
    **신규 오픈 (절감 예산 + 추가 예산 투입)**

    | 광고그룹명 | 캠페인 | 일예산 | 근거 |
    |-----------|--------|--------|------|
    | `male4069-2601_ct_pgacutterbuck-promotion` | PBTD UA (신규) | 80만 | RT Display ROAS 448%, 전환 124건/주 |
    | `male3564-2602_ct_benefit-promotion` | PBTD UA (신규) | 50만 | RT ROAS 650%, CPC 327원 |
    | `male3064-2602_ct_runningshoes-promotion` | PBTD UA (신규) | 40만 | RT ROAS 515%(disp), 시즌 수요 |
    | `male3564-2604_ct_hiking-promotion` | PBTD UA (신규) | 30만 | RT ROAS 454%, CPC 168원 최저 |
    | `male3064-custom_lecaf_selection-promotion` | PBTD UA (기존) | 30만→50만 증액 | ROAS 502%, 전환 183건/주 검증 |
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # ─── 4. 이번 달(4월) 장기 계획 ───
    st.markdown("### 4. 이번 달(4월) 장기 해결 로드맵")

    roadmap = pd.DataFrame({
        "주차": ["1주차 (4/7~13)", "2주차 (4/14~20)", "3주차 (4/21~27)", "4주차 (4/28~5/4)"],
        "카카오 PBTD UA": [
            "비효율 2개 중단 + 1순위 4개 오픈\n일예산 200만 시작",
            "성과 리뷰, 2순위 3개 추가 오픈\n일예산 350만",
            "전체 리뷰, 비효율 축소→고효율 확대\n일예산 450만",
            "안정화, 일예산 500만 목표 도달\n월간 리포트 작성",
        ],
        "카카오 앱설치": [
            "캠페인 셋업 + 소재 준비",
            "일예산 50만 테스트 시작",
            "학습 확인, 100만 증액",
            "150만 목표 도달",
        ],
        "메타 앱구매": [
            "앱구매 메인 일 50만 확대",
            "신규 기획전 그룹 오픈",
            "크로스채널 소재 테스트",
            "안정화 운영",
        ],
        "구글 앱설치": [
            "일예산 80만 증액",
            "일예산 120만\ntROAS 캠페인 테스트",
            "일예산 150만",
            "안정화",
        ],
    })
    st.dataframe(roadmap, use_container_width=True, hide_index=True)

    # ─── 갭 해소 시뮬레이션 ───
    st.markdown("### 5. 4월 말 예상 지표 (갭 해소 시)")

    sim_df = pd.DataFrame({
        "항목": ["카카오 PBTD UA 일예산", "카카오 앱설치 일예산", "메타 앱구매 일예산", "구글 앱설치 일예산",
                 "카카오 RT 보정 ROAS", "카카오 UA 보정 ROAS", "메타 Raw ROAS", "구글 Raw ROAS",
                 "예상 일 전환수", "예상 월 매출 증분"],
        "현재 (14주차)": ["38만", "0", "32만", "53만",
                        "484%", "442%", "367%", "413%",
                        "~150건", "-"],
        "4월 말 목표": ["500만", "150만", "50만", "150만",
                      "500%+", "400%+", "Raw 유지", "Raw 유지",
                      "~500건", "+5~6억"],
        "갭": ["+462만", "+150만", "+18만", "+97만",
              "-16%p (미달)", "+42%p (달성)", "-", "-",
              "+350건", "-"],
    })
    st.dataframe(sim_df, use_container_width=True, hide_index=True)

    st.markdown("""
    > **핵심 메시지**:
    > - **카카오 RT**: 보정 ROAS 484%로 목표 500% **미달 (-16%p)** → 비효율 그룹 CPC 관리가 급선무
    > - **카카오 UA**: 보정 ROAS 442%로 목표 400% 달성 중이나, **볼륨이 일 38만으로 크게 부족** → 500만까지 단계적 확장
    > - **메타·구글**: 보정 없이 Raw ROAS 기준 운영, 학습 안정화 후 확장
    """)


# ═══════════════════════════════════════════════════════════════
# TAB 1: 전체 현황
# ═══════════════════════════════════════════════════════════════
with tab_overview:
    st.markdown('<div class="section-header"><h3>채널별 UA 성과 요약 (3/9~4/6)</h3></div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card metric-red"><h3>카카오 RT (보정)</h3><h1>497%</h1><h3>목표 500% | 비용 1.13억</h3></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card metric-green"><h3>카카오 UA (보정)</h3><h1>487%</h1><h3>목표 400% | 비용 2.10억</h3></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><h3>메타 앱구매 (Raw)</h3><h1>341%</h1><h3>보정 없음 | 비용 0.08억</h3></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><h3>구글 앱설치 (Raw)</h3><h1>388%</h1><h3>보정 없음 | 비용 0.06억</h3></div>', unsafe_allow_html=True)

    channel_df = pd.DataFrame({
        "채널": ["카카오 RT\n(보정)", "카카오 UA\n(보정)", "메타 앱구매\n(Raw)", "구글 앱설치\n(Raw)"],
        "비용(만)": [11290, 21019, 790, 636],
        "매출(만)": [31900, 58843, 2691, 2471],
        "ROAS(%)": [497, 487, 341, 388],
        "ROAS 유형": ["보정", "보정", "Raw", "Raw"],
        "전환수": [5753, 17785, 401, 470],
    })

    col_l, col_r = st.columns(2)
    with col_l:
        fig_ch = go.Figure()
        fig_ch.add_trace(go.Bar(x=channel_df["채널"], y=channel_df["비용(만)"], name="비용", marker_color="#ef4444"))
        fig_ch.add_trace(go.Bar(x=channel_df["채널"], y=channel_df["매출(만)"], name="매출", marker_color="#22c55e"))
        fig_ch.update_layout(title="채널별 비용 vs 매출 (4주)", height=380, template="plotly_dark", barmode="group",
                             yaxis_title="만원", legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(fig_ch, use_container_width=True)

    with col_r:
        fig_roas = go.Figure()
        colors = ["#ef4444", "#22c55e", "#a855f7", "#eab308"]
        fig_roas.add_trace(go.Bar(x=channel_df["채널"], y=channel_df["ROAS(%)"],
                                  marker_color=colors, text=channel_df["ROAS(%)"].apply(lambda x: f"{x}%"),
                                  textposition="outside"))
        fig_roas.update_layout(title="채널별 ROAS (카카오=보정, 메타·구글=Raw)", height=380, template="plotly_dark",
                               yaxis_title="ROAS (%)")
        st.plotly_chart(fig_roas, use_container_width=True)

    st.markdown('<div class="section-header"><h3>UA 확장 예산 배분안 (일예산 기준)</h3></div>', unsafe_allow_html=True)
    budget_all = pd.DataFrame({
        "채널": ["카카오 UA (웹)", "카카오 앱설치-다운", "메타 앱설치-구매", "구글 앱설치-구매"],
        "일예산": ["350만", "150만", "확장 예정 (별도)", "50만→150만 (별도)"],
        "캠페인 유형": ["PBTD UA 기획전 중심", "앱설치 + 인앱구매 최적화", "앱설치-구매 (콘텐츠)", "앱 캠페인 Purchase 최적화"],
        "예상 ROAS": ["보정 420~500%", "보정 400~450%", "Raw 340%+", "Raw 390%+"],
        "비고": ["기존 유지 + 신규 5개 그룹", "신규 캠페인 셋업 필요", "기존 확장 + 소재 다양화", "예산 증액 + 소재 다양화"],
    })
    st.dataframe(budget_all, use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════
# TAB 2: 카카오 (UA + 앱설치)
# ═══════════════════════════════════════════════════════════════
with tab_kakao:
    st.markdown('<div class="channel-kakao"><h3>카카오 UA 확장 + 앱설치-다운 캠페인</h3></div>', unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown('<div class="metric-card"><h3>RT 비용 (4주)</h3><h1>1.13억</h1></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h3>RT 보정 ROAS</h3><h1>497%</h1></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><h3>기존 UA 비용</h3><h1>2.10억</h1></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><h3>기존 UA 보정 ROAS</h3><h1>487%</h1></div>', unsafe_allow_html=True)
    with col5:
        st.markdown('<div class="metric-card"><h3>PBTD UA 보정 ROAS</h3><h1>462%</h1></div>', unsafe_allow_html=True)

    weekly_data = pd.DataFrame({
        "주차": ["11주차 (3/9~)", "12주차 (3/16~)", "13주차 (3/23~)", "14주차 (3/30~)"],
        "RT ROAS(보정)": [4.40, 4.65, 5.33, 4.73],
        "UA ROAS(보정)": [5.02, 5.03, 4.88, 4.68],
    })
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=weekly_data["주차"], y=weekly_data["RT ROAS(보정)"],
        name="RT 보정 ROAS", mode="lines+markers+text",
        text=[f"{v*100:.0f}%" for v in weekly_data["RT ROAS(보정)"]],
        textposition="top center", line=dict(color="#f59e0b", width=3), marker=dict(size=10)))
    fig_trend.add_trace(go.Scatter(x=weekly_data["주차"], y=weekly_data["UA ROAS(보정)"],
        name="UA 보정 ROAS", mode="lines+markers+text",
        text=[f"{v*100:.0f}%" for v in weekly_data["UA ROAS(보정)"]],
        textposition="bottom center", line=dict(color="#3b82f6", width=3), marker=dict(size=10)))
    fig_trend.add_hline(y=5.0, line_dash="dash", line_color="#ef4444", annotation_text="RT 목표 500%")
    fig_trend.add_hline(y=4.0, line_dash="dash", line_color="#eab308", annotation_text="UA 목표 400%")
    fig_trend.update_layout(title="카카오 주간 보정 ROAS 추이", height=350, template="plotly_dark",
                            legend=dict(orientation="h", y=-0.15))
    st.plotly_chart(fig_trend, use_container_width=True)

    # ═══ 신규 오픈 광고그룹 ═══
    st.markdown('<div class="section-header"><h3>카카오 UA 신규 오픈 광고그룹</h3></div>', unsafe_allow_html=True)
    st.markdown("> **선정 기준**: RT 보정 ROAS 400%+ & 전환 검증됨 & 기존 PBTD UA에 미오픈")

    st.markdown("#### 1순위 - 즉시 오픈 (일예산 250만)")
    tier1 = pd.DataFrame({
        "광고그룹명": [
            "male4069-2601_ct_pgacutterbuck-promotion",
            "male3564-2602_ct_benefit-promotion",
            "male3564-2512_ct_now-promotion",
            "male3064-2602_ct_runningshoes-promotion",
            "male3564-2604_ct_hiking-promotion",
        ],
        "캠페인": ["bizboard / display", "bizboard", "bizboard / display", "bizboard / display", "bizboard"],
        "14주 RT 보정ROAS": ["448% (disp)", "650%", "400%", "515% (disp)", "454%"],
        "14주 전환": [124+95, 59, 103+30, 102+64, 36],
        "CPC": ["294~304원", "327원", "257~370원", "304~457원", "168원"],
        "제안 일예산": ["80만", "50만", "50만", "40만", "30만"],
    })
    st.markdown('<div class="tier-1">', unsafe_allow_html=True)
    st.dataframe(tier1, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("#### 2순위 - 테스트 오픈 (일예산 50만)")
    tier2 = pd.DataFrame({
        "광고그룹명": [
            "male3564-2604_ct_warehouserelease-promotion",
            "male3564-2604_ct_shortsleeve-promotion",
            "male3564-2601_ct_highend-promotion",
        ],
        "캠페인": ["bizboard", "bizboard", "bizboard"],
        "14주 RT 보정ROAS": ["419%", "304%", "319%"],
        "14주 전환": [45, 19, 19],
        "CPC": ["353원", "459원", "390원"],
        "제안 일예산": ["20만", "15만", "15만"],
    })
    st.markdown('<div class="tier-2">', unsafe_allow_html=True)
    st.dataframe(tier2, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("#### 3순위 - 기존 PBTD UA 최적화 (일예산 50만)")
    tier3 = pd.DataFrame({
        "광고그룹명": [
            "male3064-custom_lecaf_selection-promotion",
            "male3064-custom_ct_highbrand-promotion",
            "male3064-custom_ct_athleredition-promotion",
        ],
        "캠페인": [
            "bizboard_da_pr_pbtd-ua-purchase",
            "bizboard_da_pr_pbtd-ua-purchase",
            "bizboard_da_pr_pbtd-ua-purchase",
        ],
        "14주 보정ROAS": ["502%", "785% (4주)", "277%"],
        "14주 전환": [183, 7, 2],
        "CPC": ["222원", "133원", "153원"],
        "액션": [
            "예산 확대 → 일 30만",
            "예산 확대 → 일 10만 (볼륨 테스트)",
            "소재 리프레시 → 일 10만 유지",
        ],
    })
    st.markdown('<div class="tier-3">', unsafe_allow_html=True)
    st.dataframe(tier3, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ═══ 앱설치 ═══
    st.markdown('<div class="section-header"><h3>카카오 앱설치-다운 캠페인 (신규 셋업)</h3></div>', unsafe_allow_html=True)
    st.markdown('<div class="tier-new">', unsafe_allow_html=True)
    st.markdown("""
    **현재 상태**: 카카오에 앱설치 캠페인 없음 → **신규 생성 필요**

    | 항목 | 설정값 |
    |------|--------|
    | **캠페인명 (제안)** | `bizboard_da_pr_pbtd-ua-appinstall-purchase` |
    | **게재 지면** | Bizboard + Display (별도 캠페인) |
    | **일예산** | 150만 (Bizboard 100만 + Display 50만) |
    | **타겟** | 남성 30~64세, 앱 미설치자 |

    | 우선순위 | 광고그룹명 (제안) | 참조 RT 광고그룹 |
    |---------|-----------------|----------------|
    | 1 | `male3064-appinstall_ct_pgacutterbuck-promotion` | RT 전환 965건, ROAS 477% |
    | 2 | `male3064-appinstall_lecaf_selection-promotion` | RT ROAS 653%, UA 검증 |
    | 3 | `male3064-appinstall_ct_benefit-promotion` | RT ROAS 557% |
    | 4 | `male3064-appinstall_ct_now-promotion` | RT 전환 509건 |
    | 5 | `male3064-appinstall_ct_runningshoes-promotion` | 시즌 수요 + RT 439건 |
    """)
    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# TAB 3: 메타
# ═══════════════════════════════════════════════════════════════
with tab_meta:
    st.markdown('<div class="channel-meta"><h3>메타 앱설치-구매 캠페인 (보정 없음, Raw ROAS)</h3></div>', unsafe_allow_html=True)
    st.markdown("> **대상 캠페인**: `facebook_da_pr-ua-apppurchase-android-main` 만 | 카탈로그 제외")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><h3>비용 (4주)</h3><h1>790만</h1></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h3>Raw ROAS</h3><h1>341%</h1></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><h3>전환</h3><h1>401건</h1></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><h3>CPC</h3><h1>415원</h1></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header"><h3>캠페인 성과</h3></div>', unsafe_allow_html=True)
    meta_camp = pd.DataFrame({
        "캠페인": ["facebook_da_pr-ua-apppurchase-android-main"],
        "광고그룹명": ["male3064-apppurchase_contents-promotion-main"],
        "비용": ["790만"],
        "전환": [401],
        "Raw ROAS": ["341%"],
        "CPC": ["415원"],
        "상태": ["운영 중"],
    })
    st.dataframe(meta_camp, use_container_width=True, hide_index=True)

    # 주간 추이
    st.markdown('<div class="section-header"><h3>주간 Raw ROAS 추이</h3></div>', unsafe_allow_html=True)
    meta_weekly = pd.DataFrame({
        "주차": ["11주차 (3/9~)", "12주차 (3/16~)", "13주차 (3/23~)", "14주차 (3/30~)"],
        "비용(만)": [129, 198, 214, 221],
        "전환": [70, 110, 92, 108],
        "Raw ROAS(%)": [336, 385, 272, 354],
    })
    fig_meta = go.Figure()
    fig_meta.add_trace(go.Bar(x=meta_weekly["주차"], y=meta_weekly["비용(만)"], name="비용(만)", marker_color="#a855f7"))
    fig_meta.add_trace(go.Scatter(x=meta_weekly["주차"], y=meta_weekly["Raw ROAS(%)"],
        name="Raw ROAS(%)", yaxis="y2", mode="lines+markers+text",
        text=[f"{v}%" for v in meta_weekly["Raw ROAS(%)"]], textposition="top center",
        line=dict(color="#eab308", width=3), marker=dict(size=12)))
    fig_meta.update_layout(title="메타 앱구매 주간 추이 (Raw ROAS)", height=380, template="plotly_dark",
        yaxis=dict(title="비용 (만원)"), yaxis2=dict(title="Raw ROAS (%)", overlaying="y", side="right"),
        legend=dict(orientation="h", y=-0.15))
    st.plotly_chart(fig_meta, use_container_width=True)

    st.markdown("""
    #### 확장 방향
    | 액션 | 상세 |
    |------|------|
    | **예산 확대** | 일 30만 → 50만, 앱구매 직접 최적화 |
    | **소재 다양화** | 카카오 검증 기획전 소재 크로스채널 활용 |
    | **신규 광고그룹** | pgacutterbuck, benefit 등 기획전 기반 그룹 추가 |

    **참고**: 보정계수 미적용 (Raw ROAS 기준 운영)
    """)


# ═══════════════════════════════════════════════════════════════
# TAB 4: 구글
# ═══════════════════════════════════════════════════════════════
with tab_google:
    st.markdown('<div class="channel-google"><h3>구글 앱설치-구매 캠페인 (보정 없음, Raw ROAS)</h3></div>', unsafe_allow_html=True)
    st.markdown("> **대상 캠페인**: `App promotion-AppInstall-ua-Purchase` 만")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><h3>비용 (2주)</h3><h1>636만</h1></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h3>Raw ROAS</h3><h1>388%</h1></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><h3>전환</h3><h1>470건</h1></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><h3>CPC</h3><h1>421원</h1></div>', unsafe_allow_html=True)

    google_camp = pd.DataFrame({
        "캠페인": ["App promotion-AppInstall-ua-Purchase"],
        "광고그룹명": ["Ad group 20260206 pre-contents-purchase"],
        "비용": ["636만"],
        "전환": [470],
        "Raw ROAS": ["388%"],
        "CPC": ["421원"],
        "상태": ["운영 중 (3/26~)"],
    })
    st.dataframe(google_camp, use_container_width=True, hide_index=True)

    google_weekly = pd.DataFrame({
        "주차": ["13주차 (3/23~)", "14주차 (3/30~)"],
        "비용(만)": [217, 386],
        "전환": [148, 285],
        "Raw ROAS(%)": [324, 413],
    })
    fig_gw = go.Figure()
    fig_gw.add_trace(go.Bar(x=google_weekly["주차"], y=google_weekly["비용(만)"], name="비용(만)", marker_color="#22c55e"))
    fig_gw.add_trace(go.Scatter(x=google_weekly["주차"], y=google_weekly["Raw ROAS(%)"],
        name="Raw ROAS(%)", yaxis="y2", mode="lines+markers+text",
        text=[f"{v}%" for v in google_weekly["Raw ROAS(%)"]], textposition="top center",
        line=dict(color="#eab308", width=3), marker=dict(size=12)))
    fig_gw.update_layout(title="구글 앱설치 주간 추이 (Raw ROAS)", height=380, template="plotly_dark",
        yaxis=dict(title="비용 (만원)"), yaxis2=dict(title="Raw ROAS (%)", overlaying="y", side="right"),
        legend=dict(orientation="h", y=-0.15))
    st.plotly_chart(fig_gw, use_container_width=True)

    st.markdown("""
    #### 확장 계획
    | 단계 | 기간 | 일예산 | 목표 |
    |------|------|--------|------|
    | **현재** | 3/26~ (2주차) | ~46만 | 학습 안정화 |
    | **1단계** | 4월 2주차 | 80만 | Raw ROAS 유지 + 볼륨 확대 |
    | **2단계** | 4월 3주차 | 120만 | 전환수 일 40건+ |
    | **3단계** | 4월 4주차~ | 150만 | tROAS 캠페인 테스트 |

    **참고**: 보정계수 미적용 (Raw ROAS 기준 운영) | 예산 20~30%씩 점진 증액
    """)

st.markdown("---")
st.caption("마지막 업데이트: 2026-04-07 | 데이터 출처: Redash DATA_DB marketing_cost")
