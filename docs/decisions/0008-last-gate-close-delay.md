# 0008 — Last-gate close delay

**Context.** Closing the only open gate while the vac is still pulling seats the valve against full suction (stall/strain).

**Decision.** When the closing gate is the last open one, wait *Last-gate close delay* (3 s) so the vac coasts down; otherwise close immediately.

**Consequences.** Brief extra open time after a job.
