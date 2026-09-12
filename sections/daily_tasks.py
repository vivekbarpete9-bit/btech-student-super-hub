"""
pages/daily_tasks.py
--------------------
Daily Skill Tasks — Pick a task, complete Learn / Practice / Complete steps.
"""

import streamlit as st
from utils.data_loader import load_daily_tasks
from utils.tracker_utils import load_tracker, mark_task_complete, unmark_task
from components.section_header import section_header


def show() -> None:
    section_header("Daily Skill Tasks", "Build skills 30 minutes a day — consistent practice beats cramming.", "📅")

    tasks = load_daily_tasks()
    if not tasks:
        st.error("Could not load daily tasks.")
        return

    tracker_data = load_tracker()
    completed_ids = set(tracker_data.get("completed_tasks", []))

    # ── Stats ──────────────────────────────────────────────────────────────────
    total = len(tasks)
    done  = len([t for t in tasks if t["id"] in completed_ids])
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tasks", total)
    col2.metric("Completed", done)
    col3.metric("Remaining", total - done)

    if done > 0:
        st.progress(done / total)

    st.divider()

    # ── Category filter ────────────────────────────────────────────────────────
    cats = sorted({t.get("category", "General") for t in tasks})
    sel_cat = st.radio("Filter by category", ["All"] + cats, horizontal=True, key="dt_cat")
    show_completed = st.checkbox("Show completed tasks", value=True, key="dt_show_done")

    st.divider()

    # ── Task list ──────────────────────────────────────────────────────────────
    visible = [
        t for t in tasks
        if (sel_cat == "All" or t.get("category") == sel_cat)
        and (show_completed or t["id"] not in completed_ids)
    ]

    if not visible:
        st.info("No tasks to show. Try changing the filter or enabling 'Show completed tasks'.")
        return

    for task in visible:
        tid = task["id"]
        is_done = tid in completed_ids

        with st.container(border=True):
            col1, col2, col3 = st.columns([0.6, 0.25, 0.15])
            with col1:
                status_icon = "✅" if is_done else "⭕"
                st.markdown(f"**{status_icon} {task['title']}**")
                st.caption(f"📂 {task.get('category','')}  |  ⏱️ ~{task.get('estimated_minutes',0)} min  |  🎯 {task.get('difficulty','')}")
            with col2:
                if task.get("resource_url"):
                    st.markdown(f"[📖 Open Resource]({task['resource_url']})")
            with col3:
                if is_done:
                    if st.button("Undo", key=f"undo_{tid}"):
                        unmark_task(tid)
                        st.rerun()
                else:
                    if st.button("Done ✓", key=f"done_{tid}"):
                        mark_task_complete(tid)
                        st.success("🎉 Today's skill-learning task completed!")
                        st.rerun()

            if task.get("description"):
                with st.expander("Details"):
                    st.write(task["description"])
                    # Mini checklist
                    col_l, col_p, col_c = st.columns(3)
                    with col_l:
                        st.checkbox("📖 Learned the concept", key=f"learn_{tid}", disabled=is_done)
                    with col_p:
                        st.checkbox("🔧 Practised it", key=f"prac_{tid}", disabled=is_done)
                    with col_c:
                        st.checkbox("✅ Completed the task", key=f"comp_{tid}", value=is_done, disabled=is_done)

    # ── Celebration when all done ──────────────────────────────────────────────
    all_visible_done = all(t["id"] in completed_ids for t in visible)
    if visible and all_visible_done:
        st.balloons()
        st.success("🎉 All tasks in this category completed! Keep the momentum going!")
