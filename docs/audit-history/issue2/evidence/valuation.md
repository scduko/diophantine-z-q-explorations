# Historical excerpt: valuation

Origin in the research workspace: `drafts/z-in-q-candidate-preprint/review-v4b/supplements/formalization/z-in-q/ProofSources/outputs/multiplication-certificate-correctness-proof.txt`

Full origin SHA-256: `fb059d569484e38ca21648fd1cafcf7fd9d2f34f57c8293031a2e80e0f8429eb`

These are excerpts of earlier research, not new proof-acceptance certificates. Original line numbers follow. The origin hash identifies the file; it does not independently establish its date or mathematical correctness.

## Original lines 1 to 2

```text
1: The actual multiplication template: soundness and conditional completeness
2: 3 November 2026
```

## Original lines 62 to 89

```text
62: Each test_group chooses four points H,U1,U2,U3 in D and defines
63: V0=H-C0, Vi=Ui-Ci using exact group addition. Thus write
64:  H=[h]P, Ui=[zi]P, V0=[h-cstar]P, Vi=[zi-cstar*ni]P.
65: It requires H,V0 finite and their L values nonzero. Here
66:  L(z)=16575z-6630d^2 z^5+11050d^4 z^9-25500d^6 z^13
67:        +68250d^8 z^17-198900d^10 z^21+612612d^12 z^25,
68:  d=75-53sqrt(2), z(Q)=-x(Q)/y(Q), z(O)=0.
69: The inverse-x convention at O is zero.
70:
71: The twelve outputs are, in order: the four inverse-x values at H,Ui;
72: the conjugates of the four inverse-x values at V0,Vi; the three
73: differences
74:  L(z(Ui))/L(z(H)) - conjugate(L(z(Vi))/L(z(V0)));
75: and the product of the first two unprimed ratios minus the third.
76: This is precisely the output order in multiplication-certificate.js.
77:
78: The slope template excludes t in C union {1}, sets eta^2=1,
79:  R0=eta*product_(c in C)(t-c)/(t-1)^8,
80:  a=1-R0*q^2, R=ell^2*a^2*R0,
81: and requires a!=0. For six independent test groups and precisions
82: k_j=1 for j<=8 and k_j=25 for j>=9 it sets
83:  C_gj=D_gj/[R0^k_j*(t-1)^(k_j+1)],
84:  W_g=product_j(1+R*C_gj^2),
85:  Theta=Tr_F/Q(sum_g 1/W_g), B=R/Theta^2,
86: with explicit nonzero guards on W_g and Theta, and requires Phi0(B).
87: The letter B in this local calculation denotes this scalar, not a
88: root-code parameter. All quotients are guarded or have denominators
89: already proved nonzero by the same conjunction.
```

## Original lines 113 to 142

```text
113: 3. One slope forces divisibility at each height-contact prime
114:
115: Let p outside the prescribed S satisfy v_p(t-c)=delta>0 odd for
116: some c in C. All finite contacts stay distinct modulo p, since their
117: nonzero differences are at most 61 and p>324. Thus t-1 and the other
118: five t-c' are units, and v_p(R0)=delta. Also ell and cstar are units.
119:
120: If q!=0, delta+2v_p(q) is odd and nonzero. It follows that
121: b=v_p(a)=min(0,delta+2v_p(q))<=0. For q=0 take b=0. Put
122: alpha=v_p(R)=delta+2b; alpha is odd. Define, only for this argument,
123: D'_gj=(ell*a)^(2k_j)*D_gj/(t-1)^(k_j+1), so C_gj=D'_gj/R^k_j.
124:
125: At every place v above p, the valuation of each factor of W_g is
126:  min(0, alpha+2(v(D'_gj)-k_j*alpha)).
127: The expression after the comma is odd, so no equal-valuation
128: cancellation is possible. In particular every v(W_g)<=0.
129: Let lambda be the maximum v(W_g) over the six groups and all places
130: above p. Then v_p(Theta)>=-lambda>=0, including in the inert case,
131: since conjugation preserves the valuation there. By section 2 the
132: odd valuation v_p(B)=alpha-2v_p(Theta) is nonnegative. Thus
133:  alpha>0 and lambda>=-alpha/2.
134:
135: Choose one common group and place attaining lambda. All its factor
136: valuations are nonpositive and sum to lambda, so each is at least
137: lambda. Rearranging gives, for every j in this same group and place,
138:  v(D'_gj)>=(k_j-3/4)*alpha,
139:  v(D_gj)>=(k_j-3/4)*delta-(3/2)*b>=k_j-3/4.
140: The extension is unramified at p, so these valuations are integers.
141: Consequently all eight inverse-x tests have valuation >=1 and all
142: four other tests have valuation >=25, simultaneously.
```
