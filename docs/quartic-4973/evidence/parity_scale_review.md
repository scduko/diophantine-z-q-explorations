# Independent parity square-factor review

Date: 2026-11-06. Arithmetic verdict: PASS, subject to the exact row matching and privacy premises below. Reviewed proof: `parity/sub5000/PARITY_SCALE_PROOF.md`, SHA-256 `5d36002ff1b144135c5c27735c909553e1b469774cb227ae5cf36f55ebde63c4`, relative to `work/quartic-sub10000-20261106/`.

This is an algebraic projection equivalence for arbitrary rational retained inputs r,W. It does not require the inputs to be nonzero or distinct and does not introduce a trace-set or prime hypothesis.

For W!=0, the stated old-to-new map gives u=uo/W^2, v=vo/W, p=po/W, w=wo/W^4, s=so/W^2 and q=qo/W^3, with the remaining new variables defined by the new rows. The old norm row divided by W^4 is u^2+rv^2=r^2. The old p row divided by W^2 is the new p row. Since b=rW^2, co=rW^2e and zo=W^4u^2,

```
wo=co(17b-zo)=W^4 r e(17r-W^2u^2)=W^4 w.
```

The old last row divided by W^8 is exactly the new last row. The remaining rows are defining equations. Reversing these substitutions gives the displayed new-to-old map; no division by r or by another coordinate occurs.

At W=0, every new solution maps to an old solution under that polynomial new-to-old map: all old variables except the unconstrained eo=e become zero, and b=0. Conversely any old solution at W=0 can be replaced, preserving r,W and all outside coordinates, by the proposed new witnesses

```
u=r, v=a=L=z=p=q=k=0, e=1, c=r,
w=17r^2, s=17r, j=289r^2.
```

The conic row is r^2=r^2, the p row has coefficient -17-34+51=0, and j=17w makes the last row (289+578-867)w^2=0. This works also at r=0. The branch changes internal witnesses, which is permitted only under the complete privacy check.

Thus the fourteen-variable, eleven-row old block (including B2=W^2 and b=rB2) is equivalent, on the outside variables, to the thirteen-variable, ten-row new block. The local reduction is exactly one coordinate and one equation per matched block. This is not an independently measured global saving.

The finite checker must match all nine old conic rows and both argument rows, up to nonzero rational scaling; verify all fourteen deleted coordinates are distinct non-input coordinates private to those rows; keep r,W outside the deleted set; use fresh replacement coordinates; and remove exactly the matched old rows. In particular it must not discard an outside use of b, B2 or any old witness, even if that use appears redundant. Aliasing r=W is allowed. The proof does not justify sharing witnesses between calls or applying the rule to a differently normalized height module without a fresh match.

I read and checked the proof algebra. This note does not independently certify the rule implementation, a run, or a complete polynomial.
