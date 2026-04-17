

# Introduction 



Welcome to the **RFExposure User's Manual**. This guide is designed to assist amateur radio operators in using this RF exposure report tool, which helps ensure compliance with regulatory guidelines by calculating potential RF exposure limits for your specific radio setup. The manual first guides you through a series of data entry panels, each of which collects important information that will be used to generate a personalized RF exposure report. Next, it explains the results generated, as well as details (if selected by the user) calculations made for each frequency analyzed.

### Purpose of the Form

The **RFExposure Calculation Worksheet** is where we define an antenna's operating parameters for calculating a complete RF exposure report. The required data and the data entry process for a given antenna is very similar to the legacy RF exposure calculator models employed by amateur radio operators for many years. 

However, there are some data entry differences that you should to be aware of:

* To define various report titles and labels, there is a short worksheet section called **Report Personalization** where you define a description of the report, as well as define your name, call sign, and email address which are printed on the cover page.

* RF Exposure Report features the ability to compute either "**Single** **Frequency**" or "**Multi-Band Group** exposure analyses. If you choose the "Single Band" option, the calculator works virtually identical to legacy RF exposure calculators. However, if you select the "Multi-Band Group" option, all "bands" within either the "HF" or "VHF/UHF" frequency ranges will be generated.

* The **Transmission Specifications** section of the worksheet now supports **FT8** and **FT4** as selections in the **Mode Duty Factor** field. The existing legacy calculators don't support sub-minute Transmit and Receive Times in their internal power calculation algorithms. 

The primary purpose of the RF Exposure Report tool is to assess the potential exposure to radio frequency (RF) energy that may result from your antenna system. The report you generate will provide a detailed analysis based on the data you enter, including the type of antenna, transmission power, operating frequency, and other key parameters. This report is crucial for ensuring that your station complies with regulatory exposure limits, thereby protecting you and others from excessive RF exposure.

### Summary of Panels

1. **Report Personalization:** In this panel, you'll provide essential details to personalize your report, such as a brief description of the report, your full name, amateur radio call sign, and optionally, your email address.

2. **Single or Multi-Frequency Analysis:** Here, you will select the band plan and frequency position for analysis. You also have the option to focus on a single frequency if your setup requires it.

3. **Antenna Specifications:** This panel captures detailed information about your antenna, including its description, gain, and whether you want to factor in ground reflection effects for a worst-case scenario analysis.

4. **Transmission Specifications:** In this section, you'll specify the transmitter power, mode duty factor, and transmit and receive times. These details are vital for accurately calculating RF exposure.

5. **Generate RF Exposure Report:** The final panel allows you to decide whether to include detailed calculation pages in your report. Once you have reviewed all inputs, you can generate your RF exposure report, which will be customized based on the data provided.

By following this manual and carefully entering the required data, you will ensure that the RF Exposure Report accurately reflects your station's operating conditions, helping you maintain safe and compliant operations.





### Report Personalization

The **Report Personalization** form panel allows users to tailor their RF Exposure report by providing essential information that will be reflected throughout the report. The form collects basic details such as a description of the report, the user's name, their amateur radio call sign, and an optional email address. This information helps personalize the generated report, making it specific to the user's unique radio/antenna configuration and preferences.

#### Data Entry Fields

1. **Report Description**  
   - **Purpose:** This field is for entering a short description of the report. The description should summarize the content or purpose of the report. 
   - **Character Limit:** 128 characters.
   - **Mandatory:** Yes.
   - **Guidance:** The description should be concise yet informative enough to identify the report easily. For example, "Field Day Event Exposure Report" or "Home Station Compliance Check."

2. **First and Last Name**  
   - **Purpose:** This field captures the user's full name, which will be displayed on the report.
   - **Mandatory:** Yes.
   - **Guidance:** Enter your first and last name as you would like it to appear on the report. This will ensure that the report is personalized and identifiable.

3. **Call Sign**  
   - **Purpose:** The call sign uniquely identifies the amateur radio operator. It is an essential part of the report, linking the report to the operator's licensed identity.
   - **Mandatory:** Yes.
   - **Guidance:** Enter your U.S. amateur radio call sign in the format. This call sign will appear prominently in the report.

4. **Email Address**  
   - **Purpose:** The email address allows for optional contact or follow-up regarding the report.
   - **Mandatory:** No.
   - **Guidance:** If you would like to receive a copy of the report via email or want to be contacted for further communication, please provide a valid email address. This field can be left blank if you do not wish to share your email address.

#### Additional Information
- **Information Icons**: Small blue icons with an "i" are located next to each field label. Hovering over these icons will provide additional information or tips regarding the corresponding field.
- **Field Requirements**: Fields marked with an asterisk (*) are mandatory and must be completed before proceeding to the next step.





### Single or Multi-Frequency Analysis Panel

The **Single or Multi-Frequency Analysis** panel allows users to select the specific Amateur Radio Band Plan and Frequency Position that will be used to generate the RF Exposure Report. The panel also offers an option to analyze a single frequency within a band, providing flexibility in how exposure limits are calculated and reported.

#### Data Entry Fields

1. **Band Plan to Generate Exposure Report**
   - **Purpose:** This field allows the user to select the desired Amateur Radio Band Plan for which the RF Exposure Report will be generated. The chosen band plan determines the frequency ranges that will be analyzed.
   - **Options:** 
     - MF/HF (137.8 kHz - 54.0 MHz)
     - [Additional options may be available based on the full list within the application]
   - **Mandatory:** Yes.
   - **Guidance:** Select the band plan that corresponds to the frequencies you are interested in. The RF exposure limits for each band within the selected plan will be automatically generated for the report.

   
   
2. **Frequency Position in Band**
   - **Purpose:** This field specifies which frequency position within the selected band will be used for computing RF exposure limits. The default setting uses the highest frequency value in the band, but the user can choose other positions as needed.
   - **Options:**
     - Highest Frequency in Band
     - Lowest Frequency in Band
     - [Additional options based on the band plan]
   - **Mandatory:** Yes.
   - **Guidance:** If you want to analyze exposure based on a specific frequency position in the band, select the appropriate option. This allows for more targeted analysis based on the characteristics of your radio setup.

   
   
3. **Single Frequency Analysis**
   - **Purpose:** This optional field allows users to specify a single frequency within the chosen band for analysis. When a frequency is entered here, the system will ignore the selected Band Plan and Frequency Position, focusing exclusively on the provided frequency.
   - **Mandatory:** No.
   - **Guidance:** If you wish to analyze exposure limits for a specific frequency only, enter the valid U.S. Amateur Band Frequency (in MHz) here. This feature is particularly useful if your setup operates predominantly on a single frequency rather than across a range.



### Antenna Specifications Panel

The **Antenna Specifications** panel is designed to capture details about the antenna used in your RF Exposure analysis. This section allows you to input a brief description of your antenna, specify its gain, and decide whether to include ground reflection effects in your calculations. The information entered here will influence the accuracy and relevance of the exposure limits calculated in the report.

#### Data Entry Fields

1. **Antenna Description**
   - **Purpose:** This field is for entering a short description of the antenna being analyzed. The description will be used throughout the report to identify the specific antenna setup under review.
   - **Character Limit:** 128 characters.
   - **Mandatory:** Yes.
   - **Guidance:** Provide a concise description of your antenna, including any relevant details such as the model, type, and installation specifics. For example, "Dipole Antenna 20m mounted at 30 feet" or "Yagi 3-element at 40 feet above ground."

2. **Antenna Gain**
   - **Purpose:** This field requires the user to input the gain of the antenna in decibels relative to an isotropic radiator (dBi). Antenna gain is a crucial factor in calculating RF exposure levels as it indicates how much power is directed in a particular direction.
   - **Mandatory:** Yes.
   - **Guidance:** Enter the gain value in dBi as specified by the antenna manufacturer or determined through measurement. This value is essential for accurate exposure calculations.

3. **Ground Reflection Effects**
   - **Purpose:** This checkbox option allows users to include ground reflection effects in the RF exposure analysis. Ground reflections can increase the power density at certain locations, leading to a more conservative (worst-case) exposure scenario.
   - **Mandatory:** No (Optional).
   - **Guidance:** If you want to factor in ground reflections for a worst-case scenario analysis, check the "Use Ground Reflection Effects" box. This option is recommended if your antenna is installed at a height where ground reflections might significantly affect exposure levels.





### Transmission Specifications Panel

The **Transmission Specifications** panel is critical for defining the parameters that directly affect the RF exposure calculations. This section gathers key information about the transmitter power, mode duty factor, and the duration of transmit and receive times. Correctly inputting these values is essential for producing an accurate RF exposure assessment.

#### Data Entry Fields

1. **Transmitter Power**
   - **Purpose:** This field captures the Peak Envelope Power (PEP) that is fed into the antenna during transmission. This value is one of the primary factors in determining RF exposure levels.
   - **Mandatory:** Yes.
   - **Guidance:** Enter the PEP value in watts as used during your transmissions. Ensure that this value reflects the actual power being used for accurate calculations.

   
   
1. **Mode Duty Factor**
   
   - **Purpose:** The Mode Duty Factor represents the percentage of time the transmitter is actually producing RF energy during a transmission cycle. Different transmission modes (e.g., SSB, CW, FM) have varying duty factors.
   - **Options:** A dropdown menu offers various mode settings, such as:
     - SSB (Conversational, No Speech Processing) [20%]
     - CW [40%]
     - FM [100%]
     - [Additional options may be available based on the full list within the application]
   - **Mandatory:** Yes.
   - **Guidance:** Select the duty factor that corresponds to your mode of operation. This value accounts for the nature of the transmission mode and significantly impacts the exposure calculation.
   
   
   
3. **Transmit Time**
   - **Purpose:** This field specifies the duration of time (in minutes) that the transmitter is active during the exposure calculation period.
   - **Mandatory:** Yes.
   - **Guidance:** Select the transmit time in minutes (e.g., 0.125 for 7.5 seconds). This should reflect the average duration of your transmissions during a typical operating period.

   
   
4. **Receive Time**
   
   - **Purpose:** This field captures the duration of time (in minutes) that the station is in receive mode during the exposure calculation period.
   - **Mandatory:** Yes.
   - **Guidance:** Select the receive time in minutes. Typically, this value complements the transmit time, ensuring the total time represents a full operating cycle.






### Generate RF Exposure Report Panel

The **Generate RF Exposure Report** panel is the final step in the process of creating your personalized RF Exposure Report. This section allows you to decide whether to include detailed calculation pages for each frequency in the band plan used. Once your selection is made, you can generate the report, which will incorporate all the data you've entered throughout the previous panels.

#### Data Entry Fields and Options

1. **Include Calculation Pages in Report**
   - **Purpose:** This checkbox option allows users to include detailed calculation pages in their final report. These pages provide an in-depth view of the calculations performed for each frequency within the selected band plan.
   - **Mandatory:** No (Optional).
   - **Guidance:** If you want to review the detailed exposure calculations for each frequency analyzed, check this box. This option is helpful for those who need a comprehensive understanding of the exposure levels across all frequencies. Leaving this box unchecked will produce a more concise report without the detailed calculation breakdowns.

   
   
2. **Generate RF Exposure Report**
   
   - **Purpose:** Clicking this button initiates the generation of your RF Exposure Report based on all the data and selections you've made in the preceding panels.
   - **Mandatory:** Yes.
   - **Guidance:** After verifying your inputs and deciding whether to include calculation pages, click the "Generate RF Exposure Report" button. The system will compile your data into a personalized report, which can then be reviewed, saved, or printed.

#### Next Steps
Once the report is generated, you can review the output to ensure it meets your needs. If any adjustments are required, you may return to the **RF Exposure Report Worksheet** to modify your inputs and regenerate the report.

---

This manual section covers the **Generate RF Exposure Worksheet Report** panel, which concludes the data entry process for creating your RF Exposure Report. Further guidance on interpreting the report or troubleshooting will be provided in subsequent sections of the user manual.

