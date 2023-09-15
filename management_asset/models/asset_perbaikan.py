from odoo import fields, models, api
import base64

class AssetPerbaikan (models.Model):
    _name="asset.perbaikan"
    _inherit = ['mail.thread']
    _description = "Membuat asset perbaikan"

    items=fields.Many2one('asset.status', string="Nama Barang", required=True)
    durasi=fields.Integer(string="Durasi")
    state = fields.Selection([('fix', 'Fixed'), ('maintenance', 'Maintenance'), ('todo', 'To Do')],
                              string="Status Perbaikan")
    fix_date = fields.Date(string="Tanggal Perbaikan")
    done_date = fields.Date(string="Tanggal K`1embali")
    jumlah_perbaikan = fields.Integer(string="Jumlah Barang", default=1)
    assets_image=fields.Binary(string="Gambar")

    @api.depends('source_record_id.assets_img')
    def _compute_display_image(self):
        for record in self:
            if record.source_record_id.assets_img:
                record.assets_image = base64.b64encode(record.source_record_id.assets_img).decode('utf-8')

    @api.onchange('items')
    def onchange_(self):
        self.jumlah_perbaikan = 1

    @api.model
    def create(self,vals):
        res = super(AssetPerbaikan, self).create(vals)
        res.items.jumlah_barang -= res.jumlah_perbaikan
        if res.items.jumlah_barang == 0:
            res.items.state = 'unavailable'
        res.state = 'maintenance'
        return res

    def write(self,vals):
        if vals.get('items'):
            self.items.jumlah_barang += self.jumlah_perbaikan - vals.get('jumlah_perbaikan', self.jumlah_perbaikan)
            if self.items.jumlah_barang == 0:
                self.items.state = 'unavailable'
            elif self.items.state == 'unavailable':
                self.items.state = 'available'
            new_status_asset = self.env['asset.status'].browse(vals['items'])
            new_status_asset.jumlah_barang -= vals.get('jumlah_perbaikan', self.jumlah_perbaikan) - self.jumlah_perbaikan
            if new_status_asset.jumlah_barang == 0:
                new_status_asset.state = 'unavailable'
            elif new_status_asset.state == 'unavailable':
                new_status_asset.state = 'available'
        elif vals.get('jumlah_perbaikan'):
            self.items.jumlah_barang += vals['jumlah_perbaikan'] - self.jumlah_perbaikan
            if self.items.jumlah_barang == 0:
                self.items.state = 'unavailable'
            elif self.items.state == 'unavailable':
                self.items.state = 'available'
        return super(AssetPerbaikan, self).write(vals)


    def action_mainte(self):
        self.state='maintenance'

    def action_todo(self):
        self.state='todo'

    def action_fix(self):
        self.state='fix'

    def asset_fix(self):
        self.state='fix'
        if self.items.state == 'unaivalable' :
            self.items.state = 'available'