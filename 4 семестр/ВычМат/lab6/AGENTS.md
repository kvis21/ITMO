# AGENTS.md — lab6 (ВычМат, ОДУ)

## Repo context
- Self-contained Python lab inside one large academic git monorepo rooted at `F:\ITMO`. Do not `git init` here; all commits happen at the repo root.
- Siblings `lab1`–`lab5` under `F:\ITMO\4 семестр\ВычМат\` are independent, similar projects.
- Current state: **no code yet** — only `docs/` (assignment `docs/Задание ЛР№6.pdf`, lecture `docs/Лекция №6. Решение ОДУ.pdf`, both Russian). PDFs are the source of truth; if you cannot open them, ask the user to paste the task text.
- Topic: numerical solution of ODEs (Cauchy problem `y' = f(x, y)`). **Variant 10**: methods 1, 3, 5 — Euler, Runge-Kutta 4th order, Milne (multistep predictor-corrector).

## Variant 10 methods
| # | Method | Type | Key formula | Order |
|---|--------|------|-------------|-------|
| 1 | Метод Эйлера | One-step | y_{i+1} = y_i + h·f(x_i, y_i) | O(h) |
| 3 | Рунге-Кутта 4 | One-step | k1=h·f(x_i,y_i), k2=h·f(x_i+h/2, y_i+k1/2), ... | O(h^4) |
| 5 | Милн | Multistep predictor-corrector | Predictor: y_{i+1}=y_{i-3}+4h/3(2f_{i-3}-f_{i-2}+2f_{i-1}); Corrector: y_{i+1}=y_{i-2}+h/3(f_{i-2}+4f_{i-1}+f_{i+1}) | O(h^4) |

- Accuracy estimation: Runge rule for one-step methods; exact-solution comparison ε = max|y_exact - y_i| for multistep.
- Milne requires 3 starting values (y1, y2, y3) computed by Runge-Kutta before the multistep loop begins.
- Assignment requires at least 3 ODEs available for user selection in the program.

## Conventions to mirror (lab4/lab5 are the closest templates)
- Layout: `src/main.py` entry point calling `from gui.solver import run_gui`; `src/data.py` (result/state `@dataclass`es); `src/methods.py` (one function per method); `src/utils.py`; `src/gui/{input,solver,graphics}.py`.
- A Jupyter notebook `lab6.ipynb` may also be expected by the assignment.
- GUI is Streamlit; plots use Plotly. Run with `streamlit run src/main.py` from the lab dir — imports are src-relative, so `src` must be the script root.
- Core numerics are written from scratch — no numpy/scipy for the algorithms.
- Each method returns a result `@dataclass` with a `status: str` field (`"Успешно"` / `"Ошибка: ..."`); failures return a result, never raise.
- **All comments, docstrings, UI labels, and error messages are in Russian** — this is a hard convention.
- Show result tables/metrics with `st.table` / `st.dataframe`.

## Tooling
- Use `uv init` (Python >=3.12, deps: `streamlit`, `plotly`) with a local `.venv` like `lab2`/`lab3`/`lab5`.
- `.venv/` is git-ignored; root `.gitignore` covers `__pycache__`, `.gigacode`, `.gradle`. Do not commit venv/build junk.

## Git
- One repo at `F:\ITMO`; commit style is lowercase, terse messages (e.g. `finish code comp-math 4`). Only commit when explicitly asked.
