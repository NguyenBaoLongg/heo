const User = require('../models/user')
const Cart = require('../models/cart');
const Product = require('../models/products')
const mongoose = require('mongoose')


const addtoCart = async (userId, productId) => {
    return new Promise(async (resolve, reject) => {
        try {
            // Kiểm tra xem người dùng có tồn tại không
            let checkUser = await User.findById(userId);
            if (!checkUser) {
                return resolve({
                    status: "FAILED",
                    message: "The user isn't defined",
                });
            }

            // Chuyển đổi productId thành ObjectId



            let cart = await Cart.findOne({ idUsers: userId });

            if (!cart) {
                cart = new Cart({ idUsers: userId });
            }

            // Lấy chi tiết sản phẩm từ cơ sở dữ liệu


            let productExists = false;
            for (let item of cart.products) {
                if (item.idProducts === productId) {
                    item.quanlity += 1;
                    productExists = true;
                    break;
                }
            }
            console.log(productId)
            const productDetail = Product.findOne(productId);
            if (productExists) {
                await cart.save();
            } else {
                const productObject = {
                    idProducts: productId,
                    quanlity: 1
                };
                cart.products.push(productObject);
                console.log(cart)
                await cart.save();
            }

            // Trả về kết quả thành công
            resolve({
                status: 200,
                message: "success",
            });
        } catch (e) {
            console.error(e); // Log lỗi để dễ debug
            reject({
                status: 400,
                message: "Error",
            });
        }
    });
};





module.exports = {
    addtoCart
}