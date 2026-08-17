# Blog 4 — Information Causality: Working Notes (v2)

*Project seed. Extends and corrects the first-pass notes. Verified numerical
anchors are flagged ✓. Claims still needing a primary-source check are flagged
⚠ and collected in §15.*

---

## Working role in the series

Blog 3 (the geometry post) establishes the shapes in RAC advantage space:
the classical cross-polytope, the quantum sphere, the no-signalling cube.
Blog 4 picks up there and asks the harder question:

> **Why does quantum theory stop at the sphere?**

Information causality (IC) is one proposed answer. The post should *not* present
it as a settled explanation. The more honest — and more interesting — story is to
work through the argument, visualize it geometrically, show *why* it recovers the
Tsirelson threshold, and then be explicit about what it leaves open.

The personal angle stays: the initial hope was that IC might *explain the sphere*.
Looking at the geometry carefully makes that reading less obvious. That tension is
the spine of the post, and it should be introduced honestly rather than resolved
prematurely.

**One framing to hold onto throughout.** Blog 3 already separated two independent
facts (see `rotations_advantage_space_summary.md`, Part VIII): the cube comes from
*binary-tree combinatorics alone*, and the sphere comes from *inner-product
structure alone*. Neither premise assumes the other. IC should be read against that
backdrop — it is a candidate *dynamical* reason the world sits on the sphere rather
than the cube, and Blog 4's job is to test how much of that "why" IC actually
delivers.

---

## Working title

### Why Does Quantum Theory Stop at the Sphere?

**Subtitle candidates:**
- *We know what lies beyond the quantum boundary. Explaining why nature refuses to go there is harder than it looks.*
- *Information causality finds the right threshold. Whether it explains the shape is a subtler question.*

IC-section heading: **Does Information Really Explain the Quantum Limit?**

---

# 1. Start from the geometry

Use the RAC bias/advantage coordinate from Blog 3:

\[
c_i = 2P_i - 1, \qquad c_i \in [-1,1].
\]

The reader already knows three regions in this space:

- **Classical:** the cross-polytope \(\sum_i |c_i| \le 1\) (flat faces).
- **Quantum:** the Euclidean ball \(\sum_i c_i^2 \le 1\) (curved) — for the pyramid
  RAC construction of Blog 3.
- **No-signalling / perfect random access:** the hypercube \(|c_i| \le 1\)
  (flat faces).

Blog 4 introduces a **fourth** shape: the **information-causality entropy body**,
the region carved out by the direct IC inequality below.

**Keep the Blog 3 caveat visible.** The "quantum sphere" here is the boundary the
*pyramid family lies on and fills* — proved in Blog 3 by the even-error product law
plus surjectivity of hyperspherical coordinates. That the sphere is the *actual
Tsirelson boundary* (nothing reaches strictly outside) is still the one open seam
in Blog 3, supplied externally by Tsirelson's theorem. Blog 4 does not close that
seam; it studies a *different* boundary (the entropy body) and how it relates to
the sphere.

---

# 2. The information-causality quantity

Setup. Alice holds \(N\) independent uniform bits. Bob chooses one index \(i\),
Alice sends **one** classical bit, and Bob outputs a guess \(\beta_i\) for \(a_i\).

Information causality imposes

\[
\sum_i I(a_i : \beta_i) \le 1,
\]

i.e. the total accessible information cannot exceed the one transmitted bit.

For an unbiased source bit and a symmetric binary guess with success probability
\(P_i\),

\[
I_i = 1 - h(P_i),
\]

with \(h\) the binary entropy. Using \(P_i = \tfrac{1+c_i}{2}\), the direct
constraint becomes

\[
\boxed{\;\sum_i\Big[1 - h\!\big(\tfrac{1+c_i}{2}\big)\Big] \le 1\;}
\qquad\Longleftrightarrow\qquad
\sum_i h\!\big(\tfrac{1+c_i}{2}\big) \ge N-1.
\]

⚠ **Correction / precision (was stated too loosely in v1).** This inequality is the
IC bound *specialized to a symmetric binary channel with symmetric decoding*. In
the general case the honest statement is:

- IC proper is the bound on the **mutual-information sum** \(\sum_i I(a_i:\beta_i)\le 1\),
  which Pawłowski et al. derive from the data-processing / chain-rule structure of
  a physically transmitted bit.
- \(\sum_i[1-h(P_i)] \le 1\) coincides with that bound **only** when each channel is
  the symmetric binary one and the guess is the optimal symmetric decoder. Then
  \(I(a_i:\beta_i) = 1 - h(P_i)\) exactly.
- For asymmetric or non-binary decoding, \(1 - h(P_i)\) is a **Fano-type lower
  bound** on \(I_i\) (equivalently an upper bound on error), and the boxed
  inequality is a *necessary* condition, not an identity. Do not present it as "the"
  IC boundary without this qualifier. (⚠ verify exact conditions — §15.1.)

For the symmetric RAC strategies this post cares about, the boxed form is exact, so
it is the right object to plot.

---

# 3. A fourth geometric object (N = 2)

Plot four nested regions in the same \((c_1,c_2)\) plane:

1. classical diamond \(|c_1|+|c_2|\le 1\);
2. quantum circle \(c_1^2+c_2^2 \le 1\);
3. IC entropy boundary \(h(\tfrac{1+c_1}{2}) + h(\tfrac{1+c_2}{2}) = 1\);
4. no-signalling square \(|c_i|\le 1\).

The entropy contour is a rounded, square-ish curve sitting **outside** the quantum
circle but **inside** the no-signalling square.

**The key visual point:**

> **The quantum boundary is *not* the direct information-causality boundary.**

On the diagonal \(c_1 = c_2 = c\):

- quantum: \(c_Q = 1/\sqrt2 \approx 0.7071\) ✓
- direct entropy boundary: \(c_{MI} \approx 0.7799\) ✓ (solves \(h(\tfrac{1+c}{2}) = \tfrac12\))

The four regions all coincide on the coordinate axes, e.g. at \((1,0)\): one bit
known perfectly, the other not at all. That axis-touching is worth calling out —
it's where "spend everything on one question" makes all four physics regimes agree.

✓ Both diagonal numbers reproduced numerically (0.7071 and 0.7799).

**Figure (probably the central one of the post):** diamond + circle + entropy
contour + square, with the diagonal quantum point (0.707) and MI point (0.780)
annotated. This makes the conceptual gap visible at a glance.

---

# 4. First surprise: quantum mechanics does not use the full MI budget

At the symmetric quantum point in \(N\) dimensions, \(c_i = 1/\sqrt N\). The direct
information sum is

\[
I_N = N\Big[1 - h\!\big(\tfrac{1 + 1/\sqrt N}{2}\big)\Big].
\]

Using the small-bias expansion

\[
1 - h\!\big(\tfrac{1+c}{2}\big) = \frac{c^2}{2\ln 2} + O(c^4),
\]

we get

\[
I_N \longrightarrow \frac{1}{2\ln 2} \approx 0.7213, \qquad \text{not } 1.
\]

✓ Constant reproduced (0.72135).

So even asymptotically the symmetric quantum point **leaves ~0.28 bits on the
table**. The direct entropy body is genuinely larger than the quantum sphere;
along its large-\(N\) diagonal its Euclidean radius tends to

\[
\sqrt{2\ln 2} \approx 1.1774,
\]

versus radius 1 for the quantum sphere. ✓

**Consequence to state plainly:** the MI shape does **not** converge onto the
quantum sphere. If IC "explained the sphere" in the naive sense, these two bodies
would coincide in the symmetric limit. They don't.

---

# 5. So how does Pawłowski actually recover Tsirelson?

Through **concatenation**, not through the single-shot boundary of §3.

Take an elementary isotropic box of strength \(E\). Build the RAC pyramid: after
\(k\) levels,

\[
N = 2^k, \qquad c_i = E^k,
\]

and still **one** noiseless classical bit is sent. (This \(c_i = E^{\log_2 N}\) is
exactly the pyramid advantage law from Blog 3, `pyramid_sphere_proof_addition.md`
and the even-error product law — the same \(E^{\log_2 n}\) appears there.)

The information associated with Bob's possible guesses is

\[
I_k = 2^k\Big[1 - h\!\big(\tfrac{1+E^k}{2}\big)\Big].
\]

As \(k \to \infty\), \(E^k \to 0\) for every \(E < 1\), so the quadratic expansion
applies to each term:

\[
I_k \sim \frac{2^k E^{2k}}{2\ln 2} = \frac{(2E^2)^k}{2\ln 2}.
\]

Three regimes:

\[
E < \tfrac{1}{\sqrt2} \Rightarrow I_k \to 0, \qquad
E = \tfrac{1}{\sqrt2} \Rightarrow I_k \to \tfrac{1}{2\ln2}, \qquad
E > \tfrac{1}{\sqrt2} \Rightarrow I_k \to \infty.
\]

So any correlation even slightly above Tsirelson eventually violates \(I_k \le 1\).
That is the original Pawłowski scaling argument. ⚠ (verify exact concatenation
derivation and that the \(2E^2 > 1\) criterion is stated this way — §15.3.)

**Note for accuracy:** the source EARAC paper (Pawłowski–Żukowski, arXiv:0906.0524)
is the RAC construction being leaned on for the pyramid; the IC bound itself is
Pawłowski–Paterek–Kaszlikowski–Scarani–Winter–Żukowski, *Nature* **461**, 1101
(2009) (ref. [13] in the EARAC paper). Keep the two citations distinct — v1 blurred
them.

---

# 6. Connection to the existing scaling argument

This is the *same* critical scaling already in the RAC analysis. The pyramid bias

\[
A_{\rm pyr}(N,E) = E^{\log_2 N} = N^{\log_2 E}.
\]

The critical exponent is where this decays as \(N^{-1/2}\):

\[
\log_2 E = -\tfrac12 \iff E = \tfrac{1}{\sqrt2}.
\]

IC sees the same transition because information is quadratic in small bias,
\(I \propto c^2\), so

\[
N c^2 = N E^{2k} = (2E^2)^k,
\]

which is exactly the competition between the number of questions (\(2^k\)) and the
information per answer (\(E^{2k}\)).

Framing line:

> **Tsirelson appears as a scaling transition.** Below \(1/\sqrt2\), concatenation
> kills the information faster than questions accumulate. Above it, questions
> outrun the decay of each answer's information.

---

# 7. The geometric reservation (the heart of the post)

IC does **not** globally reproduce the quantum sphere. Instead the argument runs:

1. the direct finite-\(N\) entropy surface lies *outside* the sphere (§3–4);
2. concatenation drives the final biases \(E^k \to 0\);
3. near zero bias, binary entropy is quadratic;
4. the quadratic term is Euclidean, producing \(\sum_i c_i^2\)-type behaviour.

So the threshold emerges **in a limit where the relevant RAC point approaches the
origin** — the point of near-total ignorance.

Informal intuition:

> We start with a visibly non-spherical entropy surface. Concatenation zooms
> farther and farther into its centre, until only its quadratic curvature remains.

⚠ **Important refinement (keep this — v1 had it right).** Don't say "anything looks
like a sphere when it shrinks to a dot." That's false in general. The correct
statement: *a smooth, sign- and permutation-symmetric information surface with an
isotropic Hessian at the origin looks Euclidean to second order there.* The
isotropy is doing real work and should be named, not smuggled in.

This motivates the genuine question:

> Does IC explain the **global quantum sphere**, or only pin down its **critical
> scaling threshold** (the radius/exponent) via local quadratic geometry?

---

# 8. Open question 1 — what information does Bob actually have?

The IC quantity \(\sum_i I(a_i : \beta_i)\) sums information over *different choices*
of requested index. But Bob executes only **one** decoding and gets **one** output.
The sum is therefore something like **potentially accessible information across
mutually exclusive choices**, not a single record simultaneously held.

The original motivation is sound: a theory-independent \(I(\mathbf a : X, B)\) with
an arbitrary post-quantum system \(B\) is hard to define, so IC builds an
operational quantity purely from classical inputs and outputs. That is a feature,
not a bug — but it does mean the summed quantity deserves scrutiny.

The conceptual question (pose, don't "resolve"):

> **Is the sum of mutual informations over mutually exclusive decoding choices the
> uniquely natural measure of what Bob has gained?**

Sharper:

> Bob chooses which question to ask but cannot receive all the answers. In what
> sense should their mutual informations be *added*?

⚠ Distinguish clearly: this is conceptual discomfort about *interpretation*, **not**
a claim that the IC mathematics is wrong. The IC derivation of the bound is valid;
the question is what the bound *means*.

---

# 9. Open question 2 — why does quantum theory leave information on the table?

If IC permits \(\sum_i I_i \le 1\), why does the symmetric quantum strategy reach
only \(\approx 0.7213\) bits asymptotically? The ~0.28-bit gap suggests the direct
IC budget is **not** the thing that fixes the quantum boundary — something stronger
(operator-algebraic Tsirelson structure, or an as-yet-unnamed principle) sets the
sphere, and IC only certifies the threshold along the concatenation direction.

Reader-facing:

> If one transmitted bit permits up to one bit of potentially accessible
> information, why does quantum mechanics stop near 0.72 bits in the symmetric
> limit? What structural principle does the remaining work?

---

# 10. Open question 3 — what does the asymptotic proof really explain?

The theorem is strong: every isotropic \(E > 1/\sqrt2\) eventually violates IC under
deep enough concatenation. But interpretively, as \(k \to \infty\), \(E^k \to 0\),
so the proof probes a vanishing neighbourhood of complete ignorance, where Shannon
entropy is forced to its quadratic Taylor term.

Personal passage:

> This is where I'm still unsure what to make of it. IC finds exactly the right
> threshold — but only after repeatedly shrinking the individual advantages toward
> zero, until nothing survives but the quadratic curvature of Shannon entropy. Is
> that telling us the quantum advantage space is *globally* spherical? Or has it
> found the right radius through a scaling argument that never actually sees the
> sphere?

Good place to invite substantive reader responses.

---

# 11. Later literature: remove concatenation, keep the infinitesimal limit

Miklin & Pawłowski (and related follow-ups) reach the Tsirelson constraint
**without** an infinitely concatenated pyramid, using an increasingly **noisy
classical channel** instead. This removes the "monstrous construction" objection —
but still approaches a **zero-information / zero-capacity limit**, so the same local
quadratic behaviour of binary entropy remains central.

Line for the post:

> We can get rid of the infinite pyramid. But do we get rid of the infinitesimal
> argument?

⚠ Check the exact Miklin–Pawłowski formulation and the precise role of the
zero-capacity limit before asserting this (§15.6). Don't overstate that the noisy-
channel route "avoids" the local-quadratic regime — the current reading is that it
*relocates* it rather than removing it.

---

# 12. Visual sequence

**Figure A — Four shapes for N = 2 (the key IC figure).** Overlay diamond, circle,
entropy contour, square. Mark diagonal intersections: quantum \(0.707\), MI
\(0.780\). This is the single most important image.

**Figure B — The entropy hypershape for N = 3.** A 3D section showing the entropy
body is a genuine family of hypershapes, not a one-off 2D curve. Compare with
sphere and cube in the same axes.

**Figure C — Concatenation / scaling schematic.** Show \(E \to E^2 \to E^3 \to
\cdots\) against \(2 \to 4 \to 8 \to \cdots\) available questions, emphasizing the
competition \((2E^2)^k\). Three-regime fan-out around \(E = 1/\sqrt2\).

**Figure D — Zoom into the MI boundary.** Global entropy contour, then progressive
zoom to the origin; after symmetry normalization it becomes indistinguishable from
an ellipse/circle. This is the visual backbone of the §7 reservation. Consider
overlaying the osculating circle at the origin to make "isotropic Hessian" concrete.

---

# 13. Tone

Respectful of IC as an important, clever result. The aim is **not** "IC is wrong."
The honest arc:

- the mathematics is compelling and the Tsirelson threshold genuinely emerges;
- the geometric interpretation is subtler than expected;
- the operational "potentially accessible information" raises a real conceptual
  question;
- quantum mechanics does **not** saturate the direct MI boundary;
- the asymptotic proof lives in a regime where entropy is locally quadratic;
- so it is fair to ask *what part* of the global quantum geometry IC explains.

Keep the author's questions typographically or rhetorically distinct from
established results.

---

# 14. Possible ending

> Information causality gets something remarkable exactly right. Push the
> correlations even infinitesimally past the quantum threshold and, with a large
> enough random-access code, the information accounting eventually breaks.
>
> What I'm less sure about is what this says about the sphere itself. The direct
> information boundary isn't spherical. Quantum mechanics doesn't fill it. And the
> proof reaches the quantum threshold only after the individual advantages have
> shrunk to nothing, where Shannon entropy has forgotten everything except its
> quadratic curvature.
>
> Maybe that's the deep point. Maybe the sphere is a shadow of some stronger
> structure that information causality sees only edge-on.
>
> I don't know. If there's a better way to read this argument, I'd like to hear it.

---

# 15. Claims to verify before publication

1. **Exact status of \(\sum_i[1-h(P_i)] \le 1\).** When it is the exact IC bound
   (symmetric binary channel, optimal symmetric decoder → \(I_i = 1-h(P_i)\)) vs.
   when it is only a Fano-type *necessary* condition. State the qualifier in §2.
2. **Pawłowski et al. wording** around "potentially available / accessible"
   information — quote the concept faithfully (short paraphrase, not verbatim).
3. **Original concatenation derivation** of the \(2E^2 > 1\) criterion (EARAC /
   *Nature* IC paper) — confirm the \((2E^2)^k\) form and the three regimes.
4. **Anisotropic version:** whether tilting gives a clean quadratic condition in
   the elementary two-bias space (connects to Blog 3's anisotropic pyramid; the
   even-error product law says per-box advantages multiply, so check the IC sum
   over a tilted tree).
5. **Later literature** — exact claims about whether IC singles out the *full*
   quantum set beyond the isotropic/Tsirelson case, or only the symmetric threshold.
6. **Miklin–Pawłowski noisy-channel derivation** and the precise role of the
   zero-capacity limit; confirm whether it truly removes the local-quadratic
   dependence or merely relocates it.
7. **Do not claim** IC globally generates the quantum sphere unless a source
   establishes that stronger statement. Current best reading: it does not.

### Verified numerically in these notes (✓)
- \(c_{MI}\) diagonal, \(N=2\): **0.77994** (solves \(h(\tfrac{1+c}{2})=\tfrac12\)).
- \(c_Q\) diagonal: **0.70711** \(=1/\sqrt2\).
- Symmetric quantum info limit: \(1/(2\ln2) =\) **0.72135**.
- Large-\(N\) MI diagonal radius: \(\sqrt{2\ln2} =\) **1.17741**.

---

## One-sentence spine

> **Information causality does not draw the quantum sphere directly; concatenation
> turns the sphere's *radius* into a critical scaling threshold — an elegant result
> that leaves open why the full quantum boundary is spherical at all.**

---

## Appendix — how this connects to the rest of the project

- **Blog 3 / `rotations_advantage_space_summary.md`:** supplies the sphere, the
  even-error product law (\(c_i = \prod \cos\theta_\ell\)), and the independent
  cube-vs-sphere derivation. Blog 4's entropy body is the *fourth* shape layered on
  that picture. The open "tightness" seam in Blog 3 (is the sphere the true
  Tsirelson boundary?) and Blog 4's open question 2 (why 0.72, not 1?) are
  plausibly the *same gap* viewed from two sides — worth a cross-reference.
- **EARAC paper (arXiv:0906.0524):** the pyramid/concatenation machinery and the
  \(p = \tfrac12(1 + 1/\sqrt n)\) ceiling; its ref. [13] is the IC *Nature* paper
  this post is built on. Its eq. (12), \(K(1-h(p_K)) \le 1\), is literally the
  single-shot IC inequality for a \(K\)-bit string — cite it as the bridge.
- **`06_Open_Questions.md` item 7 / IC connections in `00_Master_Index.md`:** Blog 4
  is the natural place to seed the "Connections to Information Causality" theme.