# GenLayer Universal Prediction Market

A prediction market contract built on GenLayer that can resolve any YES/NO question by fetching real-time web data and using AI to determine the outcome.

## What is this?

Most prediction markets need a trusted third party to resolve outcomes — someone has to say "yes this happened" or "no it didn't". This contract removes that middleman entirely. It fetches the source data itself and uses an LLM to read it and decide, with multiple validators having to agree through Optimistic Democracy.

The "universal" part means it works for any topic — sports, politics, crypto, news, anything you can point to a URL for.

## How it works

1. Deploy the contract with a question, category, resolution URL and deadline
2. Call `resolve()` when you think the event has happened
3. The contract fetches the URL and passes the content to an LLM
4. The LLM returns `occurred: 1` (YES) or `occurred: 0` (NO)
5. Multiple validators independently do the same — if they agree, it's finalized

## Example

```
Question:  Did SpaceX successfully land Starship in 2024?
Category:  Technology
URL:       https://en.wikipedia.org/wiki/SpaceX_Starship
Deadline:  2024-12-31

Result: YES — occurred: 1
```

## Built with

- GenLayer Studio
- Python (GenLayer Intelligent Contract SDK)
- `gl.eq_principle.strict_eq` for Equivalence Principle
- Optimistic Democracy consensus

## Functions

- `resolve()` — fetch web data and resolve the market
- `get_outcome()` — see the current result
- `is_resolved()` — check if already resolved

## How to run it

1. Go to [GenLayer Studio](https://studio.genlayer.com)
2. Create a new file and paste `universal_prediction_market.py`
3. Set execution mode to Normal (Full Consensus)
4. Deploy with your question, category, resolution URL and deadline
5. Call `resolve()` to trigger the AI resolution

## Notes

This was the first Intelligent Contract I built for the GenLayer Hackathon. It uses `gl.eq_principle.strict_eq` which means all validators must return the exact same JSON — works well here since the outcome is binary (0 or 1).
