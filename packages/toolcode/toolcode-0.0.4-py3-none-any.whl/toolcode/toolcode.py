try:
    import requests
    import re
except ImportError:
    import os,sys
    os.system('pip install requests')
    print('pls restart file code')
class fbreact:
    def __init__(self,id,cookie,type):
        s=requests.session()
        s.headers.update({"Host":"mbasic.facebook.com","content-type":"application/x-www-form-urlencoded","user-agent":"Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36","accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","sec-fetch-site":"same-origin","sec-fetch-mode":"navigate","sec-fetch-user":"?1","sec-fetch-dest":"document","cookie":cookie})
        url2=s.get(f'https://mbasic.facebook.com/{id}').url
        url=s.get(url2).text
        findreact=re.findall('/reactions/picker/?.*?"',url)
        if findreact==[]:
            print('REACT ERROR ',end=('\r'))
            print('             ',end=('\r'))   
        else:
            replacereact2=findreact[0].replace('"',"")
            replacereact=replacereact2.replace("amp;","")
            react2=s.get(f"https://mbasic.facebook.com{replacereact}").text
            react=re.findall('/ufi/reaction/?.*?"',react2)
            if react==[]:
                print('REACT ERROR ',end=('\r'))
                print('             ',end=('\r'))   
            else:
                if type=='love' or type=='LOVE':
                    so=1
                elif type=='care' or type=='CARE':
                    so=2
                elif type=='haha' or type=='HAHA':
                    so=3
                elif type=='wow' or type=='WOW':
                    so=4
                elif type=='sad' or type=='SAD':
                    so=5
                elif type=='angry' or type=='ANGRY':
                    so=6
                else:
                    so='error'
                if so=='error':
                    print('type error',end=('\r'))
                    print('                              ',end=('\r'))
                else:
                    replacereact3=react[so].replace('"',"")
                    replacereact4=replacereact3.replace("amp;","")
                    done=s.get(f"https://mbasic.facebook.com{replacereact4}").text
                    try:
                        self.mess=s.get(f"https://mbasic.facebook.com{replaceurl}").url
                    except:
                        return print('error')
class fblike:
    def __init__(self,id,cookie):
        s=requests.session()
        s.headers.update({"Host":"mbasic.facebook.com","content-type":"application/x-www-form-urlencoded","user-agent":"Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36","accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","sec-fetch-site":"same-origin","sec-fetch-mode":"navigate","sec-fetch-user":"?1","sec-fetch-dest":"document","cookie":cookie})
        url2=s.get(f'https://mbasic.facebook.com/{id}').url
        url=s.get(url2).text
        urllike=re.findall('/a/like.php?.*?"',url)
        if urllike==[]:
            print('LIKE ERROR ',end=('\r'))
            print('             ',end=('\r'))   
        else:
            replaceurl2=urllike[0].replace('"',"")
            replaceurl=replaceurl2.replace("amp;","")
            done=s.get(f"https://mbasic.facebook.com{replaceurl}").text
            self.mess=s.get(f"https://mbasic.facebook.com{replaceurl}").url
class fbfriend:
    def __init__(self,id,cookie):
        s=requests.session()
        s.headers.update({"Host":"mbasic.facebook.com","content-type":"application/x-www-form-urlencoded","user-agent":"Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36","accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","sec-fetch-site":"same-origin","sec-fetch-mode":"navigate","sec-fetch-user":"?1","sec-fetch-dest":"document","cookie":cookie})
        url2=s.get(f'https://mbasic.facebook.com/{id}').url
        url=s.get(url2).text
        urlfriend=re.findall('/friends/center/mbasic/?.*?"',url)
        if urlfriend==[]:
            print('FRIEND ERROR ',end=('\r'))
            print('             ',end=('\r'))   
        else:
            replaceurl2=urlfriend[0].replace('"',"")
            replaceurl=replaceurl2.replace("amp;","")
            done=s.get(f"https://mbasic.facebook.com{replaceurl}").text
            self.mess=s.get(f"https://mbasic.facebook.com{replaceurl}").url
class fbfollow:
    def __init__(self,id,cookie):
        s=requests.session()
        s.headers.update({"Host":"mbasic.facebook.com","content-type":"application/x-www-form-urlencoded","user-agent":"Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36","accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","sec-fetch-site":"same-origin","sec-fetch-mode":"navigate","sec-fetch-user":"?1","sec-fetch-dest":"document","cookie":cookie})
        url2=s.get(f'https://mbasic.facebook.com/{id}').url
        url=s.get(url2).text
        urlfollow=re.findall('/a/subscribe.php?.*?"',url)
        if urlfollow==[]:
            print('FOLLOW ERROR ',end=('\r'))
            print('             ',end=('\r'))   
        else:
            replaceurl2=urlfollow[0].replace('"',"")
            replaceurl=replaceurl2.replace("amp;","")
            done=s.get(f"https://mbasic.facebook.com{replaceurl}").text
            self.mess=s.get(f"https://mbasic.facebook.com{replaceurl}").url
class fbgroup:
    def __init__(self,id,cookie):
        
        s=requests.session()
        s.headers.update({"Host":"mbasic.facebook.com","content-type":"application/x-www-form-urlencoded","user-agent":"Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36","accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","sec-fetch-site":"same-origin","sec-fetch-mode":"navigate","sec-fetch-user":"?1","sec-fetch-dest":"document","cookie":cookie})
        url2=s.get(f'https://mbasic.facebook.com/{id}').url
        url=s.get(url2).text
        urlgroup=re.findall('/a/group/join/?.*?"',url)
        if urlgroup==[]:
            print('GROUP ERROR ',end=('\r'))
            print('             ',end=('\r'))   
        else:
            replaceurl2=urlgroup[0].replace('"',"")
            replaceurl=replaceurl2.replace("amp;","")
            done=s.get(f"https://mbasic.facebook.com{replaceurl}").text
            self.mess=s.get(f"https://mbasic.facebook.com{replaceurl4}").url
class fbpage:
    def __init__(self,id,cookie):
        
        s=requests.session()
        s.headers.update({"Host":"mbasic.facebook.com","content-type":"application/x-www-form-urlencoded","user-agent":"Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36","accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","sec-fetch-site":"same-origin","sec-fetch-mode":"navigate","sec-fetch-user":"?1","sec-fetch-dest":"document","cookie":cookie})
        url2=s.get(f'https://mbasic.facebook.com/{id}').url
        url=s.get(url2).text
        urlpage=re.findall('/a/subscribe.php?.*?"',url)
        if urlpage==[]:
            print('PAGE ERROR ',end=('\r'))
            print('             ',end=('\r'))   
        else:
            replaceurl =urlfollow[0].replace('"',"").replace("amp;","")
            done=s.get(f"https://mbasic.facebook.com{replaceurl}").text
            try:
                self.mess=s.get(f"https://mbasic.facebook.com{replaceurl4}").url
            except:
                print('error')
class checkfb:
    def __init__(self,cookie):
        s=requests.session()
        s.headers.update({"Host":"mbasic.facebook.com","content-type":"application/x-www-form-urlencoded","user-agent":"Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36","accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","sec-fetch-site":"same-origin","sec-fetch-mode":"navigate","sec-fetch-user":"?1","sec-fetch-dest":"document","cookie":cookie})
        url=s.get('https://mbasic.facebook.com/profile.php?').text
        findten=re.findall('<head><title>.*?</',url)
        findid=re.findall('profile_id=.*?&',url)
        if findid==[] or findten==[]:
            print('COOKIE DIE ',end=('\r'))
            print('             ',end=('\r'))
        else:
            idfbs=findid[0].replace('profile_id=','')
            tenfbs=findten[0].replace('<head><title>','')
            self.idfb=idfbs.replace('&','')
            self.namefb=tenfbs.replace('</','')
def randstr(so):
    import random
    liststr=['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']
    randomstr=[]
    for str in range(0,so):
        rd=random.choice(liststr)
        randomstr.append(rd)
    chuoi=''
    for str2 in range(0,so):
        chuoi=chuoi+randomstr[str2]
    return chuoi
def randint(so):
    import random
    liststr=['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    randomstr=[]
    for str in range(0,so):
        rd=random.choice(liststr)
        randomstr.append(rd)
    chuoi=''
    for str2 in range(0,so):
        chuoi=chuoi+randomstr[str2]
    return chuoi
def fakename(so):
    import random
    list = ['Thanh Phi', 'Trọng Chính', 'Phục Lễ', 'Thông Tuệ', 'Sơn Hà', 'Nhật Quân', 'Công Phụng', 'Công Thành', 'Khánh Bình', 'Ðăng Khánh', 'Trường Vinh', 'Xuân Hãn', 'Nhật Dũng', 'Khang Kiện', 'Duy Hải', 'Ðình Toàn', 'Nhân Nguyên', 'Hùng Cường', 'Dũng Trí', 'Ðình Toàn', 'Thuận Hòa', 'Hữu Minh', 'Kim Hoàng', 'Ðăng Khánh', 'Sơn Trang', 'Nhật Hùng', 'Tuyền Lâm', 'Khôi Nguyên', 'Xuân Hiếu', 'Trọng Nhân', 'Cao Phong', 'Kiên Trung', 'Ðại Thống', 'Quốc Hải', 'Thịnh Cường', 'Gia Phong', 'Ðức Bình', 'Quốc Anh', 'Hữu Bào', 'Thường Xuân', 'Dũng Việt', 'Hải Sơn', 'Hữu Hiệp', 'Minh Thiện', 'Nghị Quyền', 'Chấn Phong', 'Tường Anh', 'Gia Lập', 'Quốc Hòa', 'Toàn Thắng', 'Hữu Hiệp', 'Mạnh Ðình', 'Thế Tường', 'Gia Cảnh', 'Hiếu Nghĩa', 'Duy Hiếu', 'Tuấn Hùng', 'Kim Long', 'Quốc Tuấn', 'Công Hải', 'Xuân Thuyết', 'Hữu Thiện', 'Thành Vinh', 'Công Sơn', 'Thành Khiêm', 'Khải Ca', 'Xuân Lạc', 'Huy Chiểu', 'Toàn Thắng', 'Gia Lập', 'Việt Sơn', 'Nam Tú', 'Bảo Hiển', 'Cao Minh', 'Hải Bình', 'Tấn Nam', 'Tuấn Minh', 'Xuân Hãn', 'Xuân Phúc', 'Minh Vũ', 'Hữu Nam', 'Ðức Long', 'Duy Mạnh', 'Hoàng Hải', 'Ðăng An', 'Hồng Thịnh', 'Ðức Chính', 'Sơn Lâm', 'Lập Thành', 'Ðắc Lực', 'Ðức Khang', 'Cường Thịnh', 'Nam Việt', 'Thanh Phi', 'Quốc Trung', 'Duy Tân', 'Phú Thịnh', 'Thiện Thanh', 'Uy Vũ', 'Chánh Việt', 'Nhật Duy', 'Thất Cương', 'Hữu Từ', 'Phúc Thịnh', 'Lương Quyền', 'Viễn Thông', 'Việt Phong', 'Viết Tân', 'Minh Kỳ', 'Tấn Nam', 'Long Quân', 'Gia Thiện', 'Quảng Thông', 'Ðức Trung', 'Thanh Minh', 'Bình An', 'Nhật Tấn', 'Duy Minh', 'Xuân Trường', 'Hữu Vĩnh', 'Quốc Hiển', 'Thế Doanh', 'Minh Khôi', 'Công Hiếu', 'Công Phụng', 'Thanh Huy', 'Nhân Văn', 'Thụ Nhân', 'Duy Thanh', 'Ðắc Di', 'Vĩnh Thọ', 'Duy Thông', 'Ngọc Ðoàn', 'Quốc Quang', 'Bách Du', 'Thời Nhiệm', 'Bảo Hiển', 'Việt Khôi', 'Niệm Nhiên', 'Anh Vũ', 'Tuấn Tú', 'Tấn Tài', 'Trường Thành', 'Thanh Hậu', 'Gia Ân', 'Thái Sơn', 'Quang Thái', 'Vĩnh Hải', 'An Tâm', 'Minh Thuận', 'Xuân Lộc', 'Huân Võ', 'Bá Thiện', 'Bình Dân', 'Ngọc Dũng', 'Gia Minh', 'Trung Chính', 'Thanh Phong', 'Hạo Nhiên', 'Huân Võ', 'Gia Nghị', 'Thanh Tịnh', 'Quang Triệu', 'Khải Hòa', 'Tấn Phát', 'Minh Ðức', 'Quân Dương', 'Quang Dương', 'Vạn Thắng', 'Thành Lợi', 'Dũng Trí', 'Gia Thiện', 'Ðức Hòa', 'Tiến Hoạt', 'Thanh Vinh', 'Việt Phong', 'Bảo Pháp', 'Ðức Khang', 'Hữu Chiến', 'Minh Triệu', 'Huy Chiểu', 'Lâm Dũng', 'Quang Hòa', 'Ðức Hạnh', 'Khôi Nguyên', 'Công Phụng', 'Minh Hoàng', 'Ðắc Cường', 'Ðình Hảo', 'Quang Minh', 'Anh Tài', 'Hữu Tân', 'Thái Sang', 'Ngọc Hải', 'Xuân Thiện', 'Ðức Hải', 'Duy Mạnh', 'Hoàng Dũng', 'Lâm Vũ', 'Phong Châu', 'Chí Hiếu', 'Công Lập', 'Vĩnh Hưng', 'Tiền Giang', 'Hữu Thiện', 'Tuấn Thành', 'Hữu Châu', 'Viễn Cảnh', 'Quốc Khánh', 'Thế Vinh', 'Trường Sinh', 'Như Khang', 'Huy Việt', 'Mộng Lâm', 'Khắc Tuấn', 'Hữu Hùng', 'Tích Ðức', 'Hữu Bào', 'Ngọc Thạch', 'Sơn Hải', 'Xuân Trường', 'Việt Sơn', 'Ðình Trung', 'Duy Khang', 'Minh Huấn', 'Thành Khiêm', 'Mộng Lâm', 'Ðình Hợp', 'Chí Công', 'Hữu Trác', 'Nam Hưng', 'Tuấn Hải', 'Quảng Ðại', 'Giang Thiên', 'Sơn Hải', 'Ðan Quế', 'Hữu Lương', 'Quân Dương', 'Thiện Lương', 'Đức Hòa', 'Xuân Hàm', 'Mộng Hoàn', 'Phúc Nguyên', 'Huy Hoàng', 'Ðại Thống', 'Trung Hải', 'Huy Kha', 'Hữu Châu', 'Ðại Hành', 'Quang Dương', 'Hữu Khôi', 'Minh Nhu', 'Minh Tân', 'Công Hoán', 'Vân Sơn', 'Thiện Lương', 'Cát Uy', 'Trọng Hiếu', 'Duy Tâm', 'Ngọc Thuận', 'Nguyên Văn', 'Nam Việt', 'Danh Sơn', 'Duy Hoàng', 'Hữu Hiệp', 'Phục Lễ', 'Hoài Phong', 'Nam Ninh', 'Minh Khang', 'Quốc Hạnh', 'Mạnh Ðình', 'Duy Hiền', 'Công Lý', 'Phong Dinh', 'Quang Triệu', 'Tất Hiếu', 'Thế Trung', 'Xuân Phúc', 'Xuân Minh', 'Bảo Chấn', 'Quốc Thông', 'Phúc Ðiền', 'Thông Minh', 'Khánh Huy', 'Nhật Quang', 'Vinh Diệu', 'Quốc Thiện', 'Khải Tuấn', 'Bảo Tín', 'Tân Ðịnh', 'Phúc Hưng', 'Duy Thông', 'Minh Nhân', 'Phước Thiện', 'Ðông Phương', 'Trường Sơn', 'Ðức Bảo', 'Công Hải', 'Vĩnh Luân', 'Phi Hải', 'Minh Tiến', 'Xuân Ninh', 'Long Quân', 'Thế Vinh', 'Hữu Thắng', 'Bá Thịnh', 'Thái Sơn', 'Phương Trạch', 'Hướng Dương', 'Quyết Thắng', 'Thanh Toản', 'Lam Phương', 'Hồ Bắc', 'Thái Dương', 'Từ Ðông', 'Thắng Lợi', 'Quốc Thắng', 'Trọng Hùng', 'Bảo Bảo', 'Xuân Hàm', 'Khắc Trọng', 'Thiếu Anh', 'Xuân An', 'Hồng Lân', 'Ðức Bằng', 'Cao Tiến', 'Quang Lộc', 'Ðức Hạnh', 'An Nguyên', 'Tuấn Châu', 'Ðắc Di', 'Hoàng Long', 'Huy Trân', 'Gia Thịnh', 'Khải Hòa', 'Vạn Lý', 'Ðông Phương', 'Khánh Ðan', 'Khôi Nguyên', 'Ðức Trí', 'Việt Khoa', 'Thống Nhất', 'Quang Triệu', 'Gia Bảo', 'Chí Bảo', 'Minh Quang', 'Thời Nhiệm', 'Ðức Khang', 'Trọng Tấn', 'Kiến Bình', 'Thuận Hòa', 'Anh Hoàng', 'Hồng Quý', 'Ngọc Huy', 'Vương Triều', 'Nghĩa Hòa', 'Mạnh Thắng', 'Trọng Việt', 'Minh Huấn', 'Việt Cương', 'Danh Văn', 'Khánh Hoàng', 'Thiên Mạnh', 'Hải Giang', 'Hồng Sơn', 'Vương Triều', 'Thanh Tú', 'Vĩnh Hải', 'Huy Trân', 'Duy Luận', 'Tuấn Ngọc', 'Việt Võ', 'Hoàn Vũ', 'Ngọc Sơn', 'Hữu Cương', 'Lam Phương', 'Thành Hòa', 'Hòa Bình', 'Trọng Hùng', 'Thụy Miên', 'Việt Hoàng', 'Bá Lộc', 'Hữu Thống', 'Giang Thiên', 'Tất Hòa', 'Anh Duy', 'Trung Nghĩa', 'Ðức Hạnh', 'Kiệt Võ', 'Trọng Nhân', 'Việt Cường', 'Anh Tú', 'Hạo Nhiên', 'Thế Quyền', 'Ðình Nguyên', 'Minh Triệu', 'Khắc Dũng', 'Gia Bảo', 'Duy Thạch', 'Vạn Hạnh', 'Hòa Lạc', 'Bá Thành', 'Khắc Ninh', 'Thế Dân', 'Thất Cương', 'Hoàng Phát', 'Hải Ðăng', 'Khang Kiện', 'Phụng Việt', 'Phượng Long', 'Mạnh Cường', 'Gia Minh', 'Gia Huy', 'Phi Hải', 'Ðình Sang', 'Bá Thúc', 'Việt Phương', 'Trung Nguyên', 'Quang Hưng', 'Duy Cường', 'Quang Ninh', 'Bình Ðịnh', 'Hùng Sơn', 'Ðông Hải', 'Hữu Long', 'Minh Hoàng', 'Hoàng Giang', 'Chuẩn Khoa', 'Ðình Sang', 'Minh Hỷ', 'Thành Công', 'Khánh An', 'Ngọc Tuấn', 'Chí Khang', 'Tuấn Kiệt', 'Trọng Kiên', 'Việt Thương', 'Khương Duy', 'Minh Hải', 'Huy Khiêm', 'Huy Chiểu', 'Bảo Hoàng', 'Thanh Liêm', 'Trường Sa', 'Ðức Bằng', 'Hữu Canh', 'Mạnh Quỳnh', 'Anh Hoàng', 'Hồng Liêm', 'Ngọc Ẩn', 'Duy Tiếp', 'Nhật Duy', 'Thanh Long', 'Nam An', 'Tân Phước', 'Minh Hoàng', 'Minh Nhật', 'Kiến Văn', 'Vương Triều', 'Vương Gia', 'Xuân Khoa', 'Phượng Long', 'Hoàng Linh', 'Thạch Sơn', 'Duy Bảo', 'Kim Phú', 'Nguyên Lộc', 'Quốc Hải', 'Ðức Quảng', 'Minh Nhân', 'Thanh Tùng', 'Xuân Vũ', 'Nghĩa Dũng', 'Quốc Huy', 'Thanh Kiên', 'Ðăng Minh', 'Kiên Bình', 'Thành Hòa', 'Anh Tú', 'Phú Thịnh', 'Cảnh Tuấn', 'Thất Thọ', 'Hiệp Dinh', 'Anh Tài', 'Quang Trường', 'Cảnh Tuấn', 'Lương Thiện', 'Minh Quân', 'Ðông Hải', 'Trung Chính', 'Anh Tài', 'Hạo Nhiên', 'Bá Tùng', 'Phúc Khang', 'Thế Bình', 'Quang Triệu', 'Thượng Thuật', 'Quốc Quang', 'Hữu Hiệp', 'Việt Chính', 'Bá Tùng', 'Việt Khải', 'Ngọc Tuấn', 'Chiêu Phong', 'Duy Thông', 'Thuận Phương', 'Ân Lai', 'Khôi Vĩ', 'Quang Thái', 'Ðắc Cường', 'Thiên Lương', 'Phúc Khang', 'Lâm Vũ', 'Bảo Ðịnh', 'Ðắc Trọng', 'Ngọc Hải', 'Hạnh Tường', 'Hải Phong', 'Mạnh Tuấn', 'Duy Quang', 'Hùng Thịnh', 'Hữu Thắng', 'Duy Mạnh', 'Thiện Ân', 'Thế Lâm', 'Ðức Quảng', 'Kiên Giang', 'Quang Thái', 'Thành Phương', 'Phúc Cường', 'Thế Minh', 'Chí Hiếu', 'Hồng Lân', 'Công Ân', 'Trọng Tấn', 'Chí Bảo', 'Khắc Thành', 'Kim Thông', 'Mạnh Tường', 'Thế Lâm', 'Hải Long', 'Thiện Phước', 'Trường Phát', 'Phượng Long', 'Khắc Việt', 'Minh Toàn', 'Khải Ca', 'Việt Cường', 'Quang Nhân', 'Thuận Hòa', 'Tấn Trương', 'Sơn Hải', 'Minh Vương', 'Ðông Hải', 'Uy Vũ', 'An Ninh', 'Ngọc Minh', 'Thành Châu', 'Việt Thái', 'Quốc Tuấn', 'Quang Triệu', 'Chính Thuận', 'Ðình Lộc', 'Huy Hoàng', 'Minh Ðức', 'Chánh Việt', 'Bá Phước', 'Phước Sơn', 'Minh Cảnh', 'Hải Bằng', 'Hồng Liêm', 'Phước An', 'Sỹ Hoàng', 'Bảo Khánh', 'Lương Tài', 'Ðình Luận', 'Mộng Long', 'Kim Long', 'Khánh Giang', 'Minh Huấn', 'Hùng Phong', 'Khương Duy', 'Tuấn Ngọc', 'Nhật Dũng', 'Anh Tài', 'Xuân Hiếu', 'Giang Sơn', 'Khải Ca', 'Ðại Hành', 'Hồng Thịnh', 'Ngọc Ẩn', 'Thanh Toàn', 'Ngọc Danh', 'Minh Khôi', 'Hoàng Lâm', 'Thành Ý', 'Nhật Tấn', 'Trọng Dũng', 'Duy Quang', 'Thành Ðệ', 'Quang Tuấn', 'Phương Triều', 'Ðắc Lộ', 'Hồng Đức', 'Sơn Trang', 'Nguyên Giáp', 'Hồng Thụy', 'Quang Thạch', 'Trường Giang', 'Ðức Anh', 'Thụy Du', 'Thế Lực', 'Hồng Việt', 'Trung Hiếu', 'Minh Giang', 'Hữu Thắng', 'Ðức Phú', 'Gia Kiên', 'Minh Nhân', 'Thanh Ðạo', 'Ngọc Lai', 'Trí Hào', 'Khuyến Học', 'Nguyên Phong', 'Vĩnh Thọ', 'Bảo Thạch', 'Phước An', 'Thành Khiêm', 'Minh Thuận', 'Hiệp Hào', 'Ðăng An', 'Thượng Năng', 'Minh Ðạt', 'Khải Tuấn', 'Bảo Hoa', 'Quang Thái', 'Nam Nhật', 'Công Tuấn', 'Phú Hải', 'Hữu Hoàng', 'Nam Dương', 'Hùng Sơn', 'Thượng Khang', 'Công Hào', 'Phi Hùng', 'Nhật Quang', 'Mộng Lâm', 'Khắc Thành', 'Duy Thanh', 'Bảo Tín', 'Hiệp Hà', 'Quảng Ðại', 'Bình Quân', 'Minh Khôi', 'Thái Minh', 'Tấn Nam', 'Thành Nguyên', 'Giang Lam', 'Phúc Cường', 'Ðức Tường', 'Công Hiếu', 'Hoàng Khôi', 'Minh Nhật', 'Giang Lam', 'Thụ Nhân', 'Thành Nguyên', 'Trường Sinh', 'Bảo Quốc', 'Gia Cẩn', 'Thượng Khang', 'Đăng Quang', 'Kim Toàn', 'Sơn Giang', 'Trung Anh', 'Minh Khôi', 'Hoài Phong', 'Tuấn Kiệt', 'Tường Phát', 'Thái Sơn', 'Thiếu Cường', 'Ðức Toản', 'Thượng Cường', 'Phúc Sinh', 'Quảng Ðại', 'Quang Lâm', 'Thế Hùng', 'Thanh Trung', 'Hoài Tín', 'Minh Hiên', 'Trung Việt', 'Long Quân', 'Huy Tuấn', 'Cao Nghiệp', 'Nhật Bảo Long', 'Thế Anh', 'Cương Nghị', 'Nghĩa Hòa', 'Huy Khánh', 'Thanh Tịnh', 'Bảo Ðịnh', 'Ðình Luận', 'Kim Hoàng', 'Ðức Phong', 'Việt An', 'Ngọc Sơn', 'Trí Tịnh', 'Ðạt Hòa', 'Chấn Hưng', 'Phước Thiện', 'Nhật Hồng', 'Trọng Duy', 'Vạn Thông', 'Quốc Mạnh', 'Kim Long', 'Quyết Thắng', 'Bảo Long', 'Hiền Minh', 'Quảng Ðại', 'Quang Nhật', 'Hồng Sơn', 'Hải Long', 'Thiên Phú', 'Xuân Thuyết', 'Kiên Lâm', 'Quốc Hiển', 'Trí Hữu', 'Duy Kính', 'Thường Kiệt', 'Kiến Văn', 'Bình Nguyên', 'Hoàng Giang', 'Chí Hiếu', 'Hiệp Hào', 'Duy Thạch', 'Ðức Ân', 'Ðại Thống', 'Hữu Minh', 'Hải Sơn', 'Quốc Trung', 'Long Giang', 'Minh Thạc', 'Chấn Hưng', 'Thuận Hòa', 'Thông Minh', 'Hoàng Dũng', 'Hải Ðăng', 'Hữu Hùng', 'Hòa Thái', 'Duy Hiền', 'Bình Ðịnh', 'Công Luận', 'Duy Hải', 'Xuân Hàm', 'Thiện Sinh', 'Ðức Tâm', 'Xuân Quý', 'Quang Tài', 'Phước Nhân', 'Tiền Giang', 'Hướng Bình', 'Trường Hiệp', 'Thiện Minh', 'Thiện Tâm', 'Mạnh Cương', 'Quốc Tuấn', 'Nhật Duy', 'Tuấn Ngọc', 'Sơn Dương', 'Nhân Từ', 'Thanh Thế', 'Anh Khôi', 'Khải Ca', 'Tiến Ðức', 'Kiến Bình', 'Quang Lâm', 'Hữu Canh', 'Lam Phương', 'Vinh Quốc', 'Đức Hòa', 'Hùng Anh', 'Lâm Ðồng', 'Vinh Quốc', 'Duy An', 'Bảo An', 'Công Hiếu', 'Thanh Thuận', 'Khắc Dũng', 'Thiện Ðức', 'Đức Hòa', 'Bảo Lâm', 'Bình An', 'Chính Trực', 'Thăng Long', 'Bình An', 'Vạn Thông', 'Mạnh Cương', 'Thanh Thiên', 'Tuyền Lâm', 'Tuấn Trung', 'Nghị Lực', 'Phú Hải', 'Tuấn Khải', 'Cát Tường', 'Thành Nguyên', 'Yên Bằng', 'Lương Tài', 'Thái Ðức', 'Sơn Quyền', 'Gia Kiệt', 'Xuân Trung', 'Quang Anh', 'Lâm Viên', 'Thành Vinh', 'Bình An', 'Quang Khải', 'Chung Thủy', 'Trường Nam', 'Thành Ðệ', 'Xuân Cao', 'Trường Nam', 'Hoài Trung', 'Minh Vu', 'Tường Phát', 'Tích Ðức', 'Quốc Trụ', 'Bảo Bảo', 'Duy Hiếu', 'Xuân Quân', 'Nam Lộc', 'Thiện Lương', 'Nhân Nguyên', 'Tùng Lâm', 'Ðông Dương', 'Xuân Trường', 'Minh Vương', 'Trọng Khánh', 'Hùng Phong', 'Chính Thuận', 'Thiên An', 'Vạn Thông', 'Bình Yên', 'Minh Tú', 'Bình Hòa', 'Ðức Toàn', 'Quốc Phong', 'Minh Huấn', 'Phú Hiệp', 'Huy Kha', 'Vương Triệu', 'Ðức Bảo', 'Hoàng Minh', 'Ðức Anh', 'Thái Dương', 'Thái Dương', 'Việt Khôi', 'Thành Châu', 'Ðức Anh', 'Phú Ân', 'Thành Lợi', 'Tường Phát', 'Hiếu Nghĩa', 'Khôi Nguyên', 'Minh Vũ', 'Thuận Phong', 'Thụy Vũ', 'Hữu Thiện', 'Ðức Tài', 'Viễn Cảnh', 'Phước Sơn', 'Công Hoán', 'Thiên An', 'Quang Dương', 'Huy Hà', 'Thành Vinh', 'Nguyên Hạnh', 'Ân Thiện', 'Hữu Tân', 'Vĩnh Thọ', 'Mạnh Tuấn', 'Ngọc Thạch', 'Tùng Minh', 'Gia Phong', 'Thiện Khiêm', 'Hữu Hoàng', 'Hồng Vinh', 'Khánh Giang', 'Gia Kiệt', 'Hữu Vượng', 'Long Giang', 'Minh Hỷ', 'Ðức Anh', 'Thái Hòa', 'Minh Nhật', 'Yên Bình', 'Thắng Lợi', 'Ðức Phú', 'Thịnh Cường', 'Ðức Quang', 'Sơn Giang', 'Gia Hùng', 'Trúc Cương', 'Minh Quân', 'Huy Khiêm', 'Ðồng Khánh', 'Quang Khanh', 'Bình Dân', 'Ân Thiện', 'Thiện Tính', 'Xuân Hàm', 'Phúc Hòa', 'Nam Hải', 'Hồng Thịnh', 'Minh Quang', 'Hồng Liêm', 'Thái Tân', 'Quý Khánh', 'Nghị Lực', 'Nhật Tiến', 'Hiệp Hào', 'Nam Nhật', 'Hùng Thịnh', 'Huy Tuấn', 'Thế Huấn', 'Kỳ Võ', 'Quang Hưng', 'Thiệu Bảo', 'Giang Nam', 'Nhật Quân', 'Thành Trung', 'Hồng Minh', 'Vĩnh Long', 'Hồ Nam', 'Công Hiếu', 'Ðức Bằng', 'Quảng Ðại', 'Thế Huấn', 'Bảo Hoa', 'Ngọc Danh', 'Mạnh Thắng', 'Hữu Minh', 'Viễn Ðông', 'Hữu Nam', 'Ngọc Huy', 'Công Lập', 'Phi Cường', 'Lâm Ðồng', 'Kiến Bình', 'Trường Phát', 'Phú Hải', 'Trung Nguyên', 'Khánh Huy', 'Danh Văn', 'Huy Trân', 'Thế Năng', 'Thế Anh', 'Phong Dinh', 'Ðức Thành', 'Hòa Lạc', 'Sỹ Thực', 'Viết Sơn', 'Tấn Sinh', 'Cao Nhân', 'Tuấn Ðức', 'Hòa Hiệp', 'Ðại Ngọc', 'Việt Khoa', 'Phúc Ðiền', 'Thành Thiện', 'Duy Cường', 'Trọng Tường', 'Trọng Trí', 'Thuận Anh', 'Bá Lộc', 'Nhật Bảo Long', 'Thanh Kiên', 'Minh Khánh', 'Mạnh Trường', 'Ân Lai', 'Ðình Chương', 'Ngọc Thạch', 'Anh Khoa', 'Gia Vinh', 'Ðông Dương', 'Hoài Thanh', 'Nhân Nguyên', 'Ðức Phi', 'Minh Thạc', 'Nhật Duy', 'Vĩnh Long', 'Kim Thông', 'Hồng Vinh', 'Hải Nguyên', 'Long Quân', 'Thiên Mạnh', 'Minh Trung', 'Quang Sáng', 'Thiện Ân', 'Hoài Tín', 'Bảo Duy', 'Thụ Nhân', 'Advertisement', '']
    listname=[]
    for soname in range(0,int(so)):
        rd=random.choice(list)
        rd2=random.choice(list)
        n1=rd.split(' ')[0]
        n2=rd2.split(' ')[0]
        name=n1+' '+n2
        listname.append(name)
    return listname
def wait(string,so,string2):
    import time
    for wait in range(1,int(so)):
        print(string+str(wait)+str(string2),end=('\r'))
        time.sleep(1)