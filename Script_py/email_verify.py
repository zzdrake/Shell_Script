import re
import smtplib
import dns.resolver
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# 发件人邮箱地址（可为任意有效邮箱）
fromAddress = 'cron@bt.com'

# 正则表达式用于验证基本的邮箱格式
regex = r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[_a-z0-9-]+)*(\.[a-z]{2,})$'

# 用于存储无效邮箱地址的列表
invalid_emails = []
dns_cache = {}

def check_email(email):
    if pd.isna(email):
        return None
    email = str(email).strip()
    match = re.match(regex, email)
    if match is None:
        return {'邮箱': email, '原因': 'Bad Syntax'}

    splitAddress = email.split('@')
    if len(splitAddress) != 2:
        return {'邮箱': email, '原因': 'Invalid Format'}

    domain = str(splitAddress[1])
    print(f'Checking domain: {domain} for email: {email}')

    if domain in dns_cache:
        mxRecord = dns_cache[domain]
    else:
        try:
            # 查找 MX 记录
            records = dns.resolver.resolve(domain, 'MX')
            mxRecord = str(records[0].exchange)
            dns_cache[domain] = mxRecord
        except (dns.resolver.NoNameservers, dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout) as e:
            return {'邮箱': email, '原因': f'Domain Error: {e}'}

    try:
        # 连接到邮箱服务器并验证邮箱地址
        server = smtplib.SMTP(timeout=10)
        server.set_debuglevel(0)

        server.connect(mxRecord)
        server.helo(server.local_hostname)
        server.mail(fromAddress)
        code, message = server.rcpt(email)
        server.quit()

        if code != 250:
            return {'邮箱': email, '原因': 'Invalid Address'}
    except Exception as e:
        return {'邮箱': email, '原因': f'Error: {str(e)}'}
    return None

def process_worksheet(worksheet):
    # 读取工作表中的数据
    df = worksheet
    
    # 假设邮箱列的列名为 "邮箱"
    email_column = df['邮箱']
    
    # 使用线程池并行处理
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(check_email, email_column))
    
    # 过滤掉 None 值（即有效的邮箱）
    invalid_emails.extend([result for result in results if result is not None])

# 读取 Excel 文件中的所有工作表
file_path = 'xxx.xlsx'
with pd.ExcelFile(file_path) as xls:
    sheet_names = xls.sheet_names
    for sheet_name in sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        process_worksheet(df)

# 将无效邮箱地址保存到 Excel 文件中
invalid_emails_df = pd.DataFrame(invalid_emails)
invalid_emails_df.to_excel('invalid_emails_all.xlsx', index=False, engine='openpyxl')

print("Invalid emails have been saved to 'invalid_emails.xlsx'")