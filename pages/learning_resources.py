"""
pages/learning_resources.py
---------------------------
Learning Resources — Browse all learning platforms and YouTube channels
with tag/category filters.
"""

import streamlit as st
from utils.data_loader import load_platforms, load_youtube_channels
from utils.filters import apply_all_filters
from components.section_header import section_header
from components.tag_filter import tag_filter, keyword_search_bar


def _platform_card(item: dict) -> None:
    with st.container(border=True):
        col1, col2 = st.columns([0.82, 0.18])
        with col1:
            st.markdown(f"**[{item['name']}]({item['url']})**")
        with col2:
            st.caption(item.get("type", "Platform"))
        if item.get("description"):
            st.caption(item["description"])
        tags = item.get("tags", [])
        if tags:
            st.markdown(" ".join(f"`{t}`" for t in tags))


def show() -> None:
    section_header("Learning Resources", "Discover platforms and channels for every skill and subject.", "📖")

    platforms = load_platforms()
    channels  = load_youtube_channels()

    tabs = st.tabs([
        "🌐 All Platforms",
        "🎓 Academic",
        "💻 Programming / CS",
        "☁️ Cloud / DevOps",
        "🤖 AI / Data",
        "🎨 Design / Creative",
        "📣 Marketing",
        "🔒 Security",
        "▶️ YouTube Channels",
    ])

    def show_items(items, key_prefix):
        keyword = keyword_search_bar(key=f"{key_prefix}_kw", placeholder="Search…")
        selected_tags, selected_types = tag_filter(key_prefix=key_prefix)
        filtered = apply_all_filters(items, keyword=keyword, selected_tags=selected_tags, selected_types=selected_types)
        st.caption(f"{len(filtered)} result(s)")
        for item in filtered:
            _platform_card(item)

    with tabs[0]:
        show_items(platforms, "lr_all")

    with tabs[1]:
        academic = [p for p in platforms if "academic" in p.get("category","").lower()]
        show_items(academic, "lr_acad")

    with tabs[2]:
        prog = [p for p in platforms if "programming" in p.get("category","").lower() or "coding" in p.get("category","").lower()]
        show_items(prog, "lr_prog")

    with tabs[3]:
        cloud = [p for p in platforms if "cloud" in p.get("category","").lower()]
        show_items(cloud, "lr_cloud")

    with tabs[4]:
        ai = [p for p in platforms if "ai" in p.get("category","").lower() or "data" in p.get("category","").lower()]
        show_items(ai, "lr_ai")

    with tabs[5]:
        design = [p for p in platforms if "design" in p.get("category","").lower() or "creative" in p.get("category","").lower()]
        show_items(design, "lr_design")

    with tabs[6]:
        mkt = [p for p in platforms if "marketing" in p.get("category","").lower() or "business" in p.get("category","").lower()]
        show_items(mkt, "lr_mkt")

    with tabs[7]:
        sec = [p for p in platforms if "security" in p.get("category","").lower() or "cyber" in p.get("category","").lower()]
        show_items(sec, "lr_sec")

    with tabs[8]:
        yt_cats = sorted({c.get("category","") for c in channels})
        sel_cat = st.selectbox("Category", ["All"] + yt_cats, key="yt_cat_sel")
        filtered_ch = channels if sel_cat == "All" else [c for c in channels if c.get("category") == sel_cat]
        kw_yt = keyword_search_bar(key="yt_kw", placeholder="Search channels…")
        if kw_yt:
            kw = kw_yt.lower()
            filtered_ch = [c for c in filtered_ch if kw in c.get("name","").lower() or kw in c.get("description","").lower()]
        st.caption(f"{len(filtered_ch)} channel(s)")
        for ch in filtered_ch:
            _platform_card(ch)
