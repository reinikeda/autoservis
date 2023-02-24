from PIL import Image
cover = Image.open('autoservis/car_repair_servis/static/car_repair_servis/img/default_car.png')
cover_resize = cover.resize((200, 200))
# print(cover_resize.size)
cover_resize.save('autoservis/car_repair_servis/static/car_repair_servis/img/default_car_small.png')