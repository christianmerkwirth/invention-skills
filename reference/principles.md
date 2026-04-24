# Inventive Principles (40)

| ID | Name | Software analogy (one line) |
|----|------|-----------------------------|
| 1 | Segmentation | Microservices, modular decomposition, splitting monoliths |
| 2 | Extraction / Taking Out | Encapsulation, abstraction, private/public method boundaries |
| 3 | Local Quality | Method overloading, localized data scoping |
| 4 | Asymmetry | Try/catch exception handling routing edge cases to recovery logic |
| 5 | Merging | Grouping functions into libraries, server clustering |
| 6 | Universality | Generic types, templates, polymorphism |
| 7 | "Nested Doll" | Wrapper classes, Docker containers, class inheritance |
| 8 | Anti-weight | Garbage collection, background multithreading |
| 9 | Preliminary Anti-action | Test-Driven Development, defensive programming |
| 10 | Preliminary Action | Initialization routines, bootstrapping, pre-fetching cache |
| 11 | Beforehand Cushioning | Redundancy, automated backups, failover clustering |
| 12 | Equipotentiality | Load balancing, parallel processing |
| 13 | "The Other Way Around" | Undo/redo stacks, reverse engineering, de-compilation |
| 14 | Spheroidality / Curvature | CLI to GUI transition, event-driven non-linear control flows |
| 15 | Dynamics | Late binding, hot-swapping, plug-in architectures |
| 16 | Partial or Excessive Actions | Excess memory buffers, incremental update patching |
| 17 | Another Dimension | Hardware virtualization, hypervisors, multi-OS on single machine |
| 18 | Mechanical Vibration | Hardware polling, interrupt requests, signals |
| 19 | Periodic Action | Cron jobs, scheduled timers, batch processing intervals |
| 20 | Continuity of Useful Action | Persistent storage engines, parallel processing pipelines |
| 21 | Skipping / Hurrying | JIT compilation rushing interpretation to optimize execution |
| 22 | "Blessing in Disguise" | Honey-pots, verbose error logging to study attack patterns |
| 23 | Feedback | Asynchronous callbacks, event listeners, reactive UI monitors |
| 24 | Mediator | Message brokers (Kafka), middleware, decoupling service communication |
| 25 | Self-service | Auto-scaling, self-diagnosis, autonomous container provisioning |
| 26 | Copying | Software mocks, stubs, virtual simulation environments |
| 27 | Cheap Short-lived Objects | Temporary variables, session cookies, stateless tokens |
| 28 | Mechanics Substitution | Voice controls, gesture recognition, Natural Language Processing |
| 29 | Pneumatics and Hydraulics | Data streams, message pipes, UNIX pipes |
| 30 | Flexible Shells and Thin Films | UI skins, CSS frameworks, presentation wrappers |
| 31 | Porous Materials | Extensible API hooks, plugin interfaces, intentional extension points |
| 32 | Color Changes | IDE syntax highlighting, visual code differentiation |
| 33 | Homogeneity | Standardized protocols, common base classes (JSON over REST) |
| 34 | Discarding and Recovering | Memory deallocation, explicit object disposal |
| 35 | Parameter Changes | Environment variables, external settings files |
| 36 | Phase Transitions | Software compilation lifecycle: source → AST → bytecode → binary |
| 37 | Thermal Expansion | Cloud elasticity, dynamic resource allocation under traffic load |
| 38 | Strong Oxidants | High-level abstraction languages, optimizing compilers |
| 39 | Inert Atmosphere | Application sandboxing, Virtual Machines for untrusted code |
| 40 | Composite Materials | Software frameworks, multi-library bundles (Spring, Django) |

---

## 1. Segmentation

**Traditional concept:** Divide an object into independent parts.

**Software analogy:** Breaking monolithic codebases into discrete objects, components, subroutines, or microservices. Improves maintainability and isolates fault domains.

**Examples:**
- Extracting a payments module from a monolith into a standalone service
- Splitting a 2000-line class into focused single-responsibility classes
- Decomposing a complex algorithm into small, independently testable functions

---

## 2. Extraction / Taking Out

**Traditional concept:** Isolate a disturbing or useful property from an object.

**Software analogy:** Utilizing encapsulation, abstraction, and private/public method boundaries to extract volatile logic from the core execution path, preventing ripple effects during updates.

**Examples:**
- Extracting database queries behind a repository interface so the caller never knows the storage engine
- Moving hard-coded configuration into environment variables
- Isolating third-party SDK calls behind an adapter so they can be swapped without touching business logic

---

## 3. Local Quality

**Traditional concept:** Adapt properties of an object to local optimal conditions.

**Software analogy:** Implementing method overloading and localized data scoping. A function behaves differently depending on the specific data type it receives, optimizing localized execution.

**Examples:**
- Function overloads that handle integers and strings differently without branching in the caller
- Localized variable scope preventing unintended mutation across a large function body
- Context-specific validation rules applied only to the subset of data that requires them

---

## 4. Asymmetry

**Traditional concept:** Replace symmetrical forms with asymmetrical ones.

**Software analogy:** Utilizing try/catch exception handling. Standard execution flow (symmetry) is intentionally broken to route edge cases and errors (asymmetry) to specialized recovery logic.

**Examples:**
- Structured exception handling that routes timeout errors differently from validation errors
- Circuit breaker that short-circuits requests after N failures (asymmetric threshold behaviour)
- Retry logic with exponential backoff — each retry attempt is handled differently

---

## 5. Merging

**Traditional concept:** Combine identical or similar objects or operations.

**Software analogy:** Grouping identical or related functions into redistributable static/dynamic libraries, arrays, or deploying servers in highly clustered networks.

**Examples:**
- Consolidating shared utilities into a published internal library reused across services
- Server clustering behind a load balancer to handle traffic as a unified pool
- Batching individual database writes into a single bulk insert to reduce round trips

---

## 6. Universality

**Traditional concept:** Make a part perform multiple functions.

**Software analogy:** Utilizing generic types, templates, and polymorphism. A single piece of logic is designed to universally process varied data structures without redundant code generation.

**Examples:**
- A generic `Repository<T>` that handles persistence for any entity type
- A polymorphic `render()` method on a base `Widget` class, implemented differently per subtype
- A single serialization library that handles JSON, XML, and Protobuf via a unified interface

---

## 7. "Nested Doll"

**Traditional concept:** Place one object inside another.

**Software analogy:** Employing wrapper classes, containers (like Docker), or class inheritance. Legacy code is nested within a modern wrapper to interface with new protocols.

**Examples:**
- Wrapping a legacy SOAP client in a REST-compatible adapter
- Docker containers nested inside Kubernetes pods nested inside nodes
- Decorator pattern layering caching, logging, and auth around a core handler

---

## 8. Anti-weight

**Traditional concept:** Compensate for the weight of an object by merging with another that provides a lifting force.

**Software analogy:** Offloading the "weight" of memory management to automated garbage collectors, or utilizing background multithreading to keep the main application thread responsive.

**Examples:**
- JVM garbage collector reclaiming heap without explicit `free()` calls
- Web Worker running heavy computation off the main browser thread to keep the UI responsive
- Async I/O freeing the thread to serve other requests while waiting on disk

---

## 9. Preliminary Anti-action

**Traditional concept:** Perform actions in advance to control harmful effects.

**Software analogy:** Practicing Test-Driven Development (TDD) and defensive programming. Writing tests before code acts as a preliminary anti-action against production bugs.

**Examples:**
- TDD red-green cycle — failure conditions are encoded before the implementation exists
- Input validation at system boundaries preventing invalid state from propagating inward
- Schema migrations run in a test environment before touching production

---

## 10. Preliminary Action

**Traditional concept:** Perform required changes to an object completely or partially in advance.

**Software analogy:** Utilizing initialization routines, bootstrapping, and pre-fetching caching strategies. Critical data is loaded into memory before the user requests it.

**Examples:**
- Pre-warming a cache with likely keys before the first user request arrives
- Database connection pool initialized at application startup to avoid cold-start latency
- Static assets preloaded via `<link rel="preload">` before they are needed during navigation

---

## 11. Beforehand Cushioning

**Traditional concept:** Prepare emergency means in advance to compensate for unreliability.

**Software analogy:** Engineering robust redundancy, automated database backups, and failover clustering to cushion the inevitable unreliability of hardware or network infrastructure.

**Examples:**
- Multi-region database replicas that allow failover within seconds of primary loss
- Automated daily snapshots with tested restore procedures
- Dead-letter queues capturing failed messages for reprocessing rather than dropping them

---

## 12. Equipotentiality

**Traditional concept:** Change the operating condition so an object need not be raised or lowered.

**Software analogy:** Implementing load balancing and parallel processing. Traffic is distributed evenly across identical nodes, eliminating the need to constantly spin individual servers up or down.

**Examples:**
- Round-robin load balancer distributing requests across a homogeneous server fleet
- MapReduce spreading equal partitions of a dataset across identical worker nodes
- Consistent hashing ensuring even key distribution in a distributed cache

---

## 13. "The Other Way Around"

**Traditional concept:** Invert the action used to solve the problem.

**Software analogy:** Utilizing undo/redo action stacks, reverse engineering, and de-compilation. Processing tasks backward from a desired end-state rather than executing linearly forward.

**Examples:**
- Command pattern with an inverse `undo()` for every `execute()`
- Event sourcing replaying event history in reverse to reconstruct past state
- Reverse proxy that moves the concern of TLS termination from each service to the perimeter

---

## 14. Spheroidality / Curvature

**Traditional concept:** Move from linear to spherical/curved forms.

**Software analogy:** Transitioning from linear Command Line Interfaces (CLI) to multi-dimensional Graphical User Interfaces (GUI) and event-driven, non-linear control flows.

**Examples:**
- Replacing a sequential wizard with a free-form dashboard where users navigate non-linearly
- Event-driven architecture replacing a linear request/response pipeline
- A graph data model replacing a flat relational table for highly interconnected data

---

## 15. Dynamics

**Traditional concept:** Allow characteristics to change and become optimal at each stage of operation.

**Software analogy:** Designing applications with late binding, hot-swapping capabilities, and plug-in architectures that allow features to change without requiring a hard system restart.

**Examples:**
- Hot module replacement in webpack allowing UI changes without a browser reload
- Feature flags enabling runtime behaviour toggles without redeployment
- Plugin architecture where new file-format parsers are loaded without restarting the application

---

## 16. Partial or Excessive Actions

**Traditional concept:** If 100% is hard to achieve, go slightly more or less.

**Software analogy:** Allocating excess memory buffers to prevent overflow during spikes, or utilizing incremental update patching rather than demanding full software reinstalls.

**Examples:**
- Over-provisioning connection pool size to absorb burst traffic without exhaustion
- Delta sync sending only changed records rather than a full dataset on each sync
- Throttling to 90% of capacity to leave headroom for traffic spikes

---

## 17. Another Dimension

**Traditional concept:** Move objects into two- or three-dimensional space.

**Software analogy:** Moving from a physical hardware layer into "another dimension" via hardware virtualization and hypervisors, allowing multiple OS instances on one machine.

**Examples:**
- Hypervisor running multiple isolated VMs on a single physical host
- Flyweight pattern externalizing shared state into a separate dimension (a shared pool object)
- Columnar database storage organizing data by column (another dimension) for analytics efficiency

---

## 18. Mechanical Vibration

**Traditional concept:** Cause an object to oscillate or vibrate.

**Software analogy:** Implementing hardware polling, interrupt requests, and signals. A system rapidly checking a peripheral for updates mimics physical high-frequency vibration.

**Examples:**
- Polling a sensor endpoint at 100ms intervals to detect state changes
- Interrupt-driven I/O notifying the CPU only when data is ready, avoiding busy-wait
- WebSocket heartbeat pinging the server to detect dropped connections

---

## 19. Periodic Action

**Traditional concept:** Replace continuous action with periodic or pulsating ones.

**Software analogy:** Utilizing execution loops, cron jobs, and scheduled timers. Running a batch process at specific intervals saves resources compared to a continuously running daemon.

**Examples:**
- Nightly cron job aggregating daily metrics into summary tables
- Kubernetes controller reconciliation loop running every 30 seconds
- Polling an external API on a 5-minute schedule instead of maintaining a persistent connection

---

## 20. Continuity of Useful Action

**Traditional concept:** Carry on work continuously; make all parts of an object work at full load.

**Software analogy:** Deploying persistent storage engines and parallel processing pipelines to ensure systems remain continuously active, immediately capturing asynchronous data.

**Examples:**
- Change Data Capture (CDC) stream continuously replicating database mutations to a data lake
- Kafka consumer group processing messages continuously without batch boundaries
- Read replicas kept in sync continuously so any replica can serve reads at full capacity

---

## 21. Skipping / Hurrying

**Traditional concept:** Conduct a hazardous or harmful operation at high speed.

**Software analogy:** Employing Just-In-Time (JIT) compilation. The hazardous, slow process of interpreting high-level code is rushed through at runtime to optimize execution velocity.

**Examples:**
- JVM JIT compiling hot bytecode paths to native machine code after profiling
- Ahead-of-time (AOT) compilation skipping runtime interpretation entirely
- Lazy evaluation skipping computation of values that will never be consumed

---

## 22. "Blessing in Disguise"

**Traditional concept:** Use harmful factors to obtain positive effects.

**Software analogy:** Utilizing honey-pots or verbose error logging. Exposing a vulnerable server to malicious actors to study their attack patterns and fortify the actual production environment.

**Examples:**
- Honeypot API endpoint logging all probe attempts to build an attacker profile
- Chaos engineering intentionally injecting failures to discover hidden resilience weaknesses
- Verbose production error logs surfacing latent bugs that would otherwise stay hidden until critical

---

## 23. Feedback

**Traditional concept:** Introduce feedback to improve a process.

**Software analogy:** Implementing asynchronous callbacks, event listeners, and monitors. The system continuously receives feedback from executing threads to dynamically update user interfaces.

**Examples:**
- Reactive UI that re-renders only when observed state changes (React, MobX)
- Prometheus alerting feeding back metric threshold breaches to an on-call system
- Event-driven architecture where downstream services emit success/failure events consumed upstream

---

## 24. Mediator

**Traditional concept:** Use an intermediary carrier object or process.

**Software analogy:** Deploying message brokers (e.g., Kafka) or middleware. Decoupling direct communication between services prevents bottlenecking by placing an intermediary queue between them.

**Examples:**
- Kafka topic decoupling a high-throughput producer from a slower consumer
- API gateway mediating between external clients and internal microservices
- Adapter pattern translating between two incompatible interfaces via a dedicated boundary class

---

## 25. Self-service

**Traditional concept:** Make an object serve itself and carry out auxiliary and repair functions.

**Software analogy:** Implementing auto-scaling and self-diagnosis. A cloud orchestrator automatically provisions new containers when it detects its own CPU utilization exceeding thresholds.

**Examples:**
- Kubernetes Horizontal Pod Autoscaler scaling replicas based on CPU/memory metrics
- Self-healing service that detects its own degraded state and triggers a restart
- Database auto-vacuum process reclaiming space without manual `VACUUM` invocation

---

## 26. Copying

**Traditional concept:** Replace an expensive or fragile object with inexpensive copies.

**Software analogy:** Utilizing software mocks, stubs, and virtual simulation. Testing logic against a simulated database copy rather than executing expensive queries against a live production database.

**Examples:**
- Test doubles (mocks, stubs, fakes) replacing expensive external dependencies in unit tests
- Database snapshot cloned to a staging environment for safe load testing
- Read replica handling all analytical queries as a copy of the primary

---

## 27. Cheap Short-lived Objects

**Traditional concept:** Replace an expensive, durable item with multiple inexpensive, short-lived ones.

**Software analogy:** Generating temporary local variables, session cookies, and stateless tokens. Short-lived tokens avoid the heavy resource cost of maintaining persistent, long-term server connections.

**Examples:**
- Short-lived JWT tokens (15-minute expiry) instead of long-lived session state on the server
- Ephemeral containers that spin up, do one job, and are discarded
- Temporary tables in a database query plan, used and dropped within the transaction

---

## 28. Mechanics Substitution

**Traditional concept:** Replace a mechanical system with sensory (optical, acoustic, olfactory) ones.

**Software analogy:** Transitioning from mechanical keyboard inputs (CLI) to advanced sensory inputs, including voice-activated controls, gesture recognition, and Natural Language Processing.

**Examples:**
- Voice command interface replacing a form-based UI for hands-free operation
- Gesture recognition in a VR environment replacing physical controllers
- Natural language query replacing a structured SQL form for non-technical users

---

## 29. Pneumatics and Hydraulics

**Traditional concept:** Use gas or liquid parts of an object instead of solid parts.

**Software analogy:** Treating data as continuous "streams" or utilizing message pipes. Instead of dealing with rigid, static files, data is processed fluidly in transit (video streaming, UNIX pipes).

**Examples:**
- UNIX pipeline: `cat log.txt | grep ERROR | awk '{print $3}' | sort | uniq -c`
- Video streaming delivering frames as a continuous flow rather than waiting for full download
- Reactive streams processing infinite event sequences without buffering the entire dataset in memory

---

## 30. Flexible Shells and Thin Films

**Traditional concept:** Use flexible shells and thin films instead of three-dimensional structures.

**Software analogy:** Abstracting the visual layer using UI skins, CSS frameworks, and presentation wrappers. The "thin film" of the interface is highly flexible and distinct from the rigid backend logic.

**Examples:**
- CSS theme system allowing complete visual restyling without touching HTML or business logic
- Presentation layer separated from domain logic so the same API serves web, mobile, and CLI
- Skin-able UI components that adapt to brand guidelines without changing component behaviour

---

## 31. Porous Materials

**Traditional concept:** Make an object porous or use supplementary porous elements.

**Software analogy:** Designing software with intentional empty interfaces or extensible API "hooks." These architectural "holes" allow third-party developers to inject custom plugin logic.

**Examples:**
- Webpack loader and plugin hooks that let the community extend the build pipeline
- VS Code extension API providing event hooks into the editor lifecycle
- Django middleware chain where custom middleware is inserted between request and response

---

## 32. Color Changes

**Traditional concept:** Change the colour of an object or its environment.

**Software analogy:** Utilizing IDE syntax highlighting. Visually differentiating code keywords, strings, and operators using colour drastically reduces the cognitive load of reading complex codebases.

**Examples:**
- Syntax highlighting distinguishing keywords, strings, and identifiers in an IDE
- Heat-map visualizations colouring code paths by execution frequency in a profiler
- Traffic-light status indicators (red/amber/green) in a deployment dashboard

---

## 33. Homogeneity

**Traditional concept:** Make objects interact with a given object of the same material.

**Software analogy:** Enforcing standardized protocols and common base classes. Ensuring disparate microservices communicate via a homogenous format (e.g., JSON over REST) rather than proprietary binaries.

**Examples:**
- All services exposing a JSON/REST API regardless of internal implementation language
- A monorepo enforcing a single linting ruleset across every package
- Shared base `Error` class ensuring all application errors have a consistent structure

---

## 34. Discarding and Recovering

**Traditional concept:** Make portions of an object that have fulfilled their functions disappear or restore them directly.

**Software analogy:** Enforcing strict memory deallocation. In lower-level languages, explicitly disposing of objects and freeing heap memory once a task is complete to prevent system crashes.

**Examples:**
- RAII pattern in C++ ensuring resources are freed when objects go out of scope
- `defer` in Go guaranteeing file handles and mutexes are released even on error paths
- Soft-delete with scheduled purge — records are logically deleted then physically removed after a retention window

---

## 35. Parameter Changes

**Traditional concept:** Change an object's physical state, concentration, or flexibility.

**Software analogy:** Utilizing environment variables and external settings files. Abstracting hard-coded IP addresses into flexible external parameters allows the same compiled binary to run in dev, test, and production.

**Examples:**
- Twelve-factor app storing all config in environment variables
- Feature flags changing runtime behaviour without a code deployment
- Dynamic thread-pool sizing tuned via a config value without recompilation

---

## 36. Phase Transitions

**Traditional concept:** Use phenomena occurring during phase transitions.

**Software analogy:** The lifecycle of software compilation, deployment, and installation. Source code transitions through multiple "phases": source → abstract syntax tree → bytecode → machine binary.

**Examples:**
- TypeScript compilation: `.ts` → type-checked AST → `.js`
- Docker build: `Dockerfile` → image layers → running container
- CI pipeline stages: lint → test → build → publish → deploy, each a distinct phase

---

## 37. Thermal Expansion

**Traditional concept:** Use the expansion or contraction of material due to temperature change.

**Software analogy:** Cloud elasticity and dynamic resource allocation. Automatically expanding server instances in response to the "heat" of high web traffic, and contracting them when traffic cools.

**Examples:**
- AWS Auto Scaling Group adding EC2 instances during a traffic spike and terminating them after
- Kubernetes cluster autoscaler provisioning new nodes when pod scheduling is constrained
- Serverless functions scaling to zero when idle and to hundreds of instances under load

---

## 38. Strong Oxidants

**Traditional concept:** Replace ordinary air with enriched or concentrated oxygen.

**Software analogy:** Utilizing high-level abstraction languages and optimizing compilers. Replacing verbose, low-level assembly code with "enriched," highly expressive languages (e.g., Python) to boost productivity.

**Examples:**
- Replacing C assembly with Python for a data processing pipeline, trading execution speed for development speed
- Domain-specific languages (SQL, regex, Terraform) expressing complex intent in a few lines
- Compiler optimizations (inlining, dead-code elimination) that extract performance from readable source

---

## 39. Inert Atmosphere

**Traditional concept:** Replace a normal environment with an inert one.

**Software analogy:** Deploying application sandboxing and Virtual Machines. Executing volatile or untrusted code within a strictly isolated "inert" environment prevents contamination of the host OS.

**Examples:**
- Browser sandbox preventing JavaScript from accessing the OS filesystem
- gVisor intercepting syscalls from untrusted containers before they reach the host kernel
- Serverless function execution in an ephemeral, isolated runtime with no persistent state

---

## 40. Composite Materials

**Traditional concept:** Transition from homogeneous to composite materials.

**Software analogy:** Building systems using software frameworks and multi-library bundles. Fusing disparate routing, security, and database libraries into a cohesive "composite" framework (e.g., Spring, Django).

**Examples:**
- Django combining ORM, URL routing, templating, and auth into a single cohesive framework
- Spring Boot composing security, dependency injection, and data access into one opinionated stack
- A monorepo "platform" package bundling shared logging, tracing, and config libraries for all services
