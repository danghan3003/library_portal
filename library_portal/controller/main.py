from odoo import http
from odoo.http import request
import json

class LibraryPortalController(http.Controller):

    # -----------------------------------------
    # PHẦN 2: CONTROLLER HTTP (QWeb Templates)
    # -----------------------------------------
    
    # 2.1 - Trang danh sách sách
    @http.route('/library/books', type='http', auth='public', website=True)
    def list_books(self, **kwargs):
        # Dùng sudo() để bypass security cho khách vãng lai, dùng phương thức search() để lọc [5, 8]
        books = request.env['library.book'].sudo().search([('state', '=', 'available')])
        return request.render('library_portal.books_list_template', {'books': books})

    # 2.2 - Trang chi tiết sách
    @http.route('/library/book/<int:id>', type='http', auth='public', website=True)
    def book_detail(self, id, **kwargs):
        # Dùng phương thức browse() để lấy 1 bản ghi qua ID [5]
        book = request.env['library.book'].sudo().browse(id)
        if not book.exists():
            return request.not_found()
        return request.render('library_portal.book_detail_template', {'book': book})

    # 2.3 - Form đăng ký mượn (GET)
    @http.route('/library/borrow/<int:book_id>', type='http', auth='public', website=True)
    def borrow_form(self, book_id, **kwargs):
        book = request.env['library.book'].sudo().browse(book_id)
        return request.render('library_portal.borrow_form_template', {'book': book})

    # 2.3 - Xử lý Form đăng ký (POST)
    @http.route('/library/borrow/submit', type='http', auth='public', website=True, methods=['POST'], csrf=True)
    def borrow_submit(self, **post):
        name = post.get('name')
        email = post.get('email')
        phone = post.get('phone')
        book_id = post.get('book_id')

        # Validate dữ liệu
        error = None
        if not name:
            error = "Tên không được để trống."
        elif '@' not in email:
            error = "Email không hợp lệ."

        if error:
            book = request.env['library.book'].sudo().browse(int(book_id))
            return request.render('library_portal.borrow_form_template', {
                'book': book, 'error': error, 'name': name, 'email': email, 'phone': phone
            })

        # Lưu vào model bằng phương thức create() [9]
        req_record = request.env['library.borrow.request'].sudo().create({
            'name': name,
            'email': email,
            'phone': phone,
            'book_id': int(book_id),
        })
        return request.redirect(f'/library/borrow/thank-you?id={req_record.id}')

    @http.route('/library/borrow/thank-you', type='http', auth='public', website=True)
    def borrow_thank_you(self, **kwargs):
        return request.render('library_portal.thank_you_template', {'req_id': kwargs.get('id')})


    # -----------------------------------------
    # PHẦN 3: CONTROLLER JSON (Dành cho API)
    # -----------------------------------------
    
    # 3.1 - API danh sách sách
    @http.route('/api/library/books', type='json', auth='public')
    def api_get_books(self):
        books = request.env['library.book'].sudo().search([('state', '=', 'available')])
        return [{'id': b.id, 'name': b.name, 'author': b.author, 'quantity': b.quantity} for b in books]

    # 3.2 - API tạo borrow request
    @http.route('/api/library/borrow', type='json', auth='public', methods=['POST'])
    def api_create_borrow(self, **kwargs):
        book_id = kwargs.get('book_id')
        book = request.env['library.book'].sudo().browse(book_id)
        
        if not book.exists() or book.quantity <= 0:
            return {"success": False, "error": "Sách không tồn tại hoặc đã hết."}

        req = request.env['library.borrow.request'].sudo().create({
            'name': kwargs.get('name'),
            'email': kwargs.get('email'),
            'phone': kwargs.get('phone'),
            'book_id': book.id,
        })
        return {"success": True, "request_id": req.id}

    # 3.3 - API yêu cầu đăng nhập
    @http.route('/api/library/my-requests', type='json', auth='user')
    def api_my_requests(self):
        # Lọc theo email của user đang đăng nhập
        user_email = request.env.user.email
        # Domain filter bằng toán tử '=' [10]
        requests = request.env['library.borrow.request'].search([('email', '=', user_email)])
        return [{'id': r.id, 'book': r.book_id.name, 'state': r.state} for r in requests]