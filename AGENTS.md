# Research review and reporting

Before classifying a mathematical objection, closing a review item, or claiming that a manuscript incorporates an earlier audit, follow [the audit integration protocol](docs/audit-history/PROTOCOL.md).

Read the actual earlier argument, not only its verdict. Keep historical justification and incorporation into the current manuscript separate. Record exact sources, conventions, hypothesis checks, and the consuming passage. If the history has not been checked, say that it is unresolved rather than calling a repair new. A passing structural or computational check is not proof of the arithmetic theorem.

Run `python -B scripts/check_audit_history.py` after changing this register or its bound sources. Do not refresh hashes merely to silence a failed check; review the changed application first. User instructions take precedence. This protocol introduces no additional permission requirement.
