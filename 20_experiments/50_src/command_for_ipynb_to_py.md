# Command to convert Jupyter Notebooks to Python Scripts

To properly include the notebooks in the thesis via Minted, you can use the following command to convert Jupyter notebooks to Python scripts:

```bash
jupyter nbconvert --output-dir='20_experiments/50_src/nb_to_py' --to script 20_experiments/50_src/evaluation*.ipynb
```

By this, the evaluation*.ipynb files will be converted to Python scripts, which are then included in the thesis using the Minted package.