from odoo import models, fields, api

class AssetForm(models.Model):
    _name = 'asset.loan'
    _inherit = ['mail.thread']
    _description = 'Form Peminjaman Asset'

    name = fields.Char(string="Nama", required=True)
    status_asset = fields.Many2one('asset.status', string="Nama Barang", required=True, domain="[('state', '=', 'available')]")
    divisi = fields.Char(string="Divisi", required=True)
    loan_date = fields.Date(string="Tanggal Peminjaman", default=fields.Date.today, required=True)
    duration = fields.Integer(string="Durations (Months)", required=True)
    return_date = fields.Date(string="Tanggal Kembali")
    notes = fields.Text(string="Description")
    id_peminjam_lines_ids = fields.One2many('asset.form.peline', 'id_asset', string="Id Lines")
    state = fields.Selection([('draft', 'Draft'), ('borrowed', 'Borrowed'), ('returned', 'Returned')],
                             string='State', default='draft')
    jumlah_pinjam = fields.Integer(string="Jumlah Barang dipinjam", default=1)
    assets_img = fields.Binary(string="Add Image")


    @api.onchange('status_asset')
    def _onchange_status_asset(self):
        self.jumlah_pinjam = 1

    @api.model
    def create(self, vals):
        res = super(AssetForm, self).create(vals)
        res.status_asset.jumlah_barang -= res.jumlah_pinjam
        if res.status_asset.jumlah_barang == 0:
            res.status_asset.state = 'unavailable'
        res.state = 'borrowed'
        return res

    def write(self, vals):
        if vals.get('status_asset'):
            self.status_asset.jumlah_barang += self.jumlah_pinjam - vals.get('jumlah_pinjam', self.jumlah_pinjam)
            if self.status_asset.jumlah_barang == 0:
                self.status_asset.state = 'unavailable'
            elif self.status_asset.state == 'unavailable':
                self.status_asset.state = 'available'
            new_status_asset = self.env['asset.status'].browse(vals['status_asset'])
            new_status_asset.jumlah_barang -= vals.get('jumlah_pinjam', self.jumlah_pinjam) - self.jumlah_pinjam
            if new_status_asset.jumlah_barang == 0:
                new_status_asset.state = 'unavailable'
            elif new_status_asset.state == 'unavailable':
                new_status_asset.state = 'available'
        elif vals.get('jumlah_pinjam'):
            self.status_asset.jumlah_barang += vals['jumlah_pinjam'] - self.jumlah_pinjam
            if self.status_asset.jumlah_barang == 0:
                self.status_asset.state = 'unavailable'
            elif self.status_asset.state == 'unavailable':
                self.status_asset.state = 'available'
        return super(AssetForm, self).write(vals)

    def action_borrw(self):
        self.state = 'borrowed'

    def action_returned(self):
        self.state = 'returned'

    def action_draft(self):
        self.state = 'draft'

    def return_asset(self):
        self.state = 'returned'
        self.status_asset.jumlah_barang += self.jumlah_pinjam
        if self.status_asset.state == 'unavailable':
            self.status_asset.state = 'available'


class AssetFormPerceptionLine(models.Model):
    _name = 'asset.form.peline'
    _description = 'Asset Form Perceptions'

    name = fields.Char(String="ID")
    namaa_barang = fields.Many2one('asset.status', string="Nama Barang", required=True, domain="[('state', '=', 'available')]")
    id_asset = fields.Many2one('asset.loan', string="Asset ID")