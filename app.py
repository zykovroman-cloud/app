import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as pio
from datetime import datetime, timedelta

# ============================
# GLOBAL STYLE / THEME
# ============================

PALETTE = [
    "#2E86DE",  # blue
    "#E74C3C",  # red
    "#F1C40F",  # yellow
    "#27AE60",  # green
    "#9B59B6",  # purple
    "#E67E22",  # orange
    "#16A085",  # teal
    "#34495E",  # dark gray
]


THEMES = {
    "Светлая": "plotly_white",
    "Тёмная": "plotly_dark",
}

# ============================
# STREAMLIT UI THEMES
# ============================
STREAMLIT_UI = {
    "Светлая": {
        "bg": "#FFFFFF",
        "fg": "#111827",
        "card": "#F8FAFC",
        "border": "rgba(17,24,39,0.12)",
        "sidebar": "#F3F4F6",
    },
    "Тёмная": {
        "bg": "#0E1117",
        "fg": "#E5E7EB",
        "card": "#111827",
        "border": "rgba(229,231,235,0.14)",
        "sidebar": "#0B1220",
    },
}

def apply_ui_theme(theme_choice: str) -> None:
    """Apply Plotly template + lightweight Streamlit UI CSS theme."""
    tpl = THEMES.get(theme_choice, "plotly_white")
    px.defaults.template = tpl
    px.defaults.color_discrete_sequence = PALETTE
    pio.templates.default = tpl

    ui = STREAMLIT_UI.get(theme_choice, STREAMLIT_UI["Светлая"])

    st.markdown(
        f"""
<style>
/* Page */
.stApp {{
  background: {ui['bg']};
  color: {ui['fg']};
}}

/* Sidebar */
section[data-testid="stSidebar"] > div {{
  background: {ui['sidebar']};
}}

/* Containers / cards */
div[data-testid="stVerticalBlockBorderWrapper"] {{
  border-color: {ui['border']} !important;
  background: {ui['card']} !important;
}}

/* Metric cards */
div[data-testid="stMetric"] {{
  background: {ui['card']};
  border: 1px solid {ui['border']};
  border-radius: 12px;
  padding: 10px 12px;
}}

/* Tables */
div[data-testid="stDataFrame"] {{
  border: 1px solid {ui['border']};
  border-radius: 12px;
  overflow: hidden;
}}

</style>
        """,
        unsafe_allow_html=True,
    )

# ============================
# BADGES (priority / status)
# ============================

PRIO_STYLE = {
    "P1 (Critical)": "background-color:#E74C3C;color:white;font-weight:700;padding:2px 10px;border-radius:999px;",
    "P2 (High)"    : "background-color:#E67E22;color:white;font-weight:700;padding:2px 10px;border-radius:999px;",
    "P3 (Medium)"  : "background-color:#F1C40F;color:#111;font-weight:700;padding:2px 10px;border-radius:999px;",
    "P4 (Low)"     : "background-color:#27AE60;color:white;font-weight:700;padding:2px 10px;border-radius:999px;",
}

STATUS_STYLE = {
    "Open": "background-color:#E74C3C;color:white;font-weight:700;padding:2px 10px;border-radius:999px;",
    "In progress": "background-color:#2E86DE;color:white;font-weight:700;padding:2px 10px;border-radius:999px;",
    "Done": "background-color:#27AE60;color:white;font-weight:700;padding:2px 10px;border-radius:999px;",
    "Blocked": "background-color:#9B59B6;color:white;font-weight:700;padding:2px 10px;border-radius:999px;",
    "Mitigated": "background-color:#34495E;color:white;font-weight:700;padding:2px 10px;border-radius:999px;",
    "Submitted": "background-color:#2E86DE;color:white;font-weight:700;padding:2px 10px;border-radius:999px;",
    "Draft": "background-color:#F1C40F;color:#111;font-weight:700;padding:2px 10px;border-radius:999px;",
    "Yes": "background-color:#27AE60;color:white;font-weight:700;padding:2px 10px;border-radius:999px;",
    "No": "background-color:#E74C3C;color:white;font-weight:700;padding:2px 10px;border-radius:999px;",
    "Partially": "background-color:#E67E22;color:white;font-weight:700;padding:2px 10px;border-radius:999px;",
}

def styled_df(df: pd.DataFrame):
    sty = df.style
    if "priority" in df.columns:
        sty = sty.map(lambda v: PRIO_STYLE.get(v, ""), subset=["priority"])
    if "status" in df.columns:
        sty = sty.map(lambda v: STATUS_STYLE.get(v, ""), subset=["status"])
    return sty

def donut(df, names, values, title):
    fig = px.pie(df, names=names, values=values, hole=0.55, title=title)
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(legend_title_text="", template=px.defaults.template)
    return fig

def section(title, icon=""):
    box = st.container(border=True)
    with box:
        st.markdown(f"### {icon} {title}")
    return box
st.set_page_config(
    page_title="ПКС — демо",
    page_icon="🛡️",
    layout="wide",
)

st.sidebar.title("ПКС — DEMO")

theme_choice = st.sidebar.selectbox("Тема интерфейса", list(THEMES.keys()))
apply_ui_theme(theme_choice)

snapshot = st.sidebar.selectbox(
    "Снимок инфраструктуры",
    ["Текущий", "7 дней назад", "30 дней назад"]
)

page = st.sidebar.radio(
    "Раздел",
    [
        "Главная",
        "Активы",
        "Уязвимости",
        "Риски",
        "Compliance",
        "Меры и задачи",
        "Каталоги",
        "Интеграции",
        "LLM / RAG объяснение",
    ]
)

st.sidebar.caption("Демо-режим: все данные синтетические.")
def seed_data():
    assets = pd.DataFrame([
        {"asset_id": "srv-ad-01", "type": "AD DC", "zone": "T0", "criticality": 5, "owner": "IT"},
        {"asset_id": "srv-db-01", "type": "DB", "zone": "T1", "criticality": 5, "owner": "Product"},
        {"asset_id": "srv-app-01", "type": "App", "zone": "T1", "criticality": 4, "owner": "Product"},
        {"asset_id": "gw-vpn-01", "type": "VPN", "zone": "Edge", "criticality": 5, "owner": "NetSec"},
        {"asset_id": "srv-git-01", "type": "CI/CD", "zone": "T2", "criticality": 4, "owner": "DevOps"},
    ])

    vulns = pd.DataFrame([
        {"cve": "CVE-2024-1111", "asset_id": "gw-vpn-01", "cvss": 9.4, "vector": "Network", "status": "Open"},
        {"cve": "CVE-2023-2222", "asset_id": "srv-db-01", "cvss": 8.7, "vector": "Internal", "status": "Open"},
        {"cve": "CVE-2022-3333", "asset_id": "srv-app-01", "cvss": 7.2, "vector": "Adjacent", "status": "Open"},
        {"cve": "CVE-2021-4444", "asset_id": "srv-ad-01", "cvss": 6.5, "vector": "Internal", "status": "Mitigated"},
    ])

    crit = assets.set_index("asset_id")["criticality"].to_dict()
    reach = {"Network": 1.0, "Adjacent": 0.7, "Internal": 0.5}

    risks = vulns.copy()
    risks["criticality"] = risks["asset_id"].map(crit)
    risks["reach"] = risks["vector"].map(reach)
    risks["risk_score"] = (risks["cvss"] * risks["criticality"] * risks["reach"]).round(1)

    def prio(x):
        if x >= 30: return "P1 (Critical)"
        if x >= 20: return "P2 (High)"
        if x >= 12: return "P3 (Medium)"
        return "P4 (Low)"

    risks["priority"] = risks["risk_score"].apply(prio)
    risks["loss_max"] = risks["risk_score"].apply(lambda x: 120 if x > 30 else 40 if x > 20 else 10)

    days = 30
    idx = pd.DataFrame({
        "date": [datetime.now().date() - timedelta(days=i) for i in range(days)][::-1],
        "risk_index": np.linspace(65, 48, days) + np.random.normal(0, 1.5, days)
    })

    return assets, vulns, risks.sort_values("risk_score", ascending=False), idx

assets, vulns, risks, risk_index = seed_data()
if page == "Главная":
    st.title("🛡️ ПКС — обзор рисков")

    open_v = (vulns["status"] == "Open").sum()
    p1 = (risks["priority"] == "P1 (Critical)").sum()
    p2 = (risks["priority"] == "P2 (High)").sum()
    loss = risks.loc[risks["status"] == "Open", "loss_max"].sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Открытые уязвимости", open_v, delta=-1)
    col2.metric("P1 риски", p1, delta=-1)
    col3.metric("P2 риски", p2, delta=0)
    col4.metric("Потенциальный ущерб, млн ₽", loss, delta=-20)

    with section("Индекс киберриска", "📈"):
        fig = px.line(risk_index, x="date", y="risk_index", markers=True)
        fig.update_traces(line=dict(width=3))
        st.plotly_chart(fig, width="stretch")

    with section("ТОП-риски", "🔥"):
        st.dataframe(styled_df(risks.head(5)), width="stretch")

    with section("Распределение", "🍩"):
        c1, c2 = st.columns(2)
        c1.plotly_chart(
            donut(risks.groupby("priority").size().reset_index(name="count"),
                  "priority", "count", "Приоритеты рисков"),
            width="stretch"
        )
        c2.plotly_chart(
            donut(vulns.groupby("status").size().reset_index(name="count"),
                  "status", "count", "Статусы уязвимостей"),
            width="stretch"
        )
elif page == "Активы":
    st.title("🧩 Активы (демо)")

    with section("Реестр активов", "🗂️"):
        st.dataframe(assets, width="stretch")

    with section("Срез по зонам", "📊"):
        zone_counts = assets.groupby("zone").size().reset_index(name="count")
        st.plotly_chart(px.bar(zone_counts, x="zone", y="count", title="Активы по зонам"), width="stretch")

        # Donut по зонам
        st.plotly_chart(donut(zone_counts, "zone", "count", "Распределение активов по зонам"), width="stretch")


elif page == "Уязвимости":
    st.title("🧨 Уязвимости (демо CAG)")

    with section("Фильтры", "🎛️"):
        c1, c2, c3 = st.columns(3)
        asset_filter = c1.selectbox("Актив", ["(все)"] + sorted(vulns["asset_id"].unique().tolist()))
        status_filter = c2.selectbox("Статус", ["(все)"] + sorted(vulns["status"].unique().tolist()))
        min_cvss = c3.slider("Минимальный CVSS", 0.0, 10.0, 7.0, 0.1)

    df = vulns.copy()
    if asset_filter != "(все)":
        df = df[df["asset_id"] == asset_filter]
    if status_filter != "(все)":
        df = df[df["status"] == status_filter]
    df = df[df["cvss"] >= min_cvss]

    with section("Список уязвимостей", "📋"):
        st.dataframe(styled_df(df.sort_values("cvss", ascending=False)), width="stretch")

    with section("Визуализация", "📈"):
        # Histogram CVSS
        st.plotly_chart(px.histogram(vulns, x="cvss", nbins=10, title="Распределение CVSS"), width="stretch")

        # Donut по вектору
        vec = vulns.groupby("vector").size().reset_index(name="count")
        st.plotly_chart(donut(vec, "vector", "count", "Вектор атаки (Network / Internal / Adjacent)"), width="stretch")


elif page == "Риски":
    st.title("📌 Риски и потенциальный ущерб (демо)")

    with section("Риск-реестр", "🧾"):
        view = risks[["priority","asset_id","cve","cvss","vector","criticality","risk_score","loss_max","status"]]
        st.dataframe(styled_df(view), width="stretch")

    with section("Карта риска", "🗺️"):
        fig = px.scatter(
            risks,
            x="risk_score",
            y="loss_max",
            hover_data=["asset_id","cve","priority","cvss","vector"],
            title="Риск-скор vs Потенциальный ущерб"
        )
        st.plotly_chart(fig, width="stretch")

    with section("Приоритеты (donut)", "🍩"):
        prio_counts = risks.groupby("priority").size().reset_index(name="count")
        st.plotly_chart(donut(prio_counts, "priority", "count", "Распределение рисков по приоритетам"), width="stretch")

    with section("Симуляция эффекта мер", "🧪"):
        measure = st.selectbox("Мера", ["Патч/обновление", "Сегментация", "Ограничение доступа", "Hardening CI"])
        factor = {"Патч/обновление": 0.55, "Сегментация": 0.75, "Ограничение доступа": 0.80, "Hardening CI": 0.85}[measure]

        sim = risks.copy()
        sim["risk_score_new"] = (sim["risk_score"] * factor).round(1)
        sim["loss_new"] = (sim["loss_max"] * factor).round(1)

        cA, cB = st.columns(2)
        cA.metric("Ущерб ДО, млн ₽", f"{risks.loc[risks['status']=='Open','loss_max'].sum():.0f}")
        cB.metric("Ущерб ПОСЛЕ (демо), млн ₽", f"{sim.loc[sim['status']=='Open','loss_new'].sum():.0f}")

        st.dataframe(
            styled_df(sim[["priority","asset_id","cve","risk_score","risk_score_new","loss_max","loss_new","status"]].head(10)),
            width="stretch"
        )
elif page == "Compliance":
    st.title("✅ Compliance (демо)")

    # --- Мок-данные комплаенса (можно расширять) ---
    reqs = pd.DataFrame([
        {"framework":"ISO 27001", "req_id":"A.5.1", "requirement":"Политики ИБ утверждены и актуальны", "status":"Partially"},
        {"framework":"ISO 27001", "req_id":"A.8.1", "requirement":"Инвентаризация активов ведётся централизованно", "status":"Yes"},
        {"framework":"ISO 27001", "req_id":"A.12.6", "requirement":"Управление тех. уязвимостями", "status":"No"},
        {"framework":"КИИ-профиль", "req_id":"KII-01", "requirement":"Сегментация и изоляция критических зон", "status":"Partially"},
        {"framework":"КИИ-профиль", "req_id":"KII-02", "requirement":"Журналирование и контроль админ-действий", "status":"Yes"},
        {"framework":"Внутр. регламент", "req_id":"REG-07", "requirement":"Управление изменениями (approval/CAB)", "status":"No"},
    ])

    controls = pd.DataFrame([
        {"control_id":"C-01", "control":"Сегментация зон (T0/T1/T2)", "type":"Technical", "owner":"NetSec", "maturity":2},
        {"control_id":"C-02", "control":"Hardening CI/репозитория + секреты", "type":"Technical", "owner":"DevOps", "maturity":1},
        {"control_id":"C-03", "control":"Управление уязвимостями (SLA/patch mgmt)", "type":"Process", "owner":"SecOps", "maturity":1},
        {"control_id":"C-04", "control":"Управление доступами (review/JML)", "type":"Process", "owner":"IT", "maturity":2},
        {"control_id":"C-05", "control":"Контроль обновлений и защиты от отката", "type":"Technical", "owner":"Product", "maturity":1},
    ])

    req_map = pd.DataFrame([
        {"req_id":"A.8.1", "control_id":"C-01"},
        {"req_id":"A.12.6", "control_id":"C-03"},
        {"req_id":"KII-01", "control_id":"C-01"},
        {"req_id":"KII-02", "control_id":"C-04"},
        {"req_id":"REG-07", "control_id":"C-02"},
        {"req_id":"REG-07", "control_id":"C-03"},
    ])

    with section("Профиль/стандарт", "🎯"):
        fw = st.selectbox("Выберите профиль", ["(все)"] + sorted(reqs["framework"].unique().tolist()))
        df_req = reqs if fw == "(все)" else reqs[reqs["framework"] == fw]

    with section("Реестр требований", "📋"):
        st.dataframe(styled_df(df_req), width="stretch")

    with section("Статусы выполнения", "📊"):
        stat = df_req.groupby("status").size().reset_index(name="count")
        c1, c2 = st.columns(2)
        c1.plotly_chart(px.bar(stat, x="status", y="count", title="Статусы требований (bar)"), width="stretch")
        c2.plotly_chart(donut(stat, "status", "count", "Статусы требований (donut)"), width="stretch")

    with section("Требования ↔ меры (controls)", "🔗"):
        merged = (
            req_map.merge(reqs[["req_id","requirement","framework","status"]], on="req_id", how="left")
                  .merge(controls[["control_id","control","owner","maturity","type"]], on="control_id", how="left")
        )
        st.dataframe(styled_df(merged), width="stretch")

    st.info(
        "Демо-логика: комплаенс связан с рисками и бюджетом мер. "
        "Статусы No/Partially → формируют задачи и приоритет инвестиций."
    )


elif page == "Меры и задачи":
    st.title("🧩 Меры (Controls) и задачи — демо")

    # --- Session-state tasks (если ещё не было) ---
    if "tasks" not in st.session_state:
        st.session_state["tasks"] = pd.DataFrame([
            {"task_id":"T-1001","title":"Патч VPN-шлюза","priority":"P1 (Critical)","owner":"NetSec","status":"Open","due":"7 дней","linked":"gw-vpn-01 / CVE-2024-1111"},
            {"task_id":"T-1002","title":"Hardening CI и секреты","priority":"P2 (High)","owner":"DevOps","status":"In progress","due":"14 дней","linked":"srv-git-01 / CVE-2023-2222"},
            {"task_id":"T-1003","title":"Сегментация доступа к БД","priority":"P1 (Critical)","owner":"Product","status":"Open","due":"10 дней","linked":"srv-db-01 / CVE-2023-2222"},
        ])

    controls = pd.DataFrame([
        {"control_id":"C-01", "control":"Сегментация зон (T0/T1/T2)", "type":"Technical", "owner":"NetSec", "maturity":2},
        {"control_id":"C-02", "control":"Hardening CI/репозитория + секреты", "type":"Technical", "owner":"DevOps", "maturity":1},
        {"control_id":"C-03", "control":"Управление уязвимостями (SLA/patch mgmt)", "type":"Process", "owner":"SecOps", "maturity":1},
        {"control_id":"C-04", "control":"Управление доступами (review/JML)", "type":"Process", "owner":"IT", "maturity":2},
        {"control_id":"C-05", "control":"Контроль обновлений и защиты от отката", "type":"Technical", "owner":"Product", "maturity":1},
    ])

    with section("Реестр мер", "🧱"):
        st.dataframe(controls, width="stretch")

    with section("Задачи (Task manager)", "✅"):
        st.dataframe(styled_df(st.session_state["tasks"]), width="stretch")

    with section("Создать демо-задачу", "➕"):
        with st.form("new_task_form"):
            title = st.text_input("Название", "Проверка конфигурации обновлений")
            pr = st.selectbox("Приоритет", ["P1 (Critical)", "P2 (High)", "P3 (Medium)", "P4 (Low)"])
            owner = st.selectbox("Ответственный", ["IT","SecOps","NetSec","DevOps","Product"])
            due = st.selectbox("Срок", ["3 дня","7 дней","14 дней","30 дней"])
            linked = st.text_input("Связь (актив/риск)", "srv-app-01 / CVE-2022-3333")
            submitted = st.form_submit_button("Создать")

        if submitted:
            new_id = f"T-{1000 + len(st.session_state['tasks']) + 1}"
            st.session_state["tasks"] = pd.concat(
                [
                    st.session_state["tasks"],
                    pd.DataFrame([{
                        "task_id": new_id,
                        "title": title,
                        "priority": pr,
                        "owner": owner,
                        "status": "Open",
                        "due": due,
                        "linked": linked
                    }])
                ],
                ignore_index=True
            )
            st.success("Задача создана (демо). В боевой версии: выгрузка в Jira/Service Desk и контроль SLA.")

    with section("Workflow: смена статуса", "🔁"):
        tid = st.selectbox("Задача", st.session_state["tasks"]["task_id"].tolist())
        new_status = st.selectbox("Новый статус", ["Open","In progress","Done","Blocked"])
        if st.button("Применить"):
            tdf = st.session_state["tasks"].copy()
            tdf.loc[tdf["task_id"] == tid, "status"] = new_status
            st.session_state["tasks"] = tdf
            st.success("Статус обновлён (демо).")
elif page == "Каталоги":
    st.title("📚 Каталоги (демо)")

    with section("MITRE ATT&CK (витрина)", "🧠"):
        mitre = pd.DataFrame([
            {"technique":"T1190", "name":"Exploit Public-Facing Application", "coverage":"Partially", "note":"Есть контроль WAF/patching, но нет SLA и инвентаря версий"},
            {"technique":"T1566", "name":"Phishing", "coverage":"No", "note":"Нужна платформа контрфишинга, обучение, симуляции"},
            {"technique":"T1078", "name":"Valid Accounts", "coverage":"Partially", "note":"Нужен JML, review доступов, MFA, контроль привилегий"},
            {"technique":"T1486", "name":"Data Encrypted for Impact", "coverage":"Partially", "note":"Нужно резервирование, сегментация, EDR, IR-процедуры"},
        ])
        # Переиспользуем status-style через колонку status (для бейджей)
        mitre_view = mitre.rename(columns={"coverage": "status"})
        st.dataframe(styled_df(mitre_view), width="stretch")

    with section("БДУ/уязвимости (витрина)", "🧾"):
        bdu = pd.DataFrame([
            {"bdu_id":"BDU:2024-001", "vendor":"VendorX", "product":"VPN Gateway", "severity":"Critical", "mapped_cve":"CVE-2024-1111"},
            {"bdu_id":"BDU:2023-014", "vendor":"VendorY", "product":"DB Engine", "severity":"High", "mapped_cve":"CVE-2023-2222"},
            {"bdu_id":"BDU:2022-207", "vendor":"VendorZ", "product":"App Server", "severity":"Medium", "mapped_cve":"CVE-2022-3333"},
        ])
        st.dataframe(bdu, width="stretch")

    with section("Связка: каталоги → риски → меры", "🔗"):
        st.markdown(
            "- В боевой версии сюда подключаются: **CVE/NVD**, **БДУ/ФСТЭК**, vendor advisories.\n"
            "- Затем нормализация (CAG), сопоставление с активами и расчёт **ущерба/риска**.\n"
            "- На выходе: рекомендации по мерам + задачи в ITSM/Jira с SLA."
        )


elif page == "Интеграции":
    st.title("🔌 Интеграции (демо)")

    integrations = pd.DataFrame([
        {"integration":"AD/LDAP", "status":"Done", "details":"Импорт пользователей/групп, привязка к зонам"},
        {"integration":"CMDB/Invent", "status":"In progress", "details":"Импорт активов и критичности"},
        {"integration":"Scanner (Nessus/OpenVAS)", "status":"Draft", "details":"Подтягивание результатов сканирования"},
        {"integration":"SIEM (Wazuh)", "status":"In progress", "details":"События, алерты, правила, юзкейсы"},
        {"integration":"EDR", "status":"No", "details":"Планируется, зависит от выбора вендора"},
        {"integration":"ITSM (Jira/SD)", "status":"Partially", "details":"Создание задач/инцидентов, SLA"},
        {"integration":"Repo/CI (Git)", "status":"Partially", "details":"Проверка секретов, SBOM, пайплайны"},
    ])

    with section("Матрица готовности", "🧩"):
        st.dataframe(styled_df(integrations), width="stretch")

    with section("Статусы интеграций (donut)", "🍩"):
        stat = integrations.groupby("status").size().reset_index(name="count")
        c1, c2 = st.columns(2)
        c1.plotly_chart(px.bar(stat, x="status", y="count", title="Статусы (bar)"), width="stretch")
        c2.plotly_chart(donut(stat, "status", "count", "Статусы (donut)"), width="stretch")

    with section("Что происходит при разворачивании в контуре (демо)", "🏗️"):
        st.markdown(
            "**Авто-сбор (bootstrap) в контуре заказчика:**\n"
            "1) Подключение к источникам: AD/CMDB/сканер/агенты.\n"
            "2) Сбор активов, версий ПО, ролей, зон, владельцев.\n"
            "3) Нормализация данных и построение графа зависимостей.\n"
            "4) Сопоставление с CAG (CVE/БДУ) и расчёт риска.\n"
            "5) Публикация на дашборде + генерация задач/мер.\n"
        )


elif page == "LLM / RAG объяснение":
    st.title("🤖 LLM + RAG (демо-концепт)")

    with section("Зачем LLM здесь", "🧠"):
        st.markdown(
            "- **Пояснение риска** на языке ЛПР: “что случится”, “сколько стоит”, “что делать первым”.\n"
            "- **Авто-генерация мер/задач** по типовым паттернам (hardening, segmentation, patch SLA).\n"
            "- **Q&A по инфраструктуре**: ответы на вопросы по активам/рискам/мероприятиям.\n"
        )

    with section("Как не “ломать RAG” при изменениях инфраструктуры", "🧱"):
        st.markdown(
            "**Ключевая идея:** RAG не должен хранить “снимок инфраструктуры” как статичный текст.\n\n"
            "✅ Делай **двухконтурную модель знаний:**\n"
            "1) **CAG (статическая база знаний)**: CVE/БДУ/ATT&CK, типовые конфиги, стандарты (ISO/КИИ-профиль), playbooks.\n"
            "2) **Dynamic Context (динамический контекст)**: активы/версии/топология/события берутся из коннекторов и БД *на запрос*.\n\n"
            "То есть при изменениях в инфраструктуре — обновляются **данные/граф/индексы**, а не “переписывается RAG-архив”."
        )

    with section("Пример ответа LLM (демо)", "🗣️"):
        q = st.text_input("Вопрос", "Почему риск по VPN критический и что делать первым?")
        if st.button("Сгенерировать ответ (демо)"):
            st.success(
                "Риск критический, потому что уязвимость имеет высокий CVSS и доступна по сети, "
                "а актив относится к периметру (Edge). Рекомендуемый первый шаг: патч/обновление и проверка конфигурации, "
                "далее — сегментация и ограничение административных доступов. "
                "Ожидаемый эффект: снижение риск-скора ~45–60% и уменьшение потенциального ущерба."
            )

    st.caption("Это демо. В боевой версии: вызов LLM, RAG над CAG, подтягивание динамического контекста из БД/графа.")


else:
    st.title("ПКС — демо")
    st.warning("Раздел не найден. Проверьте значение переменной page в sidebar.")
    st.write("Текущее значение page:", page)