# Z is Diophantine in Q

## Version 5

This repository contains *Z is Diophantine in Q*, Version 5, dated November 6, 2026. The manuscript presents three integer-coefficient polynomials whose rational zero projections it proves to be the ordinary integers. It retains the original large construction and the fully expanded Version 4 quartic, and adds a reconstructed quartic in 1,272 variables.

The project uses the collective agentic notes from Stefan Baranczuk, Gabe Conant, Sohail Farhangi, James Freitag, Elliot Glazer, Jennifer Park, and Caroline Terry.

| To | Open |
| --- | --- |
| Read Version 5 | [Manuscript PDF](quartic_1272.pdf), [TeX source](quartic_1272.tex) |
| Reproduce the new 1,272-variable quartic | [Polynomial, source program and independent checks](quartics/quartic-1272/README.md) |
| Read the fully expanded Version 4 quartic | [4,973-variable package](quartics/quartic-4973/README.md), [integer monomial table](quartics/quartic-4973/polynomial.expanded.txt) |
| Inspect theorem applications and conventions | [Version 5 inventory](docs/quartic-1272/README.md) |
| Build the manuscript or run the checks | [Build instructions](docs/building.md) |
| Download the Version 5 research handoffs | [Full handoff](https://github.com/elliotglazer/diophantine-z-q/releases/download/quartic-1272-version-5/z-in-q-version5-full-handoff.zip), [current-only handoff](https://github.com/elliotglazer/diophantine-z-q/releases/download/quartic-1272-version-5/z-in-q-version5-current-handoff.zip), [contents and verification](handoff/README.md) |
| Read collaborator notes and the height replacement | [Research update](research/2026-11-06-collaborator-notes/README.md) |
| Read the October 11 manuscript | [Manuscript and provenance](October%2011%20Manuscript/README.md) |
| Find earlier constructions and research history | [Research guide](docs/research-guide.md) |
| Inspect the partial formalization | [Accepted Lean helpers](lean/README.md) |
| Cite the manuscript or report an issue | [BibTeX](CITATION.bib), [contribution guide](CONTRIBUTING.md) |

The full handoff includes the current public snapshot, selected research notes, and the unchanged November 4 archive. The current-only handoff omits the embedded historical archive. Neither includes a conversational transcript.

## The three polynomials

For each polynomial, the input and all witnesses range over the rationals. The asserted defining property is

$$
q\in\mathbb Z \quad\Longleftrightarrow\quad
\exists\,\mathbf w\in\mathbb Q^{m-1},\quad P(q,\mathbf w)=0.
$$

| Construction | Total variables, including input | Degree | Nonzero monomials | Coefficient magnitude |
| --- | ---: | ---: | ---: | --- |
| Original | 292,890,231,905 | Less than $2\uparrow\uparrow7$ | Not expanded | Less than $2\uparrow\uparrow8$ |
| Version 4 quartic, retained | 4,973 | 4 | 72,925 | Maximum 685,783,949,153,203,534,233,890, less than $2^{80}$ |
| Version 5 quartic | 1,272 | 4 | 48,001 | Maximum $64\cdot3^{2^{28}}$ |

The [original construction](construction/README.md) is specified by an expression tree. The [Version 4 monomial table](quartics/quartic-4973/polynomial.expanded.txt) writes every coefficient as an ordinary integer. Its SHA-256 is `094f6a7ed17e7cc8d5d17a2f809127bbaffd0fe343cb2a32d18ac97e61279876`.

The [Version 5 table](quartics/quartic-1272/polynomial.json) lists every monomial and specifies its integer coefficient using the fixed constant $S=3^{2^{27}}$. It has 47,993 coefficients independent of $S$, seven linear in $S$, and one equal to $64S^2$. Its SHA-256 is `02e4771ba6e6c2abc749e33e8440cc256939f48005d5102fba7d9853489c8586`. The large coefficients are not written out digit by digit. This difference is why the fully expanded Version 4 quartic remains in the manuscript.

The new polynomial comes from an independent reconstruction of the public formulas in [José Brox's improvements manuscript](https://github.com/JoseBrox/diophantine-z-q_improvements), followed by an exact change of coordinates and certified eliminations. It is not claimed to recover Brox's unavailable original 1,315-variable coefficient table. Its 1,229 quadratic residuals and their sum of squares are included in the package. None of the counts asserts minimality.

## Verification scope

The finite checks verify the source program, algebraic coordinate changes, projection-preserving eliminations, complete sum-of-squares expansion and coefficient statistics. Independent checks and rejection tests accompany the package. These checks do not prove the source system's arithmetic characterization of the integers.

The manuscript supplies that arithmetic argument. The [Version 5 inventory](docs/quartic-1272/README.md) records exact theorem applications, source versions, hypotheses, conventions and the translations used. It carries forward the inherited source qualifications and separately records the new prime-pattern argument. Publication status is explicit: in particular, the Frei–Tinková input is checked against its arXiv version and is listed by its author as accepted by *Mathematika*, to appear. The repository does not describe every dependency as a verified published final version.

The [Version 4 inventory](docs/quartic-4973/README.md) and the [earlier 82-record inventory](docs/theorem-application-audit/README.md) retain their own frozen scopes. Structural inventory checks detect stale or mismatched records; they are not proofs of mathematical theorems.

The Lean formalization is incomplete. The accepted snapshot contains 48 helper modules; the main bounded-polynomial declaration still contains `sorry`. AI review and successful finite checks do not constitute independent human peer review or a completed formal proof.

## Earlier work and provenance

The October 11, 2026 manuscript, *A conditional Diophantine definition of Z in Q from four arithmetic inputs*, was produced by Sohail Farhangi with ChatGPT 6. Its PDF is preserved without modification. Its provenance and conditional scope are distinct from Version 5.

The November manuscript was produced by Elliot Glazer with Astra 6, Sol 6.1, and Opus 5.5, with auditing from Fable 5.1. The [Version 4 manuscript](quartic_4973.pdf), [Version 3 manuscript](quartic_9625.pdf) and [Version 2 manuscript](quartic_12504.pdf) remain historical references, with their separate polynomial packages and inventories. Earlier research handoffs identify their own snapshots.

The project builds on OpenAI's October 6, 2026 preprint, [*Hilbert's tenth problem over the rational numbers*](https://github.com/openai/math/blob/main/preprints/Hilberts-tenth-problem-over-the-rational-numbers-October-6-2026/main.pdf). The rank-one elliptic-curve and local-divisibility strategy goes back to Thanases Pheidas, as credited in the manuscript. The Version 5 construction also credits Brox and Zhi-Wei Sun for their formulas and prime-pattern argument.

The manuscript author field is blank, and [CITATION.bib](CITATION.bib) intentionally omits author fields. See [archival notes](docs/archiving.md) for citation and DOI status, and [third-party notices](THIRD_PARTY_NOTICES.md) for source attribution and redistribution scope.
