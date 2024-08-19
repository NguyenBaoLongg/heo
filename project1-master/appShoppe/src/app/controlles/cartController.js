const mongoose = require('mongoose');
const Cart = require("../models/cart");
const jwtVerify = require('../serviecs/JwtVerify');
const Product = require("../models/products");
const CartService = require('../serviecs/cartServiecs');

class cartController {
  // GET /cart
  async show(req, res, next) {
    try {
      const userId = req.session.user._id;
      const cart = await Cart.findOne({ userId: userId }).lean();

      if (!cart) {
        return res.render("me/cart", {
          layout: "cart",
          cart: { products: [] },
          userKey: req.session.user,
          notificationMessage: "Giỏ hàng trống",
          handle: ``
        })
      }

      res.render("me/cart", {
        layout: "cart",
        cart: { products: [] },
        userKey: req.session.user,
        notificationMessage: "",
        handle: ``
      })


    } catch (e) {
      next(e);
    }

  }
  // post /add-cart
  async add_cart(req, res, next) {
    try {
        var userId = "668ea1103971580c26e5d021";
        req.params.id = "667b05741ec5a7ee43101d91"
        const res = await CartService.addtoCart(userId, req.params.id);
        return res.redirect("back");
    } catch (e) {
        console.error(e); // Log lỗi để dễ debug
        return res.redirect("back");
    }
}


}

module.exports = new cartController();
