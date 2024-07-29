import re
import whois

def extract_domain(email):
    match = re.match(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@([a-z0-9-]+(\.[a-z0-9-]+)*\.[a-z]{2,})$', email)
    if match:
        return match.group(2)
    else:
        raise ValueError('电子邮件格式无效')

def get_domain_country(domain):
    try:
        domain_info = whois.whois(domain)
        if domain_info:
            if isinstance(domain_info, list):
                domain_info = domain_info[0]
            country = domain_info.get('country')
            if country:
                return country
            else:
                return "未知"
        else:
            return "未知"
    except Exception as e:
        print(f"错误: {e}")
        return "未知"

if __name__ == "__main__":
    input_email = input("请输入要分析的电子邮件地址：")
    domain = extract_domain(input_email)
    country = get_domain_country(domain)
    print(f"域名 {domain} 注册在 {country}")
