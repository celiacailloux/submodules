# submodules

submodules is a repository containing modules and objects that I use frequently when handling data and automating data processes. 

## Purpose

I like to google smart ways to handle data and to conduct mathematical operations and modelling - using a variety of packages but also incorporating other people's codes (thank your stackoverflow!). 
But I also to easily be able to reuse my modules and objects - aka saving time! This is why I gather all my modules and object in one repository that I can easily clone.

## Usage 

I use git's tool *Submodules* to keep my repository *submodules* as a subdirectory of my project.
*Git Submodules* allows me to keep a Git repository as a subdirectory of my main Git repository (for more info > [Git - Submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules)). See example in [PhD-Data-Analysis > XRD](PhD-Data-Analysis/README.md) under *folder structure*.
This way I can clone *submodules* into my project and while keeping my commits separate.

## Directory Structure

All modules are named in such a way that the first word mirrors the category of the modules, e.g., *api, file_managing, plot, ..., etc.*. 
Next, is a specifikation or subcategory, e.g., *api_Dropbox, api_OneDrive*. For the more general or uncategorizable specifications exist a *misc* module, e.g., *plot_misc*. I.e.

- category1_subcategory1
- category1_subcategory2
- category1_subcategory3
- category1_misc
- category2_subcategory1
- category2_subcategory2
- category2_misc

## Packages

- pandas
- matplotlib
- lmfit
- scipy
- os
- sys
