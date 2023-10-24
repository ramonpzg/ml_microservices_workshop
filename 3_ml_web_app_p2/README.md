## Part 3

There is a mismatch of dependencies between mlserver and nicegui, so it would be best to 
create a new environment with only the frontend.

```bash
mamba create -n ml_micro_frontend python=3.11
mamba activate ml_micro_frontend
pip install nicegui pandas
```