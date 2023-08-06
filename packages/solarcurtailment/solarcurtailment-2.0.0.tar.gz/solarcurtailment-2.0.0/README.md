## About


This open source tool is written as part of RACE for 2030, Curtailment and Network Voltage Analysis Study (CANVAS) project. The development of the open source tool is supported by funding from Digital Grid Futures Institute (DGFI), University of New South Wales (UNSW). 
This tool measures the amount of curtailed energy from a residential or commercial distributed energy resource such as distributed PV (D-PV) and/or battery energy storage system (BESS) via one of the following inverter power quality response modes (PQRM):
1. Tripping (inverter cease to operate during high voltage conditions)
2. V-VAr Response (high levels of VAr absorbtion and injection limits inverter maximum real power)
3. V-Watt Response (inverter linearly reduces its real power output as a function of voltage conditions)

The tool uses the time-series measurements of:
1. Voltage
2. Real power (D-PV/BESS inverter)
3. Reactive power (D-PV/BESS inverter)
4. Global horizontal irradiance (GHI)
5. Site information (dc and ac capacity of the inverter)

Through analysing the data mentioned above, this tool aims to answer the questions below:
1.	Does the D-PV inverter trip? If so, how often? 
2.	How much energy is lost due to tripping curtailment in kWh/day?
3.	Does the D-PV inverter show V-VAr response?
4.	How much energy is lost due to V-VAr curtailment in kWh/day?
5.	Does the D-PV inverter show V-Watt response?
6.	How much energy is lost due to V-Watt curtailment in kWh/day?

This tool can benefit researchers and future projects which would like to understand and quantify Distributed Energy Resources (DER) curtailment due to different PQRMs.

## Getting Started

This project runs completely in python with common libraries using Jupyter Notebook (or user's preferred integrated development environment -IDE).

For quick start,
1. Download all the required data file and keep it into a certain folder. All the required data files are available in [this link](https://unsw-my.sharepoint.com/:f:/g/personal/z5404477_ad_unsw_edu_au/EvguTkYy48RGiXaQE5aP1l4B2OriyWIwqvi29mUL_ReKDw?e=4ceZec). Files inside the monthly D-PV or monthly GHI data are not needed. The dataset information are available in [this link](https://github.com/mssamhan31/Solar-Curtailment/blob/main/documentations/solar%20curtailment%20dataset%20information.docx). 
2. Install Solar-Curtailment package in terminal using "pip install solarcurtailment". This is then imported in the script using "from solarcurtailment import curtailment_calculation"
3. Adopt the script in [this link](https://github.com/mssamhan31/Solar-Curtailment/blob/main/test/test_solarcurtailment.ipynb), and edit the file_path in accordance with the place you save the data files.

## Demonstration of the tool use
Currently, the tool can only be demonstrated for D-PV systems as the BESS dataset is confidential as per the non-disclosure agreement (NDA) between project partners. The authors are working to obtain BESS data samples that can be used for the demonstration of the tool.

### Input
There are two main inputs for this tool: 
a) Time-series D-PV data from a certain site and a date, and 
b) GHI data of a certain date. 

Sample images for the format of D-PV and GHI data can be seen via the images below:
![Input Data](https://github.com/mssamhan31/Solar-Curtailment/blob/main/image/input_data.PNG?raw=true)  

GHI Data for a certain date (we showed only the relevant column):  
<img width="400" alt="image" src="https://github.com/mssamhan31/Solar-Curtailment/blob/main/image/input_ghi_cleaned.png?raw=true">

The other input files we use are 
1. UniqueCids.csv, consisting of c_id and site_id list for all sites
2. unsw_20190701_circuit_details.csv, consisting the detail of the circuit
3. unsw_20190701_site_details.csv, consisting the detail of the site.
The detailed explanations of all datasets are provided in the 'solar curtailment dataset information.docx' under the documentations folder.
Via using the input data, the tool produces 4 main outputs:


### Output 1. Summary Table
![Output 1](https://github.com/mssamhan31/Solar-Curtailment/blob/main/image/output_summary.PNG?raw=true)  
This summary table shows whether the date is a clear sky day or not, how much is the measured total energy generated in that day, how much is the expected energy generated without curtailment, estimation method used to calculate the expected energy generation, and most importantly:
1.	Tripping response and the associated tripping curtailment
2.	V-VAr response and the associated V-VAr curtailment 
3.	V-Watt response and the associated V-Watt curtailment  
To illustrate the summary table, we visualize the data into 3 plots below:

### Output 2. GHI Plot
![Output 1](https://github.com/mssamhan31/Solar-Curtailment/blob/main/image/output_ghi.png?raw=true)  

This GHI plot shows the irradiance of a certain day.

### Output 3. Scatter plot of real power, reactive power, and power factor vs voltage
![Output 3](https://github.com/mssamhan31/Solar-Curtailment/blob/main/image/output_scatter.png?raw=true)  
The real power and reactive power is normalized by VA rating of the inverter, so the maximum value is 1. For a site with V-VAr response, inverter is expected to absorb/inject VAR according to it's respective V-VAr curve.
For a site with V-Watt response, we expect a scatter of real power to reduce linearly in high voltages (as seen in the image with voltages equal or greater than 251V).

### Output 4. Line plot of real power, reactive power, expected real power, power limit, and voltage vs time.  
![image](https://user-images.githubusercontent.com/110155265/194434048-6eebe057-1a6b-4b0e-bfe9-2055198da1da.png)  

## High Level Explanation of How The Algorithm Works
### Clear Sky Day Determination
We judge whether a date is a clear sky day or not based on two criterias:
1.	The average change of GHI between two consecutive time is lower than a certain threshold which suggests there is no or minimum sudden change in GHI. Sudden change in the GHI means there is a cloud cover.
2.	The maximum GHI value is higher than a certain threshold, which must be true if there is no cloud.

### Daily Energy Generated Calculation
We calculate this value to show how much is the actual daily energy generated. This value is shown in the summary table (output 1). The difference between this value and the expected energy generated without curtailment is the total curtailed energy.  
To calculate the energy generation, we use the D-PV time series data and use these steps: 
1.	Calculate every 1 minutely energy value in Wh using the real power data value.
2.	Sum all the 1 minutely energy values within the day.
3.	Divide it by 1000 to convert the unit into kWh/day.

### Expected Energy Generated Calculation
We essentially use similar process with the energy generated calculation, but we use expected power values instead of real power value. The expected power values are obtained using estimation method below:

### Estimation Method
To obtain the power_expected value in the D-PV time series data, we use these logics:  
If it is a clear sky day: Use polyfit estimation (see below).  
Else if it is not a clear sky day and there is tripping curtailment: Use linear estimation (see below).  
Else if it is not a clear sky day and there is no tripping curtailment: Do not estimate, because we cannot be sure whether the reduction in power is due to V-VAr curtailment, V-Watt curtailment, or cloud cover.   

### Linear Estimation
This method is only used in a non clear sky day with tripping curtailment. Major steps:
1.	Filter the D-PV time series data into times between sunrise and sunset.
2.	Detect the zero power values, which indicates a tripping event.
3.	Detect the ramping down power values before zero values and ramping up power values after zero values, and consider them as tripping event as well.
4.	Detect starting point and end point for each tripping event.
5.	Use points obtained from step 4 to make a linear regression of each tripping event, and use the linear equation to get the estimated power value without curtailment in every tripping timestamps.
6.	For times other than the tripping event, leave the power expected to be the same with the actual power.  

Sample result can be seen below:
![image](https://user-images.githubusercontent.com/110155265/193732043-71bb6e3b-608b-4f25-9c26-15ff328222bb.png)


### Polyfit Estimation
This method is only used in a clear-sky day condition. It is used to estimate the power expected without curtailment. To make the polyfit estimate, we first filter points to be used in the polyfit estimation. Necessary steps include:
1.	Filter the D-PV time series data into times between sunrise and sunset. Before sunrise and after sunset, the real power value is zero, so they should not be used for the polyfit estimation. 
2.	Filter out curtailed power values because we want the estimation fits the actual power without curtailment (D-PV is expected to generate a parabolic curve in clear sky-day conditions. This is validated through observing the system throughout the year and confirm that it is not exposed to regular shading conditions). We filter the curtailed power because it does not make sense to fit the polyfit estimate with the curtailed power. The method we use:  
a. Seperate the power data into two parts: sunrise until solar noon, and solar noon until sunset  
b. In the first half of the data (from sunrise until solar noon), we include only increasing power value  
c. In the second half of the data (solar noon until sunset), we invert the data so the order is from sunset to solar noon  
d. In that second half of the data, we include only increasing power value.  
3.	Filter to include only decreasing gradient real power value. In a parabolic curve with concavity facing downward, the slope is always decreasing. In other words, the gradient is always decreasing, meaning the second derivative is always negative. The illustration can be seen below: 
<img width="450" alt="image" src="https://user-images.githubusercontent.com/110155265/193730666-e3ac130c-ece7-4115-a8f3-2abdbc1e4c0c.png">
<img width="450" alt="image" src="https://user-images.githubusercontent.com/110155265/193735422-96f7466f-4734-4dbf-b4f5-802e64d87fcd.png">

In this image, P3 is filtered out because it is a curtailed power data point (step 2b). P6 is also filtered out because the slope from P4 to P6 is higher than P2 to P4 (step 3). 
 
After filtering the points to be used in the fitting, we then proceed into:  
4.	Convert the timestamp from datetime object into numerical values for fitting  
5.	Fit the power values & numerical timestamp values using a polyfit with degree = 2 (quadratic function)  
6.	Obtain the values of the expected power by the polyfit for all timestamps, including outside of the times used for the fitting  
The sample result can be seen below: 
![image](https://user-images.githubusercontent.com/110155265/193734988-495fdce7-a941-475b-8f78-9ac4229d05ea.png) 

### Tripping Detection
The method is described already in the linear estimation section. We basically say there is a tripping curtailment if there are zero values (sudden drop to zero from a non-zero value) between the sunrise and sunset time. 

### Tripping Curtailed Energy Calculation
For a tripping case in a non clear sky day, using the linear estimation, we calculate the energy generation expected. The amount of curtailment is equal to the energy generation expected minus energy generated. For a tripping case in a clear sky day, we just replace the linear estimation by the polyfit estimation.

### V-VAr Response Detection
The V-VAr response example can be seen in the picture below.  
![image](https://user-images.githubusercontent.com/110155265/194429863-41bdbe57-6837-4825-b22c-ea899512478a.png)  
This image is taken from AS-NZS 4777.2 2020. At low voltage, the system is injecting reactive power to the grid. At high voltage, the system is absorbing reactive power from the grid. 

If the V-VAr response of an inverter is not enabled, we expect the reactive power to be always zero and the power factor is always 1. So, our first step is to check whether the site injects or absorbs reactive power more than a certain threshold, which is 100 VAr.

For a site having reactive power more than 100 VAr, we then compare their V-VAr scatter plots against some benchmarks which are V-VAr curve from SAPN TS-129, AS-NZS 4777.2 2015, ENA recommendation – 2019, and AS-NZS 4777.2 2020. We use 100 VAr as a threshold to take into account various glitches and inaccuracies in the monitoring device and circuit (i.e. VAr>100 for an inverter to be considered to absrob/inject any VArs). The comparison can be done either manually via visual inspection or using an algorithm below:
1. Obtain the reactive power level in % for each timestamp.  
2. Recheck and correct the polarity in case it is not valid. At low voltage, the system injects reactive power, so the polarity is positive. At high voltage, in contrast, the system absorbs reactive power, so the polarity is negative. 
3. Filter the data points by including only the the negative, decreasing reactive power. In the V-VAr curve response, it is the line between V3 and V4. We filter it to perform linear regression and obtaining the value of V3 and V4 from the actual data point. Note that we check only this part because voltage below V2 is too low and it is never observed in the actual data.  
4. Make a linear regression based on the filtered data points in the previous step
5. Obtain the value of V3, which is the voltage where the regression line gives zero reactive power. 
6. Obtian the value of V4, which is the voltage where the regression line gives minimum actual reactive power (the most negative reactive power). 
7. Create two buffer line from the linear regression to take random error into account, which is +- 15% from the regression line result.
8. We calculate the percentage of actual reactive power data points, which voltage is between V3 and V4, falling inside the upper and buffer lines made from the previous step.
9. If V3 & V4 are inside the allowed range based on the 4 standards, and the percentage from step 8 is higher than 80%, we say that the site shows V-VAr response.
The illustration can be seen below:
![image](https://user-images.githubusercontent.com/110155265/194430964-a9d299a0-489f-4c10-b765-9759acced2fe.png)  

Please note that, due to some monitoring set-up errors, the raw VAr data needed to be divided by 60 in order to find the actual one minutely values.

### V-VAr Curtailment Calculation
Unlike tripping, where tripping site must have energy curtailment, V-VAr enabled site can have zero curtailment. This is because the real power of the inverter may not be limited in the presence of VAr and it depends on the magnitude of absorbed/injected VArs. For example for an inverter with 5 kVA limit, absorbtion of 3 kVAr leaves 4 kW real power capacity and energy is only curtailed when inverter can generate more than 4 kW which is calculated based on the GHI (i.e. expected energy generation method above). To calculate the energy curtailed due to VVAr:
1.	For clear sky day, we use polyfit to estimate the power generated without curtailment. 
2.	For a non clear sky day, we multiply ghi data, dc_cap, and eff_system to estimate the PV-system power production.   
3.  We filter out instances where inverter isn't absorbing or injecting VArs (there won't be V-VAr curtailment when there is no VAr).
4.  For the remaining instances we compare the real vs. expected generation
5.  We calculate the difference between the power production and the expected power production and if there is any discrepancy, we double check with VAr values to confirm V-VAr curtailment. It is worth to note, however, that the amount of energy curtailed in a non clear sky day are most likely overestimated. This is because no one can sure whether the curtailment is due to V-VAr response or due to cloud.

### V-Watt Response Detection
In a V-Watt enabled site, the real power limit value will decrease linearly with increasing voltage. The illustration, taken from AS/NZS 4777 2020 is shown below.   
<img width="500" alt="illustration_vwatt_curve" src="https://user-images.githubusercontent.com/110155265/193739913-7682ba54-8027-4b54-a756-bba93c038d59.png">

For convenience, let's call voltage where the real power starts decreasing, as threshold voltage. In the picture above, it is denoted as V3. It can vary from 235-255 V according to AS/NZS 4777 2020. The voltage will stop decreasing exactly at V4 = 265 V, where the real power limit is 20% the ac capacity of the inverter (after this voltage, inverter must trip and cease to operate). That is why we need to check the scatter plot of power with voltage, whether it matches one of the possible V-Watt curve, as the voltage threshold can vary from 235-255 V. The preliminary steps for V-Watt response detection are:
1.	If it is not a clear sky day, it is inconclusive. This is because in a non clear sky day, we cannot be sure the decreasing value of real power is due to cloud or due to V-Watt respones.
2.	Else we check the polyfit quality. If the polyfit quality is not good enough, it is inconclusive as well. This is because the ghi observation station can be far than the actual site location, which makes the clear sky day judgement inaccurate. In that case, it is possible for the script to detect the day as a clear sky day, but the polyfit quality is not good enough because the cloud only covers the site area and not the ghi observation station area. 
3.	Else we check whether the dataset contain points where the voltage is more 235 V. If not, it is inconclusive because there are no points to be checked for V-Watt response, as 235 V is the minimum possible value of threshold value.  

If it passes these preliminary steps, meaning it is a clear sky day with good polyfit quality and available overvoltage points, we then check the V-Watt response. For each of the possible V-Watt curve (from 235-255 V threshold voltage), we check the actual data with these steps:
1. Determine the threshold voltage value, for example, 235 V
2. Form a V-Watt response curve with the corresponding threshold value. For example, if we have 235 V as the threshold value, the maximum real power starts decreases linearly until 265 V, where the real power limit is 20%. We call this curve as Power Limit VWatt.
3. Find datapoints where the expected real power is higher than the Power Limit VWatt. It means there is a possibility of curtailment in these datapoints. We call this points as suspect data. The visualization can be seen below. 
![image](https://user-images.githubusercontent.com/110155265/193739423-4d9e537d-936b-44ea-8112-2805ab6848e3.png)  
4. Add buffer for the Power Limit VWatt curve from the step 2, using 150 watt value distance. Using this step, we obtain the lower buffer and upper buffer which is illustrated below.  
![image](https://user-images.githubusercontent.com/110155265/193739479-c1d57c00-d000-4759-93f1-6ae82ba45af0.png)

5.	Then, we count the percentage of datapoints in the suspect data which lie in the buffer range of the V-Watt curve from step 3. The percentage, which we call compliance percentage, is calculated by dividing the number of actual real power points in the buffer range by the total number of actual real power points. If the current compliance percentage is higher than the current best percentage, we renew the best percentage value by this number.  
![image](https://user-images.githubusercontent.com/110155265/193739516-6aa71a98-1859-4ceb-8535-4f437ca313f7.png)

6. We do step 1-5 through all possible threshold voltage and decide which threshold voltage gives the highest compliance percentage and what is its corresponding compliance percentage value.

We decide a certain site is a V-Watt enabled site only if the highest percentage compliance is higher than a percentage threshold, 84% and the number of actual point lying in the buffer is more than a count threshold, which is 30. 

If  
1. The above criteria is not satisfied and 
2. The maximum available voltage of the suspect data is less than 255,  

we say that it is inconclusive due to insufficient data points. This is because the possibility of it being a V-Watt enabled site but the voltage threshold value is higher than the maximum available voltage datapoints. 

If
1. The above criteria is not satisfied and 
2. The maximum available voltage of the suspect data is at least 255,  

we decide that it is a non V-Watt enabled site. 


### V-Watt Curtailment Calculation
For a V-Watt enabled site, the curtailed energy is equal to the expected energy generated subtracted by the actual energy generated. The expected energy generated and the actual energy generated are calculated by the time-series power data and time-series expected power data using the Expected Energy Generation Method by polyfit estimation mentioned before. 

### Sample File Creation
The raw time series D-PV data is from Solar Analytics which consists of a monthly data with 500 sites mixed into a file. In this tool, we analyze a specific site for a certain date. So, for testing purpose, we create sample simply by filtering the data for a certain day and certain site. 
For convenience, we also process the time series D-PV data by converting the time from UTC time into local time (Adelaide GMT + 9:30). 
Similary, the GHI data we have is a monthly data. So, we filter it into certain dates for the sample analysis period. We also process the ghi data by adding a timestamp column by combining some columns like year, month ,day, hour, and minute information. 

## Tool Limitation & Notes

1. The tool is currently limited to measuring one curtailment mode at a time. Tripping curtailment can't co-exist with other modes however, V-VAr and V-Watt can operate simultaneously. In the studied sites, majority didn't have V-VAr mode enabled so this limitation didn't impact our results. However, as more inverters start complying with both modes, analysis of simultaneous operations of these modes are necessary and this is a primary future research objective.

2. The data-set doesn't include the actual VA capacity of the inverter, and therefore, we used the AC capacity as VA capacity. For some sites, this was an underestimation, as their VA capacity calculated from the real and reactive power exceeded the inverter's AC capacity. This may have resulted in over-estimation of V-VAr curtailment for some inverters as they had higher VA capacity in reality than their assumed VA capacity (AC capacity) in our study.   


## Some Related Articles and Papers
1. https://www.pv-magazine-australia.com/2021/05/24/unsw-digs-the-data-how-much-solar-energy-is-lost-through-automated-inverter-settings/
2. https://www.abc.net.au/news/science/2022-02-16/solar-how-is-it-affected-by-renewable-energy-curtailment/100830738
3. https://greenreview.com.au/energy/rooftop-solar-pv-curtailment-raises-fairness-concerns/
4. https://theconversation.com/solar-curtailment-is-emerging-as-a-new-challenge-to-overcome-as-australia-dashes-for-rooftop-solar-172152
5. https://www.racefor2030.com.au/wp-content/uploads/2021/11/CANVAS-Succinct-Final-Report_11.11.21.pdf

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for instructions to contribute to this open-source tool.

## Project Partners
The project partners of CANVAS are: AGL, SA Power Networks (SAPN), Solar Analytics, and University of New South Wales (UNSW).

## Authors

* **Naomi M Stringer** - *Tripping Algorithm*
* **Baran Yildiz** - *VVAr Algorithm* & Lead Chief Investigator
* **Tim Klymenko** - *VWatt Algorithm*
* **M. Syahman Samhan** - *Merging of algorithms, Open Source Development & Implementation, Debugging*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details. 

## Contact
Email baran.yildiz@unsw.edu.au
