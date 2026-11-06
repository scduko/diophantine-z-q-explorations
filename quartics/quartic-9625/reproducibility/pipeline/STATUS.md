Prepared a source revision of the measured H19/high40/beta12/root37 source.
Raw contact positions5 through12 become beta-only comparisons with16 free
arguments; the other29 remain the exact old full comparison. The new batch
has17 rational tests, with orders [1]*11+[12]*6. Both beta-only logarithms
have precision12. Anchor25 and scalar32 remain unchanged.

The source arithmetic is under independent review by precision/guards. A
finite checker or measured count will not establish arithmetic acceptance.
No frozen high40 file is changed.

Builder, independent source checker, malformed-source tests, dual-module
adapter, fresh-lift pipeline, and named-source negative tests are ready.
Small hash/template and synthetic locator checks passed. Actual source
generation and complete replay await the root's remote dispatch.
