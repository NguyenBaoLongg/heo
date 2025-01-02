from xml.dom.domreg import registered

from django.http import HttpResponse
from django.shortcuts import render, redirect
import pyrebase
from django.contrib import auth
from requests import session
firebaseConfig = {
  "apiKey": "AIzaSyBiMxTtnlU1F_JHKNPDSJ43GkjNTJ_pOXU",
  "authDomain": "btl-python-a45d1.firebaseapp.com",
  "databaseURL": "https://btl-python-a45d1-default-rtdb.firebaseio.com",
  "projectId": "btl-python-a45d1",
  "storageBucket": "btl-python-a45d1.firebasestorage.app",
  "messagingSenderId": "504874076401",
  "appId": "1:504874076401:web:7b4b194568d04c9a428150",
  "measurementId": "G-57DYVJ4HWQ"
}

app = pyrebase.initialize_app(firebaseConfig)
auth = app.auth()
database = app.database()

# Create your views here.

# View page
def get_home(request):
  context = {"products": [],"user": {}}
  item= {}
  products = database.child("products").child("list-items").get()
  uid = request.session.get('uid') 
  if uid:
        try:
            user_ref = database.child("users").child(uid)
            user_data = user_ref.get().val()
            if user_data:
                context["user"] = {
                    "name": user_data.get("name"),
                }
            else:
                print("Không tìm thấy thông tin người dùng.")
        except Exception as e:
            print(f"Lỗi khi lấy thông tin người dùng: {e}")
  else:
    message = "Yêu cầu đăng nhập để sử dụng trang"
    context = {"message":message}
    return render("login",context)
  try:
    if products.each():
      for product in products.each():
          item = {
            "id": product.key(),
            "title": product.val().get("title"),
            "image": product.val().get("image"),
            "category": product.val().get("category"),
            "price": product.val().get("price"),
          }
          context["products"].append(item)
    else: 
      print("No products found.")
    return render(request, "product.html",context)
  except:
    context = {"message": []}
    context["message"].append("Lỗi khi tải trang web")
    return render(request,"product.html",context)

def login_view(request):
  return render(request, "login.html")

def signup_view(request):
  return render(request, "signup.html")

def view_admin(request):
  uid = request.session['uid']
  context = {"products": []}
  item= {}
  user = database.child("users").child(uid)
  user_data = user.get().val()
  if user_data.get("role")== "Admin":
    products = database.child("products").child("list-items").get()
    if products.each():
      for product in products.each():
          item = {
            "id": product.key(),
            "title": product.val().get("title"),
            "image": product.val().get("image"),
            "category": product.val().get("category"),
            "price": product.val().get("price"),
          }
          context["products"].append(item)
    else: 
      print("No products found.")
    return render(request,"admin/list-product.html",context)
  return redirect("home")

def view_list_user(request):
  context = {"users": []}
  item= {}
  users = database.child("users").get()
  if users.each():
    for user in users.each():
        item = {
          "id": user.key(),
          "name": user.val().get("name"),
          "address": user.val().get("address"),
          "dob": user.val().get("dob"),
          "phone": user.val().get("phone"),
          "role": user.val().get("role"),
          "status": user.val().get("status"),
          "email": user.val().get("email"),
          "gender": user.val().get("gender"),
        }
        context["users"].append(item)
  else: 
    print("No products found.")
  print(item)
  return render(request,"admin/list-user.html",context)

def view_list_product(request):
  context = {"products": []}
  item= {}
  products = database.child("products").child("list-items").get()
  if products.each():
    for product in products.each():
        item = {
          "id": product.key(),
          "title": product.val().get("title"),
          "image": product.val().get("image"),
          "category": product.val().get("category"),
          "price": product.val().get("price"),
        }
        context["products"].append(item)
  else: 
    print("No products found.")
  return render(request,"admin/list-product.html",context)

def view_add_product(request):
  return render(request,"admin/add-product.html")

def update_product_view(request,product_id):
  context = {"products": []}
  try:
      dataProduct = database.child("products").child("list-items").child(product_id)
      product_data = dataProduct.get().val()
      if product_data:
        item = {
          "id": product_id,
          "title": product_data["title"],
          "image": product_data["image"],
          "category": product_data["category"],
          "price": product_data["price"],
          "description": product_data["description"],
        }
        context["products"].append(item)
      else: 
        print("Không tìm thấy dữ liệu sản phẩm")
  except Exception as e:
      return HttpResponse(f"Lỗi khi kết nối tới data {e}")
  return render(request,"admin/update-product.html",context)

def view_cart(request):
  uid = request.session.get('uid') 
  context = {"products":[],"user":"","sum":"","length":"","userId":""}
  if uid:
    context["userId"] = uid
    user_ref = database.child("users").child(uid)
    user_data = user_ref.get().val()
    if user_data:
        context["user"] = {
            "name": user_data.get("name"),
        }
    else:
        print("Không tìm thấy thông tin người dùng.")
    product_info= {}
    sum = 0
    length = 0
    products = database.child("cart").child(uid).child("items").get()
    if products.each():
      for p in products.each():
          data_info_product = database.child("products").child("list-items").child(p.key()).get().val()
          if data_info_product:
            product_info = {
            "id": p.key(),
            "title": data_info_product["title"],
            "image": data_info_product["image"],
            "category": data_info_product["category"],
            "price": data_info_product["price"],
            "size": p.val().get("size"),
            "quantity": p.val().get("quantity"),  
            }
            sum = sum+(int(p.val().get("quantity"))*int(data_info_product["price"]))
            length+=int(p.val().get("quantity"))
            context["products"].append(product_info)
            context["sum"]= sum
            context["length"] =length
      summary_data = {
            "sum": sum,
            "length": length
        }
      print(uid)
      database.child("cart").child(uid).child("summary").update(summary_data)
    else: 
      print("No products found.")
    return render(request,"cart.html",context)
  else:
    return redirect("login")

def products_view(request):
  context = {"products": [],"user": {}}
  item= {}
  products = database.child("products").child("list-items").get()
  uid = request.session.get('uid') 
  if uid:
        try:
            user_ref = database.child("users").child(uid)
            user_data = user_ref.get().val()
            if user_data:
                context["user"] = {
                    "name": user_data.get("name"),
                }
            else:
                print("Không tìm thấy thông tin người dùng.")
        except Exception as e:
            print(f"Lỗi khi lấy thông tin người dùng: {e}")
  else:
    message = "Yêu cầu đăng nhập để sử dụng trang"
    context = {"message":message}
    return render("login",context)
  try:
    if products.each():
      for product in products.each():
          item = {
            "id": product.key(),
            "title": product.val().get("title"),
            "image": product.val().get("image"),
            "category": product.val().get("category"),
            "price": product.val().get("price"),
          }
          context["products"].append(item)
    else: 
      print("No products found.")
      return render(request, "home-list-products.html",context)
  except:
    context = {"message": []}
    context["message"].append("Lỗi khi tải trang web")
  return render(request,"home-list-products.html",context)

def products_view_male(request):
  context = {"products": [],"user": {}}
  item= {}
  products = database.child("products").child("list-items").get()
  uid = request.session.get('uid') 
  if uid:
        try:
            user_ref = database.child("users").child(uid)
            user_data = user_ref.get().val()
            if user_data:
                context["user"] = {
                    "name": user_data.get("name"),
                }
            else:
                print("Không tìm thấy thông tin người dùng.")
        except Exception as e:
            print(f"Lỗi khi lấy thông tin người dùng: {e}")
  else:
    message = "Yêu cầu đăng nhập để sử dụng trang"
    context = {"message":message}
    return render("login",context)
  try:
    if products.each():
      for product in products.each():
          if product.val().get("category")=="Nam":
            item = {
              "id": product.key(),
              "title": product.val().get("title"),
              "image": product.val().get("image"),
              "category": product.val().get("category"),
              "price": product.val().get("price"),
            }
            context["products"].append(item)
    else: 
      print("No products found.")
      return render(request, "home-list-products.html",context)
  except:
    context = {"message": []}
    context["message"].append("Lỗi khi tải trang web")
  return render(request,"home-list-products.html",context)

def products_view_female(request):
  context = {"products": [],"user": {}}
  item= {}
  products = database.child("products").child("list-items").get()
  uid = request.session.get('uid') 
  if uid:
        try:
            user_ref = database.child("users").child(uid)
            user_data = user_ref.get().val()
            if user_data:
                context["user"] = {
                    "name": user_data.get("name"),
                }
            else:
                print("Không tìm thấy thông tin người dùng.")
        except Exception as e:
            print(f"Lỗi khi lấy thông tin người dùng: {e}")
  else:
    message = "Yêu cầu đăng nhập để sử dụng trang"
    context = {"message":message}
    return render("login",context)
  try:
    if products.each():
      for product in products.each():
          if product.val().get("category")=="Nu":
            item = {
              "id": product.key(),
              "title": product.val().get("title"),
              "image": product.val().get("image"),
              "category": product.val().get("category"),
              "price": product.val().get("price"),
            }
            context["products"].append(item)
    else: 
      print("No products found.")
      return render(request, "home-list-products.html",context)
  except:
    context = {"message": []}
    context["message"].append("Lỗi khi tải trang web")
  return render(request,"home-list-products.html",context)

#Staff
def view_staff(request):
    uid = request.session['uid']
    context = {"invoices": []} 
    if not uid:
      return redirect("home")
    user = database.child("users").child(uid)
    user_data = user.get().val()
    if user_data.get("role") == "Staff":
        invoice_ref = database.child("invoice").get()
        if invoice_ref.each():
            for i in invoice_ref.each():
                user_ref = database.child("users").child(i.val().get("id"))
                user_data = user_ref.get().val()
                if user_data:
                    context["invoices"].append({
                        "id": i.key(),
                        "status": i.val().get("status"),
                        "name": user_data.get("name"),
                        "address": user_data.get("address"),
                        "phone": user_data.get("phone"),
                    })
        else:
            print("No invoices found.")
        print(context)
        return render(request, "staff/list-invoice.html", context)
    return redirect("home")

def detailInvoice(request,invoice_id):
  uid = request.session['uid']
  context = {"user":[],"products":[],"status":"","invoice_id":"","status":"","total_sum":""}
  user_info = {}
  product_info = {}
  context["invoice_id"] = invoice_id
  total_sum = 0
  if uid:
    invoice_ref = database.child("invoice").child(invoice_id).get().val()
    if invoice_ref:
      context["status"] = invoice_ref.get("status")
      user_data= database.child("users").child(invoice_ref.get("id")).get().val()
      if user_data:
        user_info = {
          "name": user_data.get("name"),
          "email": user_data.get("email"),
          "address": user_data.get("address"),
          "phone": user_data.get("phone"),
        }
        context["user"].append(user_info)
      else:
          return redirect("staffView")
      for product in invoice_ref.get("products"):
        product_info={
          "title":product["title"],
          "size":product['size'],
          "quantity":product["quantity"],
          "price":product["price"],
          "price_total_product":int(product["quantity"])*int(product["price"])
        }
        total_sum = total_sum + (int(product["quantity"])*int(product["price"]))
        context["products"].append(product_info)
  else:
     return redirect("login")
  context["total_sum"] = total_sum
  return render(request,"staff/detail-invoice.html",context)


# -------------
# infor user

def view_info_user(request):
  context = {"user": []}
  item= {}
  uid = request.session.get('uid') 
  if uid:
        try:
            user_ref = database.child("users").child(uid)
            user_data = user_ref.get().val()
            if user_data:
              print(user_data)
              item = {
                "name": user_data.get("name"),
                "email": user_data.get("email"),
                "dob": user_data.get("dob"),
                "gender": user_data.get("gender"),
                "address": user_data.get("address"),
                "phone": user_data.get("phone"),
              }
              context["user"].append(item)
            else:
                print("Không tìm thấy thông tin người dùng.")
        except Exception as e:
            print(f"Lỗi khi lấy thông tin người dùng: {e}")
  else:
    message = "Yêu cầu đăng nhập để sử dụng trang"
    context = {"message":message}
    return render("login",context)
  print(context)
  return render(request,"user/account-user.html",context)

def list_order(request):
  uid = request.session['uid']
  context = {"invoices": []} 
  user = database.child("users").child(uid)
  user_data = user.get().val()
  if uid:
    invoice_ref = database.child("invoice").get()
    if invoice_ref.each():
      for i in invoice_ref.each():
          if i.val().get("id")==uid:
            user_ref = database.child("users").child(i.val().get("id"))
            user_data = user_ref.get().val()
            if user_data:
                context["invoices"].append({
                    "id": i.key(),
                    "status": i.val().get("status"),
                    "name": user_data.get("name"),
                    "address": user_data.get("address"),
                    "phone": user_data.get("phone"),
                })
    else:
      print("Khong tim thay san pham")
  else:
     return redirect("login")
  return render(request,"user/list-order.html",context)

def detail_order(request,invoice_id):
  uid = request.session['uid']
  context = {"user":[],"products":[],"status":"","invoice_id":"","status":"","total_sum":""}
  user_info = {}
  product_info = {}
  context["invoice_id"] = invoice_id
  total_sum = 0
  if uid:
    invoice_ref = database.child("invoice").child(invoice_id).get().val()
    if invoice_ref:
      context["status"] = invoice_ref.get("status")
      user_data= database.child("users").child(invoice_ref.get("id")).get().val()
      if user_data:
        user_info = {
          "name": user_data.get("name"),
          "email": user_data.get("email"),
          "address": user_data.get("address"),
          "phone": user_data.get("phone"),
        }
        context["user"].append(user_info)
      else:
          return redirect("staffView")
      for product in invoice_ref.get("products"):
        product_info={
          "title":product["title"],
          "size":product['size'],
          "quantity":product["quantity"],
          "price":product["price"],
          "price_total_product":int(product["quantity"])*int(product["price"])
        }
        total_sum = total_sum + (int(product["quantity"])*int(product["price"]))
        context["products"].append(product_info)
  else:
     return redirect("login")
  context["total_sum"] = total_sum
  return render(request,"user/detail-order.html",context)
# =========================================
# module

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session_id = user.get('localId')
            if session_id: 
                request.session['uid'] = str(session_id)
                user_data = database.child("users").child(request.session['uid']).get().val()
                if not user_data:
                    raise ValueError("Tài khoản hoặc mật khẩu không chính xác.")
                role_redirects = {
                    "User": "home",
                    "Admin": "adminView",
                    "Staff": "staffView"
                }
                role = user_data.get("role")
                if role in role_redirects:
                    return redirect(role_redirects[role])
                else:
                    raise ValueError("role sai.")
        except Exception as e:
            context = {"message": e}
            return render(request, "login.html", context)
    return render(request, "login.html")

def postsignup(request):
  context={"message":""}
  name = request.POST.get('name')
  phone = request.POST.get('phone')
  email = request.POST.get('email')
  password = request.POST.get('password')
  address = request.POST.get('address')
  dob = request.POST.get('dob')
  gender = request.POST.get('gender')
  try:
    user = auth.create_user_with_email_and_password(email,password)
    if user:
      uid = user['localId']
      data = {
        "name":name,
        "email":email,
        "phone":phone,
        "address":address,
        "dob":dob,
        "gender":gender,
        "role":"User",
        "status":1
      }
      database.child("users").child(uid).set(data)
      return render(request,"login.html")
    else:
      context["message"]="Tài khoản đã tồn tại"
      return render(request,"signup.html",context)
  except:
    context["message"]="Tài khoản đã tồn tại"
    return render(request,"signup.html",context)

def logout(request):
  request.session['uid'] = ""
  return render(request, "login.html")
# admin
def post_add_product(request):
  title = request.POST.get('title')
  image = request.POST.get('image')
  category = request.POST.get('category')
  price = request.POST.get('price')
  description = request.POST.get('description')
  try:
    data = {
      "title":title,
      "image":image,
      "category":category,
      "price":price,
      "size":["S","M","XL"],
      "description":description,
    }
    database.child("products").child("list-items").push(data)
    return render(request,"admin/add-product.html")
  except:
    message="Nhap lai san pham"
    return render(request,"admin/add-product.html",message)
  
def delete_product(request, product_id):
  try:
      database.child("products").child("list-items").child(product_id).remove()
      return redirect("/admin-view/list-product")
  except Exception as e:
      print("LỖi khi xóa sản phẩm {e}")
      return redirect("/admin-view/list-product")
  
def update_product(request,product_id):
  if request.method == "POST":
        title = request.POST.get('title')
        image = request.POST.get('image')
        category = request.POST.get('category')
        price = request.POST.get('price')
        description = request.POST.get('description')
        try:
            data = {
                "title": title,
                "image": image,
                "category": category,
                "price": price,
                "description": description,
            }
            database.child("products").child("list-items").child(product_id).update(data)
            return redirect("/admin-view/list-product")
        except Exception as e:
            return HttpResponse(f"Lỗi khi cập nhật sản phẩm: {e}")
  else:
    return HttpResponse("Phương thức không được hỗ trợ")

def delete_user(request,user_id):
  try:
      database.child("users").child(user_id).remove()
      print(user_id)
  except Exception as e:
      print("Lỗii khi xóa người dùng {e}")
  return redirect("listUser")

#home page
def product_detail(request,product_id):
  context = {"products": []}
  try:
      dataProduct = database.child("products").child("list-items").child(product_id)
      product_data = dataProduct.get().val()
      if product_data:
        item = {
          "id":product_id,
          "title": product_data["title"],
          "image": product_data["image"],
          "category": product_data["category"],
          "price": product_data["price"],
          "size" : product_data['size'],
          "description": product_data["description"],
        }
        context["products"].append(item)
      else: 
        print("Không tìm thấy dữ liệu sản phẩm")
  except Exception as e:
      return HttpResponse(f"Lỗi khi kết nối tới data {e}")
  return render(request,"product-detail.html",context)

def add_cart(request, product_id):
  if request.method == "POST":
      size = request.POST.get('size')
      uid = request.session.get('uid') 
      if not uid:
          return render(request, "login.html")
      item = {"quantity": 0, "size": "", "price": 0}
      dataProduct = database.child("products").child("list-items").child(product_id)
      product_data = dataProduct.get().val()
      if not product_data:
          context = {"message": "Sản phẩm không tồn tại!"}
          return render(request, "product.html", context)
      price = int(product_data["price"])
      try:
          cart_ref = database.child("cart").child(uid).child("items").child(product_id)
          existing_product = cart_ref.get().val()
          if existing_product:
              print(existing_product)
              quantity = existing_product.get("quantity", 0)  
              database.child("cart").child(uid).child("items").child(product_id).update({"quantity": quantity + 1})
          else:
              item = {
                  "quantity": 1,
                  "size": size,
                  "price": price
              }
              database.child("cart").child(uid).child("items").child(product_id).set(item)
          return redirect("home")
      except Exception as e:
          print(f"Error: {e}")  
          context = {"message": "Lỗi khi tải trang web"}
          return render(request, "home.html", context)

#user
def update_info_user(request):
  name = request.POST.get('name')
  phone = request.POST.get('phone')
  email = request.POST.get('email')
  address = request.POST.get('address')
  dob = request.POST.get('dob')
  gender = request.POST.get('gender')
  uid = request.session.get('uid') 
  if uid:
    try:
        data = {
            "name": name,
            "phone": phone,
            "email": email,
            "address": address,
            "dob": dob,
            "gender": gender,
        }
        database.child("users").child(uid).update(data)
        return redirect("/user/info/")
    except Exception as e:
        return HttpResponse(f"Lỗi khi cập nhật thông tin người dùng {e}")


# Tăng số lượng
def increaseQuantity(request,product_id):
  uid = request.session.get('uid') 
  if uid:
    try:
      product = database.child("cart").child(uid).child("items").child(product_id).get().val()
      if product:
        quantity = int(product["quantity"])+1
        data = {
            "quantity":quantity
        }
        database.child("cart").child(uid).child("items").child(product_id).update(data)
        return redirect("cartView")
    except:
      print("Không tồn tại sản phẩm này")
      return redirect("cartView")
  else:
     return redirect("login")
  return redirect("cartView")

#Giảm số lượng
def decreaseQuantity(request, product_id):
    uid = request.session.get('uid')
    if uid:
        try:
            product = database.child("cart").child(uid).child("items").child(product_id).get().val()
            if product:
                quantity = int(product["quantity"]) - 1
                if quantity == 0:
                    database.child("cart").child(uid).child("items").child(product_id).remove()
                else:
                    data = {
                        "quantity": quantity
                    }
                    database.child("cart").child(uid).child("items").child(product_id).update(data)
                return redirect("cartView")
            else:
                print("Không tồn tại sản phẩm này trong giỏ hàng.")
                return redirect("cartView")
        except Exception as e:
            print(f"Lỗi khi giảm số lượng sản phẩm: {e}")
            return redirect("cartView")
    else:
        return redirect("login")


#Xóa sản phẩm trong Cart
def deleteProductCart(request,product_id):
  uid = request.session.get('uid') 
  if uid:
    try:
      product = database.child("cart").child(uid).child("items").child(product_id).get()
      if product:
        database.child("cart").child(uid).child("items").child(product_id).remove()
    except Exception as e:
       print("Không tồn tại sản phẩm này",e)
  else:
     return redirect("login")
  return redirect("cartView")

def saveInvoice(request,user_id):
  uid = request.session.get('uid')
  if uid:
    arr = []
    products = database.child("cart").child(user_id).child("items").get()
    if products.each():
      for p in products.each():
          data_info_product = database.child("products").child("list-items").child(p.key()).get().val()
          if data_info_product:
            product_info = {
            "userId":uid,
            "id": p.key(),
            "title": data_info_product["title"],
            "image": data_info_product["image"],
            "category": data_info_product["category"],
            "price": data_info_product["price"],
            "size": p.val().get("size"),
            "quantity": p.val().get("quantity"),  
            }
            arr.append(product_info)
      data = {
        "id":user_id,
        "products":arr,
        "status":"pending"
      }
      database.child("invoice").push(data)
    else: 
      print("No products found.")
  else:
     return redirect("login")
  return redirect("home")

def decentralization(request,user_id):
  role  = request.POST.get("role")
  print(role)
  if role:
    data = {
        "role":role
    }
    database.child("users").child(user_id).update(data)
    return redirect("listUser")
  else:
    print("Khong co du lieu")
    return redirect("listUser")
  
#module Staff
def acceptInvoice(request,invoice_id):
  uid = request.session.get('uid')
  data = {}
  if uid:
    invoice_ref = database.child("invoice").child(invoice_id).get().val()
    if invoice_ref:
      data= {
          "status":"accepted"
      }
      database.child("invoice").child(invoice_id).update(data)
  else:
    return redirect("login")
  return redirect("staffView")

def rejectInvoice(request,invoice_id):
  uid = request.session.get('uid')
  data = {}
  if uid:
    invoice_ref = database.child("invoice").child(invoice_id).get().val()
    if invoice_ref:
      data= {
          "status":"rejected"
      }
      database.child("invoice").child(invoice_id).update(data)
  else:
    return redirect("login")
  return redirect("staffView")

def cancelInvoice(request,invoice_id):
  uid = request.session.get('uid')
  data = {}
  if uid:
    invoice_ref = database.child("invoice").child(invoice_id).get().val()
    if invoice_ref:
      data= {
          "status":"cancel"
      }
      database.child("invoice").child(invoice_id).update(data)
  else:
    return redirect("login")
  return redirect("listOrder")