import re

aa = re.compile('您的验证码是：(\d+),').findall(
    '''<p style="text-align:left;" size="0" _root="undefined" __ownerid="undefined" __hash="undefined" __altered="false">尊敬的用户：<br/>您好，欢迎使用票易通发票管理及供应链协同平台<br/>您的验证码是：879076,请在15分钟内在页面填入验证码<br/>如果您并未发出此请求，请忽略此邮件。</p><p></p><p>专业的增值税发票管理及供应链协同平台</p><p>为您解决一切后顾之忧</p><p>本邮件由系统自动发出，请勿直接回复<br/></p>''')[
    0]
