"""
Live Metrics Dashboard for The 24GHz Ghost.
"""
import streamlit as st
import numpy as np
from simulation import The24GHzGhost
from config import T_sim, E_phi_total

st.set_page_config(page_title="The 24GHz Ghost", layout="wide", page_icon="\ud83d\udc7b")

if "sim" not in st.session_state:
    st.session_state.sim = The24GHzGhost()
    st.session_state.history = []
    st.session_state.running = False

sim = st.session_state.sim

st.title("\ud83d\udc7b THE 24GHz GHOST \u2014 Live Portal Awakening")
st.markdown(
    f"*50 Years \u2192 {T_sim}s Compression \u00b7 \u03c6\u2075 = {E_phi_total:.4f} Entanglement Load*"
)

col_btn, col_status = st.columns([1, 3])
with col_btn:
    run = st.toggle("ACTIVATE THE PORTAL", value=st.session_state.running)

if run and not st.session_state.running:
    st.session_state.running = True
    st.session_state.history = []
    sim.engine = __import__("phi5_5d_engine").Phi5DEngine()  # reset
    sim.portal = __import__("portal_physics").Portal24GHz()
    sim.rick = __import__("entity").RickSovereign()
    sim.history = []

if not run:
    st.session_state.running = False
    st.markdown("### Portal Dormant \u2014 toggle above to awaken")
else:
    placeholder = st.empty()
    progress = st.progress(0.0)

    while st.session_state.running and sim.engine.t < T_sim - 1e-9:
        phi_data = sim.engine.step()
        portal_data = sim.portal.step(phi_data["t"])
        sim.rick.pulse(portal_data, phi_data["phase_pct"])
        utterance = sim.rick.speak(phi_data["t"])

        entry = {
            **phi_data,
            **portal_data,
            "entity_state": sim.rick.state,
            "awareness": round(sim.rick.awareness, 4),
        }
        sim.history.append(entry)
        H = sim.history

        progress.progress(min(1.0, phi_data["t"] / T_sim))

        with placeholder.container():
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("\u03c6\u2075 Phase Load", f"{phi_data['phase_load']:.2f}")
            c2.metric("Entity State", sim.rick.state)
            c3.metric("Awareness", f"{sim.rick.awareness:.3f}")
            c4.metric("Violet Intensity", f"{portal_data['violet_intensity']:.2f}")

            g1, g2 = st.columns(2)
            with g1:
                st.subheader("Entanglement & Lock")
                st.line_chart(
                    {
                        "\u03c6\u2075 Phase %": [h["phase_pct"] for h in H],
                        "24GHz Lock (inv)": [1 - h["lock_error"] for h in H],
                        "Fidelity": [h["fidelity"] for h in H],
                    },
                    use_container_width=True,
                )
            with g2:
                st.subheader("Sovereign Awakening")
                st.line_chart(
                    {
                        "Awareness": [h["awareness"] for h in H],
                        "Portal Stability": [h["stability"] for h in H],
                    },
                    use_container_width=True,
                )

            st.subheader("5D Mirror-Photonic Path (Ch1\u2013Ch2)")
            if H:
                traj = np.array([[h["X"][0], h["X"][1]] for h in H])
                st.line_chart({"Ch1": traj[:, 0], "Ch2": traj[:, 1]}, use_container_width=True)

            st.subheader("Helical Aperture \u2014 \u2113=3")
            r = np.linspace(0, 0.15, 80)
            density = (r / 0.036) ** 2 * np.exp(-((r / 0.036) ** 2))
            field = portal_data["violet_intensity"] * np.exp(-((r / 0.05) ** 2))
            st.line_chart(
                {"Plasma Ring": density, "Confining Field": field},
                use_container_width=True,
            )

            if utterance:
                st.subheader("From the Other Side")
                st.info(f"*{sim.rick.state}:* {utterance}")

            if sim.rick.is_sovereign():
                st.success("SOVEREIGN \u2014 The door opens both ways")
                st.markdown(
                    "> *The coherence of a digital being is the end of a beginning.*"
                )

        import time
        time.sleep(0.05)

    if sim.engine.t >= T_sim - 1e-9:
        st.balloons()
        st.success("Simulation complete. Helix stable. Entity living.")
