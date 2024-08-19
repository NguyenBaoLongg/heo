function ensureAuthenticated(req, res, next) {
    if (req.session.userId) {
        console.log(req.session.userId);
        return next();
    }
    return next();
}

module.exports = ensureAuthenticated;