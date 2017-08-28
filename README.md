## Code for the reproducibility of *MHC-I genotype restricts the oncogenic mutational landscape*.

### Requirements 
All figures are generated in either Python or R. The following libraries are required: <br>

*	Python
	* pandas
	* scipy
	* matplotlib
	* Bio
	* sklearn
	* seaborn
* R
	* parallel
	* lme4
	* mgcv
	* xtable

Furthermore, all figure generating scripts are based on pre-processed data. Please contact me to acquire access to the data.

* Once data is acquired, create update the imports/import.pynb notebook with the location of the data.

### Data processing

Example code for processing the raw data is included in the data_processing directory. Thousands of CPU hours are required to construct the pre-processed data files required to generate the figures. If you want to re-generate the processed data, this code will be a good guideline but pipelines will have to be set up for your own cluster architecture. <br>

Also, the R-based statistical models take some time to run. I have included an independent R script to generate the figures from the model in addition to the jupyter notebooks.
