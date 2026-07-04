# \[iMama\]

AI chatbot for maternal pregnancy tracking.

## Prerequisites

- \[ Python 3.10+

- \[Gemma 4-E4B

## Installation

- Clone the repo

```
   git clone https://github.com/AsaKal/imama-api.git
```

- Install dependencies

```
   pip install -r requirements.txt
```

- Run it

```
   uvicorn main:app --reload
```

## Verify it worked

- Visit `http://localhost:8000/docs` — you should see \[***\{"name":"IMaMa API","docs":"/docs","health":"/health"\} **\]

## Common Issues

| Problem | Fix |
| - | - |
| `ModuleNotFoundError: X` | `pip install X` or check you're in the venv |
| Address already in use | `lsof -i :8000` then kill the process, or change port |
| ***""detail":"Not Found"** | Wrong URL path |


## Next Steps

- \[Link to full docs / usage guide\]

