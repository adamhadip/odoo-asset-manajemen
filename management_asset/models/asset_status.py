from odoo import models, fields

class AssetStatus(models.Model):
    _name = 'asset.status'
    _inherit = ['mail.thread']
    _description = 'Asset Status'

    name = fields.Char(string='Nama Asset', required=True)
    code = fields.Char(string='Kode Asset', required=True)
    tipe_asset = fields.Char(string='Tipe Asset')
    geo_tag = fields.Char(string='Geo Tag')
    description = fields.Text(string='Deskripsi')
    asset_img = fields.Image(string="Add Image")
    state = fields.Selection([
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
        ('none', 'None')], default='available', string="Status")
    idpinjaman_ids = fields.One2many('asset.loan', 'status_asset', string="ID Pinjaman")
    jumlah_barang = fields.Integer(string="Jumlah Barang")

    def action_avai(self):
        self.state = 'available'

    def action_unava(self):
        self.state = 'unavailable'

    def action_none(self):
        self.state = 'none'