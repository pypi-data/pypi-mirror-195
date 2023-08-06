class NoBalance(Exception):
  def __init__(self, message: str, status_code: int):
    self.message = message
    self.status_code = status_code
    
  def __str__(self):
    return "({}) {}".format(self.message, str(self.status_code))  
    
class HCaptchaError(Exception):
  def __init__(self, message: str, status_code: int):
    self.message = message
    self.status_code = status_code
    
  def __str__(self):
    return "({}) {}".format(self.message, str(self.status_code))