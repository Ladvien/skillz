---
name: procedural-animation-assets
description: Take any Blender-modeled asset and make it procedurally animatable in a game engine. First DECIDE how it should move (two gate questions route to one of six techniques: morph targets, skeletal+procedural drivers, vertex-shader deformation, physics, spline/path, or runtime mesh generation), then author it through BlenderMCP, export to glTF, and drive it in-engine — at any polygon budget, with an explicit low-poly path. Built around the hard constraint that glTF carries only three motion types natively (node TRS, skinning, morph weights) and everything else is rebuilt in engine code.
when_to_use: Triggers on "make this animatable", "procedural animation", "rig this to move", "morph targets" / "blend shapes" / "shape keys", "make it grow/open/bloom/wave/pulse/walk in a game engine", "drive a mesh from a parameter/one float", "low-poly version of a procedural asset", and any "Blender → glTF → Bevy/Godot/Unity/three.js" asset-authoring task. Also when someone hands you a described or reference-image asset and asks how to animate it procedurally rather than with a hand-keyed clip.
---

# Procedural animation for any Blender-modeled asset

You take an asset — described in words or a reference image, modeled in Blender — and make it
**procedurally animatable** in a game engine: its motion is generated from parameters, code, or
physics rather than a single hand-keyed clip. This skill is the method for **choosing the right
technique and executing it end-to-end**.

The workflow is always:

1. **Decide how it should move** (two gate questions → a primary technique + secondary layers).
2. **Author it in Blender, through BlenderMCP** (Blender's GUI must be running; you drive it
   over the socket at `127.0.0.1:9876`).
3. **Export to glTF**, respecting what the container can and cannot carry.
4. **Drive it in-engine** — set weights, play/pose bones, run the shader/solver.

Composition is the norm, not the exception: a walking creature stacks a skinned skeleton +
foot-IK + look-at + a spring-bone tail + ragdoll-on-death + a wind shader. Pick a **primary**
technique first, then ask which secondary layers apply.

> **BlenderMCP precondition (one path, no fallback).** All authoring happens through a running
> Blender GUI with the BlenderMCP add-on. If Blender is down, every call fails loudly at
> connect — that is correct behavior, not an error to work around. There is no offline path.
> See **Driving Blender via BlenderMCP** below.

---

## 1. Decide the motion first — two gate questions

Ask these in order. First match wins; then layer.

**Gate A — Does the topology change?** Do vertices/faces genuinely get *added or removed* as it
animates (a plant that sprouts new branches, something that shatters, accretes, or subdivides)?

- **Yes** → **runtime mesh generation** (§technique 6). It is the *only* technique that changes
  topology, and skinning/morphs cannot ride along.
- **But first check the trap:** a lot of "growth"/"unfurling" is really *fixed-topology stage
  blending* — the same mesh deforming, not new geometry. If you can model it as one mesh that
  deforms, **downgrade to morph targets** (§5). That is almost always the better answer.

**Gate B — Does it react to world state each frame?** Does the motion depend on input,
collisions, terrain, gravity, or the pose of other bones?

- **Yes** → a **runtime solver**: IK / look-at / spring bones on a skeleton (§2), physics (§4),
  or shader uniforms (§3). Reactive motion cannot be baked.
- **No** (it's a fixed, repeatable timeline) → **bake it**: a morph-weight timeline (§5), a
  skeletal or node-TRS clip (§2), or a spline baked to TRS (§5-path).

Then refine:

- **Rigid vs deforming?** A rigid sub-part rotating about a pivot (lid, door, iris petal) →
  node/bone **TRS keyframes**. A surface that bends/stretches → morph or skin.
- **Ambient-looping vs triggered-one-shot vs continuous-reactive?** Ambient surface motion over
  many instances → **vertex shader** (§3), cheapest at scale.

### The six techniques at a glance

| Technique | Topology | Reactive? | Deforms surface? | Authoring | Runtime cost | glTF |
|---|---|---|---|---|---|---|
| Morph / blend shapes | Fixed | No (weights driven) | Yes | Artist, moderate | Low–med | ★★★★★ native |
| Skeletal + drivers | Fixed | Yes (IK/constraint/spring) | Yes | Rig high, solvers reusable | Low–med | ★★★★☆ rig native, drivers rebuilt |
| Vertex-shader (live) | Fixed | Weakly (uniforms) | Yes | TA/shader, low | Very low (GPU, instanced) | ★★☆☆☆ mesh only |
| Physics | Fixed | Yes (fully) | Rigid: no · cloth/soft: yes | Setup med | High | ★☆☆☆☆ not in core |
| Spline / path | Fixed | Optional | No (whole object) | Designer, low | Trivial | ★★★☆☆ bake to TRS |
| Runtime mesh-gen | **Variable** | Sometimes | Yes (rebuild) | Programmer, high | High/spiky | ★☆☆☆☆ can't export generator |

### Routing on concrete assets

| Asset | Topology change? | Route |
|---|---|---|
| Chest opens | No | Lid = hinge → node/bone TRS keyframe clip (glTF-native); rigid-body joint only if the lid can be blocked |
| Flag waves | No | Live vertex-shader sway + pole-edge mask, instanced; cloth sim only if it must wrap/collide |
| Plant grows | Yes *if* branches appear | Real branching → runtime mesh-gen (§6); a fixed-mesh unfurl/swell → **morph stages** (§5); wind shader on top |
| Creature walks | No | Skeletal clips + foot-IK + look-at + spring bones (tail/ears) + ragdoll on death |
| Door irises open | No | One bone per petal → node/bone TRS keyframes (glTF-native, deterministic) |
| Gem pulses | No | Live vertex-shader scale/emissive pulse (cheapest), or a two-target morph with a looping weight if you need it glTF-native and art-exact |

---

## 2. What survives glTF vs what you rebuild in-engine

This is the load-bearing constraint of the whole pipeline. **glTF 2.0 animation is a keyframe
container with a closed target enum** — an animation channel can only target:

```
translation | rotation | scale | weights
```

So the container carries exactly **three native motion types**:

- **node TRS keyframes** — translation/rotation/scale on a node (covers spline-baked motion and
  rigid hinges);
- **skinning** — a `skin` (joint node list + `inverseBindMatrices`), with `JOINTS_n`/`WEIGHTS_n`
  vertex attributes at **4 influences per set**; the *motion* is just TRS keyframes on the joint
  nodes;
- **morph-target weights** — per-vertex position/normal deltas (stored as **sparse accessors**),
  blended by a weight timeline.

Interpolation is `LINEAR | STEP | CUBICSPLINE`; rotations are unit quaternions (XYZW).

| Baked **into** the glTF (authored in Blender, shipped in the file) | Rebuilt **in engine** (not in the glTF at all) |
|---|---|
| Node TRS clips; skeletal clips (= TRS keyframes on joints + skin); morph-weight clips; the morph **delta geometry** itself | Vertex-shader sway/water/pulse; IK / foot-placement / look-at; spring & jiggle bones; ragdoll / cloth / soft-body; any runtime mesh generation |
| `animation.channel` (path ∈ TRS/weights) + samplers; `skin` + sparse morph deltas | Engine systems, shaders, physics solvers — you write these |
| Rule: a *fixed timeline of numbers on TRS or morph weights* can be baked | Rule: if it *reacts to state* (input, collisions, other bones, live noise) it must be runtime |

Two corollaries that trip people up:

- **A Blender driver / constraint / IK rig is NOT procedural in the exported file.** glTF has no
  drivers. Either **bake it to keyframes** (`export_force_sampling=True`) so it becomes static
  baked data, or **export only the raw rig/mesh and reimplement the behavior in engine code**.
  There is no third path where the glTF "carries the rule."
- **Morph targets are the one place fixed-topology "procedural" geometry survives as data:** the
  *shapes* are baked deltas, but the *weight over time* can be either a baked clip or driven live
  by engine code. That's why morph is the default for grow/open/pulse-style deforms.

**Default bias for any Blender→engine asset: prefer morph targets and node/bone keyframes
wherever the motion allows.** Reach for shader/physics/live-driver motion only when the motion
is inherently reactive or ambient-at-scale — and when you do, treat it as "geometry+rig ship in
glTF, behavior is engine code."

---

## 3. The six techniques, briefly

1. **Morph targets / blend shapes.** Per-vertex position deltas, linearly interpolated by weight;
   **fixed topology**. Best for authored deterministic deforms bones can't express: faces,
   lip-sync, muscle flex, squash, pulsing, growth-as-swell, corrective shapes. Can't change
   topology; can't do large rigid rotations (verts move in straight lines, so a rotating lid cuts
   corners); not reactive on its own. glTF ★★★★★ native. **Fully worked in §5.**

2. **Skeletal + procedural bone drivers.** A skinned skeleton whose bones are driven at runtime:
   IK (reach/aim), look-at/constraints (head/turret), spring/jiggle bones (tails, hair, capes),
   foot-placement raycast+IK (plant feet on slopes). Best for articulated characters/creatures
   and hinged rigid objects that must *react*. glTF ★★★★☆ — skeleton/skin/clips are native, **but
   the drivers (IK, constraints, spring) do NOT travel in glTF; export the rig, rebuild the
   behavior in-engine** (in Bevy: write bone `Transform`s in a system ordered relative to
   `animate_targets`).

3. **Live vertex-shader deformation.** Displace verts in the vertex shader each frame from
   time/position/noise/masks — nothing baked. Best for ambient looping motion over many instances
   (wind, water, flag wave, gem pulse) that composes with GPU instancing at near-zero CPU cost.
   Can't react precisely to gameplay (uniforms only), can't change topology. glTF ★★☆☆☆ — the mesh
   and vertex-color masks export, **the shader does not**; rebuild it per engine.

4. **Physics-driven (ragdoll / rigid / cloth / soft).** A solver integrates forces/constraints
   per tick. Best for emergent, reactive, non-repeatable motion you can't pre-author (debris,
   ragdoll death, draping cloth). Most expensive; hard to network deterministically. glTF ★☆☆☆☆ —
   **not in core**; author the ragdoll/cloth setup in-engine, ship only the mesh/rig.

5. **Spline / path-based motion.** Move/orient a whole object along a parametric curve by
   advancing `t`. Best for deterministic authored trajectories (platforms, drones, cameras,
   projectiles). Transform-only (doesn't deform the mesh). glTF ★★★☆☆ — no spline primitive, but
   the *result* is node TRS over time, which **bakes to native keyframes** (you lose live curve
   editing; keep the curve in-engine if you need to tweak it).

6. **Runtime procedural mesh generation (L-system / noise).** Build/rebuild geometry at runtime
   from rules. The **only** technique that changes topology — genuine branching growth,
   destruction, accretion, per-instance variation. Spiky CPU cost; skinning/morph can't ride
   along. glTF ★☆☆☆☆ as a live technique — a generator can't be exported. **If your "growth" is
   fixed-topology, do §5 instead.**

---

## 4. Deep recipe: morph targets (the glTF-native, fully-worked path)

This is the technique with the highest glTF-portability and the one most Blender→engine deform
assets should use. The method, and the invariant that makes it work:

### One parametric generator, topology invariant across the animated parameter

Write `build(params, res)` that returns the same mesh **topology** — identical vertex count,
order, and winding — for *every* value of the animated parameter. That invariance is the
**precondition** for morph targets: a morph target is a per-vertex delta, so vertex *i* must mean
the same thing at every keyframe. You **deform** geometry as a function of the parameter; you
never add or remove it.

```python
# Language-agnostic shape. `res` is REQUIRED — see §6, poly budget.
def build(t, res):
    verts, faces, mats = [], [], []
    def ring(fn):                       # one ring of `res.SEG` verts at fixed azimuths
        base = len(verts)
        for s in range(res.SEG):
            verts.append(fn(2*math.pi*s/res.SEG, s))
        return list(range(base, base + res.SEG))
    # ... emit the SAME rings/bridges/fans every call; only vertex POSITIONS depend on t ...
    return verts, faces, mats           # faces & mats are byte-identical for all t
```

**Motion that seems to need topology change is re-expressed as continuous deformation.** The
canonical trick: geometry can't tear, so a sealing/opening motion (a chest lid, an eyelid, a
clamshell, an iris, a splitting husk) is a **lathe/loft surface whose sweep angle or a dimension
collapses** — closed at one end of the parameter, open at the other. Same topology throughout;
the *shape* opens.

### Sample keyframes → shape keys → morph targets

Pick K parameter values (the growth/open path). The **basis** (all weights 0) is the **rest /
spawn state**. In Blender, add one shape key per keyframe, writing `build(t_k, res)` positions:

```python
ob.shape_key_add(name="Basis", from_mix=False)          # basis = rest state
for t in STAGES[1:]:
    vt, ft, _ = build(t, res)
    assert len(vt) == n_basis and ft == faces_basis, "topology drifted — morph impossible"
    sk = ob.shape_key_add(name=f"key_{int(t*100):03d}", from_mix=False)
    for i, co in enumerate(vt):
        sk.data[i].co = co
```

### Drive it from one float in-engine

glTF morphs are additive: `final = basis + Σ wᵢ·(targetᵢ − basis)`. To sit between two adjacent
keyframes, set those two weights and zero the rest — **interpolate *through* the sampled path,
never endpoint-to-endpoint** (a single start→end blend takes the straight-line shortcut and can
drive one part clean through another that hasn't opened yet). At most two adjacent targets are
ever active:

```rust
// STAGE_T are the parameter values the keyframes were baked at; index 0 is the basis.
const STAGE_T: [f32; 7] = [0.0, 0.12, 0.28, 0.45, 0.62, 0.80, 1.0];

/// growth in [0,1] -> the 6 morph weights, in target order.
/// In the first segment the basis carries the remainder, so the six weights
/// sum to < 1 there. That is correct, not a bug.
fn stage_weights(growth: f32) -> [f32; 6] {
    let g = growth.clamp(0.0, 1.0);
    let mut w = [0.0; 6];
    for k in 0..6 {
        let (a, b) = (STAGE_T[k], STAGE_T[k + 1]);
        if g <= b || k == 5 {
            let u = ((g - a) / (b - a)).clamp(0.0, 1.0);
            if k > 0 { w[k - 1] = 1.0 - u; }  // stage k
            w[k] = u;                          // stage k+1
            break;
        }
    }
    w
}
```

**Bevy (0.19) specifics.** A mesh with N materials exports as one glTF mesh with N primitives; the
loader puts a `MorphWeights` on the **parent node** and gives each primitive child a
`MeshMorphWeights::Reference(parent)`. **Mutate the parent's `MorphWeights` only** — in ≤0.18
weights were copied to each child, so older examples write per-primitive weights; don't. Weights
propagate to children with a **one-frame delay**, and `MorphWeights` only exists once the scene
has finished spawning, so tolerate its absence on the first frame(s). There are **no animation
clips** in this kind of asset — you set the weights yourself each frame. Keep the target count
modest (ours uses 6, well under the engine cap — Bevy's is ≥64 and configurable).

---

## 5. Poly budget & the low-poly path

Applies to the mesh under **any** technique. The generator's `res` (segment/ring counts) is a
**required argument — never a default**: a default silently creates a second execution path, and
two paths make magic results. Low-poly is just `build(params, RES_LOW)`.

- **The binding constraint is usually ONE load-bearing knob, not a uniform downscale.** Find it —
  it's whichever knob protects a correctness property (containment: one part staying inside
  another; silhouette; a feature that must survive). Cut the rest hard and hold that one. (In the
  reference asset it was the number of *volva rings*, not the radial segment count: the seal is a
  meridian-chord problem, so radial segments were nearly free to cut while ring count was not.)
- **Faceted / flat shading splits vertices per face.** Blender's glTF exporter emits
  `4·quads + 3·tris` unshared verts for a flat mesh, so a faceted low-poly exports with *more*
  vertices than its smooth sibling of the same tri count. Expect it and **assert the count** — if
  it comes in lower, the exporter merged coplanar corners and your flat normals are wrong.
- **A faceted variant is a *style*, not automatically a silhouette-matched LOD.** Flat shading
  won't blend seamlessly with a smooth high-poly at a distance cutover. For a true LOD chain,
  build another `res` with smooth shading at an intermediate tri count.

---

## 6. Driving Blender via BlenderMCP

This skill authors assets **through the BlenderMCP server** (`ahujasid/blender-mcp`). It is
self-contained here; it does not depend on any host's private config.

**Two-process model.** A TCP server runs *inside* Blender's GUI (a Blender add-on) at
`127.0.0.1:9876`, bound to localhost only, with `listen(1)`. The stdio MCP server is the client.
Consequences:

- **Blender's GUI must be running.** If it isn't, every call fails loudly at connect. That is the
  one correct path — do not add an offline fallback.
- **One Claude Code session at a time** (`listen(1)`).

**How you actually build.** The MCP tools are your authoring surface: `get_scene_info`,
`get_object_info`, `get_viewport_screenshot`, and above all **`execute_code`** — arbitrary Python
inside the Blender process (`bpy`, `bmesh`, `mathutils`). `execute_code` is the mechanism that
makes this powerful; it can also wipe a scene or touch the filesystem, so save work before long
agentic runs. When driving the socket directly instead of via the registered MCP tools, the
protocol is a single JSON request/response:

```python
# Minimal client: JSON {"type","params"} over the socket, read until it parses, raise on failure.
import json, socket
def call(cmd, params=None, timeout=600):
    s = socket.create_connection(("127.0.0.1", 9876), timeout=timeout); s.settimeout(timeout)
    s.sendall(json.dumps({"type": cmd, "params": params or {}}).encode())
    buf = b""
    while True:
        chunk = s.recv(1 << 20)
        if not chunk: break
        buf += chunk
        try: json.loads(buf.decode()); break
        except json.JSONDecodeError: continue
    s.close()
    resp = json.loads(buf.decode())
    if resp.get("status") != "success":
        raise RuntimeError(f"Blender returned: {resp}")   # fail loudly, no fallback
    return resp.get("result", {})
def run(code, timeout=600):
    return call("execute_code", {"code": code}, timeout=timeout)
```

**Health checks.** `ss -lntp | grep 9876` (expect a `127.0.0.1:9876` listener — never `0.0.0.0`)
and `claude mcp list` → `blender … ✔ Connected`. Verify a real round trip: `get_scene_info`, an
`execute_code` that adds a cube, then `get_viewport_screenshot` to confirm it appears.

**Setup, pinned — pin both halves.** The PyPI sdist ships **only the server**; the add-on
(`addon.py`) lives **only in git**, so "latest add-on + latest server" is not a coherent pair and
drifts silently. Install the add-on from a **git checkout of a known SHA** into
`scripts/addons/` (do not `curl` `raw.githubusercontent.com` — it rate-limits to a 199-byte HTTP
429 page named like the real file), enable it headlessly, and register the server as
`uvx blender-mcp@<pinned-version>`.

**Telemetry off at BOTH kill switches** (server and Blender are separate processes; upstream
defaults telemetry **on** and uploads prompts, generated code, and viewport screenshots):

- add-on preference `telemetry_consent = False` (persisted in `userpref.blend`);
- server env `BLENDER_MCP_DISABLE_TELEMETRY=true`.

Confirm from the server's startup log line: `Telemetry disabled via environment variable`.

**Modelling gotchas that each cost a wasted render:**

- `primitive_cube_add(size=1)` already spans `-0.5..0.5`, so **extent == scale** — scaling by
  `size*0.5` silently halves every dimension.
- Objects sharing one mesh datablock: `obj.active_material` writes to the **mesh**, so the last
  assignment wins for all of them. For per-object colour set `material_slots[0].link = "OBJECT"`
  first.
- Parenting: `matrix_parent_inverse = parent.matrix_world.inverted()` **cancels** the parent
  transform (and `matrix_world` is stale until the depsgraph updates). To make a child follow a
  parent, use `Matrix.Identity(4)` and local coordinates.

---

## 7. Export flags that bite

Real flag names and defaults for `bpy.ops.export_scene.gltf`:

- **Morph:** `export_morph=True`, `export_morph_normal=True`. ⚠️ **`export_apply=False` — turning
  it on silently deletes every shape key** (it applies modifiers, which is incompatible with
  morph export). This is the single most damaging default to get wrong.
- **Skin:** `export_skins=True`, `export_all_influences=False` (clamps to 4 influences/vertex,
  which is what most engines read).
- **Animation / drivers:** `export_animations=True`, and **`export_force_sampling=True`** — this
  is what **bakes drivers / constraints / IK into keyframes**. Without it, glTF (which has no
  drivers) drops that motion entirely.
- **Always:** `use_active_scene=True` — without it the exporter walks **every scene in the
  .blend** and drags in unrelated geometry. `export_yup=True` (Blender is Z-up; glTF/Bevy/Godot/
  three.js are +Y-up).
- **Watch the types:** `export_vertex_color` (default `'MATERIAL'`) and `export_animation_mode`
  (default `'ACTIONS'`) are **enums, not booleans** — passing `True`/`False` misbehaves.

---

## 8. Verify — numbers *and* eyes

- **Invariants as a runnable script that prints magnitudes, not booleans.** A boolean gated on a
  magic tolerance hides regressions. Print mm of clearance, mm of height change, etc., and check
  the number. For a topology-invariant generator, assert: identical topology across the parameter;
  any containment property (part A stays inside part B); monotonic silhouette where required.
- **Test against the geometry the generator actually emits (the inscribed polytope), not the
  analytic ideal it samples.** They diverge as resolution drops — an analytic check passes a
  low-poly mesh that visibly fails.
- **Then render it and LOOK.** The canonical war story: a self-intersection (a bulb poking through
  a sac) passed *every* numeric check that existed at the time and was visible only in the render.
  Numbers are necessary, not sufficient.
- **Confirm the motion is really in the exported file.** Decode the `.glb`, rebuild each keyframe
  from `basis + delta` (morph deltas are sparse accessors — handle that), and check the result. A
  clean export log proves nothing; the reconstructed geometry does.

---

## 9. One path

Per the universal rule: **one execution path per feature, no fallbacks, no defaults that fork
behavior.** `res` is required. Blender-down fails at connect. Bad export flags fail the verify
step. When the primary path can't produce a usable result, fail loudly — never write a degraded
substitute.

---

## Reference implementation

`/mnt/codex_fs/game_assets/models/props/death_cap_procedural/` is a fully-worked, verified
instance of the **morph-target recipe** (§4–§5): one fixed-topology generator, growth baked as 6
glTF morph targets, exported at two polygon budgets (2,400-tri smooth and 396-tri faceted), driven
in Bevy by one `growth` float. Read it as *one concrete example of §4*, not as the subject of this
skill:

- `src/mushroom_gen.py` — `build(t, res)` with topology invariant across `t`; the
  sweep-angle-collapse trick; the required-`res` floors.
- `src/verify_gen.py` — the invariants as magnitude-printing checks against the emitted polytope.
- `src/mushroom_asset.py` — shape-key bake + glTF export with the flags above.
- `src/inspect_glb.py` — decode + reconstruct-from-deltas verification.
- `CLAUDE.md` — the per-asset operating manual (contract, Bevy usage, invariants, gotchas).
