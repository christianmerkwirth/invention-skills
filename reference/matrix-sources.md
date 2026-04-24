# Matrix Source Bibliography

## rea-1999
Rea, K.C. (1999). *TRIZ for Software — Using the Inventive Principles*. The TRIZ Journal.
URL: https://the-trizjournal.com/triz-software-using-inventive-principles/
Used for cells: 9-6

Rea's article solves a concurrency/accuracy contradiction in a Win32 telecommunications application using the IT-TRIZ matrix. The "waste of time" parameter (classical P25, IT-TRIZ P9 Loss of Time) conflicted with "accuracy" (classical P29, IT-TRIZ P6 Accuracy). The matrix output was Principle 24 (Mediator) and Principle 26 (Copying): an intelligent agent mediator copied spec changes into XML, which was then parsed to auto-generate C++ header files, eliminating the human-error vector.

## mann-2011
Mann, D. (2011). *TRIZ and Software Innovation*. AITRIZ Articles.
URL: https://www.aitriz.org/articles/TRIZFeatures/323031312D30382D4D616E6E.pdf
Used for cells: 19-10

Mann's article is the primary reference for the 21-parameter IT-TRIZ matrix. The source document (doc/TRIZ for Software Engineering.md, lines 50–51) explicitly cites Mann's work for the System Complexity (19) vs Loss of Data (10) contradiction in distributed microservices architectures, noting that two-phase commit protocols increase complexity to achieve data integrity. Specific principle outputs for this cell are inferred from Mann's framework; confidence is accordingly "weak."

## ijosi-review
*Review of Systematic Software Innovation Using TRIZ*. International Journal of Systematic Innovation (IJOSI).
URL: https://ojs.ijosi.org/index.php/IJOSI/article/download/175/374
Used for cells: 16-5, 5-2

This review paper (cited as reference 1 in doc/TRIZ for Software Engineering.md) synthesises Domb & Stamey's 2006 research formally establishing the GoF–TRIZ correspondence. The paper documents:
- Flyweight pattern ↔ Principle 17 (Another Dimension): resolves the speed/memory (5-2) trade-off by projecting shared state into an external pool.
- Proxy pattern ↔ Principle 35 (Parameter Changes): resolves the security/speed (16-5) trade-off by substituting a heavyweight secure object with a lightweight configurable proxy.
