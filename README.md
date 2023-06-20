# TICTOC data project

## Project description:
**MPI fields (MA samples)**
The **C3** (*Phacelia tanacetifolia* Benth., *Helianthus annuus* L., *Triticum spec*. L.) -**C4** (*Eragrostis curvula* Wolf, *Zea mays* L., *Amaranthus spec*. L. and *Sorghum spec*. Moench) vegetation change experiment at the Max Planck Institute for Biogeochemistry in Jena, Germany was established in 2002. It includes 48 samples of soil water from different depth (10, 20 and 30 cm) from the eight plots of 24 m2  that were set up directly next to each other to avoid environmental biases, such as climate. (Mellado-Vázquez, P.G., Lange, M. & Gleixner, G. Soil microbial communities and their carbon assimilation are affected by soil properties and season but not by plants differing in their photosynthetic pathways (C3 vs. C4). Biogeochemistry 142, 175–187 (2019). https://doi.org/10.1007/s10533-018-0528-9).

<p style="text-align: center"><img src="https://github.com/EvgenyChur/TIC_TOC_postprocessing/blob/main/RESULTS/MPI%20fields.jpg"></p>

**Figure 1:** Plot plan of **"MPI fields"**

**Jena Experiment fields (MH and MH-r samples)**
Since 2002, the Jena Experiment has been looking at the importance of biodiversity for the ecosystem, making it one of the longest-running biodiversity experiments in the world. Soil water sampling takes place on the experimental plots on Wiesenstraße in northern Jena. It includes 212 samples from different depth (10, 20 and 30 cm) from the 90 plots of grassland plant communities. 13 of these samples are from two plots with **C4** plants (*Eragrostis curvula* Wolf, *Zea mays* L., *Amaranthus spec*. L. and *Sorghum spec*. Moench). C4 plots are classified as reference plots. Reference plots include also 4 more plots: 2 arable fields, and 2 extensively used meadows with in total 14 samples of soil water.

<p style="text-align: center"><img src="https://github.com/EvgenyChur/TIC_TOC_postprocessing/blob/main/RESULTS/Jena_exp_image.jpg"></p>

**Figure 2:** Plot plan of **"Jena Experiment fields"**

<p style="text-align: center"><img src="https://github.com/EvgenyChur/TIC_TOC_postprocessing/blob/main/RESULTS/C3_C4_plants.jpg"></p>

**Figure 3:** C3 / C4 plants** on the experimental sites "MPI fields" and "Jena Experiment fields"

## Content of TICTOC project:
Project has 2 main folders:
1. `scripts` -> has modules for TICTOC data processing with additional readme.md file;

2. `RESULTS` -> examples of output figures;

3. `DATA` -> examples of input data;

4. `README.md` -> current file.

## Cloning TICTOC processing scripts:
In order to use/develop TICTOC processing scripts repository should be cloned. To clone from gitlab, you need to provide a valid public key or use HTTPS connection. In the latter case, you have to write your login and password everytime when you want to do something with gitlab server. More information is available on the official gitlab web-page ([how to use SSH keys to communicate with Github][2]):

If you want to continue developing of *TICTOC* processing scripts you have to do the next things:
1. Open the web version of *TICTOC* project and create `a new issue` with the name of your research or task. Name should gives other users the key aspect of your work;
2. From your new issue, you have to create a new branch with the name **/feature/{direction_of_your_updates}**. You have to use a branch `main` as a source branch;
3. At the moment, your new branch is a full copy of the main branch and you can clone it to your "local" computer:
```
git clone --branch /feature/{direction_of_your_updates} git@github.com:EvgenyChur/TIC_TOC_postprocessing.git TICTOC
cd TICTOC
git status
```
4. If you want to add changes into TICTOC scripts you have to use these commands:
```
git status
git add *
git commit -m 'your commit name'
git push
```
Now all your changes are visible in web-version and you can check them.
5. If you want to `merge` your updates to the main branch you have to `create a new merge reguest`;
6. Sometimes, you branch can have the older version that the source branch and if you want to update your branch to the last version of source branch you can use:
```
git pull
```
However, your updates will be replaced by the updated version. More information about git command you can find in Google!


***P.S.1: You have to change these name {direction_of_your_updates} and {your commit name} to yours***

***P.S.2: Don't forget that before you start working with TICTOC processing scripts on MPI-BGC SLURM cluster or your local computer, you have to plug SLURM modules, install and set your enviroments for miniconda (anaconda), set git parameters (user.name and user.email), set a valid public key for GitLab. More information about you can find in MPI-BGC discourse. The main useful links are presented in section Additional materials***

## Additional materials:
There are a lot of useful information in MPI-BGC discourse platform for communication. For example:
1. **BGC SLURM cluster**:
    - [Introduction to BGC slurm-cluster][9]
    - [BGC slurm-cluster basics][10]
    - [Basic introduction to the BGC slurm-cluster][11]

2. **Python instructions**:
    - [Setting up Python/IPython/Jupyter on the slurm-cluster][6]
    - [Python code publishing recipes and info][7]
    - [How-to embarassingly parallel Python Jobs on BGC Slurm cluster][8]

3. **Git usage tutorials**:
    - [General information about git][3] and more detailed discussion [how to use gitlab on MPI-BGC cluster][4];
    - [Using Github on MPI-BGC cluster][5];

Don't forget to get access to MPI-BGC Discourse.

[2]: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account
[3]: https://bgc.discourse.mpg.de/t/git-usage-tutorial/40
[4]: https://bgc.discourse.mpg.de/t/git-usage-tutorial-discussion/3049
[5]: https://bgc.discourse.mpg.de/t/using-github-on-cluster-development-nodes/3711
[6]: https://bgc.discourse.mpg.de/t/setting-up-python-ipython-jupyter-on-the-slurm-cluster/2975
[7]: https://bgc.discourse.mpg.de/t/python-code-publishing-recipes-and-info/2132
[8]: https://bgc.discourse.mpg.de/t/how-to-embarassingly-parallel-python-jobs-on-bgc-slurm-cluster/3691
[9]: https://bgc.discourse.mpg.de/t/introduction-to-bgc-slurm-cluster/3142
[10]: https://bgc.discourse.mpg.de/t/bgc-slurm-cluster-basics/3482
[11]: https://bgc.discourse.mpg.de/t/basic-introduction-to-the-bgc-slurm-cluster/3663