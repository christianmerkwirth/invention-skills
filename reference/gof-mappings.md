# GoF ↔ TRIZ Pattern Correlations

| GoF Pattern | Category | TRIZ Principle ID | TRIZ Principle Name | Insight |
|-------------|----------|-------------------|---------------------|---------|
| Adapter | Structural | 24 | Mediator | Translator between incompatible interfaces; both isolate the conflict into a dedicated boundary layer |
| Bridge | Structural | 2 | Extraction / Taking Out | Decouples abstraction from implementation so both can vary independently; extracting the interface from the logic prevents rigid class hierarchies |
| Composite | Structural | 6 | Universality | Treats individual objects and compositions uniformly; a single universal interface eliminates redundant code paths across a tree of objects |
| Iterator | Behavioral | 6 | Universality | Provides uniform traversal of different data structures (lists, trees, arrays) without exposing their internals; one generic mechanism universally serves multiple aggregates |
| Decorator | Structural | 7 | "Nested Doll" | Dynamically adds behaviours by placing an object inside wrapper classes; recursive encapsulation yields cumulative functionality without altering the core object |
| Flyweight | Structural | 17 | Another Dimension | Minimises memory by sharing intrinsic state in an external shared pool — moving data into "another dimension" outside the object instance |
| Proxy | Structural | 35 | Parameter Changes | Substitutes a heavyweight resource with a lightweight placeholder; fundamentally changes the operational parameter (instantiation cost) while preserving the same interface |

---

## Adapter ↔ Principle 24 (Mediator)

**GoF intent:** Convert the interface of a class into another interface clients expect, enabling classes with incompatible interfaces to work together.

**TRIZ link:** Principle 24 prescribes using an intermediary to merge incompatible elements. The Adapter *is* that intermediary — a disposable boundary layer that absorbs the translation cost so neither party has to change.

**Typical contradiction resolved:** Compatibility / Connectability (Parameter 13) improving while avoiding changes to Interface (Parameter 4) of either existing system.

---

## Bridge ↔ Principle 2 (Extraction / Taking Out)

**GoF intent:** Decouple an abstraction from its implementation so that the two can vary independently.

**TRIZ link:** Principle 2 advises extracting a volatile property to eliminate constraints. The Bridge extracts the implementation hierarchy from the abstraction hierarchy — once separated, each can evolve without breaking the other.

**Typical contradiction resolved:** Adaptability / Versatility (Parameter 12) improving without increasing System Complexity (Parameter 19).

---

## Composite ↔ Principle 6 (Universality)

**GoF intent:** Compose objects into tree structures to represent part-whole hierarchies; let clients treat individual objects and compositions uniformly.

**TRIZ link:** Principle 6 calls for making a part universally functional. By treating a tree of objects exactly like a single leaf, the same traversal and operation logic is universally applicable — eliminating redundant code paths.

**Typical contradiction resolved:** Ease of Use (Parameter 14) improving without increasing System Complexity (Parameter 19).

---

## Iterator ↔ Principle 6 (Universality)

**GoF intent:** Provide a way to sequentially access elements of a collection without exposing its underlying representation.

**TRIZ link:** Same principle as Composite. A single iterator protocol is universally applied across lists, trees, and arrays — one generic mechanism eliminates the need for callers to know collection internals.

**Typical contradiction resolved:** Compatibility / Connectability (Parameter 13) improving while reducing System Complexity (Parameter 19).

---

## Decorator ↔ Principle 7 ("Nested Doll")

**GoF intent:** Attach additional responsibilities to an object dynamically by wrapping it in decorator objects. Decorators provide a flexible alternative to subclassing for extending functionality.

**TRIZ link:** Principle 7 prescribes placing one object inside another. The Decorator is the programmatic implementation: recursive encapsulation layers caching, logging, or auth around a core handler without modifying it.

**Typical contradiction resolved:** Adaptability / Versatility (Parameter 12) improving without increasing System Complexity (Parameter 19).

---

## Flyweight ↔ Principle 17 (Another Dimension)

**GoF intent:** Use sharing to support large numbers of fine-grained objects efficiently. Separate intrinsic (shared) state from extrinsic (per-instance) state; store intrinsic state in a shared pool.

**TRIZ link:** Principle 17 prescribes moving into another dimension. The shared intrinsic state is moved into an external dimension (a pool outside each object instance), elegantly circumventing per-instance memory limits.

**Typical contradiction resolved:** Size (Dynamic) (Parameter 2) improving while preserving Reliability / Robustness (Parameter 15).

---

## Proxy ↔ Principle 35 (Parameter Changes)

**GoF intent:** Provide a surrogate or placeholder for another object to control access to it. Useful for lazy initialisation, access control, logging, or caching.

**TRIZ link:** Principle 35 prescribes changing a system parameter. The Proxy substitutes a lightweight stand-in for a heavy resource, fundamentally changing the instantiation cost parameter while preserving the identical interface.

**Typical contradiction resolved:** Speed (Parameter 5) improving while reducing Size (Dynamic) (Parameter 2) — deferred instantiation avoids paying the cost until actually needed.
