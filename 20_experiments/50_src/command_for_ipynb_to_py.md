# Command to convert Jupyter Notebooks to Python Scripts

To properly include the notebooks in the thesis via Minted, you can use the following command to convert Jupyter notebooks to Python scripts:

```bash
jupyter-nbconvert --to script 20_experiments/50_src/evaluation*.ipynb
```