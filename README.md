# CPT_S 440 Term Project

This is the repository for Project Team 11's Minesweeper Implementation. 

- Allysa Sewell

- Connor Hill

- Jacob Ibach

- Kenan Anderson

This repository contains all submission items for the Project. In the Main Branch, the minesweeper.py file contains our implementation for the Minesweeper Project. The CPTS440_Minesweeper_report.pdf contains the pdf file for our 10 page Project Writeup. The CPTS440_Minesweeper_Presentation.pptx contains the Presentation slidedeck, the following link is for the Google Colab that will function as our demo, and the embedded Youtube video is our presentation. 

[Google Colab Notebook](https://colab.research.google.com/drive/1E8uVc0U50U84UgbxAPuJRPvtSlQncNSa?usp=sharing)

[![Presentation](https://img.youtube.com/vi/Ze55ul56udM/0.jpg)](https://www.youtube.com/watch?v=Ze55ul56udM)

The code in the Colab is identical to the code in minesweeper.py. The following is documentation regarding a brief overview of the project and how to run the model. 

---

Running the Demo: There is a single file that needs to be run as-is to produce the results. This can be done by simply downloading the xxx.py file and running it on a local environment, or going to the linked Colab and running it there. Both files are the same.

Our implementation starts with a few functions that generate a random 10 by 10 minesweeper board populated with 10 mines in random placements. These functions create a dictionary that contains every tile on the board and its corresponding neighbors, and a dictionary that contains every tile on the board and it's corresponding tile value (for adjacent mines). The State class initializes a list for known positions and a dictionary of mine positions, and is populated with helper functions that help update passed-in objects for each iteration, calculate mine probabilities, generate a list of models, and check board consistency. The main 'wrapper' function is search(), which populates a node_list and probability dictionary, and a PriorityQueue Frontier. After initializing these objects, it runs a while loop that continously 'flips' a tile and then regenerates models to determine probabilities. The function will end once either a mine has been struck, or all tiles have been flipped. The Result Runner code at the bottom of the file is used to run one iteration of our implementation. The commented Testing Implementation below this was the code used to generate our testing/resultant data. Simply running the code will generate the board and then begin initializing and populating probabilities.   
