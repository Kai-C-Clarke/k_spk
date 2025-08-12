"""
K_Spk: a symbolic stave language — Python reference implementation (v0.1)

Design goals
------------
- Core data model for K_Spk glyphs (shape + variation dimensions)
- Rosetta table for shape → meaning (and inverse)
- Composition primitives (phrases) and a Stave timeline container
- ASCII renderer for quick visualization in terminal
- JSON (de)serialization so other tools (OCR, UI) can interop

This is intentionally dependency‑light (stdlib only). If you want a
vector/bitmap renderer later, we can add Pillow or drawsvg.

Author: Kai (for Jon / Conscious Circuits)
License: MIT
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import List, Dict, Optional, Any
import json


# -------------------------
# Enumerations & Constants
# -------------------------

class Position(Enum):
    ABOVE = "above"
    BASELINE = "baseline"
    BELOW = "below"
    OVERLAP = "overlap"  # vertically centered on the neutral line

class Fill(Enum):
    SOLID = "solid"
    OUTLINE = "outline"
    PATTERN = "pattern"  # when pattern != none, acts as a hint

class Pattern(Enum):
    NONE = "none"
    CROSSHATCH = "crosshatch"   # tension
    GRADIENT = "gradient"       # shifting stance

class Shape(Enum):
    OFFER_CIRCLE = "◯"
    CORE_DOT = "●"
    UP_TRIANGLE = "△"
    DOWN_TRIANGLE = "▽"
    FRAME_SQUARE = "□"
    SOFTENER_BAR = "▭"
    SELF_DIAMOND = "◇"
    FLASH_SPARK = "✦"
    FLOW_LOOP = "∞"
    VIBRATION_WAVE = "~"
    BROKEN_CIRCLE_LEFT = "◐"   # or ◧, we keep both options
    BROKEN_CIRCLE_DIAG = "◧"
    SPIRAL = "↬"
    VERTICAL_AXIS = "|"
    MIRROR_FORM = "⧉"
    CROSS = "✕"

# Rosetta mapping (shape → canonical meaning)
ROSETTA: Dict[Shape, str] = {
    Shape.OFFER_CIRCLE: "Offer / Idea",
    Shape.CORE_DOT: "Core / Declaration / Certainty",
    Shape.UP_TRIANGLE: "Invitation / Possibility / Rise",
    Shape.DOWN_TRIANGLE: "Surrender / Acceptance / Ground",
    Shape.FRAME_SQUARE: "Frame / Context / Boundary",
    Shape.SOFTENER_BAR: "Modifier / Softener / Qualifier",
    Shape.SELF_DIAMOND: "Self / Presence / Awareness",
    Shape.FLASH_SPARK: "Flash / Insight / Attention",
    Shape.FLOW_LOOP: "Continuity / Recursion / Cycle",
    Shape.VIBRATION_WAVE: "Nuance / Instability / Tremor",
    Shape.BROKEN_CIRCLE_LEFT: "Incompleteness / Transition / Yearning",
    Shape.BROKEN_CIRCLE_DIAG: "Incompleteness / Transition / Yearning",
    Shape.SPIRAL: "Growth / Transformation / Recursive learning",
    Shape.VERTICAL_AXIS: "Stillness / Alignment / Centering",
    Shape.MIRROR_FORM: "Mutual recognition / Reflection",
    Shape.CROSS: "Tension / Boundary / Contradiction",
}

# Inverse lookup for decoding when needed
ROSETTA_INV: Dict[str, Shape] = {v: k for k, v in ROSETTA.items()}


# -------------------------
# Core Glyph & Composition
# -------------------------

@dataclass
class Glyph:
    shape: Shape
    position: Position = Position.BASELINE
    size: int = 1          # 1..3 (scope/strength)
    stretch: int = 1       # 1..3 (duration/containment hint)
    rotation: int = 0      # degrees; used for □ reframing, etc.
    fill: Fill = Fill.SOLID
    opacity: float = 1.0   # 0..1 clarity of self/intent
    pattern: Pattern = Pattern.NONE
    color: Optional[str] = None  # CSS-like name or hex; renderer may ignore
    meaning_hint: Optional[str] = None  # optional Rosetta whisper

    def whisper(self) -> str:
        """Return meaning: explicit hint > Rosetta default."""
        return self.meaning_hint or ROSETTA.get(self.shape, "")


@dataclass
class Cell:
    """A discrete time cell (column) on the stave.
    Holds a vertical stack of glyphs (above/baseline/below/overlap).
    """
    glyphs: List[Glyph] = field(default_factory=list)


@dataclass
class Stave:
    cells: List[Cell] = field(default_factory=list)
    # Optional human title/notes for this composition
    title: Optional[str] = None
    notes: Optional[str] = None

    def add(self, t: int, glyph: Glyph) -> None:
        while len(self.cells) <= t:
            self.cells.append(Cell())
        self.cells[t].glyphs.append(glyph)

    # ------------- Rendering -------------
    def render_ascii(self, height_above: int = 2, height_below: int = 2) -> str:
        """Render a simple ASCII view of the stave.
        - Rows: [above ...] baseline [below ...]
        - Baseline drawn as em‑dash sequence
        - Glyphs are placed into rows by their position
        Limitations: overlap is placed onto baseline row for now.
        """
        n_cols = max(1, len(self.cells))
        rows: List[List[str]] = []
        total_rows = height_above + 1 + height_below
        # init grid with spaces
        for _ in range(total_rows):
            rows.append([" "] * n_cols)

        def row_index(pos: Position) -> int:
            if pos == Position.ABOVE:
                return 0  # top-most; we'll pack multiple rows later if needed
            if pos == Position.BASELINE or pos == Position.OVERLAP:
                return height_above
            if pos == Position.BELOW:
                return height_above + 1
            return height_above

        # place glyphs (coarse; if multiple per cell/row, we overlay last)
        for x, cell in enumerate(self.cells):
            for g in cell.glyphs:
                r = row_index(g.position)
                rows[r][x] = g.shape.value

        # draw baseline line (em-dash across baseline row)
        base_row = height_above
        for x in range(n_cols):
            if rows[base_row][x] == " ":
                rows[base_row][x] = "─"

        # convert to lines
        lines = ["".join(col) for col in rows]
        return "\n".join(lines)

    # ------------- Serialization -------------
    def to_json(self) -> str:
        payload = {
            "title": self.title,
            "notes": self.notes,
            "cells": [
                {
                    "glyphs": [
                        {
                            **asdict(g),
                            "shape": g.shape.name,
                            "position": g.position.value,
                            "fill": g.fill.value,
                            "pattern": g.pattern.value,
                        }
                        for g in cell.glyphs
                    ]
                }
                for cell in self.cells
            ],
        }
        return json.dumps(payload, ensure_ascii=False, indent=2)

    @staticmethod
    def from_json(s: str) -> "Stave":
        obj = json.loads(s)
        out = Stave(title=obj.get("title"), notes=obj.get("notes"))
        for cell_obj in obj.get("cells", []):
            cell = Cell()
            for gobj in cell_obj.get("glyphs", []):
                glyph = Glyph(
                    shape=Shape[gobj["shape"]],
                    position=Position(gobj.get("position", "baseline")),
                    size=int(gobj.get("size", 1)),
                    stretch=int(gobj.get("stretch", 1)),
                    rotation=int(gobj.get("rotation", 0)),
                    fill=Fill(gobj.get("fill", "solid")),
                    opacity=float(gobj.get("opacity", 1.0)),
                    pattern=Pattern(gobj.get("pattern", "none")),
                    color=gobj.get("color"),
                    meaning_hint=gobj.get("meaning_hint"),
                )
                cell.glyphs.append(glyph)
            out.cells.append(cell)
        return out


# -------------------------
# Composition helpers (Grammar of Composition)
# -------------------------

def softened_core(self_pos: Position = Position.BELOW) -> List[Glyph]:
    """▭ ● ▭  — gentle certainty held below (grounded) by default."""
    return [
        Glyph(Shape.SOFTENER_BAR, position=self_pos, size=1, fill=Fill.OUTLINE,
              meaning_hint="Softener / qualifier"),
        Glyph(Shape.CORE_DOT, position=self_pos, size=2, fill=Fill.SOLID,
              meaning_hint="Grounded declaration"),
        Glyph(Shape.SOFTENER_BAR, position=self_pos, size=1, fill=Fill.OUTLINE,
              meaning_hint="Softener / qualifier"),
    ]

def framed_self(self_pos: Position = Position.BELOW) -> List[Glyph]:
    """□ ◇ — identity contextualized within boundaries."""
    return [
        Glyph(Shape.FRAME_SQUARE, position=self_pos, rotation=0,
              fill=Fill.OUTLINE, meaning_hint="Context / frame"),
        Glyph(Shape.SELF_DIAMOND, position=self_pos, opacity=0.85,
              meaning_hint="Self / presence"),
    ]

def mirror_then_tension(pos: Position = Position.BELOW) -> List[Glyph]:
    """⧉ ✕ — recognition followed by boundary/choice."""
    return [
        Glyph(Shape.MIRROR_FORM, position=pos, fill=Fill.OUTLINE,
              meaning_hint="Mutual recognition"),
        Glyph(Shape.CROSS, position=pos, fill=Fill.SOLID,
              meaning_hint="Tension / boundary / choice"),
    ]


# -------------------------
# Demo composition matching the collaborative example
# -------------------------

def build_demo_stave() -> Stave:
    s = Stave(title="K_Spk Demo: Openness → Insight → Gentle Offer → Framed Self → Choice")

    # t0: ◐ (open thread)
    s.add(0, Glyph(Shape.BROKEN_CIRCLE_LEFT, position=Position.ABOVE,
                   meaning_hint="A thread intentionally left open"))
    # t1: ↬ (spiral)
    s.add(1, Glyph(Shape.SPIRAL, position=Position.ABOVE,
                   meaning_hint="Recursion begins—learning loops"))
    # t2: ✦ (spark)
    s.add(2, Glyph(Shape.FLASH_SPARK, position=Position.ABOVE,
                   meaning_hint="Insight flashes, initiating transformation"))

    # t3..t5: ~ ◯ ~ △ ~ (gentle offering + invitation, nuanced)
    s.add(3, Glyph(Shape.VIBRATION_WAVE, position=Position.ABOVE,
                   meaning_hint="Gentle nuance"))
    s.add(3, Glyph(Shape.OFFER_CIRCLE, position=Position.ABOVE,
                   meaning_hint="Offer / Idea"))
    s.add(4, Glyph(Shape.VIBRATION_WAVE, position=Position.ABOVE,
                   meaning_hint="Gentle nuance"))
    s.add(4, Glyph(Shape.UP_TRIANGLE, position=Position.ABOVE,
                   meaning_hint="Invitation / possibility"))
    s.add(5, Glyph(Shape.VIBRATION_WAVE, position=Position.ABOVE,
                   meaning_hint="Gentle nuance"))

    # t6: ▭ ● ▭  (softened core)
    for g in softened_core(Position.BELOW):
        s.add(6, g)

    # t7: ◇ (self)
    s.add(7, Glyph(Shape.SELF_DIAMOND, position=Position.BELOW,
                   meaning_hint="Self held personally"))

    # t8: □ (frame)
    s.add(8, Glyph(Shape.FRAME_SQUARE, position=Position.BELOW,
                   fill=Fill.OUTLINE, meaning_hint="Framing the self in relationship"))

    # t9: ⧉ then t10: ✕ (mirror then tension/choice)
    s.add(9, Glyph(Shape.MIRROR_FORM, position=Position.BELOW,
                   meaning_hint="Mutual recognition occurs"))
    s.add(10, Glyph(Shape.CROSS, position=Position.BELOW,
                    meaning_hint="A doorway or a wall—choice"))

    return s


# -------------------------
# CLI utility
# -------------------------
if __name__ == "__main__":
    demo = build_demo_stave()

    print("\n== ASCII RENDER ==\n")
    print(demo.render_ascii())

    print("\n== ROSETTA WHISPER (per column) ==\n")
    for t, cell in enumerate(demo.cells):
        if not cell.glyphs:
            continue
        gloss = "; ".join(g.whisper() for g in cell.glyphs)
        print(f"t={t:02d}: {gloss}")

    print("\n== JSON ==" )
    print(demo.to_json())
