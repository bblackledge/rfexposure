let helpTexts = "";
let helpTitle = "";


helpTitle = {
    report_description: `<span><strong>Report Description</strong></span>`,
    antenna_description: `<span><strong>Antenna Description</strong></span>`,
    operator_name: `<span><strong>First and Last Name</strong></span>`,
    call_sign: `<span><strong>Call Sign</strong></span>`,
    email: `<span><strong>Email Address</strong></span>`,
    frequency_mode: `<span><strong>Multi-Band Group</strong></span>`,
    frequency_position: `<span><strong>Frequency Position in the Band</strong></span>`,
    frequency: `<span><strong>Single Frequency Exposure Analysis</strong></span>`,
    antenna_gain: `<span><strong>Antenna Gain</strong></span>`,
    power: `<span><strong>Use Ground Reflection Effects in Analysis</strong></span>`,
    effective_power: `<span><strong>Transmitter Power</strong></span>`,
    duty_factor: `<span><strong>Mode Duty Factor</strong></span>`,
    transmit_time: `<span><strong>Transmit Time</strong></span>`,
    receive_time: `<span><strong>Receive Time</strong></span>`,
    include_calculations: `<span><strong>Include Calculations</strong></span>`,
};


helpTexts = {
    report_description: `Enter a short, less than 128 characters, <strong>Report Description</strong> for this set 
                         of computations. The description should be concise yet informative enough to identify 
                         the report easily. For example, "<b>Field Day Event Exposure Report</b>" or "<b>Home Station 
                         Compliance Check for G5RV at 100 Watts</b>."`,

    antenna_description: `Provide a concise description of your antenna, including any relevant details such 
                          as the model, type, and installation specifics. For example, 
                          "20-Meter Dipole Mounted at 30 feet" or "Yagi 3-Element at 40 Feet."`,

    operator_name: `Enter your <b>First and Last Name</b> as you would like it to appear on the report. 
                    This information will ensure that the report is personalized and identifiable.`,

    call_sign: `Enter your U.S. amateur radio <b>Call Sign</b>. This call sign will appear prominently in the report.`,

    email: `Please provide a valid <b>Email Address</b> that will appear prominently in the report.`,

    frequency_mode: `RFExposure is capable of generating exposure calculations for a <b>single frequency</b> similar 
                     to the legacy RF exposure calculators operators have used for years. 
                     <br><br>
                     However, RFExposure, by default, automatically 
                     calculates and reports exposure limits across multiple U.S. amateur radio bands that we define
                     as <b>Multi-Band Groups</b>. These groups are based on the frequency ranges of the U.S. amateur 
                     radio bands defined as either <b>MF/HF bands (1.8MHz to 54.0 MHz)</b> or 
                     <b>VHF/UHF bands (50MHz to 1.3 GHz)</b>. 
                     <br/><br/>
                     Select the Multi-Band Group you wish to generate an RF Exposure Report. Exposure limits 
                     for each U.S. Amateur Radio Band defined within the selected multi-band group's frequency 
                     range are then automatically generated for the exposure report.`,

    frequency_position: `Select the band's <b>Frequency Position</b> to use in computing exposure limits. 
                         By default, the <b>Highest</b> frequency value within each band is used in computing 
                         exposure limits. However, you may also select for analysis either the <b>Center</b> 
                         frequency or the <b>Lowest</b> frequency value within each band.   
                         <br/><br/>
                         For example, the <b>20 Meter Band</b> has a frequency range of <b>14.000 MHz to 14.350 MHz</b>.
                         Thus, the <b>Lowest</b> frequency value is 14.000 MHz, the <b>Center</b> frequency value 
                         is 14.175 MHz, and the <b>Highest</b> frequency value is 14.350 MHz.`,

    frequency: `If you wish to analyze exposure limits for only a <b>single frequency</b>, enter a valid 
                U.S. amateur band frequency (in the range of <b>1.8 to 1,300 MHz</b>) here.
                This feature is particularly useful if your 
                setup operates predominantly on a single frequency rather than across a range.
                <br><br>
                It's important to note that when the <b>Single Frequency Exposure Analysis</b> field is selected, 
                any values selected in either the <b>Multi-Band Group</b> and <b>Frequency Position in Band</b> 
                fields are ignored and a RF exposure report is generated with only the single frequency entered.
`,

    antenna_gain: `Enter your antenna's <b>Antenna Gain</b> value in dBi as specified by the antenna manufacturer 
                   or determined through measurement. 
                   <br><br>
                   Antenna gain is a measure of how efficiently an antenna directs radio frequency (RF) energy in 
                   a specific direction compared to an ideal reference, such as an isotropic radiator (dBi) 
                   or a half-wave dipole (dBd). Gain is not an increase in transmitted power but rather a 
                   redistribution of energy, focusing the signal in certain directions while reducing it in others. 
                   This directional enhancement improves communication range and signal strength in desired paths, 
                   making it a critical factor in antenna system design.

                    <br><br><b>
                    Antenna gain is particularly important when computing RF exposure levels, as it directly 
                    influences the Effective Radiated Power (ERP) or Equivalent Isotropically Radiated Power (EIRP). 
                    Since RF exposure regulations, such as those from the FCC, are based on power density at a 
                    given distance, a high-gain antenna can significantly increase localized exposure in its main lobe. 
                    Understanding gain is essential in ensuring compliance with safety limits, as operators must 
                    consider how their antenna’s radiation pattern affects exposure to both themselves and 
                    others in the vicinity.</b>`,

    ground_reflection: `If you want to factor in <b>Ground Reflections</b> for a worst-case scenario analysis, 
                        check the "<b>Use Ground Reflection Effects</b>" box. This option is recommended if your 
                        antenna is installed at a height where ground reflections might significantly 
                        affect exposure levels.
                        <br><br>
                        Because we are creating a truly "worst case" calculation of power density near surfaces, 
                        such as ground-level areas or rooftops, 100% reflection of incoming radiation represents 
                        can be assumed. The U.S. Environmental Protection Agency (EPA) developed models for 
                        predicting ground reflection calculations in the context of RF exposure assessments. 
                        These models were used by the Federal Communications Commission (FCC) and referenced 
                        in OET Bulletin 65 for estimating RF field strengths at ground level. These models suggest 
                        that ground reflections can increase field strength by up to 1.6 times, 
                        resulting in a 2.56-fold increase in power density. 
                        `,

     effective_power: `Enter the <b>Power</b> in watts delivered to your antenna during your transmissions.                       
                      Because we are computing worst case exposure levels, 
                      the output wattage from your radio, without line losses, is an acceptable and 
                      desired value for this field.`,

    duty_factor: `Select the <b>Mode Duty Factor</b> that corresponds to your mode of operation. 
                  The selected value represents the percentage of time the transmitter is actually producing 
                  RF energy during a transmission cycle. Different transmission modes (e.g., SSB, CW, FM, etc.) 
                  have varying duty factors. A drop-down menu offers numerous mode settings along with the corresponding
                  Duty Factor percentage (in brackets) associated with that mode.
                  <br /><br/>
                  <ul>
                      <li>SSB (Conversational, No Speech Processing) [20%]
                      <li>SSB (Conversational, Speech Processing) [50%]</li>
                      <li>CW [40%]</li>
                      <li>FM [100%]</li>
                      <li>AM [100%]</li>
                      <li>AFSK (e.g., RTTY, etc.) [100%]</li>
                      <li>FT4 [100%]</li>
                      <li>FT8 [100%]</li>
                      <li>Carrier for Tuning [100%]</li>
                      <li>Unknown Mode (Assume Worst Case) [100%]</li>
                  </ul>
                  `,

    transmit_time: `<b>Transmit Time</b> refers to the duration your station actively sends a signal. For RF exposure 
                    compliance, the FCC allows time-averaging over 6 minutes for occupational settings and 30 minutes 
                    for general public exposure. This means peak transmit power can be higher for short periods 
                    as long as the average exposure over the defined time remains within safe limits.
                    <br/><br/>
                    <b>Example</b><br/>
                    Consider an amateur radio operator running a 100-watt transmitter. If they transmit continuously 
                    for 6 minutes, their full power output must be evaluated against the FCC's exposure limits. 
                    However, if they transmit for only 3 minutes and receive for the next 3 minutes, 
                    the effective average transmit power over the 6-minute period is reduced by half (50 watts). 
                    This reduction is important because RF exposure is based on the average power a person is 
                    exposed to over time. By using push-to-talk (PTT) operation or cycling transmissions, operators 
                    can manage their duty cycle, reducing overall RF exposure and potentially allowing for higher 
                    peak power operation while still remaining compliant.`,

    receive_time: `<b>Receive</b> time is when your station is actively listening but not transmitting a signal. 
                   Since no RF energy is emitted during this time, receive periods help lower overall exposure 
                   when averaged with transmit time. The longer the receive time, the lower the averaged RF exposure, 
                   which can be important for meeting FCC compliance guidelines.
                    <br/><br/>
                    <b>Example</b><br/>
                    Suppose a radio operator is engaged in a two-way conversation using a 50-watt transmitter. 
                    If they talk for 2 minutes and then listen for 4 minutes, the overall RF exposure is 
                    significantly lower than if they had transmitted continuously. This is because, during 
                    the receive period, no RF energy is being emitted, effectively bringing the exposure down 
                    to zero for that duration. Over a full 6-minute averaging window, the effective exposure 
                    would be calculated as ((50W × 2 minutes) + (0W × 4 minutes)) ÷ 6 minutes = 16.7 watts 
                    average power. This illustrates how receive time plays a crucial role in exposure calculations, 
                    making intermittent transmissions much safer compared to continuous operation.`,

    include_calculations: `If you want to review detailed exposure calculations for each frequency analyzed, 
                           check the "<b>Include Calculation Pages in Report</b>" check box. When selected, 
                           this option instructs the report generator to create a 
                           separate calculation page for each frequency included in the report. 
                           This option is helpful for those who need a comprehensive understanding of the exposure 
                           levels at each frequency and how these calculations were generated.`,
}