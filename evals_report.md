# Evals Report — AI Persona (Shruti Verma)

## Voice Quality (Part A)

| Metric | Target | Result |
|--------|--------|--------|
| First response latency | < 2s | ~1.2s (measured via Vapi dashboard) |
| Interruption handling | No crash | Handled — agent pauses and listens |
| Task completion (booking) | End-to-end | Tested 3 times, all bookings confirmed in Cal.com |
| Accuracy (10 sample Q&As) | Correct answers | 9/10 correct — 1 partial (mixed up project dates) |

**How I measured:** Called the agent 5 times with different question sets. Timed first response with a stopwatch. Checked Cal.com dashboard after each booking attempt. Scored accuracy by comparing answers to my actual resume.

## Chat Groundedness (Part B)

| Metric | Result |
|--------|--------|
| Hallucination rate | 1/15 questions (6.7%) — said "React" instead of "React Native" once |
| Retrieval quality | 13/15 questions retrieved the correct chunks |
| Accuracy on resume questions | 5/5 correct |
| Accuracy on GitHub questions | 4/5 correct (1 partial) |
| Edge case handling | 5/5 — correctly said "I don't know" for out-of-scope questions |

**How I measured:** Asked 15 questions — 5 about resume, 5 about GitHub repos, 5 edge cases (things not in my resume). Checked each answer against the actual data. Counted any factual error as a hallucination.

**Sample edge cases tested:**
- "What's your GPA?" → correctly said "I don't have that information"
- "Tell me about your experience at Google" → correctly said "I haven't worked at Google"
- "What's your salary expectation?" → redirected to email

## 3 Failure Modes Found & Fixed

### 1. Chunk size too small → fragmented context
**Problem:** Initially used 200-char chunks. The retriever was pulling partial sentences that didn't make sense on their own. For example, a question about GeoPayLog would retrieve "GPS-tagged spending" without the project name.
**Fix:** Increased chunk size to 500 chars with 50 overlap. Also added custom separators (`===` and `---`) so chunks align with logical sections (per-project, per-job).

### 2. Voice agent giving long answers
**Problem:** The voice agent was reading full paragraphs — felt unnatural on a call. Nobody wants to listen to a 30-second monologue.
**Fix:** Added "keep responses concise on voice" to the system prompt and instructed it to give short answers first, then ask if the caller wants more details.

### 3. Booking timezone mismatch
**Problem:** When testing calendar booking, the agent was suggesting UTC times instead of IST. A slot shown as "2 PM" was actually 2 PM UTC = 7:30 PM IST.
**Fix:** Explicitly set timezone to "Asia/Kolkata" in both the Vapi function config and the system prompt. Also added a line in the prompt: "Always mention times in IST."

## What I'd Improve With 2 More Weeks

1. **Add a web-based voice widget** — embed a call button on the chat page so people don't need to use a phone number. Vapi has a web SDK for this.

2. **Better GitHub indexing** — right now the GitHub data is manually written. I'd build a script that uses the GitHub API to pull README files, file trees, and commit history automatically. This would keep the data fresh.

3. **Conversation memory across sessions** — currently each chat session starts fresh. I'd add persistent memory so the AI can reference earlier parts of the conversation.

4. **Multi-turn voice evaluation** — I only tested single Q&A turns. I'd set up a proper eval pipeline with scripted multi-turn conversations to test context retention and graceful recovery from misheard words.
