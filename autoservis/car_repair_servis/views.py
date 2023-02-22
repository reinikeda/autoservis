from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    # return HttpResponse('Autoservisas')
    return HttpResponse("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href='http://fonts.googleapis.com/css?family=Roboto' rel='stylesheet' type='text/css'>
    <link href="/static/style.css" rel="stylesheet" type="text/css">
    <title>Car Auto Servis</title>
</head>
<body>
    <div>
        <h1 style='text-align: center;'>Autoservis</h1>
    </div>
    <hr>
    <div style='text-align: center;'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/Auto_Repair_shop.jpg/640px-Auto_Repair_shop.jpg'>
    </div>
</body>
</html>
    """)

