\# ParaMVCC



\*\*Parametric Multi-Version Concurrency Control (ParaMVCC)\*\*



A research prototype that extends EasyEdit to investigate concurrency control mechanisms for Parametric Databases (Large Language Models).



\---



\# Research Objective



The objective of ParaMVCC is to adapt Multi-Version Concurrency Control (MVCC) concepts from traditional databases to parameter-efficient knowledge editing in Large Language Models.



Instead of modifying a single model directly, every knowledge update is represented as an independent adapter version, allowing multiple versions of model knowledge to coexist simultaneously.



\---



\# Current Architecture



```

User

&#x20;  │

&#x20;  ▼

Dynamic Knowledge Edit

&#x20;  │

&#x20;  ▼

Version Manager

&#x20;  │

&#x20;  ▼

Knowledge Version (Adapter)

&#x20;  │

&#x20;  ▼

Session Manager

```



\---



\# Completed Features



\## 1. Dynamic Knowledge Editing



\- Runtime knowledge editing.

\- Users provide a question and updated answer interactively.

\- No source-code modification required.



\---



\## 2. Adapter-Based Versioning



\- Every edit is stored as an independent AdaLoRA adapter.

\- Multiple versions of model knowledge are preserved.



\---



\## 3. Automatic Version Allocation



\- Version IDs are generated automatically.

\- No manual folder management.



\---



\## 4. Thread-Safe Concurrent Version Allocation



Implemented using a thread-safe Version Manager.



Supports concurrent requests without version-number collisions.



\---



\## 5. Session Management



Each user session can be associated with an independent knowledge version.



This forms the foundation for Snapshot Isolation.



\---



\## 6. Interactive Demonstration



\- Load different versions.

\- Query individual versions.

\- Verify edited knowledge.



\---



\# Work in Progress



\## Phase 5 — Snapshot Controller



The Snapshot Controller will:



\- Connect Session Manager and Version Manager.

\- Bind each user session to a specific knowledge version.

\- Ensure all queries are answered from the user's assigned snapshot.



\---



\## Phase 6 — Live Concurrent Editing



Support simultaneous edits from multiple users.



Goals:



\- Concurrent knowledge editing.

\- Automatic creation of independent adapter versions.

\- Isolation between concurrent writers.



\---



\## Phase 7 — Snapshot Isolation



Final research objective.



The system will guarantee:



\- Stable knowledge snapshots.

\- Readers always observe their assigned version.

\- Writers create newer versions without affecting existing readers.

\- Multiple knowledge versions coexist simultaneously.



\---



\# Current Status



Completed



\- Dynamic Knowledge Editing

\- Adapter Versioning

\- Automatic Version Allocation

\- Concurrent Version Allocation

\- Session Management

\- Interactive Demonstration



Currently Implementing



\- Snapshot Controller

\- Live Concurrent Editing

\- Snapshot Isolation



\---



\# Repository Structure



```

easyeditor/      Modified EasyEdit framework



paramvcc/        ParaMVCC implementation



versions/        Knowledge versions



examples/        Demo programs



hparams/         Hyperparameters

```



\---



\# Future Research



\- Snapshot Controller

\- Concurrent Adapter Loading

\- Snapshot Isolation

\- Semantic-region Concurrency Control

\- Conflict Detection

\- Commit / Rollback

\- Serializable Knowledge Transactions



\---



\# Author



\*\*Rishit Chaudhary\*\*



BITS Pilani



Research Prototype — ParaMVCC

