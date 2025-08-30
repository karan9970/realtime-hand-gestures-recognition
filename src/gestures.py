
from typing import Dict, Tuple, List
import math

# MediaPipe landmark indices
WRIST = 0
TH_CMC, TH_MCP, TH_IP, TH_TIP = 1,2,3,4
IX_MCP, IX_PIP, IX_DIP, IX_TIP = 5,6,7,8
MD_MCP, MD_PIP, MD_DIP, MD_TIP = 9,10,11,12
RG_MCP, RG_PIP, RG_DIP, RG_TIP = 13,14,15,16
PK_MCP, PK_PIP, PK_DIP, PK_TIP = 17,18,19,20

FINGERS = {
    'thumb':   (TH_MCP, TH_IP, TH_TIP),
    'index':   (IX_MCP, IX_PIP, IX_TIP),
    'middle':  (MD_MCP, MD_PIP, MD_TIP),
    'ring':    (RG_MCP, RG_PIP, RG_TIP),
    'pinky':   (PK_MCP, PK_PIP, PK_TIP),
}

def _to_xyz(lm) -> Tuple[float,float,float]:
    return (lm.x, lm.y, getattr(lm, 'z', 0.0))

def _dist(a, b) -> float:
    return math.dist(a, b)

def angle_between(a, b, c) -> float:
    """Return angle ABC (in degrees) given 3 points in 3D. Robust to tiny norms."""
    import numpy as np
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    c = np.array(c, dtype=float)
    v1 = a - b
    v2 = c - b
    n1 = np.linalg.norm(v1)
    n2 = np.linalg.norm(v2)
    if n1 < 1e-6 or n2 < 1e-6:
        return 0.0
    cosang = float(np.dot(v1, v2) / (n1*n2))
    cosang = max(-1.0, min(1.0, cosang))
    return math.degrees(math.acos(cosang))

def estimate_hand_size(pts: List[Tuple[float,float,float]]) -> float:
    # Simple proxy: distance wrist -> middle MCP
    return _dist(pts[WRIST], pts[MD_MCP]) + 1e-6

def finger_extended(pts, finger: str) -> bool:
    mcp, piv, tip = FINGERS[finger]
    # For thumb use IP as pivot; others use PIP
    a = pts[mcp]
    b = pts[piv]
    c = pts[tip]
    ang = angle_between(a, b, c)
    return ang > 160.0  # fairly straight

def compute_finger_states(landmarks) -> Dict[str, bool]:
    pts = [_to_xyz(lm) for lm in landmarks]
    states = {f: finger_extended(pts, f) for f in FINGERS.keys()}
    return states

def thumb_up_orientation(landmarks) -> bool:
    # True if thumb roughly points upward in image coords (y decreases upward)
    pts = [_to_xyz(lm) for lm in landmarks]
    size = estimate_hand_size(pts)
    dy = pts[TH_TIP][1] - pts[TH_MCP][1]
    return dy < -0.15  # generous upward threshold (normalized coords)

def classify_gesture(landmarks, handedness: str = "") -> Tuple[str, Dict[str,bool]]:
    states = compute_finger_states(landmarks)
    ext = [f for f, v in states.items() if v]
    ext_set = set(ext)

    # Rules
    # Fist
    if len(ext) == 0:
        return "Fist", states

    # Open Palm (index..pinky extended; thumb optional)
    if all(states[f] for f in ("index","middle","ring","pinky")):
        return "Open Palm", states

    # Peace (index & middle only; thumb can vary slightly)
    if states["index"] and states["middle"] and not states["ring"] and not states["pinky"]:
        # allow thumb either way
        if states["thumb"] in (True, False):
            return "Peace", states

    # Thumbs Up (thumb extended, others curled) + orientation check
    if states["thumb"] and not states["index"] and not states["middle"] and not states["ring"] and not states["pinky"]:
        if thumb_up_orientation(landmarks):
            return "Thumbs Up", states
        else:
            # fallback: still call it Thumbs Up if clearly only thumb is extended
            return "Thumbs Up", states

    # If none matched, return a generic label with the set of extended fingers for transparency
    label = f"Unknown: {','.join(sorted(ext_set))}" if ext_set else "Unknown"
    return label, states
