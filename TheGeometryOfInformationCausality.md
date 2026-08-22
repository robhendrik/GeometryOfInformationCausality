# Why Isn’t Nature More Quantum?

### *Quantum physics draws a boundary. Information theory approaches the same limit from a completely different direction.*

Alice and Bob are playing a simple guessing game: QSeaBattle. Alice sees a board containing *n* bits and may send Bob one bit, while Bob is asked about one randomly chosen position. His job is simple: guess whether the bit at that position is 0 or 1.

We discussed this game in previous posts and ended with a surprisingly simple result. The **classical strategy space** became more and more complicated as we increased the number of bits, but **quantum mechanics** did the opposite: it replaced that many-faced geometry with a sphere. For two bits we had a circle, for three a sphere, and in general a hypersphere,

*c₁*² + *c₂*² + ⋯ + *cₙ*² = 1.

This boundary comes from physics. Behind it sits the mathematical structure of quantum mechanics: states in Hilbert space, observables represented by operators, and the Born rule that turns quantum amplitudes into probabilities. Almost exactly a century ago, Heisenberg's new mechanics, Born's recognition of its matrix structure, and the probabilistic interpretation that followed established the rules from which the quantum limit ultimately follows. Famously, Born's 1926 scattering paper first stated the probability interpretation incorrectly in the main text and corrected it in proof: it was the square of the amplitude that mattered.

So quantum mechanics tells us where Nature stops. But that is not quite the same as understanding *why* it stops there.

Nothing in the geometry alone prevents us from imagining a hypothetical post-quantum resource that pushes Alice and Bob a little farther out, giving Bob a larger advantage for several possible questions at the same time. Push this all the way to the extreme and Bob could correctly retrieve whichever bit he is asked for.

For two bits, that extreme corresponds to the corners of a square in advantage space. At *c₁* = *c₂* = 1, Bob could retrieve either of Alice's two bits perfectly, depending on which one he is asked for. Quantum mechanics does not come close to that corner — but, remarkably, correlations of this kind can still obey **no-signalling**. Alice cannot use them to send Bob an instantaneous message. So relativity, at least in this familiar no-faster-than-light sense, does not by itself explain why Nature stops at the quantum circle.

Perhaps we should therefore change perspective. Instead of starting from quantum physics and asking what correlations it permits, can we start from information and recover the same restriction?

> **Can an information-theoretical principle explain why Nature stops at the quantum boundary?**

## The Information Boundary

Let's forget quantum mechanics for a moment and evaluate the same game from an **information** perspective.

For each possible question, Bob's advantage *cᵢ* corresponds to a success probability

*Pᵢ* = ½(1 + *cᵢ*).

From that probability we can calculate how much information Bob's answer carries about Alice's bit. For a uniformly random bit this is

*Iᵢ* = 1 − *h₂(Pᵢ*),

where *h₂* is the binary entropy.

Alice sends Bob only one classical bit. Pawłowski and colleagues proposed that this should impose a deeper restriction: however Alice and Bob exploit their shared resources, the total information available through Bob's possible retrieval choices should not exceed the information Alice actually communicates [2]. For our game,

Σᵢ *Iᵢ* ≤ 1.

They called this proposed physical principle **Information Causality**.

The proposal is stronger than merely using the inequality as a convenient mathematical bound. The suggestion is that Nature itself respects this information budget. So let us take the principle seriously and see what boundary it draws.

![Blog4_Figure_MI_n2.png](Blog4_Figure_MI_n2.png)

> *Figure 1: Classical, quantum, Information Causality and no-signalling boundaries for the two-bit guessing game. Classical one-bit strategies form the inner diamond, while quantum strategies reach the circle. The Information Causality boundary extends beyond the quantum circle in most directions. Farther out, the dashed square marks the no-signalling / PR-box limit, where both retrieval advantages can in principle reach ±1.*
>
> Alt text: Two-dimensional RAC advantage-space diagram with four nested regions. A classical diamond lies inside the quantum circle. A larger rounded Information Causality boundary extends beyond the circle, while an outer dashed square marks the no-signalling / PR-box limit at |c₁| ≤ 1 and |c₂| ≤ 1. Along the positive diagonal, classical majority, quantum and information-boundary points are marked.

Figure 1 combines the two perspectives in a single picture. The circle is the boundary supplied by quantum physics. The rounded shape outside it is the boundary supplied by the information principle.

They are not the same.

For two bits, Information Causality is more permissive than quantum mechanics. Along the diagonal there is visible room between the quantum point and the point where the information budget is exhausted. So if Information Causality is going to tell us something about why Nature selects the quantum limit, the answer is not simply that its finite-game boundary reproduces the quantum circle.

Perhaps two bits are simply too few.

## As the Game Gets Bigger

The Information Causality condition does not depend on Alice having only two bits. We can apply the same one-bit information budget to three bits, four bits, or many more.

With three bits we get one last chance to see the complete geometry before it escapes into higher dimensions.

![Blog4_Figure_n3_classical_quantum_mutual_information_3D.png](Blog4_Figure_n3_classical_quantum_mutual_information_3D.png)

> *Figure 2: The same comparison in the full n = 3 advantage space. The classical strategies form a faceted polytope, the quantum boundary is a sphere, and Information Causality defines a larger, distinctly non-spherical body.*
>
> Alt text: Three-dimensional RAC advantage-space rendering for n = 3. A faceted classical polytope sits inside a translucent quantum sphere, while a larger rounded Information Causality surface surrounds the quantum boundary in most directions. The three advantage axes c₁, c₂ and c₃ are shown.

Figure 2 shows the full three-dimensional advantage space. Figure 3 shows two cross-sections through it. The sphere becomes a circle in each cut, while the information boundary produces a different, somewhat larger curve. Just as for two bits, information theory still leaves room outside the quantum boundary.

![Blog4_Figure_n3_2D_cross_sections_classical_quantum_MI_symmetric.png](Blog4_Figure_n3_2D_cross_sections_classical_quantum_MI_symmetric.png)

> *Figure 3: Two cross-sections through the three-dimensional advantage space for n = 3. The classical polytope, quantum sphere and Information Causality boundary produce visibly different shapes. In particular, the information boundary still leaves room beyond the quantum sphere.*
>
> Alt text: Two two-dimensional cross-sections through the n = 3 advantage space, comparing the classical polytope, the circular cross-section of the quantum sphere and the larger Information Causality boundary.

For four bits the full advantage space is already four-dimensional, so we can no longer draw it. But the cross-sections give us a way forward. We can take equivalent two-dimensional cuts through higher-dimensional shapes and watch what happens as the game grows.

There is one direction that is particularly useful: the symmetric direction *(1,1,…,1)*, where Bob has the same advantage for every possible question. On the quantum sphere, if every coordinate has the same value *c*, then

*n c²* = 1,

so the quantum boundary lies at

*c* = 1/√*n*.

As the game grows, the quantum advantage available for each individual question therefore shrinks: 1/√2 for two bits, 1/2 for four, 1/√8 for eight, and so on.

Now compare that known quantum boundary with the boundary obtained from the same one-bit information budget.

![Fig4_sketch](Fig4_sketch.png)

> *Figure 4: Quantum and Information Causality boundaries for progressively larger guessing games. Equivalent cross-sections for n = 4, 8, 16 and 32 contain the symmetric (1,1,…,1) direction. At every finite n the information boundary remains outside the quantum boundary, even as both move toward the origin as the game grows.*
>
> Alt text: Four equivalent two-dimensional cross-sections through advantage spaces for n = 4, 8, 16 and 32. Each panel compares the circular quantum boundary with the larger Information Causality boundary and marks the positive symmetric direction. Both boundaries move inward as n increases, while the information boundary remains outside the quantum one at every finite game size.

This is subtler than simply watching one boundary converge onto the other. It does not. At every finite *n*, Information Causality still allows some points beyond the quantum sphere.

But both boundaries are shrinking.

Take the symmetric quantum value

*c* = 1/√*n*

and step a fixed amount ε beyond it,

*c* = 1/√*n* + ε,

with ε > 0, however small. As *n* grows, the quantum value tends toward zero, and so does the Information Causality boundary. Eventually there is always a game large enough for that fixed step ε to lie outside the information boundary.

In the familiar language of analysis: **for every ε > 0, there exists an n for which information theory objects.**

Pawłowski and colleagues showed something stronger still. By applying Information Causality to recursively constructed random-access codes, they found that even an arbitrarily small excess in the underlying nonlocal correlation beyond the quantum limit eventually violates the one-bit information budget [2]. The information boundary never literally becomes the finite-*n* quantum sphere, yet the strongest correlation that survives this test indefinitely is precisely the quantum one.

> **Go even slightly beyond the quantum limit, and eventually there is a guessing game large enough for information theory to object.**

## Why Isn’t Nature More Quantum?

We have arrived at the same limiting correlation strength by two very different roads.

The first road began with physics. The mathematical structure developed in the first years of quantum mechanics became the modern framework of Hilbert spaces, operators and probabilities. Within that framework, quantum mechanics determines how far Alice and Bob can go.

The second road did not assume quantum mechanics. We started with a guessing game, one communicated bit and a proposed principle about information. At any finite game size that principle is actually more permissive than quantum mechanics. Yet when Pawłowski and colleagues ask which correlations can survive the information test for arbitrarily large games, the same quantum limit reappears.

That coincidence is the remarkable part.

Perhaps Information Causality is telling us *why* Nature is not more quantum: correlations stronger than the quantum limit would eventually allow Alice and Bob to violate a fundamental information budget.

But does that close the story? Maybe not completely.

The first thing to wonder about is the sum itself. Bob never retrieves all *n* bits. He is asked for one bit, chooses the corresponding measurement, and obtains one answer. Had he been asked for another bit, he would have made another choice instead. Information Causality adds the mutual informations associated with all these alternative experiments. That is a perfectly well-defined mathematical quantity — but should we interpret it literally as the amount of information Bob *has*? Or is it better understood as the sum of what he *could have learned* under mutually exclusive choices?

There is also something curious about the limit in which the quantum correlation strength emerges. The sharp result is obtained by considering arbitrarily large games. Yet in that same limit the individual guessing advantages approach zero and Bob's success probabilities approach 50%. We distinguish quantum mechanics from a slightly stronger theory through more and more questions for which Bob becomes less and less able to predict the answer.

And our geometric pictures suggest one more question. Close to *cᵢ* = 0, binary mutual information is approximately quadratic in *cᵢ*. A sum of quadratic terms naturally produces something locally spherical. So how much of the spherical geometry that appears for large games is telling us something specifically about quantum mechanics, and how much is already built into the local shape of the information measure we chose?

None of this makes Information Causality less remarkable. One route begins with the physical and mathematical structure of quantum mechanics. The other begins with a proposed principle about information. Yet both single out the same limiting correlation strength.

The question is what we should make of that coincidence.

Information Causality is not the only attempt to understand why Nature stops where it does. Communication-complexity arguments [3,4] and principles such as Macroscopic Locality [5] constrain the post-quantum world from different directions.

Perhaps information really is the fundamental principle hiding behind the quantum boundary. Or perhaps Information Causality is seeing the shadow of something deeper — a principle of geometry, consistency or symmetry that we have not yet identified.

So, after starting with a simple guessing game, we have arrived at a question that is still very much alive:

**Why isn't Nature more quantum?**

> **Does Information Causality explain the quantum boundary — or merely find the same limit from another direction?**

## References

[1] V. Scarani, “Feats, Features and Failures of the PR-box,” *AIP Conference Proceedings* **844**, 309 (2006). https://doi.org/10.1063/1.2219371

[2] M. Pawłowski, T. Paterek, D. Kaszlikowski, V. Scarani, A. Winter and M. Żukowski, “Information Causality as a Physical Principle,” *Nature* **461**, 1101–1104 (2009). https://doi.org/10.1038/nature08400

[3] W. van Dam, “Implausible Consequences of Superstrong Nonlocality,” *Natural Computing* **12**, 9–12 (2013); originally arXiv:quant-ph/0501159 (2005).

[4] G. Brassard, H. Buhrman, N. Linden, A. A. Méthot, A. Tapp and F. Unger, “Limit on Nonlocality in Any World in Which Communication Complexity Is Not Trivial,” *Physical Review Letters* **96**, 250401 (2006). https://doi.org/10.1103/PhysRevLett.96.250401

[5] M. Navascués and H. Wunderlich, “A Glance Beyond the Quantum Model,” *Proceedings of the Royal Society A* **466**, 881–890 (2010). https://doi.org/10.1098/rspa.2009.0453