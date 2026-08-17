# Why Isn’t Nature More Quantum?

### *Stronger-than-quantum correlations obey causality. Information theory may explain why Nature still refuses to use them.*

<!--
BLOG 4 SKELETON

Overall arc:
We ended Blog 3 with the remarkably simple quantum sphere. Start by asking
whether this sphere is really the maximum. It is not: information theory
allows a larger region at finite n, and no-signalling correlations can go
far beyond quantum mechanics, all the way to the PR-box extreme.

Then make the key turn: although the finite-n MI shape leaves room outside
the quantum sphere, concatenation changes the story. Any fixed correlation
strength E > 1/sqrt(2) eventually violates the mutual-information bound for
a sufficiently large RAC. This motivates Information Causality.

Do not end by presenting IC as a solved explanation. Question what the sum
of mutual informations means operationally, and question how much explanatory
weight to put on an asymptotic limit where the individual guessing advantages
vanish. End by opening the door to other proposed principles and the
geometric/symmetry perspective for a later post.

Tone:
Investigation rather than textbook explanation. We discover the apparent
freedom beyond quantum first; Information Causality arrives later as a
possible answer. The final section reopens the question.
-->


## Is This Really the Limit?

<!--
KEY GOAL:
Reconnect directly to the ending of Blog 3. We found the quantum sphere /
hypersphere in advantage space. It is beautifully simple, but nothing shown
so far proves that Nature has to stop there.

Introduce the mutual-information condition geometrically. For a coordinate
advantage c_i, P_i = (1+c_i)/2 and the binary mutual information is
I_i = 1 - h_2(P_i). The surface sum_i I_i = 1 defines another shape.

Start with n=2 because the geometry is immediately visible. The classical
diamond lies inside the quantum circle, while the MI boundary lies farther
out in most directions. The quantum circle is therefore NOT simply the
largest shape compatible with this finite-n information bound.

Then use n=3 (2D sections first, optionally the full 3D rendering) to show
that this is not an accident of two dimensions.

Important conceptual distinction:
Call this the "mutual-information bound used in Information Causality" or
similar at this stage. Do not yet present the full Information Causality
principle; that comes later.
-->

> **Stronger-than-quantum does not automatically mean stronger-than-causality.**

<!-- Figure: Blog4_Figure_MI_n2(1).png -->

*Figure 1: Classical, quantum and mutual-information boundaries for the two-bit guessing game. The classical strategies form the inner diamond and the quantum strategies reach the circle. The mutual-information bound extends beyond the quantum circle in most directions.*

**Alt text:** Two-dimensional advantage-space diagram for a two-bit guessing game. A classical diamond lies inside a quantum circle, while a larger rounded mutual-information boundary surrounds the circle except where the boundaries meet along special directions.

<!-- Figure: Blog4_Figure_n3_2D_cross_sections_classical_quantum_MI_symmetric.png -->

*Figure 2: Two cross-sections through the three-dimensional advantage space for n = 3. The classical polytope, quantum sphere and mutual-information boundary produce visibly different shapes. In particular, the mutual-information boundary leaves room beyond the quantum sphere at finite n.*

**Alt text:** Two two-dimensional cross-sections through the n equals 3 advantage space, comparing the classical polytope, the circular cross-section of the quantum sphere and the larger mutual-information boundary.

<!--
OPTIONAL FIGURE:
Blog4_Figure_n3_classical_quantum_mutual_information_3D.png

Use only if the 3D shape materially helps the narrative. Figure 2 is probably
the stronger teaching figure; the 3D rendering can then show what the full
mutual-information body looks like.
-->

*Figure 3: The same comparison in the full n = 3 advantage space. The quantum boundary is a sphere, while the mutual-information condition defines a larger, distinctly non-spherical body.*

**Alt text:** Three-dimensional advantage-space rendering for n equals 3 showing the classical polytope, the quantum sphere and a larger rounded mutual-information surface surrounding the quantum sphere in most directions.*


## Beyond Quantum Mechanics

<!--
KEY GOAL:
Ask the obvious question created by the figures: if information theory leaves
space outside the quantum sphere, could we actually go there?

Introduce Popescu-Rohrlich / PR-box-type correlations as hypothetical
post-quantum resources. At the extreme, Bob can retrieve whichever requested
bit he chooses perfectly, giving the hypercube |c_i| <= 1.

The surprise is NOT merely that these objects are mathematically definable.
They can respect no-signalling: Alice cannot use the box to send an
instantaneous message to Bob. So relativity/no-superluminal-signalling alone
does not recover the quantum boundary.

Use Scarani [2] as the main accessible reference for the PR-box discussion.
Mention Popescu and Rohrlich historically in the prose.

Be precise:
Prefer "no-signalling" over a broad claim that PR boxes satisfy every notion
of causality or every other fundamental physical principle.
-->

<!--
Possible transition:
So the sphere is not the edge of what probability allows, and it is not even
the edge of what no-signalling allows. This triggers the question: why does
Nature stop there?
-->


## When the Game Gets Bigger

<!--
KEY GOAL:
This is the central reveal of the post.

Move from geometry at one fixed n to scaling under concatenation. For the
isotropic correlation strength E, concatenating the basic protocol gives
individual advantages that scale as powers of E. At the quantum/Tsirelson
value E = 1/sqrt(2), the scaling matches the information-theoretic threshold.

If E is fixed even slightly above 1/sqrt(2), the individual advantages still
go to zero as n grows, but too slowly. Eventually there is some sufficiently
large n for which the sum of binary mutual informations exceeds one bit.

This resolves the apparent tension in the finite-n figures:
for every small finite n there is visible MI room beyond the quantum sphere,
but no fixed superquantum E can remain inside the MI bound for arbitrarily
large concatenated games.

The n=4 figure can be used here as the bridge from the pictures to the
higher-dimensional argument. Do not imply that n=4 itself proves the
asymptotic result.
-->

> **Go even slightly beyond the quantum boundary, and eventually there is a guessing game large enough for information theory to object.**

<!-- Figure: Blog4_Figure_n4_classical_quantum_mutual_information_cross_sections.png -->

*Figure 4: Four three-dimensional cross-sections through the n = 4 advantage space. The classical boundary depends strongly on the direction of the cut, while the quantum hypersphere remains geometrically simple. The mutual-information boundary again extends beyond the quantum boundary at finite n.*

**Alt text:** Four three-dimensional cross-sections through a four-dimensional advantage space for n equals 4, comparing the faceted classical region, spherical quantum cross-sections and larger rounded mutual-information boundaries.

<!--
Potential mathematical spine:

P_i = (1 + c_i)/2

I_i = 1 - h_2(P_i)

sum_i I_i <= 1

For the symmetric concatenated protocol:
c_i = E^k,  n = 2^k

At E = 1/sqrt(2):
c_i = 1/sqrt(n)

For E > 1/sqrt(2), the total MI eventually exceeds 1.

Keep the main prose intuitive. The exact expansion near c=0 can be introduced
later when discussing the large-n reservation.
-->


## Information Causality

<!--
KEY GOAL:
Only now name the principle.

Introduce Pawlowski et al. [1]. Alice has n independent bits, sends m
classical bits (m=1 in our game), and Bob chooses which bit he wants to
guess. Information Causality requires the sum of the information obtainable
about the individual bits to be no larger than the communicated information.

For our one-bit game:
sum_i I(a_i : beta_i) <= 1.

Explain why this is attractive:
- classical physics respects it;
- quantum mechanics respects it;
- sufficiently strong post-quantum correlations violate it;
- the concatenation argument identifies E=1/sqrt(2) asymptotically.

This is the moment where it can look as though we have found the answer to
the title: perhaps Nature is not "more quantum" because stronger correlations
would violate a fundamental principle about information.

But do not oversell this. Set up the final section with a question.
-->


## Is This Really the Answer?

<!--
KEY GOAL:
Personal / critical section. Do not attack IC; ask what exactly it explains.

Reservation 1 — the meaning of the MI sum:
Bob chooses which bit he wants and performs the corresponding decoding.
He does not simultaneously possess all n decoded bits. The IC quantity sums
mutual informations associated with alternative choices. Ask whether we
should interpret this sum as literally "the information Bob has", or as a
counterfactual measure of what he could retrieve under different choices.

Reservation 2 — the asymptotic limit:
The sharp Tsirelson result comes from n -> infinity. At the same time the
individual advantages c_i -> 0 and P_i -> 1/2. We are distinguishing theories
through increasingly tiny improvements over chance.

Reservation 3 / geometric observation:
Near c=0 the binary mutual information has a quadratic leading term,
so the MI boundary becomes locally spherical after the appropriate scaling.
Do NOT say generically that "everything becomes a sphere." Phrase this as a
question: how much of the spherical asymptotic geometry is specifically
quantum, and how much follows from the local quadratic form of the information
measure itself?

Then broaden carefully:
IC is not the only proposed reason for excluding post-quantum correlations.
Communication-complexity arguments [3,4] and principles such as Macroscopic
Locality [5] constrain the post-quantum region from different directions.

Connect this to the next post:
some alternative approaches may be closer to geometry, consistency or
symmetry than to information as the fundamental principle. This connects
naturally to the symmetries identified in the earlier guessing-game posts.

End OPEN. Do not conclude that IC is wrong, nor that another principle is
correct. The question "Why isn't Nature more quantum?" remains alive.
-->

> **But does Information Causality explain the quantum boundary — or merely describe it from another direction?**

<!--
Possible final thought, to be written in the finished article rather than
copied mechanically:

Information Causality gives us something remarkable: move even slightly
beyond the quantum correlation strength and, somewhere in a sufficiently
large guessing game, information theory objects. Whether that tells us why
Nature chose the quantum boundary is a different question.

Perhaps the sphere is telling us something fundamental about information.
Or perhaps Information Causality is seeing the shadow of a deeper geometric
or symmetry principle. That is where we can look next.
-->


## References

[1] M. Pawłowski, T. Paterek, D. Kaszlikowski, V. Scarani, A. Winter and M. Żukowski, “Information Causality as a Physical Principle,” *Nature* **461**, 1101–1104 (2009). https://doi.org/10.1038/nature08400

[2] V. Scarani, “Feats, Features and Failures of the PR-box,” *AIP Conference Proceedings* **844**, 309 (2006). https://doi.org/10.1063/1.2219371

[3] W. van Dam, “Implausible Consequences of Superstrong Nonlocality,” *Natural Computing* **12**, 9–12 (2013); originally arXiv:quant-ph/0501159 (2005).

[4] G. Brassard, H. Buhrman, N. Linden, A. A. Méthot, A. Tapp and F. Unger, “Limit on Nonlocality in Any World in Which Communication Complexity Is Not Trivial,” *Physical Review Letters* **96**, 250401 (2006). https://doi.org/10.1103/PhysRevLett.96.250401

[5] M. Navascués and H. Wunderlich, “A Glance Beyond the Quantum Model,” *Proceedings of the Royal Society A* **466**, 881–890 (2010). https://doi.org/10.1098/rspa.2009.0453
