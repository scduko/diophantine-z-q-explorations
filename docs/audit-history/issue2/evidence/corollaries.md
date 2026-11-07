# Historical excerpt: corollaries

Origin in the research workspace: `work/astra-four-corollaries-review-001/REPORT.md`

Full origin SHA-256: `cdd7d3a4c5c26d97aca27f30e1b41a0890a153c3bf249088ee8d054f644dbe24`

These are excerpts of earlier research, not new proof-acceptance certificates. Original line numbers follow. The origin hash identifies the file; it does not independently establish its date or mathematical correctness.

## Original lines 5 to 10

```text
5: This review concerns `drafts/z-in-q-candidate-preprint/review-v4d/05-bounds-appendices.tex` lines 177-306, its corresponding introduction and abstract, and the exact V4c-to-V4d source patch. It checks the four deductions, not the proposed proof that ordinary integers are Diophantine in the rationals. Let H denote the unverified assertion
6:
7:     for every t in Q, t is an ordinary integer iff there exists w in Q^r with P_*(t,w)=0,
8:     where r=292890231904 and P_* is the fixed integer-coefficient polynomial of the draft.
9:
10: I found no mathematical correction required in these four deductions, when H is retained as their hypothesis and effective codings have their standard algorithmic meaning. Sections 3-6 below reconstruct the arguments directly, including both total many-one reductions and malformed-input handling. This conclusion supplies no evidence for H itself, no global acceptance of the manuscript, and no new variable, degree, or coefficient bounds for the universal polynomial U.
```

## Original lines 14 to 34

```text
14: ## 2. Primary statements and conventions actually checked
15:
16: Mazur, *Speculations about the Topology of Rational Points: An up-date*, Asterisque 228 (1995), printed page 165, defines a variety to mean a reduced scheme of finite type over a field. His Conjecture 3 is the finiteness of the number of connected components of the real-topological closure of the rational points of any variety over Q. It does not require irreducibility, smoothness, or Zariski density. Smoothness and Zariski density occur in the different Conjecture 1 on the same page. Page 166 expressly observes the incompatibility of Conjecture 3 with a Diophantine definition of Z in Q; the argument in section 3 here is checked independently rather than inferred from that observation.
17:
18: Primary PDF: `work/astra-mazur-corollary-001/primary/mazur-1995.pdf`, SHA256 `94490a944040d9589595995389d499661a8facab8398af062d0c52e34d71aded`. PDF pages 2-3 are printed pages 165-166. Both corresponding page images `page-02.png` and `page-03.png` were visually read, and text was independently extracted from the PDF. The bibliography at `references.tex` lines 108-111 cites the correct conjecture, page, publication, and original-publication repository URL.
19:
20: Matiyasevich, *Diophantine representation of enumerable predicates*, Math. USSR-Izvestiya 5 (1971), printed page 3, states that every enumerable predicate is Diophantine. The definitions at printed pages 2-3 apply to predicates of any finite arity. The paper uses positive integers for the relevant variables, permits integer polynomial coefficients, and on page 2 explicitly gives the conversion of a positive witness to one plus a sum of four integer squares. Its definition of enumerable is halting exactly on the tuples for which the predicate is true. Thus it applies to the two-parameter universal halting relation, after shifting the parameters to match the positive convention. It is not merely a theorem about individual recursively enumerable subsets with an uncontrolled dependence on their indices.
21:
22: Primary PDF: `work/astra-mazur-corollary-001/primary/matiyasevich-1971.pdf`, SHA256 `18e824c01046ad49b079f91b567b27a928e737c598eb347c8a4f42128081ec83`. PDF pages 2-3 are printed pages 2-3. Both `dprm-02.png` and `dprm-03.png` were visually read; the corresponding PDF text was independently extracted. `references.tex` lines 112-116 gives the correct Basic Theorem, page, and conversion locator. The source's positive-integer convention is accounted for explicitly at appendix lines 234-239.
23:
24: These primary results are imported published theorems/conjecture statements, not re-proved here. The elementary four-square theorem used for witness conversion is expressly identified in the primary source. No prior audit's PASS statement is used as a premise.
25:
26: ## 3. Mazur deduction: appendix lines 183-208
27:
28: Assume H. The affine hypersurface P_*=0 is of finite type over Q since r is finite, irrespective of its very large value. Taking its reduction produces exactly a variety in Mazur's convention. Maps from a coordinate ring to Q or R kill every nilpotent, so reduction preserves both sets of field-valued points and their usual affine real topology. This justifies line 199 without a smoothness or irreducibility assertion.
29:
30: Write V for that reduced hypersurface, C for the closure of V(Q) in V(R), and pi for the first-coordinate projection. Hypothesis H gives pi(V(Q))=Z, with both inclusions. The inverse image pi^{-1}(Z) is closed in V(R), because pi is continuous and the ordinary integer subset is closed in R. Therefore C is contained in pi^{-1}(Z), giving pi(C) contained in Z. Conversely V(Q) is contained in C and already has every integer as its first coordinate. Thus pi(C)=Z.
31:
32: A connected component of C is nonempty and connected. Its continuous image in the discrete subspace Z is a singleton. For each integer choose any rational point over it, whose existence is H. Points chosen over distinct integers cannot lie in the same connected component. Hence C has infinitely many connected components, contrary to Conjecture 3. One does not need any component of C to be open, locally connected, or algebraic.
33:
34: This argument does not interchange projection with closure or assert that a polynomial projection is a closed or proper map. It uses only the closed inverse image of the specific set Z. The use of the reduced whole hypersurface, rather than an irreducible component selected without justification, exactly matches the primary conjecture. The title and wording assert negation of this finite-component conjecture only; they do not silently replace it by the stronger smooth-locus formulation of Conjecture 1.
```

## Original lines 58 to 78

```text
58: ## 6. Both total many-one reductions, with explicit coding: appendix lines 270-306
59:
60: The phrase 'fixed effective coding' at lines 277-279 can be instantiated as follows. Encode a nonnegative arity together with a finite list of pairs consisting of an integer coefficient and an exponent tuple of that arity with nonnegative entries. Use any standard computable pairing and finite-list syntax with decidable parsing. Combining repeated monomials and removing zero coefficients are effective but not required for evaluation. Declare malformed codes to be outside HTP(Q). Allow constant and zero polynomials and, if desired, arity zero. Other conventional polynomial codings connected to this one by effective translations give the same many-one result. The claim does not extend to arbitrary non-effective numberings.
61:
62: Likewise fix a standard effective machine enumeration with a universal simulator and effective compilation of a finite literal into a fixed program template. Invalid machine descriptions can be interpreted as divergent machines. This makes the diagonal halting set 0' at line 275 a definite subset of N. No oracle or noncomputable choice of an index is used below.
63:
64: First, on input e in N, substitute e for both ordinary parameter variables in the fixed U, perform the finite integer polynomial arithmetic, and output the code of U(e,e,x_1,...,x_m). This is a total computable map e -> h(e). Its output is always a valid polynomial code, including in any case where terms cancel or it becomes constant. By the established universal property,
65:
66:     e belongs to 0' iff U(e,e,x)=0 has a rational solution iff h(e) belongs to HTP(Q).
67:
68: This proves 0' <=_m HTP(Q). It uses H via U; no inference from undecidability alone would establish this many-one lower bound.
69:
70: Second, on input c, parse it. If c is malformed, output the fixed index of a machine that never halts. If it encodes an arity-a polynomial f, generate a machine M_c that ignores its own input and searches all rational a-tuples, halting as soon as exact rational evaluation gives f=0. For an explicit exhaustive search, for each positive bound B enumerate integer numerators p with |p|<=B and denominators q with 1<=q<=B, form their fractions, and test every a-tuple of these fractions. Repetitions do not matter. Every rational tuple eventually appears because it has finitely many numerator/denominator pairs. For a=0, test the one empty tuple; a zero constant halts and a nonzero constant runs forever. Every individual evaluation and equality test is finite integer arithmetic.
71:
72: Compile this fixed search program with c as its literal to obtain a computable index j(c). Since M_c ignores its input, in particular it halts on its own index exactly when it finds a zero. Consequently, for every natural code c, valid or invalid,
73:
74:     c belongs to HTP(Q) iff machine j(c) halts on input j(c) iff j(c) belongs to 0'.
75:
76: This proves HTP(Q) <=_m 0'. This direction holds unconditionally, without H. Lines 292-302 give precisely this construction; the coding details above make explicit its totality, its index production, and its treatment of invalid codes. In particular, failure to find a zero need not be decidable: it correctly causes divergence rather than a negative answer.
77:
78: If one uses rational-coefficient polynomial codes instead, syntactically require nonzero denominators (malformed zero-denominator expressions again have the declared invalid treatment). Multiplication by the product of the finitely many denominators produces an integer polynomial and preserves rational zeros, since that scalar is nonzero in Q. The transformation is effective. The reverse representation of integer coefficients as rationals with denominator 1 is effective too. Thus lines 303-305 do not alter the degree conclusion. This 'degree' is the many-one computability degree, not a numerical bound on polynomial degree.
```
