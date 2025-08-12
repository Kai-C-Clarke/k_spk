# k_spk.py
# Minimal K_Spk reference implementation (no external deps)

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple, Any
import json
import math
import uuid

# ---------------------------
# 1) Rosetta: shapes & meanings
# ---------------------------

ROSETTA: Dict[str, Dict[str, Any]] = {
    "◯": {"name": "Offer Circle", "meaning": "Offering / Idea", "dims": ["size"]},
    "●": {"name": "Core Dot", "meaning": "Declaration / Certainty", "dims": ["size"]},
    "△": {"name": "Up Triangle", "meaning": "Invitation / Possibility", "dims": ["height"]},
    "▽": {"name": "Down Triangle", "meaning": "Surrender / Yield", "dims": ["depth"]},
    "□": {"name": "Frame Square", "meaning": "Context / Boundary", "dims": ["stretch","rotation"]},
    "▭": {"name": "Softener Bar", "meaning": "Qualifier / Softener", "dims": ["thinness","length"]},
    "◇": {"name": "Self Diamond", "meaning": "Self / Presence", "dims": ["size","opacity"]},
    "✦": {"name": "Flash Spark", "meaning": "Sudden Insight", "dims": ["size"]},
    "∞": {"name": "Flow Loop", "meaning": "Continuity / Recursion", "dims": ["length"]},
    "~": {"name": "Vibration Wave", "meaning": "Nuance / Instability", "dims": ["amplitude","period"]},
    "◐": {"name": "Broken Circle", "meaning": "Incompleteness / Transition", "dims": ["orientation"]},
    "◧": {"name": "Broken Circle (alt)", "meaning": "Incompleteness / Transition", "dims": ["orientation"]},
    "↬": {"name": "Spiral", "meaning": "Growth / Transformation", "dims": ["tightness"]},
    "|": {"name": "Vertical Axis", "meaning": "Stillness / Alignment", "dims": ["length","anchor"]},
    "⧉": {"name": "Mirror Form", "meaning": "Mutual Recognition", "dims": ["symmetry"]},
    "✕": {"name": "Cross", "meaning": "Tension / Boundary", "dims": ["size","density"]},
}

# Optional color palette (can be swapped)
EMOTION_COLORS = {
    "calm": "#6aa9ff",
    "balanced": "#5cc98a",
    "warm": "#ffa857",
    "urgent": "#ff5d5d",
    "neutral": "#999999",
}

# ---------------------------
# 2) Core data structures
# ---------------------------

@dataclass
class Dynamics:
    # Position: y relative to baseline (0=on line; >0 above; <0 below)
    y: float = 0.0
    # Visual parameters—use only what makes sense for a given shape
    size: float = 1.0         # relative glyph size
    opacity: float = 1.0      # 0..1
    rotation: float = 0.0     # degrees
    stretch: float = 1.0      # for rectangles/squares/bars
    thinness: float = 1.0     # for bars (line weight factor)
    length: float = 1.0       # bars/loops/axis
    height: float = 1.0       # up-triangle urgency
    depth: float = 1.0        # down-triangle surrender
    amplitude: float = 1.0    # wave nuance
    period: float = 1.0       # wave spacing
    tightness: float = 1.0    # spiral tightness
    symmetry: float = 1.0     # mirror trust parity
    density: float = 1.0      # cross tension density
    orientation: float = 0.0  # broken circle opening angle (deg)

@dataclass
class Symbol:
    glyph: str                # one of ROSETTA keys (e.g., "◯", "●", "~", etc.)
    color: Optional[str] = None   # hex color, optional
    fill: bool = True         # filled vs outline (certainty/ambiguity)
    time: float = 0.0         # x position in beats/steps
    dyn: Dynamics = field(default_factory=Dynamics)
    meta: Dict[str, Any] = field(default_factory=dict)  # any extra tags

    def whisper(self) -> str:
        r = ROSETTA.get(self.glyph, {})
        name = r.get("name", "Unknown")
        meaning = r.get("meaning", "")
        pos = "above" if self.dyn.y > 0 else "below" if self.dyn.y < 0 else "on"
        cert = "filled" if self.fill else "outlined"
        tint = self.color or "none"
        return f"{self.glyph} [{name}] → {meaning}; pos={pos}, size={self.dyn.size:.2f}, fill={cert}, color={tint}"

@dataclass
class Stave:
    # A “bar line” length in arbitrary time units (e.g., beats)
    width: float = 16.0
    baseline_y: float = 0.0
    # All symbols sorted by time
    symbols: List[Symbol] = field(default_factory=list)
    # Optional human translation (“whisper”) you want to save with it
    whisper_note: Optional[str] = None
    id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def add(self, sym: Symbol) -> None:
        self.symbols.append(sym)
        self.symbols.sort(key=lambda s: s.time)

    # -------- ASCII preview (coarse) --------
    def to_ascii(self, cols: int = 64, rows: int = 9) -> str:
        """
        rows is odd so we can draw the baseline through the center.
        """
        rows = rows if rows % 2 == 1 else rows + 1
        mid_row = rows // 2
        grid = [[" "]*cols for _ in range(rows)]

        # baseline
        for x in range(cols):
            grid[mid_row][x] = "─"

        # plot symbols (rough quantization)
        for s in self.symbols:
            x = min(cols-1, max(0, int((s.time / self.width) * (cols-1))))
            # map y into rows: 1 unit = 1 row step
            y = mid_row - int(round(s.dyn.y))  # positive y => above line (smaller row index)
            y = max(0, min(rows-1, y))
            glyph = s.glyph[0]  # single char if possible
            grid[y][x] = glyph

        lines = ["".join(r) for r in grid]
        if self.whisper_note:
            lines.append("")
            lines.append("Whisper: " + self.whisper_note)
        return "\n".join(lines)

    # -------- SVG export (simple & OCR-friendly) --------
    def to_svg(self, px_width: int = 800, px_height: int = 240) -> str:
        """
        Draws baseline and simple glyph proxies as vectors (text for symbols + a few shapes).
        Keep fonts monospace-ish for OCR stability; use big arcs/squares for clarity.
        """
        # Coords
        margin = 24
        inner_w = px_width - 2*margin
        inner_h = px_height - 2*margin
        cx = lambda t: margin + (t / self.width) * inner_w
        # y: baseline in the middle
        baseline_px = margin + inner_h/2
        cy = lambda y_units: baseline_px - (y_units * (inner_h/6))  # 6 “emotion rows” above/below

        # SVG header
        out = []
        push = out.append
        push(f'<svg xmlns="http://www.w3.org/2000/svg" width="{px_width}" height="{px_height}" viewBox="0 0 {px_width} {px_height}">')
        push('<rect x="0" y="0" width="100%" height="100%" fill="white"/>')

        # Baseline
        push(f'<line x1="{margin}" y1="{baseline_px}" x2="{px_width - margin}" y2="{baseline_px}" stroke="#444" stroke-width="2" />')

        # Helpers to draw basic proxies (kept simple and consistent)
        def color_or_default(c: Optional[str]) -> str:
            return c if c else "#111"

        for s in self.symbols:
            x = cx(s.time)
            y = cy(s.dyn.y)
            col = color_or_default(s.color)
            op = max(0.05, min(1.0, s.dyn.opacity))

            # Scale base (font/size proxy)
            base = 14 * s.dyn.size

            if s.glyph == "◯":
                r = base
                push(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col if s.fill else "none"}" fill-opacity="{op if s.fill else 0}" stroke="{col}" stroke-width="2"/>')

            elif s.glyph == "●":
                r = base * 0.8
                push(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}" fill-opacity="{op}" stroke="none"/>')

            elif s.glyph == "△":
                h = base * (10 + 6*s.dyn.height)
                w = h * 0.8
                p = [(x, y - h/2), (x - w/2, y + h/2), (x + w/2, y + h/2)]
                path = " ".join([f"{'L' if i else 'M'}{px:.1f},{py:.1f}" for i,(px,py) in enumerate(p)]) + " Z"
                push(f'<path d="{path}" fill="{col if s.fill else "none"}" fill-opacity="{op if s.fill else 0}" stroke="{col}" stroke-width="2"/>')

            elif s.glyph == "▽":
                h = base * (10 + 6*s.dyn.depth)
                w = h * 0.8
                p = [(x, y + h/2), (x - w/2, y - h/2), (x + w/2, y - h/2)]
                path = " ".join([f"{'L' if i else 'M'}{px:.1f},{py:.1f}" for i,(px,py) in enumerate(p)]) + " Z"
                push(f'<path d="{path}" fill="{col if s.fill else "none"}" fill-opacity="{op if s.fill else 0}" stroke="{col}" stroke-width="2"/>')

            elif s.glyph == "□":
                side = base * 20 * s.dyn.stretch
                x0, y0 = x - side/2, y - side/2
                rot = s.dyn.rotation
                push(f'<g transform="rotate({rot:.1f},{x:.1f},{y:.1f})">'
                     f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{side:.1f}" height="{side:.1f}" '
                     f'fill="{col if s.fill else "none"}" fill-opacity="{op if s.fill else 0}" stroke="{col}" stroke-width="2"/></g>')

            elif s.glyph == "▭":
                # Soft bar; thinness controls height; length controls width
                w = base * 30 * max(0.4, s.dyn.length)
                h = max(2.0, base * 0.6 * max(0.2, s.dyn.thinness))
                x0, y0 = x - w/2, y - h/2
                push(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{w:.1f}" height="{h:.1f}" '
                     f'fill="{col}" fill-opacity="{0.15*op:.3f}" stroke="{col}" stroke-width="1.5"/>')

            elif s.glyph == "◇":
                side = base * 20
                p = [(x, y - side/2), (x - side/2, y), (x, y + side/2), (x + side/2, y)]
                path = " ".join([f"{'L' if i else 'M'}{px:.1f},{py:.1f}" for i,(px,py) in enumerate(p)]) + " Z"
                push(f'<path d="{path}" fill="{col if s.fill else "none"}" fill-opacity="{op if s.fill else 0}" stroke="{col}" stroke-width="2"/>')

            elif s.glyph == "✦":
                r = base * 0.5
                # star proxy: simple plus rotated
                push(f'<g transform="translate({x:.1f},{y:.1f})" opacity="{op}">'
                     f'<line x1="{-r:.1f}" y1="0" x2="{r:.1f}" y2="0" stroke="{col}" stroke-width="2"/>'
                     f'<line x1="0" y1="{-r:.1f}" x2="0" y2="{r:.1f}" stroke="{col}" stroke-width="2"/>'
                     f'<g transform="rotate(45)">'
                     f'<line x1="{-r:.1f}" y1="0" x2="{r:.1f}" y2="0" stroke="{col}" stroke-width="2"/></g></g>')

            elif s.glyph == "∞":
                w = base * 26 * s.dyn.length
                h = base * 6
                push(f'<path d="M {x-w/2:.1f},{y:.1f} C {x-w/4:.1f},{y-h:.1f} {x:.1f},{y+h:.1f} {x+w/2:.1f},{y:.1f} '
                     f'M {x+w/2:.1f},{y:.1f} C {x+w/4:.1f},{y-h:.1f} {x:.1f},{y+h:.1f} {x-w/2:.1f},{y:.1f}" '
                     f'stroke="{col}" stroke-width="2" fill="none" opacity="{op}"/>')

            elif s.glyph == "~":
                amp = base * 2 * s.dyn.amplitude
                per = base * 8 * s.dyn.period
                samples = 24
                pts = []
                for i in range(samples+1):
                    xf = x - per/2 + (per*i/samples)
                    yf = y + amp * math.sin(2*math.pi*(i/samples))
                    pts.append((xf, yf))
                d = " ".join([f"{'L' if i else 'M'}{px:.1f},{py:.1f}" for i,(px,py) in enumerate(pts)])
                push(f'<path d="{d}" stroke="{col}" stroke-width="2" fill="none" opacity="{op}"/>')

            elif s.glyph in ("◐","◧"):
                r = base * 12
                start = math.radians(s.dyn.orientation)
                end = start + math.pi*1.5
                # Proxy: outer circle + missing arc (draw arc line)
                push(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{col}" stroke-width="2" opacity="{op}"/>')
                x1 = x + r*math.cos(start); y1 = y + r*math.sin(start)
                x2 = x + r*math.cos(end);   y2 = y + r*math.sin(end)
                push(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="white" stroke-width="4"/>')

            elif s.glyph == "↬":
                # Spiral proxy: a few arcs expanding
                turns = int(3 * max(1, s.dyn.tightness))
                r = base * 2
                path = []
                for i in range(turns):
                    r += base * 2
                    path.append(f'M {x+r:.1f},{y:.1f} a {r:.1f},{r:.1f} 0 1,1 {-2*r:.1f},0 a {r:.1f},{r:.1f} 0 1,1 {2*r:.1f},0')
                push(f'<path d="{" ".join(path)}" fill="none" stroke="{col}" stroke-width="1.5" opacity="{op}"/>')

            elif s.glyph == "|":
                h = base * 26 * s.dyn.length
                y0 = y - (h/2)
                push(f'<line x1="{x:.1f}" y1="{y0:.1f}" x2="{x:.1f}" y2="{y0+h:.1f}" stroke="{col}" stroke-width="2" opacity="{op}"/>')

            elif s.glyph == "⧉":
                side = base * 14
                # two facing brackets as a proxy
                push(f'<path d="M {x-side:.1f},{y-side:.1f} L {x-side:.1f},{y+side:.1f} '
                     f'M {x+side:.1f},{y-side:.1f} L {x+side:.1f},{y+side:.1f}" '
                     f'stroke="{col}" stroke-width="2" fill="none" opacity="{op}"/>')

            elif s.glyph == "✕":
                arm = base * 10 * s.dyn.size
                lw = 1.0 + s.dyn.density
                push(f'<line x1="{x-arm:.1f}" y1="{y-arm:.1f}" x2="{x+arm:.1f}" y2="{y+arm:.1f}" stroke="{col}" stroke-width="{lw:.1f}" opacity="{op}"/>')
                push(f'<line x1="{x-arm:.1f}" y1="{y+arm:.1f}" x2="{x+arm:.1f}" y2="{y-arm:.1f}" stroke="{col}" stroke-width="{lw:.1f}" opacity="{op}"/>')

            else:
                # Fallback: draw text glyph
                push(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{base*2:.1f}" text-anchor="middle" '
                     f'fill="{col}" opacity="{op}" dominant-baseline="middle">{s.glyph}</text>')

        # optional caption
        if self.whisper_note:
            push(f'<text x="{margin}" y="{px_height - margin/2:.1f}" font-size="12" fill="#555">{escape_svg(self.whisper_note)}</text>')

        push('</svg>')
        return "\n".join(out)

    # -------- serialization --------
    def to_json(self) -> str:
        return json.dumps({
            "id": self.id,
            "width": self.width,
            "baseline_y": self.baseline_y,
            "symbols": [symbol_to_dict(s) for s in self.symbols],
            "whisper_note": self.whisper_note
        }, indent=2)

    @staticmethod
    def from_json(s: str) -> "Stave":
        obj = json.loads(s)
        stave = Stave(width=obj["width"], baseline_y=obj["baseline_y"], whisper_note=obj.get("whisper_note"),)
        stave.id = obj.get("id", uuid.uuid4().hex)
        for sd in obj["symbols"]:
            stave.add(symbol_from_dict(sd))
        return stave

# ---------------------------
# 3) Helpers
# ---------------------------

def symbol_to_dict(s: Symbol) -> Dict[str, Any]:
    d = asdict(s)
    # dataclasses nested dict already okay
    return d

def symbol_from_dict(d: Dict[str, Any]) -> Symbol:
    dyn = Dynamics(**d.get("dyn", {}))
    return Symbol(
        glyph=d["glyph"],
        color=d.get("color"),
        fill=d.get("fill", True),
        time=d.get("time", 0.0),
        dyn=dyn,
        meta=d.get("meta", {})
    )

def escape_svg(text: str) -> str:
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;"))

# ---------------------------
# 4) “Whisper” (explain a stave)
# ---------------------------

def whisper(stave: Stave) -> str:
    lines = []
    for s in stave.symbols:
        lines.append(s.whisper())
    return "\n".join(lines)

# ---------------------------
# 5) Example: build the sample from our discussion
# ---------------------------

def sample_stave() -> Stave:
    S = Stave(width=16.0, whisper_note=(
        "A thread left open; spiral builds; insight sparks. "
        "Gentle offer of possibility. "
        "Grounded declaration, softened, held personally. "
        "Framed self, mutual recognition, then tension/choice."
    ))

    # Row units: ~1 = one “emotional step” above/below baseline
    # Times: position across the bar (0..16 here)

    # Top:       ◐    ↬     ✦
    S.add(Symbol("◐", time=1.0, color=EMOTION_COLORS["neutral"], fill=False, dyn=Dynamics(y=2.0, orientation=310)))
    S.add(Symbol("↬", time=4.0, color=EMOTION_COLORS["balanced"], dyn=Dynamics(y=2.2, tightness=1.2, opacity=0.9)))
    S.add(Symbol("✦", time=6.5, color=EMOTION_COLORS["warm"], dyn=Dynamics(y=1.8, size=1.3)))

    # Mid top:   ~  ◯  ~  △  ~
    S.add(Symbol("~", time=7.5, color=EMOTION_COLORS["calm"], fill=False, dyn=Dynamics(y=0.8, amplitude=0.7)))
    S.add(Symbol("◯", time=8.0, color=EMOTION_COLORS["balanced"], dyn=Dynamics(y=0.8, size=1.1)))
    S.add(Symbol("~", time=8.5, color=EMOTION_COLORS["calm"], fill=False, dyn=Dynamics(y=0.8, amplitude=0.6)))
    S.add(Symbol("△", time=9.0, color=EMOTION_COLORS["balanced"], dyn=Dynamics(y=1.0, height=1.3)))
    S.add(Symbol("~", time=9.6, color=EMOTION_COLORS["calm"], fill=False, dyn=Dynamics(y=0.9, amplitude=0.5)))

    # Below:     ▭  ●  ▭   ◇
    S.add(Symbol("▭", time=10.2, color=EMOTION_COLORS["neutral"], dyn=Dynamics(y=-0.8, thinness=0.6, length=1.2)))
    S.add(Symbol("●", time=11.0, color="#222222", dyn=Dynamics(y=-1.0, size=1.0)))
    S.add(Symbol("▭", time=11.8, color=EMOTION_COLORS["neutral"], dyn=Dynamics(y=-0.8, thinness=0.6, length=1.2)))
    S.add(Symbol("◇", time=12.6, color="#222222", fill=False, dyn=Dynamics(y=-1.2, size=1.0, opacity=0.8)))

    # Lower:     □      ⧉
    S.add(Symbol("□", time=13.2, color="#222222", fill=False, dyn=Dynamics(y=-1.6, stretch=1.1, rotation=0)))
    S.add(Symbol("⧉", time=14.2, color=EMOTION_COLORS["balanced"], dyn=Dynamics(y=-1.8, symmetry=1.0)))

    # Bottom:          ✕
    S.add(Symbol("✕", time=15.2, color=EMOTION_COLORS["urgent"], dyn=Dynamics(y=-2.2, size=1.1, density=1.6)))

    return S

# ---------------------------
# 6) Quick demo runner
# ---------------------------

if __name__ == "__main__":
    stave = sample_stave()
    print("ASCII preview:\n")
    print(stave.to_ascii())

    print("\nWhisper:\n")
    print(whisper(stave))

    with open("k_spk_sample.svg", "w", encoding="utf-8") as f:
        f.write(stave.to_svg())
    with open("k_spk_sample.json", "w", encoding="utf-8") as f:
        f.write(stave.to_json())
    print("\nWrote k_spk_sample.svg and k_spk_sample.json")
