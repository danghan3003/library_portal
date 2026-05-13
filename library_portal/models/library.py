from odoo import models, fields, api

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char(string='Tên sách', required=True) # Char lưu trữ chuỗi ký tự [5]
    author = fields.Char(string='Tác giả')
    isbn = fields.Char(string='Mã ISBN')
    quantity = fields.Integer(string='Số lượng còn', default=1)
    description = fields.Text(string='Mô tả')
    image = fields.Binary(string='Ảnh bìa')
    state = fields.Selection([
        ('available', 'Có sẵn'),
        ('out_of_stock', 'Hết sách')
    ], default='available', string='Trạng thái')

class LibraryBorrowRequest(models.Model):
    _name = 'library.borrow.request'
    _description = 'Borrow Request'

    name = fields.Char(string='Tên người mượn')
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string='Số điện thoại')
    book_id = fields.Many2one('library.book', string='Sách', required=True) # Many2one liên kết nhiều-một [6]
    request_date = fields.Datetime(string='Ngày yêu cầu', default=fields.Datetime.now)
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('confirmed', 'Đã xác nhận'),
        ('rejected', 'Đã từ chối')
    ], default='draft', string='Trạng thái')