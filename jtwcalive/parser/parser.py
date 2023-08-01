from jtwcalive.tc.tc import TC

from pathlib import Path
import re


class Parser:
    def __init__(self, report_txt: str):
        if not Path(report_txt).exists():
            raise FileNotFoundError(f"{report_txt} not found!")

        if not Path(report_txt).suffix == ".txt":
            raise TypeError(f"{report_txt} is not a txt file!")

        self.report_txt = Path(report_txt)

    @property
    def txt(self) -> str:
        with open(self.report_txt, "r") as f:
            return f.read()

    def parse(self) -> TC:
        txt = self.txt

        # Extract typhoon name and id
        typhoon_info = re.search(r'TYPHOON (\d{2}W) \((\w+)\)', txt)
        typhoon_id, typhoon_name = typhoon_info.groups()

        # Extract forecast information
        forecast_info = re.findall(
            r'(\d{2} HRS, VALID AT:\n   \d{6}Z --- [\d\.]+N [\d\.]+E\n   MAX SUSTAINED WINDS - \d+ KT, GUSTS \d+ KT.*?)(?=\n   \d{2} HRS, VALID AT:|\nREMARKS:)',
            txt, re.DOTALL)

        forecast_data = []
        for info in forecast_info:
            time = re.search(r'(\d{2}) HRS', info).group(1)
            position = re.search(r'VALID AT:\n   \d{6}Z --- ([\d\.]+N [\d\.]+E)', info).group(1)
            max_wind = re.search(r'MAX SUSTAINED WINDS - (\d+ KT, GUSTS \d+ KT)', info).group(1)
            wind_radii = re.findall(
                r'RADIUS OF (\d{3} KT WINDS - \d+ NM NORTHEAST QUADRANT\n                            \d+ NM SOUTHEAST QUADRANT\n                            \d+ NM SOUTHWEST QUADRANT\n                            \d+ NM NORTHWEST QUADRANT)',
                info)
            forecast_data.append({
                'time': time,
                'position': position,
                'max_wind': max_wind,
                'wind_radii': wind_radii
            })

        tc = TC(
            src="test",
            typhoon_id=typhoon_id,
            typhoon_name=typhoon_name,
        )

        for data in forecast_data:
            tc.append(
                tc.create_node(
                    time=data['time'],
                    lat=data['position'].split()[0],
                    lon=data['position'].split()[1],
                    ws=data['max_wind'],
                )
            )

