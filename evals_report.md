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

## 2 Failure Modes Found & Fixed

### 1. Voice Agent Hedging ("I don't know" loops)
**Problem:** The voice agent did not fumble words, but it developed a habit of prefixing answers with "I don't know the answer to this, but..." followed immediately by providing the correct relevant information.
**Fix:** Explicitly banned these standard fallback phrases in the prompt by adding a rigid instruction: "NEVER start your answers with phrases like 'I don't know about this but'. Just answer the question directly."

### 2. Chatbot hyper-focusing on a single experience
**Problem:** When asked general questions about work experience or why I am a good fit, the Chatbot would ONLY mention WittingAI, completely ignoring other roles like GoKiwi and FirstClub.
**Fix:** Modified the stream instructions in the system prompt to explicitly force the LLM to give a well-rounded summary: "If asked about your background or experience, summarize ALL your roles briefly mentioning GoKiwi, FirstClub, WittingAI, and IIT Delhi. Do not over-index on just WittingAI."

## What I'd Improve With 2 More Weeks

1. **Add a web-based voice widget** — embed a call button on the chat page so people don't need to use a phone number. Vapi has a web SDK for this.

2. **Better GitHub indexing** — right now the GitHub data is manually written. I'd build a script that uses the GitHub API to pull README files, file trees, and commit history automatically. This would keep the data fresh.

3. **Conversation memory across sessions** — currently each chat session starts fresh. I'd add persistent memory so the AI can reference earlier parts of the conversation.

4. **Multi-turn voice evaluation** — I only tested single Q&A turns. I'd set up a proper eval pipeline with scripted multi-turn conversations to test context retention and graceful recovery from misheard words.
