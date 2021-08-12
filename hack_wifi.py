########################################
#Copyright of TrungLapTrinh, 2021      #
#https://www.trunglaptrinh.blogspot.com#
#https://bit.ly/3xnY87T (Link Youtube) #
########################################

print(r"""           
    _ __
    | '_ `  
    | | | |
    |_| |_|""")  
print("\n****************************************************************")
print("\n* Copyright of TrungLapTrinh, 2021                             *")
print("\n* https://www.trunglaptrinh.blogspot.com                       *")
print("\n* https://bit.ly/3xnY87T (Link Youtube)                        *")
print("\n****************************************************************")

#    Nhập quy trình con để chúng ta có thể sử dụng các lệnh hệ thống. 
import subprocess

#    Nhập mô-đun re để chúng tôi có thể sử dụng các biểu thức chính quy.  
import re

# Python cho phép chúng tôi chạy các lệnh hệ thống bằng cách sử dụng hàm
# được cung cấp bởi mô-đun quy trình con;
# (subprocess.run (<danh sách các đối số dòng lệnh ở đây>, <chỉ định đối số thứ hai nếu bạn muốn nắm bắt đầu ra>)).
#
# Tập lệnh này là một quy trình mẹ tạo ra một quy trình con.
# Chạy một lệnh hệ thống và sẽ chỉ tiếp tục sau khi xử lý con
#    Đã được hoàn thành.
#
# Để lưu nội dung được gửi đến luồng đầu ra chuẩn
# (đầu cuối), trước tiên chúng ta phải xác định rằng chúng ta muốn nắm bắt đầu ra.
# Để làm điều này, chúng tôi chỉ định đối số thứ hai là capture_output = True.
# Thông tin này được lưu trữ trong thuộc tính stdout dưới dạng byte và
# Cần được giải mã trước khi được sử dụng như một chuỗi trong Python. 
command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()

# Tôi đã nhập mô-đun re để sử dụng các biểu thức chính quy.
# Tôi muốn tìm tất cả các tên wifi được liệt kê sau
# "TẤT CẢ Hồ sơ Người dùng:". Sử dụng biểu thức chính quy, chúng tôi có thể tạo
# Một nhóm tất cả các ký tự cho đến khi trình tự thoát trả về (\ r) xuất hiện. 
profile_names = (re.findall("All User Profile     : (.*)\r", command_output))

# Tôi tạo một danh sách trống bên ngoài vòng lặp nơi từ điển
# Chứa tất cả tên người dùng và mật khẩu wifi sẽ được lưu. 
wifi_list = []

# Nếu không tìm thấy bất kỳ tên hồ sơ nào, điều này có nghĩa là kết nối wifi
# Cũng không được tìm thấy. Vì vậy, chúng tôi chạy phần này để kiểm tra
# Chi tiết của wifi và xem liệu chúng ta có thể lấy mật khẩu của chúng hay không. 
if len(profile_names) != 0:
    for name in profile_names:
# Mọi kết nối wifi sẽ cần từ điển riêng
# Sẽ được thêm vào wifi_list biến. 
        wifi_profile = {}
         # Bây giờ chúng ta có thể chạy một lệnh cụ thể hơn để xem thông tin
         # về kết nối wifi và nếu Khóa bảo mật
         # không vắng mặt, có thể lấy được mật khẩu. 
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()
         # Chúng tôi sử dụng biểu thức chính quy để chỉ tìm kiếm các trường hợp vắng mặt để chúng tôi có thể bỏ qua chúng. 
        if re.search("Security key           : Absent", profile_info):
            continue
        else:
            # Gán ssid của cấu hình wifi vào từ điển. 
            wifi_profile["ssid"] = name
            # Những trường hợp này không vắng mặt và chúng ta nên chạy
            # "key = clear" phần lệnh để lấy mật khẩu. 
            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()
            # Một lần nữa chạy biểu thức chính quy để nắm bắt
            # nhóm sau: (là mật khẩu). 
            password = re.search("Key Content            : (.*)\r", profile_info_pass)
            # Kiểm tra xem Tôi có tìm thấy mật khẩu bằng biểu thức chính quy hay không.
            # Một số kết nối wifi có thể không có mật khẩu. 
            if password == None:
                wifi_profile["password"] = None
            else:
                # Tôi chỉ định nhóm (nơi chứa mật khẩu)
                # Tôi quan tâm đến khóa mật khẩu trong từ điển. 
                wifi_profile["password"] = password[1]
                # Tôi nối thông tin wifi vào danh sách wifi biến. 
            wifi_list.append(wifi_profile) 

for x in range(len(wifi_list)):
    print(wifi_list[x]) 