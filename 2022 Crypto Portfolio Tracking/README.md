# 2022 Crypto Portfolio

Here is the code for my [crypto portfolio series](https://andresberejnoi.com/category/investing/crypto/2022-crypto-portfolio/). I update at the end of every month with a review of what happened during that period. My goal is to track the performance of this portfolio, comprised of the top 20 coins at the time I started it (December 23rd, 2021), and using a slighlty arbitrary weighting.

## Two Conda Environments
I had to create two different Conda environments for this project because `yfinance` and `cbpro` don't play well together. Luckily, `cbpro` is only needed for the first part of the process, the "fetching" of market data. This part is accomplish with the Jupyter notebook: `Fetch Historic Crypto Data With Coinbase Pro Library.ipynb`.

On the other hand, `yfinance` is used for the second notebook: `2022 Weighted Crypto Portfolio Tracking.ipynb`.

Therefore, to run the first notebook, create a Conda environmnet with the env file `environment_fetching.yml`:

```sh
conda env create -f environment_fetching.yml
```


For the second notebook, use the env file `environmnet_plotting.yml`:

```sh
conda env create -f environment_plotting.yml
```
