.. _analysis:

********************************************
Classification of all Bildzeitung articles
********************************************

Documentation of the code in *src.analysis*. This is the core of the project. Here I import the output frm the data management part in form of two excel files. The first file contains tokenized articles together with a label that I assigned myself. The second input file contains just all other articles (or a subset depending on how long you want to wait). The python file then uses the first input to train a Naive Bayes Algorithm in order to classify the articles of the second input file.

Regression plot
=================

.. automodule:: src.analysis.regression
    :members:
