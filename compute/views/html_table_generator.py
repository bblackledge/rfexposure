class ListTable:
    def __init__(self):
        self.data_list = []
        self.crlf = ""

    def build_header(self):
        titles = [
            "<p>Frequency</p><p>(Mhz)</p>",
            "<p>Controlled Maximum<p>Density (mW/cm²)</p>",
            "<p>Controlled Minimum<p> <p>Distance (ft.)</p>",
            "<p>Uncontrolled Maximum<p>Density (mW/cm²)</p>",
            "<p>Uncontrolled Minimum</p> <p>Distance (ft.)</p>"
        ]

        ts = "<font size='2' face='Arial'>"
        ts += "<table border=1>"
        ts += "<thead style='background-color: #D6EAF8'>\n"
        for h in titles:
            ts += "<th align='center' style='padding: 10px'>" + h + "</th>\n"
        ts += "</thead>\n"
        return ts

    def build_parameter_list(self):
        str = """
        <p>Transmission Watts: {transmit_watts}</p>
        <p>Antenna Gain (dBi): {antenna_gain}</p>
        <p>Transmit Frequency (MHz): {transmit_frequency}</p>
        <p>Ground Reference: {use_ground_reference}</p>
        <p>Mode Duty Cycle (%): {mode_duty_cycle}</p>
        <p>Transmit Minutes: {txt}</p>
        <p>Receive Minutes: {rct}</p>
        """


    def build_footer(self):
        ts = "</table>\n"
        return ts

    def build_table(self):
        str = self.build_header()
        str += self.build_parameter_list()
        for index, d in enumerate(self.data_list):
            bg_color = "#fff" if index % 2 == 0 else "#D6EAF8"
            str += f"<tr style='valign=middle; height: 35px; background-color: {bg_color}'>" + d + "</tr>\n"
        str += self.build_footer()
        return str

    def add_row(self, data_list):
        ts = ""
        for data in data_list:
            ts += "<td align='right' style='padding-right: 10px'>" + data + "</td>"
        self.data_list.append(ts)

    # File output of table to an HTML file
    def write_to_html(self, filename):
        with open(filename, 'w') as file:
            file.write(self.build_table())