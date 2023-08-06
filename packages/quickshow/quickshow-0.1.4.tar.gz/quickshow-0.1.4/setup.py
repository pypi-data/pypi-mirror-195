# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quickshow']

package_data = \
{'': ['*'], 'quickshow': ['output/*']}

install_requires = \
['matplotlib>=3.7.0,<4.0.0',
 'pandas>=1.5.3,<2.0.0',
 'scikit-learn>=1.2.1,<2.0.0',
 'seaborn>=0.12.2,<0.13.0',
 'sklearn>=0.0.post1,<0.1']

setup_kwargs = {
    'name': 'quickshow',
    'version': '0.1.4',
    'description': '',
    'long_description': "\n# Quick-Show\n\n[![Contributor Covenant](https://img.shields.io/badge/contributor%20covenant-v2.0%20adopted-green.svg)](code_of_conduct.md)\n[![Python Version](https://img.shields.io/badge/python-3.6%2C3.7%2C3.8-blue.svg)](code_of_conduct.md)\n![Pypi Version](https://img.shields.io/pypi/v/quickshow.svg)\n![Code convention](https://img.shields.io/badge/code%20convention-pep8-violet)\n\nQuick-Show is a package that allows you to easily and quickly draw plots. <br>\nQuick Show is an abstraction using popular libraries such as sklearn and matplotlib, so it is very light and convenient. <br><br>\n`Note`: Quick-Show is sub-modules of other packages to manage quickshow more lightly and use more widly. \n*This is a project under development as a submodule. With the end of the project, We plan to provide documents in major version 1 and sphinx. It is **NOT** recommended to use prior to major version 1.*\n\n<br>\n\n# Installation\n  ```cmd\n  $ pip install quickshow\n  ```\n<br>\n \n# Features\n## 1  Related to dimensionality reduction\n2D or 3D t-SNE and PCA plots using specific columns of a refined dataframe. \nCreate a scatter plot very quickly and easily by inputting a clean dataframe and column names that do not have missing data. \n1) `vis_tsne2d`: Simple visuallization of 2-dimensional t-distributed stochastic neighbor embedding <br>\n2) `vis_tsne3d`: Simple visuallization of 3-dimensional t-distributed stochastic neighbor embedding <br>\n3) `vis_pca`: Simple visuallization of Principal Component Analysis (PCA) \n\n<br>\n\n## 2  Related to classification model evaluation. \n1) `vis_cm`: visuallization heatmap of confusion_matrix and return classification report dataframe. <br>\n2) `get_total_cr_df` \n3) `vis_multi_plot` \n\n<br>\n\n\n## 3  Related to clustering. \n1) `vis_cluster_plot`: <br>\n\n<br>\n\n## 4  Utils \n1) `find_all_files`: <br>\n\n<br><br><Br><Br><Br>\n\n# Examples\n## Feature 1  <br>\n  <details>\n  <summary> See example dataframe... </summary>\n\n  ```python\n  import pandas as pd\n  df = pd.DataFrame([3,2,3,2,3,3,1,1])\n  df['val'] = [np.array([np.random.randint(0,10000),np.random.randint(0,10000),np.random.randint(0,10000)]) for x in df[0]]\n  df.columns = ['labels', 'values']\n  print(df)\n  ```\n\n  |    |   labels | values           |\n  |---:|---------:|:-----------------|\n  |  0 |        3 | [8231 3320 6894] |\n  |  1 |        2 | [3485    7 7374] |\n  |  ... |        ... |... |\n  |  6 |        1 | [5218 9846 2488] |\n  |  7 |        1 | [6661 5105  136] |\n\n  </details>\n\n  ```python\n  from quickshow import vis_tsne2d, vis_tsne3d, vis_pca\n\n  return_df = vis_tsne2d(df, 'values', 'labels', True, './save/fig1.png')\n  return_df = vis_tsne3d(df, 'values', 'labels', True, './save/fig2.png')\n  return_df = vis_pca(df, 'values', 'labels', 2, True, './save/fig3.png')\n  return_df = vis_pca(df, 'values', 'labels', 3, True, './save/fig4.png')\n  ```\n\n  <details>\n  <summary> See output figure... </summary>\n\n  ![](https://github.com/DSDanielPark/quick-show/blob/main/quickshow/output/readme_fig1.png)\n  ![](https://github.com/DSDanielPark/quick-show/blob/main/quickshow/output/readme_fig2.png)\n\n  - All function returns the dataframe which used to plot. Thus, use the returned dataframe object to customize your plot. Or use [matplotlib's rcparam](https://matplotlib.org/stable/tutorials/introductory/customizing.html) methods.\n  - If the label column does not exist, simply enter `None` as an argument.\n  - For more details, please check doc string.\n  \n  </details>\n<br>\n\n## Feature 2 \n  <details>\n  <summary> See example dataframe... </summary>\n\n  ```python\n  import pandas as pd\n  label_list, num_rows = ['cat', 'dog', 'horse', 'dorphin'], 300\n  df = pd.DataFrame([label_list[np.random.randint(4)] for _ in range(num_rows)], columns=['real'])\n  df['predicted'] = [label_list[np.random.randint(4)] for _ in range(num_rows)]  \n  print(df)\n  ```\n\n  |     | real    | predicted   |\n  |----:|:--------|:------------|\n  |   0 | cat     | cat         |\n  |   1 | horse   | cat         |\n  | ... | ...     | ...         |\n  |   7 | horse   | dog         |\n  | 299 | dorphin | horse       |\n\n  </details>\n\n  ```python\n  from quickshow import vis_cm\n\n  df_cr, cm = vis_cm(df, 'real', 'predicted', 'vis_cm.csv', 'vis_cm.png')\n  ```\n\n  <details>\n  <summary> See output... </summary>\n\n  ```python\n  print(df_cr)\n  ```\n  |           |       cat |       dog |   dorphin |     horse |   accuracy |   macro avg |   weighted avg |\n  |:----------|----------:|----------:|----------:|----------:|-----------:|------------:|---------------:|\n  | precision |  0.304878 |  0.344828 |  0.285714 |  0.276316 |        0.3 |    0.302934 |       0.304337 |\n  | recall    |  0.328947 |  0.246914 |  0.328767 |  0.3      |        0.3 |    0.301157 |       0.3      |\n  | f1-score  |  0.316456 |  0.28777  |  0.305732 |  0.287671 |        0.3 |    0.299407 |       0.299385 |\n  | support   | 76        | 81        | 73        | 70        |        0.3 |  300        |     300        |\n\n\n  confusion matirx will be shown as below.\n  ![](https://github.com/DSDanielPark/quick-show/blob/main/quickshow/output/readme_fig3.png)\n\n  - This function return pandas.DataFrame obejct of classification report and confusion metix as shown below.\n  \n  </details>\n<br>\n<br>\n<br>\n\n# Use Case\n[1] [Korean-news-topic-classification-using-KO-BERT](https://github.com/DSDanielPark/fine-tuned-korean-BERT-news-article-classifier): all plots were created through Quick-Show.\n\n# References\n[1] Scikit-Learn https://scikit-learn.org <br>\n[2] Matplotlib https://matplotlib.org/\n<br>\n\n<br>\n\n### Contacts\nProject Owner(P.O): [Daniel Park, South Korea](https://github.com/DSDanielPark) \ne-mail parkminwoo1991@gmail.com <br>\nMaintainers: [Daniel Park, South Korea](https://github.com/DSDanielPark) \ne-mail parkminwoo1991@gmail.com\n",
    'author': 'parkminwoo',
    'author_email': 'parkminwoo1991@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DSDanielPark/quick-show',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
