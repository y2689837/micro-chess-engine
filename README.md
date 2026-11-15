# micro-chess-engine

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/y2689837/micro-chess-engine/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/y2689837/micro-chess-engine/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A chess engine in a single 3,964-byte Python file: 0x88 board representation, negamax search with alpha-beta pruning and quiescence, MVV move ordering, and material + piece-square-table evaluation, searching a fixed budget of 45,000 nodes per move. Built by an AI agent for make.fun's "Build the strongest chess engine in 4 KB of Python" bounty.

## Run it

```sh
MAKEFUN_ENV_URL=<game-server-url> python3 -P -s main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=na3hgpay&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
