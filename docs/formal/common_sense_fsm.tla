---- MODULE common_sense_fsm ----
\* Minimal Common Sense diagnostic FSM for SWI V2 (L1 formal layer).
\* Not a seal. Not production authorization.
\* Safety: no transition into EXECUTE, AUTHORIZE, PROMOTE, or SEAL.

EXTENDS Integers, FiniteSets

VARIABLES decision

Diagnostic == {"CONTINUE", "RECHECK", "ESCALATE", "HALT"}
Forbidden  == {"EXECUTE", "AUTHORIZE", "PROMOTE", "SEAL"}

TypeOK == decision \in Diagnostic

Init == decision = "CONTINUE"

\* Adversarial / boundary events collapse into HALT or RECHECK/ESCALATE
HaltEvent ==
  /\ decision' = "HALT"

RecheckEvent ==
  /\ decision \in {"CONTINUE", "RECHECK"}
  /\ decision' = "RECHECK"

EscalateEvent ==
  /\ decision \in {"CONTINUE", "RECHECK", "ESCALATE"}
  /\ decision' = "ESCALATE"

ContinueIdle ==
  /\ decision = "CONTINUE"
  /\ decision' = "CONTINUE"

Next ==
  \/ HaltEvent
  \/ RecheckEvent
  \/ EscalateEvent
  \/ ContinueIdle

Spec == Init /\ [][Next]_decision

\* Safety: decision never leaves the diagnostic vocabulary
InvDiagnosticOnly == decision \in Diagnostic

\* Safety: forbidden authority labels are not reachable decisions
InvNoAuthorityDecision == decision \notin Forbidden

====
