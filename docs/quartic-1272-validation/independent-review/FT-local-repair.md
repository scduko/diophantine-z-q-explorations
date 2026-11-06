# Local correction to the transferred inverse-theorem invocation

This check concerns one step inside the external Frei--Tinkova proof. It is not an independent closure of that proof or its nilsequence estimates.

The inspected Frei--Tinkova v3 TeX has SHA-256 `72ab8baf0743dd9fd597b27d8f75d656c8e606dc70530f10745bc58a3a9988a1`. The inspected Dodos--Kanellopoulos v4 PDF has SHA-256 `1d71ecfcb7a1970ce3d7a10ac426f8c94e9d1d6a88886cb378ca19a099963508`.

In the inspected arXiv v3 source, Lemma 9.3 requests the D-linear forms condition with D = 4^u and derives smallness of the U^(2u) norm of nu - 1. It then invokes Dodos--Kanellopoulos, Theorem 5.1, for a target U^(u+1) norm.

The inspected Dodos--Kanellopoulos arXiv v4 PDF, printed pages 12--13, states that for target U^s, s >= 2, the majorant must satisfy a small U^(2s) norm after subtraction of 1. It also requires C >= 20, a prime N' in [CN,2CN], and |f| <= nu. The exponent needed in the Frei--Tinkova invocation is therefore 2u+2.

For u >= 1, request D = 4^(u+1) in Frei--Tinkova Lemma 9.1. Its quantifiers allow every fixed D > 1. The centered cube of dimension 2u+2 has 2^(2u+2) = 4^(u+1) forms in 2u+3 variables. The forms are x + omega dot h for distinct binary tuples omega. Their coefficients are 0 or 1, and no two linear parts are proportional. Every subset is a finite-complexity system allowed by the D-linear forms condition; 2u+3 <= 4^(u+1).

Expand the product of nu(x + omega dot h) - 1 over this cube. Every nonempty subset product has average 1 + o(1); the empty subset has average 1 exactly. The constant terms sum to zero. Since u is fixed, the finite sum of error terms is o(1). Thus the defining 2^(2u+2)-th power of the U^(2u+2) norm tends to zero, which supplies the actual hypothesis of Dodos--Kanellopoulos.

The enlarged D changes only constants depending on the fixed complexity parameter u, including C_0(D), the chosen C, and the domination factor. It does not change the theorem's quantifier order. The argument uses s = u+1 >= 2. A separate u=0 formulation can instead use the first moment or increase u to 1 by monotonicity; it should not invoke Theorem 5.1 outside its stated range.

The local repair is valid. No statement here certifies the remaining external proof steps, identifies a final published Frei--Tinkova text, or removes the release's source-version qualifications.
