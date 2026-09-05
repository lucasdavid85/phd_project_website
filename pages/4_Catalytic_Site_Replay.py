"""Frame-by-frame replay of the DFR catalytic-site contact network.

27 molecular dynamics runs (3 orthologues x 3 substrates x 3 replicates), each
200 frames over 200 ns. A contact is present in a frame when the PSNTools
interaction force is > 0. The residence criteria and the substrate exit event
are overlaid so the loss of supporting contacts can be watched frame by frame.

Data: data/catalytic_replay.json  (built by DFR_Alone/build_frame_viewer.py)
"""
import base64
import json
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import py3Dmol
import streamlit as st

st.set_page_config(page_title="Catalytic Site Replay", layout="wide")

DATA_PATH = Path("data/catalytic_replay.json")
COORD_PATH = Path("data/site_coords.json")

ROLE_COLOR = {
    "SUB": "#C44E52",   # substrate
    "NPH": "#8C7250",   # NADPH cofactor
    "CAT": "#B03A3A",   # catalytic triad Ser123 / Tyr158 / Lys162
    "REC": "#3E68AE",   # recognition: residue 128 and Gln222
    "REG": "#3F8C5E",   # specificity region 119-162
    "OTH": "#9AA4AE",
}
ROLE_LABEL = {
    "SUB": "substrate", "NPH": "NADPH", "CAT": "catalytic triad",
    "REC": "recognition", "REG": "region 119–162", "OTH": "other contact",
}
AA1 = {"ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C", "GLN": "Q", "GLU": "E",
       "GLY": "G", "HIS": "H", "HID": "H", "HIE": "H", "HIP": "H", "ILE": "I", "LEU": "L",
       "LYS": "K", "MET": "M", "PHE": "F", "PRO": "P", "SER": "S", "THR": "T", "TRP": "W",
       "TYR": "Y", "VAL": "V"}
CRITERIA = [
    ("Hydride C4N–H···C4", "hyd", 4.0, "accessibility of the hydride-transfer coordinate"),
    ("Tyr158 OH···O4", "tyr", 4.0, "hydrogen bond to the catalytic tyrosine"),
    ("Substrate RMSD", "rmsd", 2.5, "displacement of the ligand within the site"),
]


@st.cache_data(show_spinner=False)
def load_runs():
    if not DATA_PATH.exists():
        return None
    with open(DATA_PATH) as fh:
        return json.load(fh)


@st.cache_data(show_spinner=False)
def load_coords():
    if not COORD_PATH.exists():
        return None
    with open(COORD_PATH) as fh:
        return json.load(fh)


@st.cache_data(show_spinner=False)
def frame_pdb(run_key, frame):
    """Rebuild a single-frame PDB of the catalytic site from the packed coordinates."""
    C = load_coords()
    if C is None or run_key not in C:
        return None
    c = C[run_key]
    q = np.frombuffer(base64.b64decode(c["xyz"]), dtype="<u2")
    na = c["natoms"]
    lo, span = np.array(c["lo"]), np.array(c["span"])
    xyz = lo + q[frame * na * 3:(frame + 1) * na * 3].reshape(na, 3) / 65535.0 * span
    lines = []
    for i, (m, p) in enumerate(zip(c["meta"], xyz), start=1):
        # PDB fixed columns: 13-16 atom name, 17 altLoc, 18-20 resName,
        # 22 chainID, 23-26 resSeq, 31-38/39-46/47-54 xyz, 77-78 element.
        name = m["n"] if len(m["n"]) >= 4 else " " + m["n"].ljust(3)
        lines.append(
            f"ATOM  {i:>5} {name:<4} {m['r']:>3} A{m['i']:>4}    "
            f"{p[0]:8.3f}{p[1]:8.3f}{p[2]:8.3f}  1.00  0.00          {m['e']:>2}")
    return "\n".join(lines) + "\nEND\n", c["meta"]


def render_structure(run_key, frame, show_labels=True, height=560):
    out = frame_pdb(run_key, frame)
    if out is None:
        st.info("All-atom coordinates are not available for this run.")
        return
    pdb, meta = out
    view = py3Dmol.view(width=760, height=height)
    view.addModel(pdb, "pdb")
    view.setStyle({}, {"stick": {"radius": 0.13, "color": ROLE_COLOR["OTH"]}})
    for role in ("REG", "CAT", "REC"):
        resi = sorted({m["i"] for m in meta if m["c"] == role})
        if resi:
            view.setStyle({"resi": resi},
                          {"stick": {"radius": 0.16, "color": ROLE_COLOR[role]}})
    view.setStyle({"resn": "NPH"}, {"stick": {"radius": 0.16, "color": ROLE_COLOR["NPH"]}})
    subs = sorted({m["r"] for m in meta if m["c"] == "SUB"})
    if subs:
        view.setStyle({"resn": subs},
                      {"stick": {"radius": 0.24, "color": ROLE_COLOR["SUB"]},
                       "sphere": {"radius": 0.34, "color": ROLE_COLOR["SUB"]}})

    if show_labels:
        seen = {}
        for m in meta:
            seen.setdefault((m["r"], m["i"], m["c"]), True)
        for (resn, resi, role) in seen:
            if role in ("SUB", "NPH"):
                text, sel = resn, {"resn": resn}
            else:
                text, sel = f"{AA1.get(resn, resn)}{resi}", {"resi": resi}
            view.addLabel(text, {
                "fontSize": 11, "fontColor": "white", "inFront": True,
                "backgroundColor": ROLE_COLOR[role], "backgroundOpacity": 0.75,
                "borderThickness": 0.0, "alignment": "center"}, sel)

    if subs:
        view.zoomTo({"resn": subs}); view.zoom(0.5)
    else:
        view.zoomTo()
    view.setBackgroundColor("rgba(0,0,0,0)")
    st.components.v1.html(view._make_html(), height=height + 20, scrolling=False)


def unhex(h, n):
    """Decode the packed per-frame presence bitstring."""
    bits = "".join(bin(int(c, 16))[2:].zfill(4) for c in h)
    return bits[len(bits) - n:]


@st.cache_data(show_spinner=False)
def decode(run_key):
    r = load_runs()[run_key]
    n = r["nframes"]
    edges = [
        {"a": e["a"], "b": e["b"], "occ": e["occ"], "on": unhex(e["bits"], n)}
        for e in r["edges"]
    ]
    return r, edges, unhex(r["insite"], n)


def node_xy(nodes):
    return {nd["id"]: (nd["x"], nd["y"]) for nd in nodes}


def edge_segments(edges, pos, frame, want_on):
    xs, ys, hover = [], [], []
    for e in edges:
        if (e["on"][frame] == "1") != want_on:
            continue
        (x0, y0), (x1, y1) = pos[e["a"]], pos[e["b"]]
        xs += [x0, x1, None]
        ys += [y0, y1, None]
        a = "substrate" if e["a"] == "SUB" else e["a"]
        b = "substrate" if e["b"] == "SUB" else e["b"]
        hover += [f"{a} – {b}<br>occupancy {e['occ'] * 100:.0f}% of the run"] * 3
    return xs, ys, hover


def build_figure(r, edges, insite, frame, animate):
    pos = node_xy(r["nodes"])
    n = r["nframes"]

    def traces_for(f):
        offx, offy, _ = edge_segments(edges, pos, f, False)
        onx, ony, onh = edge_segments(edges, pos, f, True)
        return [
            go.Scatter(x=offx, y=offy, mode="lines", hoverinfo="skip",
                       line=dict(color="rgba(150,160,170,0.20)", width=1)),
            go.Scatter(x=onx, y=ony, mode="lines", text=onh, hoverinfo="text",
                       line=dict(color="#6B7682", width=2.2)),
        ]

    nodes = r["nodes"]
    node_trace = go.Scatter(
        x=[nd["x"] for nd in nodes], y=[nd["y"] for nd in nodes],
        mode="markers+text",
        text=["SUBS" if nd["id"] == "SUB" else nd["id"] for nd in nodes],
        textposition="middle center",
        textfont=dict(size=9, color="white", family="monospace"),
        marker=dict(size=[34 if nd["id"] == "SUB" else 26 for nd in nodes],
                    color=[ROLE_COLOR[nd["cls"]] for nd in nodes],
                    line=dict(width=1.5, color="rgba(255,255,255,0.85)")),
        hovertext=[f"{nd['id']} · {ROLE_LABEL[nd['cls']]}" for nd in nodes],
        hoverinfo="text",
    )

    fig = go.Figure(data=traces_for(frame) + [node_trace])

    if animate:
        fig.frames = [
            go.Frame(data=traces_for(f), traces=[0, 1], name=str(f),
                     layout=go.Layout(title_text=frame_caption(r, insite, f)))
            for f in range(n)
        ]
        fig.update_layout(
            updatemenus=[dict(
                type="buttons", showactive=False, x=0.02, y=1.10, xanchor="left",
                buttons=[
                    dict(label="▶ Play", method="animate",
                         args=[None, dict(frame=dict(duration=110, redraw=True),
                                          fromcurrent=True, transition=dict(duration=0))]),
                    dict(label="❚❚ Pause", method="animate",
                         args=[[None], dict(frame=dict(duration=0, redraw=False),
                                            mode="immediate")]),
                ])],
            sliders=[dict(
                active=frame, x=0.12, len=0.86, y=1.06, xanchor="left",
                currentvalue=dict(prefix="frame ", font=dict(size=12)),
                steps=[dict(method="animate", label=str(f + 1),
                            args=[[str(f)], dict(mode="immediate",
                                                 frame=dict(duration=0, redraw=True),
                                                 transition=dict(duration=0))])
                       for f in range(n)])],
        )

    fig.update_layout(
        title=dict(text=frame_caption(r, insite, frame), x=0.0, xanchor="left",
                   font=dict(size=13)),
        showlegend=False, height=620,
        margin=dict(l=10, r=10, t=110 if animate else 50, b=10),
        xaxis=dict(visible=False, range=[-1.18, 1.18]),
        yaxis=dict(visible=False, range=[-1.18, 1.18], scaleanchor="x"),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        hoverlabel=dict(font_size=12),
    )
    return fig


def frame_caption(r, insite, f):
    inside = insite[f] == "1"
    tag = "IN the catalytic site" if inside else "OUT of the catalytic site"
    return (f"frame {f + 1}/{r['nframes']} · {tag} · "
            f"hydride {r['hyd'][f]:.2f} Å · Tyr158 {r['tyr'][f]:.2f} Å · "
            f"RMSD {r['rmsd'][f]:.2f} Å")


def residence_strip(r, insite, frame):
    n = r["nframes"]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=list(range(1, n + 1)), y=[1] * n,
        marker=dict(color=["#2F6B45" if c == "1" else "rgba(150,160,170,0.22)" for c in insite],
                    line=dict(width=0)),
        hovertext=[f"frame {i + 1} · " + ("in site" if insite[i] == "1" else "out")
                   for i in range(n)],
        hoverinfo="text", showlegend=False))
    if r["exit"] is not None:
        fig.add_vline(x=r["exit"] + 1, line=dict(color="#111", width=2))
        fig.add_annotation(x=r["exit"] + 1, y=1.28, text="exit", showarrow=False,
                           font=dict(size=11))
    fig.add_vline(x=frame + 1, line=dict(color="#00A6B8", width=2.5))
    fig.update_layout(height=92, bargap=0,
                      margin=dict(l=10, r=10, t=22, b=26),
                      xaxis=dict(title="frame", showgrid=False, range=[0.5, n + 0.5]),
                      yaxis=dict(visible=False, range=[0, 1.45]),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return fig


# ----------------------------------------------------------------- page
st.title("Catalytic site replay")
st.caption(
    "Every residue–residue contact around the bound dihydroflavonol, replayed frame by frame. "
    "A contact is present when the PSNTools interaction force exceeds zero. Scrub to an exit "
    "event to watch the supporting contacts break before the substrate leaves the site."
)

RUNS = load_runs()
if RUNS is None:
    st.error(f"Data file not found: {DATA_PATH.resolve()}")
    st.stop()

labels = {k: f"{v['organism']} · {v['ligand']} · {v['rep']}" for k, v in RUNS.items()}
suggested = [k for k in ("Vitis_DHQ_MD3", "Maize_A1b_DHK_MD1", "Maize_A1_DHQ_MD1") if k in RUNS]
order = suggested + [k for k in RUNS if k not in suggested]

top = st.columns([3, 1.4, 1.4, 1.4])
with top[0]:
    run_key = st.selectbox("Run", order, format_func=lambda k: labels[k])
with top[1]:
    show_labels = st.toggle("Residue labels", value=True)
with top[2]:
    show_absent = st.toggle("Show absent contacts", value=True,
                            help="Keeps the topology visible while contacts come and go.")
with top[3]:
    speed = st.select_slider("Speed", options=["slow", "medium", "fast"], value="medium")

TICK = {"slow": 0.6, "medium": 0.35, "fast": 0.18}[speed]

r, edges, insite = decode(run_key)
n = r["nframes"]

# frame lives in session state so Play can advance it between reruns
if "frame" not in st.session_state or st.session_state.get("frame_run") != run_key:
    st.session_state.frame = max(0, (r["exit"] or n // 2) - 12)
    st.session_state.frame_run = run_key
    st.session_state.playing = False
st.session_state.setdefault("playing", False)

exit_note = (f"exit at frame {r['exit'] + 1}" if r["exit"] is not None
             else "no sustained exit in this run")


def draw_everything():
    """The animated region. Re-runs on its own while Play is on."""
    if st.session_state.playing:
        st.session_state.frame = (st.session_state.frame + 1) % n

    ctl = st.columns([1, 1, 6])
    with ctl[0]:
        if st.button("▶ Play" if not st.session_state.playing else "❚❚ Pause",
                     use_container_width=True, key="playbtn"):
            st.session_state.playing = not st.session_state.playing
            st.rerun()
    with ctl[1]:
        if st.button("⏮ Reset", use_container_width=True, key="resetbtn"):
            st.session_state.playing = False
            st.session_state.frame = 0
            st.rerun()
    with ctl[2]:
        frame = st.slider(f"Frame  ·  {exit_note}", 1, n, st.session_state.frame + 1,
                          key=f"slider_{run_key}") - 1
        if not st.session_state.playing:
            st.session_state.frame = frame

    frame = st.session_state.frame

    viz_l, viz_r = st.columns(2)
    with viz_l:
        st.markdown("**Contact network** · edge width is occupancy over the run")
        st.plotly_chart(
            build_figure(r, edges if show_absent else
                         [e for e in edges if e["on"][frame] == "1"],
                         insite, frame, False),
            use_container_width=True, config={"displayModeBar": False})
    with viz_r:
        st.markdown("**Catalytic site, all-atom** · drag to rotate, scroll to zoom")
        render_structure(run_key, frame, show_labels=show_labels, height=620)

    st.plotly_chart(residence_strip(r, insite, frame), use_container_width=True,
                    config={"displayModeBar": False})

    info_l, info_r = st.columns([1, 2])
    with info_l:
        inside = insite[frame] == "1"
        st.markdown(
            f"<div style='padding:10px 14px;border-radius:8px;text-align:center;font-weight:600;"
            f"color:#fff;background:{'#2F6B45' if inside else '#A8434A'}'>"
            f"{'IN CATALYTIC SITE' if inside else 'OUT OF SITE'}</div>",
            unsafe_allow_html=True)
        st.caption("All three criteria must hold simultaneously.")
        for name, key, limit, note in CRITERIA:
            val = r[key][frame]
            ok = val <= limit
            st.metric(name, f"{val:.2f} Å", f"{'✓' if ok else '✗'}  threshold ≤ {limit} Å",
                      delta_color="normal" if ok else "inverse", help=note)
        active = sum(1 for e in edges if e["on"][frame] == "1")
        sub_active = sum(1 for e in edges
                         if e["on"][frame] == "1" and "SUB" in (e["a"], e["b"]))
        st.divider()
        st.write(f"**Contacts present** {active} of {len(edges)}")
        st.write(f"**Substrate contacts** {sub_active}")
        st.divider()
        st.markdown("**Residue roles**")
        st.markdown(
            " ".join(
                f"<span style='display:inline-block;margin:2px 8px 2px 0;font-size:12px'>"
                f"<span style='display:inline-block;width:9px;height:9px;border-radius:50%;"
                f"background:{c};margin-right:4px'></span>{ROLE_LABEL[k]}</span>"
                for k, c in ROLE_COLOR.items()),
            unsafe_allow_html=True)
        st.caption("Triad Ser123 · Tyr158 · Lys162 (YxxxK). Recognition: residue 128 and "
                   "Gln222. Both panels use the same colours and the same frame.")

    with info_r:
        st.markdown("**Contacts present in this frame**")
        rows = [{"contact": ("substrate" if e["a"] == "SUB" else e["a"]) + " – " +
                            ("substrate" if e["b"] == "SUB" else e["b"]),
                 "occupancy over the run (%)": round(e["occ"] * 100),
                 "touches substrate": "yes" if "SUB" in (e["a"], e["b"]) else ""}
                for e in edges if e["on"][frame] == "1"]
        st.dataframe(pd.DataFrame(rows).sort_values("occupancy over the run (%)",
                                                    ascending=False),
                     use_container_width=True, hide_index=True, height=320)


# st.fragment re-runs only this block, so Play does not redraw the whole page.
if hasattr(st, "fragment") and st.session_state.playing:
    st.fragment(run_every=TICK)(draw_everything)()
else:
    draw_everything()

st.caption(
    "27 runs · 3 orthologues × 3 substrates × 3 replicates · 200 frames over 200 ns. "
    "Residence criteria: hydride ≤ 4.0 Å, Tyr158 hydrogen bond ≤ 4.0 Å, substrate RMSD ≤ 2.5 Å."
)
