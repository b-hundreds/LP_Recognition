### License Plate Recognition
Đây là một project xây dựng một web nhận dạng biển số, gồm 2 chức năng:<br>

* Nhận dạng biển số xe (Dùng yolov8 cho cả 2 task là detection và recognition, sử dụng thư viện albumentation để quay ảnh ngẫu nhiên trong khoảng -45 độ đến 45 độ), lưu kết quả vào database
* Tìm kiếm ảnh biển số xe trong database theo chuỗi chữ số của biển

# Cách sử dụng

## Cách 1

### Cài đặt môi trường
```
pip install -r requirements.txt
```
Ngoài ra, mongodb cũng cần được cài trên máy (Đã được bật, đường kết nối là "mongodb://localhost:27017")

### Khởi động web

Chạy câu lệnh sau:
```
python -m flask run
```
Sau khi chạy, bật link http://127.0.0.1:5000 để tương tác với web 

Chú ý: biển 2 dòng sẽ được định dạng là "A-B" (A là dòng trên, B là dòng dưới), còn biển 1 dòng sẽ được định dạng thành 1 chuỗi liên tục "ABCDS..."

## Results

   <p align="center" >
   <img src="results1.jpg" >
    Chức năng nhận diện biển số
</p>

   <p align="center" >
   <img src="results3.jpg" >
    Chức năng tìm kiếm biển số
</p>

   <p align="center" >
   <img src="results2.jpg" >
    Database
</p>

## Nhận xét
* Mô hình nhận dạng đúng và chuẩn với những ảnh khác nhau, một số ảnh bị nghiêng một chút vẫn có thể nhận dạng đúng
* Tuy nhiên, với một số ảnh bị quá nghiêng, mô hình hay bị nhầm lẫn các kí tự, ví dụ như 1 với 7, 0 với D, X với K
* Đối với các loại biển số xe khác loại biển số xe thường: Chỉ nhận diện được biển số chứ không nhận dạng các kí tự của biển số xe đó (Với task detection, mô hình được huấn luyện với bộ dữ liệu bao gồm cả biển số xe thường, biển số xe quân đội, ... nhưng với task recognition, chỉ có dữ liệu của biển số xe thường)

## Hướng cải thiện project
* Thêm chức năng để có thể nhận diện từ ảnh lấy trực tiếp từ camera
* Thêm chức năng xóa các dữ liệu đã cũ 
* Tìm hiểu cách đóng gói với docker
