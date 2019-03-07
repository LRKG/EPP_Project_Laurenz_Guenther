.. _data_management:

***************
Data management
***************


Documentation of the code in *src.data_management*. This part uses an excel file as input where I noted for each day of the time horizon under consideration the tiles of articles about terrorism for a small subset of days. The algorithm here then loops over all days in the excel file and scrapes all of them (or, as by default, a small subset if you dont want to wait too long). It recognizes the articles I classified as being about terrorism through comparison of the titles in the input file with the titles on the website. This way, the algorithm creates two excel file as output that contain 1) a subset of articles with the tokenized words of that article and the label I assigned to it myself and 2) a file containing only the words of all articles (or by default a subset).

.. automodule:: src.data_management.timing
    :members:
