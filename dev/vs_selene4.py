import os as _os; _ROOT = _os.path.dirname(_os.path.abspath(__file__))
"""Selene - Starsector style v4, drawn top-down from the approved 3D block-out (ss/selene3d.html v2b).
Fast carrier cruiser. Plum armoured dome (meridian ribs, rose-gold equator band, shingled crown plates) with 4 mint visor
bands (front bridge, back, left, right; rose-gold frames + mullions) and the core petal hatch on the crown; two rounded side
pods with short graphite launch decks running forward into a hangar PORTAL in each pod front (armoured hood, dark bay, lit
edges, rose-gold lintel); 2 medium composite on rose-gold ringed sponsons on the pods' outer sides; engine crest behind the
dome with 2 small ballistic PD sunk in its corners; 3 big drives + 2 diagonal jets on the crest's outer corners."""
import json, numpy as np
import vstyle, vparts as VP
from vstyle import Ship, spline

W, H, CX = 320, 390, 160
DCY, DRX, DRZ = 262, 80, 86                          # dome (3D: 80 x 86, 58 tall)
PODX, POD0, POD1 = 60, 215, 315                      # left pod (mirrored)
DK0, DK1 = 112, 222                                  # launch deck
PORT = 210                                           # portal hood centre (py 201-219)
COMP = [(24, 262, 20), (296, 262, -20)]
PD = [(90, 330, 120), (230, 330, -120)]
DRV = [(120, 344, 368, 30), (160, 346, 372, 36), (200, 344, 368, 30)]
ENG = [[x, y1] for (x, y0, y1, w) in DRV]

AR = np.array([122, 106, 134]); AR_D = np.array([81, 70, 89]); AR_L = np.array([165, 150, 176])
ROSE = np.array([224, 160, 124]); ROSE_D = np.array([168, 108, 80]); DECK = np.array([62, 65, 72]); DECK_D = np.array([48, 51, 58])
LANE = np.array([87, 91, 99]); MINT = np.array([143, 240, 224]); WHT = np.array([236, 236, 240]); LIT = np.array([255, 226, 150])
SEAM = (52, 44, 58)
SYSTEMS = []
def sysl(n, x, y): SYSTEMS.append((n, x, y))

_L = np.array([0.0, -0.78, 0.62]); vstyle.LIGHT = _L/np.linalg.norm(_L); vstyle.SYM_CX = CX
s = Ship(W, H, seed=141)
s.auto_z = True; s.depth = dict(unit=7.0, s_str=0.9, tint=0.38, ao=0.6, ao_r=5, sdir=((0.6, 0.8), (-0.6, 0.8)), s_soft=0.9)
_plate0, _bolt0 = s.plate, s.bolt_row
def _plate(mask, color, *a, **k):
    k.setdefault('tex', 0.018); k.setdefault('grime', 0.0); k.setdefault('notch', 0); return _plate0(mask, color, *a, **k)
def _bolt(m, inset=1.8, spacing=4.0, seed=0):
    if m is not None and m.sum()/s.SS**2 > 700: _bolt0(m, inset, spacing*2.4)
s.plate, s.bolt_row = _plate, _bolt
def zmark(z, fn, *a, **k):
    before = s.rgb.copy(); a0 = s.a.copy(); r = fn(*a, **k)
    ch = (np.abs(s.rgb - before).sum(2) > 0.5) | (s.a & ~a0); s.z[ch] = z; return r
X = lambda g, dx: CX + g*dx
yy_ = s.yy/s.SS; xx_ = s.xx/s.SS

def prof(px, hwf, y0, y1, inset=0.0):
    """mask of a body of revolution-like outline: |x - px| <= hw(py) - inset between y0 and y1 (same as the 3D outline())"""
    hw = hwf(yy_) - inset
    return (np.abs(xx_ - px) <= hw) & (yy_ >= y0) & (yy_ <= y1) & (hw > 0.5)
def podHW(py):
    py = np.asarray(py, np.float32)
    return np.where(py < 233, 30*np.sqrt(np.clip(1 - ((233 - py)/18)**2, 0, 1)), np.where(py > 297, 30*np.sqrt(np.clip(1 - ((py - 297)/18)**2, 0, 1)), 30.0))
def deckHW(py):
    py = np.asarray(py, np.float32)
    return np.where(py < 134, 22*np.sqrt(np.clip(1 - ((134 - py)/22)**2, 0, 1)), 22.0)
def crestHW(py):
    py = np.asarray(py, np.float32)
    return np.minimum(80, 80*np.sqrt(np.clip(1 - ((py - 340)/42)**2, 0, 1))*1.02)

# ================================================================ silhouette + machinery base
u_ = (xx_ - CX)/DRX; v_ = (yy_ - DCY)/DRZ; rb = np.hypot(u_, v_); ab = np.degrees(np.arctan2(v_, u_))   # -90 = forward
dome = rb <= 1.0
pods = prof(PODX, podHW, POD0, POD1) | prof(X(1, 100), podHW, POD0, POD1)
decks = prof(PODX, deckHW, DK0, DK1) | prof(X(1, 100), deckHW, DK0, DK1)
crest = prof(CX, crestHW, 305, 356)
spons = (s.disk(30, 262, 20) & (xx_ < 32)) | (s.disk(290, 262, 20) & (xx_ > 288))
s.guts(dome | pods | decks | crest | spons, seed=143, tone=(50, 44, 56), minc=3, maxc=10); s.z[:] = 0

# ================================================================ 3 big drives + 2 diagonal jets (under the crest's stern face)
for (ex, y0, y1, w) in DRV:
    m = VP.engine_housing(s, ex, y0, y1, w, metal=(150, 138, 160), bands=2); s.z[m] = 1.2
    band = m & (yy_ > y1 - 5.2) & (yy_ < y1 - 3.4)                                  # rose-gold tip ring (3D: rose torus at the exit)
    s.rgb[band] = np.clip(s.rgb[band]/150.0*ROSE*1.05, 0, 255)
SMALL = []
for g in (-1, 1):
    e = np.array([X(g, 77), 350.0]); n = np.array([g*0.7071, 0.7071])
    VP.diag_jet(s, g, *(e + n*3.0), 10, T=34, metal=(170, 158, 178), z=1.6); ex_ = e + n*13; SMALL.append((float(ex_[0]), float(ex_[1]), 135 if g < 0 else -135))
sysl('3 big drives (rose-gold tip rings) + 2 diagonal jets on the crest corners', CX, 368)

# ================================================================ engine crest behind the dome: shell, lighter top plate, dark heat slots
s.plate(crest, AR*0.92, z=2.0, bevel=3.4, dome=0.6, inset=2.2, shadow_k=0.9)
ctop = prof(CX, lambda y: np.minimum(74, crestHW(y)/1.02), 309, 352, 6)
s.plate(ctop, AR_L*0.97, z=2.3, bevel=1.8, dome=0.3, inset=1.0, shadow_k=0.9, paint=[(ctop & (yy_ > 347.5) & (yy_ < 349.2), ROSE*0.9)])
for k in range(-3, 4):
    sl = s.rrect(CX + k*18 - 0.9, 316, CX + k*18 + 0.9, 346, 0.6) & ctop
    s.rgb[sl] = (34, 30, 40)
sysl('engine crest: top plate, heat slots, rose trim aft', X(-1, 60), 346)

# ================================================================ 2 small ballistic PD sunk into the crest corners (rose-gold outboard lips)
for (px, py, a) in PD:
    g = -1 if px < CX else 1
    VP.sunk_mount(s, px, py, 5.4, (g, 0.7), metal=AR_D, lip_metal=AR_L, z=2.4, lip_z=3.2, accent=ROSE)
sysl('2 small ballistic PD sunk in the crest corners, 240 deg to the rear quarters', 90, 330)

# ================================================================ side pods + sponsons (left, mirrored)
sp = s.disk(30, 262, 20) & (xx_ < 32)
s.plate(sp, AR_D, z=2.0, bevel=2.6, dome=0.5, inset=1.4, shadow_k=0.9)
pod = prof(PODX, podHW, POD0, POD1)
s.plate(pod, AR, z=2.5, bevel=4.0, dome=0.9, inset=2.4, shadow_k=0.95)
ptop = prof(PODX, podHW, 221, 309, 6)
s.plate(ptop, AR_L, z=2.7, bevel=1.8, dome=0.5, inset=1.0, shadow_k=0.9)
for yv in (250, 276):                                                                # hangar roof seams
    s.rgb[ptop & (np.abs(yy_ - yv) < 0.5)] = SEAM
for yv in (236, 290):                                                                # roof service hatches over the hangar
    h_ = s.rrect(PODX - 9, yv - 4, PODX + 9, yv + 4, 1.5)
    s.plate(h_, AR*1.02, z=2.9, bevel=1.0, inset=0.6, shadow_k=0.8)
    s.rgb[h_ & (np.abs(xx_ - PODX) < 0.4)] = SEAM
for yv in range(256, 272, 4):                                                        # vent louvres (hangar air handling)
    s.rgb[s.rrect(PODX - 12, yv, PODX + 12, yv + 1.2, 0.4)] = SEAM
for yv in range(232, 300, 7):                                                        # lit crew windows on the outer flank
    if abs(yv - 262) < 20: continue
    s.rgb[s.rrect(PODX - 27.4, yv - 1.6, PODX - 26.2, yv + 1.6, 0.3)] = LIT
sysl('rounded hangar pods: roof hatches, louvres, crew windows', PODX, 262)

# ================================================================ launch deck (left, mirrored): rim, graphite deck, lane, marks, lights, edge fairings
rim_ = prof(PODX, deckHW, DK0, DK1)
s.plate(rim_, AR_L*0.95, z=0.9, bevel=1.6, inset=0.8, shadow_k=0.8)
dk = prof(PODX, deckHW, DK0 + 4, DK1, 4)
s.plate(dk, DECK, z=1.0, bevel=0.8, shadow_k=0.6, outline=0.6,
        lines=[s.rrect(0, y, W, y + 0.5, 0.2) for y in (150, 180)])
lane = s.rrect(PODX - 6, 118, PODX + 6, 218, 1) & dk
s.rgb[lane] = (s.rgb[lane]/DECK.mean())*LANE.mean()*0.98
for e in (-1, 1): s.rgb[s.rrect(PODX + e*7.5 - 0.45, 118, PODX + e*7.5 + 0.45, 218, 0.2) & dk] = ROSE
for py in range(118, 196, 10): s.rgb[s.rrect(PODX - 0.5, py, PODX + 0.5, py + 4, 0.2)] = WHT*0.9          # dashed centreline
slot = s.rrect(PODX - 1.1, 130, PODX + 1.1, 190, 0.5); s.rgb[slot] = (24, 24, 30); s.z[slot] = 0.9     # catapult slot
sh_ = s.rrect(PODX - 2.6, 188, PODX + 2.6, 193, 1.0)
s.plate(sh_, AR_L, z=1.3, bevel=0.8, dome=0.3, shadow_k=0.8)                                              # catapult shuttle (parked)
for k in range(3):                                                                   # forward-pointing chevrons
    yc = 134 + k*6
    for e in (-1, 1):
        c = s.poly([(PODX, yc - 1.6), (PODX + e*9, yc + 3.2), (PODX + e*9, yc + 4.8), (PODX, yc + 0.1)])
        s.rgb[c & dk] = WHT*0.92
for py in range(124, 216, 16):                                                       # deck edge lights
    for e in (-1, 1):
        hw = float(deckHW(py)) - 3; s.rgb[s.disk(PODX + e*hw, py, 0.8)] = LIT
for e in (-1, 1):                                                                    # tube edge fairings along both deck edges
    tb = s.rrect(PODX + e*23 - 4.6, 127, PODX + e*23 + 4.6, 213, 4.4)
    s.plate(tb, AR_L, z=1.15, bevel=2.2, dome=0.8, shadow_k=0.85)
    for yv in (150, 180): s.rgb[tb & (np.abs(yy_ - yv) < 0.45)] = SEAM
sysl('launch deck: graphite, lane + rose lines, chevrons, catapult slot + shuttle, edge lights, tube fairings', PODX, 160)

# ================================================================ hangar PORTAL at the pod front: posts, dark lit bay, rose lintel, armoured hood
thr = s.rrect(PODX - 17, 191.5, PODX + 17, 194.2, 0.3)                                 # threshold stripes on the deck
for k in range(-2, 3):
    st = thr & (np.abs(xx_ - (PODX + k*7)) < 2.5)
    s.rgb[st] = (ROSE if k % 2 == 0 else WHT)*0.95
for e in (-1, 1):                                                                    # posts (the frame reaches forward of the roof)
    post = s.rrect(min(PODX + e*19, PODX + e*25.5), 196, max(PODX + e*19, PODX + e*25.5), 219, 1.2)
    s.plate(post, AR, z=3.9, bevel=1.6, dome=0.4, inset=0.7, shadow_k=0.95)
bay = s.rrect(PODX - 19, 196.4, PODX + 19, 204, 0.3)                                 # dark bay seen under the lintel, warm glow deep inside
t = np.clip((yy_ - 196.4)/7.6, 0, 1)[..., None]
s.rgb[bay] = (np.array([16, 14, 20])*(1 - t)**1.5 + np.array([150, 104, 60])*t**2)[bay]; s.a |= bay; s.z[bay] = 0.6
for yv in (198.5, 201): s.rgb[bay & (np.abs(yy_ - yv) < 0.35)] = (58, 52, 62)                    # retracted blast-door slats (seen edge-on)
for e in (-1, 1): s.rgb[s.rrect(PODX + e*18.6 - 0.6, 196.6, PODX + e*18.6 + 0.6, 203.8, 0.3)] = LIT           # lit bay edges
hood = s.rrect(PODX - 25.5, 204, PODX + 25.5, 219, 1.5)
s.plate(hood, AR, z=4.2, bevel=2.2, dome=0.5, inset=1.2, shadow_k=0.95)
roof = s.rrect(PODX - 22.5, 207.5, PODX + 22.5, 218, 1.2)
s.plate(roof, AR_L, z=4.4, bevel=1.4, dome=0.4, inset=0.7, shadow_k=0.9)
for k in (-1, 1): s.rgb[roof & (np.abs(xx_ - (PODX + k*8)) < 0.45)] = SEAM
lint = s.rrect(PODX - 26, 203.4, PODX + 26, 206.8, 0.8)
s.plate(lint, ROSE, z=4.3, bevel=1.0, dome=0.3, shadow_k=0.9)
for e in (-1, 1): s.plate(s.poly([(PODX + e*25.5, 207.5), (PODX + e*21.5, 207.5), (PODX + e*25.5, 212)]), AR_D, z=4.5, bevel=0.8, shadow_k=0.8)  # chamfers
sysl('hangar portal: armoured hood + posts, dark bay with lit edges, rose-gold lintel, threshold stripes', PODX, 208)

# ================================================================ medium composite on a rose-gold ringed sponson pad (plain swappable ring)
for (mx, my, a) in COMP[:1]:
    base = s.disk(mx, my, 15.5)
    s.plate(base, AR_D, z=2.9, bevel=1.8, inset=0.9, shadow_k=0.95)
    rr = np.hypot(xx_ - mx, yy_ - my)
    s.plate(base & (rr > 11.6) & (rr < 14.6), ROSE, z=3.1, bevel=1.2, dome=0.5, inset=0.3, shadow_k=0.9)
    well = rr < 10.6; s.rgb[well] = (40, 35, 46); s.z[well] = 2.8
    s.rgb[well & (np.abs(rr - 9.2) < 0.45)] = (70, 62, 78)                          # inner bearing ring
sysl('2 medium composite on rose-gold ringed sponsons, 200 deg arc angled 20 deg out', 24, 262)

# ================================================================ dome: base shell, rose equator band, ribs, shingled plates, crown
s.plate(dome, AR_D, z=2.6, bevel=3.0, dome=1.6, inset=2.0, shadow_k=0.95)
rim = dome & (rb > 0.935)
s.plate(rim, AR, z=2.8, bevel=1.4, inset=0.6, shadow_k=0.9, paint=[(rim & (rb > 0.972), ROSE)])
fr = lambda a_: np.abs(((ab + 90 + 180) % 360) - 180) < a_                          # angular window around the bow
NR = 16
for k in range(1, NR - 1):                                                           # armour gores between the ribs (bow gore = brow)
    a0 = -90 + (k + 0.5)*360/NR
    dang = ((ab - a0 + 180) % 360) - 180
    gore = dome & (rb > 0.655) & (rb < 0.94) & (np.abs(dang) < 180/NR + 0.4)
    s.plate(gore, AR*1.06 if k % 2 else AR*1.0, z=3.0, bevel=1.6, dome=0.3, inset=0.9, shadow_k=0.8)
for k in range(12):                                                                  # shingled crown plates: each overlaps the next
    a0 = -90 + (k + 0.5)*30
    if abs(((a0 + 90 + 180) % 360) - 180) < 30: continue
    dang = ((ab - a0 + 180) % 360) - 180
    tile = dome & (rb > 0.40) & (rb < 0.68) & (dang > -17.5) & (dang < 15.5)
    s.plate(tile, AR*1.14 if k % 2 else AR*1.08, z=3.4 + 0.02*k, bevel=1.6, dome=0.4, inset=0.9, shadow_k=0.8)
brow = dome & (rb > 0.40) & (rb < 0.94) & fr(180/NR*2 - 0.8)
s.plate(brow, AR*1.1, z=3.3, bevel=2.0, dome=0.6, inset=1.0, shadow_k=0.9, paint=[(brow & (np.abs(rb - 0.62) < 0.012), ROSE)])
for k in range(NR):                                                                  # meridian ribs (none on the bow): raised light rods
    a_ = -90 + k*360/NR
    if k in (0, 1, NR - 1): continue
    da = ((ab - a_ + 180) % 360) - 180; w_ = 57.3/np.maximum(rb*83, 1)                  # 1 sprite px in degrees at this radius
    band_ = dome & (rb > 0.655) & (rb < 0.94)
    rod = band_ & (np.abs(da) < 0.75*w_)
    s.rgb[rod] = AR_L*1.1; s.rgb[rod & (np.abs(da) < 0.25*w_)] = AR_L*1.25
    s.z[rod] = 3.25
s.rgb[dome & (np.abs(rb - 0.94) < 0.006)] = SEAM                                     # upper latitude seam
crown = dome & (rb < 0.415)
s.plate(crown, AR_L, z=4.1, bevel=2.2, dome=0.9, inset=1.2, shadow_k=0.95, paint=[(crown & (np.abs(rb - 0.375) < 0.012), ROSE)])
for k in range(8):                                                                   # crown panel seams radiating from the core hatch
    s.rgb[crown & (rb > 0.23) & (rb < 0.36) & (np.abs(((ab - (k*45 + 22.5) + 180) % 360) - 180) < 0.9)] = SEAM
sysl('plum dome: rose-gold equator band, meridian ribs, shingled crown plates, smooth bridge brow', X(-1, 50), 262)

# ================================================================ 4 mint visor bands (front = bridge, back, left, right): glass, rose frames, mullions
VIS = [(-90, 28.6), (90, 22.9), (180, 20.0), (0, 20.0)]
for (c, hl) in VIS:
    da = ((ab - c + 180) % 360) - 180
    band = dome & (rb > 0.862) & (rb < 0.925) & (np.abs(da) < hl)
    frame = dome & (rb > 0.848) & (rb < 0.94) & (np.abs(da) < hl + 1.8) & ~band
    s.plate(frame, ROSE, z=3.0, bevel=0.8, shadow_k=0.85, outline=0.5)
    gl = np.clip((rb - 0.862)/0.063, 0, 1)[..., None]
    s.rgb[band] = np.clip(MINT*(1.2 - 0.55*gl) + 0.0, 0, 255)[band]; s.z[band] = 2.9
    s.rgb[band & (np.abs(rb - 0.872) < 0.004)] = (225, 255, 250)                     # glint along the upper edge
    nm = int(round(np.radians(2*hl)/0.14))
    for k in range(1, nm):
        am = c - hl + 2*hl*k/nm
        s.rgb[band & (np.abs(((ab - am + 180) % 360) - 180) < 0.55)] = (40, 70, 70)
sysl('4 mint visor bands (bridge fwd, back, both sides), rose-gold frames + mullions; command room inside the dome', CX, 185)

# ---------------------------------------------------------------- dome volume: spherical light falloff (fore-lit) + soft sheen
nz_ = np.sqrt(np.clip(1 - rb**2, 0, 1)); nn = np.sqrt(u_**2 + v_**2 + nz_**2) + 1e-6
ndl = (-0.78*v_ + 0.62*nz_)/nn
dm = dome & s.a
s.rgb[dm] = np.clip(s.rgb[dm]*(0.88 + 0.26*ndl[dm])[:, None] + (28*np.exp(-(u_**2 + (v_ + 0.3)**2)/0.09))[dm][:, None], 0, 255)

# ================================================================ drive core petal hatch on the crown (the EL light plate)
VP.core_armour(s, CX, 248, 11, glow=(255, 190, 140), metal=AR_L*0.86, z=4.4)
for k in range(8):                                                                   # rose strips between the petals
    a = np.radians(k*45 + 22.5 + 22.5)
    x0, y0 = CX + 12.4*np.cos(a), 248 + 12.4*np.sin(a)
    s.rgb[s.disk(x0, y0, 0.9)] = ROSE
s.plate(s.disk(CX, 248, 3.4), ROSE, z=5.8, bevel=1.2, dome=0.8, shadow_k=0.8)
sysl('drive core under an armoured petal hatch on the crown', CX, 248)

# ================================================================ symmetry + lights
_h = CX*s.SS
s.rgb[:, _h:] = s.rgb[:, :_h][:, ::-1][:, :s.w - _h]; s.a[:, _h:] = s.a[:, :_h][:, ::-1][:, :s.w - _h]; s.z[:, _h:] = s.z[:, :_h][:, ::-1][:, :s.w - _h]
s.lights([(PODX, 115), (X(1, 100), 115)], [(255, 70, 60), (90, 255, 120)])
sprite = s.render()
sprite.save(_ROOT + '/ss_style/selene_ss_v4.png')
slots = [dict(px=x, py=y, size='MEDIUM', type='COMPOSITE', mount='TURRET', angle=a, arc=200) for (x, y, a) in COMP]
slots += [dict(px=x, py=y, size='SMALL', type='BALLISTIC', mount='TURRET', angle=a, arc=240) for (x, y, a) in PD]
slots += [dict(px=x, py=PORT - 4, size='SMALL', type='LAUNCH_BAY', mount='HIDDEN', angle=0, arc=0) for x in (PODX, X(1, 100))]
json.dump(dict(W=W, H=H, slots=slots, ENG=ENG, small=SMALL, lat=[]), open(_ROOT + '/ss_style/selene_ss_v4_slots.json', 'w'))
json.dump(SYSTEMS, open(_ROOT + '/ss_style/selene_v4_systems.json', 'w'))
print('ok')
