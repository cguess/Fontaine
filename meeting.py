import datetime
dateformat = "%Y-%m-%d"

class Meeting:

  def __init__(self, name, text, year, month, day, length):
        self.name = name.lstrip().rstrip().encode('utf-8')
        self.text = text.lstrip().rstrip().encode('utf-8')
        self.date = datetime.date(year, Meeting.number_for_month_name(month), day)
        self.length = length
  
  @classmethod      
  def number_for_month_name(self, month):
        #note: there's no default case here, should fix that
        return {
          'Jan': 1,
          'Feb': 2,
          'Mar': 3,
          'Apr': 4,
          'May': 5,
          'Jun': 6,
          'Jul': 7,
          'Aug': 8,
          'Sep': 9,
          'Oct': 10,
          'Nov': 11,
          'Dec': 12
        } [month]
    
  def list_representation(self):
    return [self.date.strftime(dateformat), self.length, self.name, self.text]
  
  def date_as_string(self):
    return self.date.strftime(dateformat)