import re


class TableFrame:
    def __init__(self, source) -> None:
        self.source = source
        self.resort_name = "Marriott"
        self.min_bedroom = 1

    def get_num_of_bedroom(self):
        span = re.search(r'<span id="bedrooms">(.+?)</span>', self.source)
        num_of_bedroom = span.group().split(">")[1].split("<")[0]
        try:
            num_of_bedroom = int(num_of_bedroom)
        except:
            num_of_bedroom = 0
        return num_of_bedroom

    def get_resort_name(self):
        span = re.search(
            r'<h3 class="resort_name">(.+?)</h3>', self.source, flags=re.DOTALL
        ).group()
        span2 = re.search(r';"(.+?)</a>', span, flags=re.DOTALL).group()
        resort_name = span2.split(">")[1].split("<")[0]
        return resort_name.strip()

    def get_date(self):
        regex = r'<td width="50%">(.+?)</div>'
        span = re.search(regex, self.source, flags=re.DOTALL).group()
        date = span.split(">")[2].split("<")[0].strip()
        return date

    def check(self):
        num_of_bedroom = self.get_num_of_bedroom()
        resort_name = self.get_resort_name()
        date = self.get_date()
        if num_of_bedroom >= self.min_bedroom and self.resort_name in resort_name:
            return self.send_sms(num_of_bedroom, resort_name, date)
        else:
            return False
